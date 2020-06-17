import numpy as np
import cv2
import pathlib

address = pathlib.PureWindowsPath(r'C:\Users\Muhammad Reza\OpenCVTutorial\foto ktp\ktp1.jpg')
image = cv2.imread(address.as_posix())
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

height,width,channel = image.shape
norm_mat = np.zeros((height,width))
final = cv2.normalize(image,norm_mat,0,255,cv2.NORM_MINMAX)

low_blue = np.array([90,45,0],np.uint8)
high_blue = np.array([140,255,255],np.uint8)

hsv = cv2.GaussianBlur(final,(7,7),0)
blue = cv2.inRange(final,low_blue,high_blue)


cv2.imshow('og',image)
cv2.imshow('normed',final)
cv2.imshow('img',blue)
cv2.waitKey(0)
cv2.destroyAllWindows()