import cv2
#import cnocr
import numpy as np
import pytesseract

from skimage.filters import threshold_sauvola

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

total_err = 0
total = 0

for i, actual_plate in enumerate(actual_plates):
    image = cv2.imread(f'metrics/cnocr/images/{i + 1}.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sauvola_thresh = threshold_sauvola(gray, window_size=43)
    binary_sauvola = gray > sauvola_thresh
    binary_sauvola = (binary_sauvola * 255).astype(np.uint8)
    #_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #thresh = cv2.resize(thresh, (0, 0), fx=2, fy=2)
    #kernel = np.ones((2, 2), np.uint8)
    #dilated = cv2.dilate(thresh, kernel, iterations=1)
    #eroded = cv2.erode(dilated, kernel, iterations=1)
    #eroded = cv2.resize(eroded, (0, 0), fx=0.1, fy=0.1)

    #predicted_plate = ocr.ocr(img_fp=eroded)
    #predicted_plate = [predicted_plate[i]['text'] for i in range(len(predicted_plate))]
    #predicted_plate = ''.join(predicted_plate).replace(' ', '')

    tesseract_predicted = pytesseract.image_to_string(binary_sauvola, lang='eng', config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    tesseract_predicted = tesseract_predicted.strip().replace(' ', '')
    total_err += min_error(tesseract_predicted, actual_plate)
    total += len(actual_plate)

accuracy = (total - total_err) / total
print('thresh window 43, psm 8 accuracy: ', accuracy * 100)