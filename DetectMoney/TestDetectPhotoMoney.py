import cv2
import time
import numpy as np


im = cv2.imread('/TrainingData/100000B.jpg') # /TrainingData/COPY20F.jpg
im = cv2.resize(im, (640,480))

im=im[130:420,40:630]

hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)   # HSV image


lower1 = np.array([81,35,141])
upper1 = np.array([157,255,255])
mask_sub1 = cv2.inRange(hsv_img , lower1, upper1)
lower2 = np.array([49,113,70])
upper2 = np.array([206,255,109])
mask_sub2 = cv2.inRange(hsv_img , lower2, upper2)

mask = cv2.bitwise_or(mask_sub1,mask_sub2)

contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

suma=0
for cnt in contours:
    area = cv2.contourArea(cnt)
    suma=suma+area

# for i in range(0,im.shape[0]):
#     for j in range(0,im.shape[1]):
#         a = im[i,j]
#         if a[0]==255 and a[1]==255 and a[2]==255:
#             suma=suma+1
# print(a)
print(suma)
print(mask.shape[0]*mask.shape[1])
res=suma/(im.shape[0]*im.shape[1])*100
if res>80:
    print("FAKE")
else:
    print("REAL")

key = cv2.waitKey(1)        
cv2.waitKey()
cv2.destroyAllWindows()