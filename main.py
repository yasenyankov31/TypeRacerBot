from time import sleep
from tkinter import E
import cv2 
import numpy as np

from pytesseract import pytesseract
from pytesseract import Output

import pyautogui
import keyboard



def check_upper(c):
    if c >= 'A' and c <= 'Z':
        return True
    else:
        return False

data_list=[]
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img=pyautogui.screenshot()
#img=cv2.imread("test.png")
img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)




hMin = 44 
sMin = 0 
vMin = 255
hMax = 179 
sMax = 255 
vMax = 255

# Set minimum and max HSV values to display
lower = np.array([hMin, sMin, vMin])
upper = np.array([hMax, sMax, vMax])

# Create HSV Image and threshold into a range.
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)
output = cv2.bitwise_and(img,img, mask= mask)


gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

#apply threshold
thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]

# find contours and get one with area about 180*35
# draw all contours in green and accepted ones in red
contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
#area_thresh = 0
min_area = 0.95*180*35
max_area = 1.05*180*35
result = img.copy()
for c in contours:
	area = cv2.contourArea(c)
	data_list.append(cv2.boundingRect(c))
	cv2.drawContours(result, [c], -1, (0, 255, 0), 1)
	if area > min_area and area < max_area:
			cv2.drawContours(result, [c], -1, (0, 0, 255), 1)

widthlist=[]

for data in data_list:
	x,y,w,h=data
	widthlist.append(w) 



x,y,w,h=data_list[widthlist.index(max(widthlist))]
crop_img = img[y:y+h, x:x+w]

thresh = cv2.threshold(crop_img, 220, 255, cv2.THRESH_BINARY)[1]

# Create custom kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# Perform closing (dilation followed by erosion)
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Invert image to use for Tesseract
result = 255 - close



image_data =pytesseract.image_to_string(crop_img, output_type=Output.DICT)    # Run tesseract.exe on image


for x in range(10):
	sleep(1)
		

print(image_data)
for  word in image_data['text']:
	if '\n' in word:
		keyboard.press("space")
	if check_upper(word):
			keyboard.press("shift+"+word.lower())
			keyboard.release("shift")
	else:
		keyboard.press(word)
	sleep(0.05)		

