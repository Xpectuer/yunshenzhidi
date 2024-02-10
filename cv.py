'''
Author: XPectuer
LastEditor: XPectuer
'''

import cv2
import pytesseract
from PIL import Image as im

# Set the path to the tesseract executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image from file
image = cv2.imread('imgs/card_1.png')


# Convert the image to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use thresholding to isolate the text
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Use dilation and erosion to remove some noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
dilate = cv2.dilate(thresh, kernel, iterations=1)
erode = cv2.erode(dilate, kernel, iterations=1)

# Use findContours to find the text region
contours, _ = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over the contours and extract the text
for contour in contours:
    
    x, y, w, h = cv2.boundingRect(contour)
    roi = gray[y:y+h, x:x+w]
    img = im.fromarray(roi)
    img.show()
    text = pytesseract.image_to_string(roi, lang='chi_sim')
    print(text)