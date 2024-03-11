import cv2
from collections import Counter

from cnocr import CnOcr
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

ocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')

annotation = [
    'AHL839', 'NCZ9506', 'NCV3895',
    'NCF1943', 'FAF1086', 'AAD7916',
    'FAB3478', 'AMA9460', 'AMA9460',
    'AMA9460', 'FAH1630', 'MAA4265',
    'FAB8503', 'FAB8503', 'FAL5430',
    'FAL5430', 'AAD7196', 'AAD7196',
    'FAH1767', 'FAH1767', 'FAH1767',
    'FAH1767', 'FAM8962', 'FAA9637',
    'FAA9637', 'FAL6925', 'FAE2187',
    'FAA2055', 'NBV8330', 'CBD6012',
    'IAE6628', 'YAB1900', 'IAC3189'
]

y_true = ['correct'] * 33
y_pred = []

for i in range(33):
    img = cv2.imread(f'../datasets/ph-license-plates-2014/test/images/{i + 1}.jpg')
    img = cv2.resize(img, (0,0), fx=3, fy=3)
    img = cv2.GaussianBlur(img, (5,5), 0)
    results = ocr.ocr(img_fp=img)
    temp = [results[i]['text'] for i in range(len(results))]
    predicted = ''.join(temp).strip()
    predicted = predicted.replace(' ', '')
    print('actual: ', annotation[i], ' | predicted: ', predicted)
    y_pred.append('correct' if annotation[i] in predicted else 'incorrect')

recall = recall_score(y_true=y_true, y_pred=y_pred, pos_label='correct')
print(f'recall: {recall}')

f1 = f1_score(y_true=y_true, y_pred=y_pred, pos_label='correct')
print(f'f1 score: {f1}')

print(Counter(y_pred))