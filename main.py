import time
from PIL import Image
import cv2
import numpy as np
from mss import mss
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def preprocess(img):
    image = np.array(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.threshold(
        gray, 100, 255, cv2.THRESH_OTSU)[1]
    gray = 255 - gray
    return gray


def getNum(s):
    search = re.search(r'\d+', s)
    if not search:
        return 0
    res = search.group()
    if res.isdigit():
        return int(res)
    else:
        return 0


left_bounds = {'top': 45, 'left': 1080, 'width': 40, 'height': 40}
right_bounds = {'top': 45, 'left': 1448, 'width': 40, 'height': 40}

with mss() as sct:
    score = [0, 0]
    # mon = sct.monitors[0]
    while True:
        last_time = time.time()
        left_img = preprocess(sct.grab(left_bounds))
        right_img = preprocess(sct.grab(right_bounds))
        left_string = getNum(pytesseract.image_to_string(
            left_img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
        right_string = getNum(pytesseract.image_to_string(
            right_img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))

        score = [left_string, right_string]

        print(score)
