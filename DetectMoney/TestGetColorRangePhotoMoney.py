import cv2
import time
import numpy as np
def Min_H(pos):
    Min_H.value = pos
Min_H.value = 0

def Min_S(pos):
    Min_S.value = pos
Min_S.value = 0

def Min_V(pos):
    Min_V.value = pos
Min_V.value = 0

def Max_H(pos):
    Max_H.value = pos
Max_H.value = 255

def Max_S(pos):
    Max_S.value = pos
Max_S.value = 255

def Max_V(pos):
    Max_V.value = pos
Max_V.value = 255

cv2.namedWindow("Con")
cv2.createTrackbar("Min H", "Con", 0, 255, Min_H)
cv2.createTrackbar("Min S", "Con", 0, 255, Min_S)
cv2.createTrackbar("Min V", "Con", 0, 255, Min_V)

cv2.createTrackbar("Max H", "Con", 0, 255, Max_H)
cv2.createTrackbar("Max S", "Con", 0, 255, Max_S)
cv2.createTrackbar("Max V", "Con", 0, 255, Max_V)

im = cv2.imread('/TrainingData/100000B.jpg')

hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)   # HSV image

while True:
    lower = np.array([Min_H.value, Min_S.value, Min_V.value])
    upper = np.array([Max_H.value, Max_S.value, Max_V.value])
    mask_sub = cv2.inRange(hsv_img , lower, upper)

    mask = cv2.merge((mask_sub,mask_sub,mask_sub))

    res = cv2.bitwise_and(im,mask)

    cv2.imshow("Mask", mask)
    cv2.imshow("Result", res)
    key = cv2.waitKey(1)        
    if key == ord('q'):
        break



cv2.waitKey()
cv2.destroyAllWindows()