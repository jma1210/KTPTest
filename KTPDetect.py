import cv2
import numpy as np
import pathlib
import imutils
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Muhammad Reza\AppData\Local\Tesseract-OCR\tesseract.exe'

def sortRectPoints(sqr):
    # Helper function to sort the points, 1 2 3 4 being top left, top right, bot right, and bot left
    pts = sqr.reshape(4,2)
    rect = np.zeros((4,2),dtype="float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts,axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def filterBlue(im):
    # Create a mask image that takes all ranges of blue
    hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    low_blue = np.array([80,0,155],np.uint8)
    high_blue = np.array([140,255,255],np.uint8)
    return cv2.inRange(hsv,low_blue,high_blue)

def chooseImage(index : int):
    # Returns an image from the chosen number in the list
    list = os.listdir(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp')
    print(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp'+'\\'+list[index])
    return cv2.imread(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp'+'\\'+list[index])

def drawBox(mask):
    # Get the largest contours in the image and draw a box
    cnts = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts,key = cv2.contourArea,reverse=True)[:15]
    cardCnts = None
    for c in cnts:
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,0.015*peri,True)
        if len(approx)==4:
            cardCnts = approx
            break
    return cardCnts
    
def perspTransform(cnts,og):
    rect = sortRectPoints(cnts)
    (tl,tr,br,bl) = rect
    
    #calculate width dimensions
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    #calculate height dimensions
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    #Get maximum dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    #construct destination points
    dst = np.array([
        [0,0],
        [maxWidth-1,0],
        [maxWidth-1,maxHeight-1],
        [0,maxHeight-1]],dtype="float32")
    M = cv2.getPerspectiveTransform(rect,dst)
    warp = cv2.warpPerspective(og,M,(maxWidth,maxHeight))
    return warp


if __name__ == "__main__":
    for i in range(len(os.listdir(r'C:\Users\Muhammad Reza\KTPDetect\Foto ktp'))):
        #Iterate over all files in specified dir
            original = chooseImage(i)
            toBeShown = filterBlue(original)
            conts = drawBox(toBeShown)
            ptimg = perspTransform(conts,original)

            #PostProcessing of images
            bounded = cv2.drawContours(original.copy(), [conts], -1, (0, 255, 0), 15)
            bounded = imutils.resize(bounded,width = 600)
            toBeShown = imutils.resize(toBeShown,width = 600)
            ptimg = imutils.resize(ptimg,width = 600)

            #Show images
            cv2.imshow('bounded',bounded)
            # cv2.imshow('img',toBeShown)
            cv2.imshow('Perspective Transformed', ptimg)
            print(pytesseract.image_to_string(ptimg))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
