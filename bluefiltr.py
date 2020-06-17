import numpy as np
import cv2
import pathlib
import imutils

address = pathlib.PureWindowsPath(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp\ktp0.jpg')
image = cv2.imread(address.as_posix())
image = imutils.resize(image,width=650)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

low_blue = np.array([80,30,155],np.uint16)
high_blue = np.array([240,255,255],np.uint16)

blue = cv2.inRange(hsv,low_blue,high_blue)
# hsv = cv2.GaussianBlur(hsv,(17,17),0)


edged = cv2.Canny(blue,30,200)

contours,hierarchy = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image,contours,-1,(255,0,0),5)

# cv2.imshow('hsv',hsv)
cv2.imshow('img',blue)
# cv2.imshow('canny',edged)
cv2.imshow('overlay',image)
cv2.waitKey(0)
cv2.destroyAllWindows()