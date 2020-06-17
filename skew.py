import numpy as np
import cv2
import pathlib
import imutils

address = pathlib.PureWindowsPath(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp\ktp5.jpg')
image = cv2.imread(address.as_posix())
img = imutils.resize(image,width=650)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)

low_blue = np.array([80,0,155],np.uint16)
high_blue = np.array([240,255,255],np.uint16)

blue = cv2.inRange(hsv,low_blue,high_blue)

cnts = cv2.findContours(blue.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts,key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

for c in cnts:
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.05*peri,True)

    if len(approx) == 4:
        screenCnt = approx
        break


cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("Box",img)
cv2.imshow('blue mask',blue)
cv2.waitKey(0)
cv2.destroyAllWindows()