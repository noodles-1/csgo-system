from collections import Counter
import pytesseract
import cv2

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    predicted = pytesseract.image_to_string(image=img, lang='eng', config='--psm 10 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    y_pred.append('correct' if annotation[i] in predicted else 'incorrect')

precision = precision_score(y_true=y_true, y_pred=y_pred, pos_label='correct')
print(f'precision: {precision}')

recall = recall_score(y_true=y_true, y_pred=y_pred, pos_label='correct')
print(f'recall: {recall}')

f1 = f1_score(y_true=y_true, y_pred=y_pred, pos_label='correct')
print(f'f1 score: {f1}')