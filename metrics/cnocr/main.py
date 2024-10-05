import cv2
import os
import base64
import numpy as np
import pytesseract

from dotenv import load_dotenv
from skimage.filters import threshold_sauvola
from anthropic import Anthropic

load_dotenv(dotenv_path='.env')
CLAUDE_KEY = os.getenv('CLAUDE_KEY')

# ocr = cnocr.CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')

actual_plates = [
    'AAK9402', 'YAA7157', 'DAN5548',
    'NFT3370', 'NFT3370', 'NFX5773',
    'AAS7974', 'NFJ6582', 'NFC1943',
    'NCF1943', 'NCF1943', 'FAF1086',
    'FAF1086', 'JAF9716', 'AAO7688',
    'AAO7688', 'AAO7688', 'AAO7688',
    'AAO7688', 'FAE1338', 'AAD7916',
    'AAD7916', 'AAD7916', 'AMA9460',
    'FAH1630', 'FAH1630', 'JAM3415',
    'JAM3415', 'JAM3415', 'FAL4146',
    'FAL4146', 'MAA4265', 'FAB8503',
    'FAB8503', 'FAA4957', 'FAA4957',
    'FAA4957', 'FAA4305', 'FAA4305',
    'FAA4305', 'FAA4305', 'AAD7196',
    'AAD7196', 'FAH1767', 'FAH1767',
    'FAL4901', 'FAL4901', 'FAA9637',
    'FAA9637', 'FAA9637', 'FAL6925',
    'FAL6925', 'FAL6925', 'FAE2187',
    'FAE2187', 'FAA2055', 'RMC853',
    'RMC853', 'DAE9241', 'YAB1900',
    'YAA6856', 'NGM9107', 'CCL9771',
    'IAC3187'
]

def extract(image):
    anthropic = Anthropic(api_key=CLAUDE_KEY)
    _, buffer = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    
    response = anthropic.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=1000,
        messages=[
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': 'image/jpeg',
                            'data': encoded_image
                        }
                    },
                    {
                        'type': 'text',
                        'text': 'This image contains a license plate. Extract the license plate number to string. Do not include any other text.'
                    }
                ]
            }
        ]
    )

    return response.content[0].text

def min_error(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][n] = m - i
    for i in range(n + 1):
        dp[m][i] = n - i
    
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            dp[i][j] = dp[i + 1][j + 1] if str1[i] == str2[j] else min(
                dp[i + 1][j],
                dp[i][j + 1],
                dp[i + 1][j + 1]
            ) + 1
    
    return dp[0][0]

models = ['eng', 'LP']
psms = [7, 8]

for model in ['claude']:
    # tessdata = '' if model == 'eng' else '--tessdata-dir tessdata'

    for psm in psms:
        total_err = 0
        total = 0

        for i, actual_plate in enumerate(actual_plates):
            image = cv2.imread(f'metrics/cnocr/images/{i + 1}.jpg')

            '''
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sauvola_thresh = threshold_sauvola(gray, window_size=43)
            binary_sauvola = gray > sauvola_thresh
            binary_sauvola = (binary_sauvola * 255).astype(np.uint8)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            thresh = cv2.resize(thresh, (0, 0), fx=2, fy=2)
            kernel = np.ones((2, 2), np.uint8)
            dilated = cv2.dilate(thresh, kernel, iterations=1)
            eroded = cv2.erode(dilated, kernel, iterations=1)
            eroded = cv2.resize(eroded, (0, 0), fx=0.1, fy=0.1)
            predicted_plate = ocr.ocr(img_fp=eroded)
            predicted_plate = [predicted_plate[i]['text'] for i in range(len(predicted_plate))]
            predicted_plate = ''.join(predicted_plate).replace(' ', '')

            tesseract_predicted = pytesseract.image_to_string(image, lang=model, config=f'{tessdata} --psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            tesseract_predicted = tesseract_predicted.strip().replace(' ', '')
            '''
            extracted_lp = extract(image)
            extracted_lp = extracted_lp.strip().replace(' ', '')

            total_err += min_error(extracted_lp, actual_plate)
            total += len(actual_plate)

        accuracy = (total - total_err) / total
        print(f'{model} accuracy: ', accuracy * 100)

# claude accuracy:  97.08520179372198