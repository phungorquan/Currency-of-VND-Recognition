from __future__ import print_function   #Use newest way to print if has new version in future
from __future__ import division         #Use newest way to division if has new version in future

import numpy as np
from time import sleep  #import sleep lib as delay in Microcontroller

import cv2              #import opencv lib
import time

# With surf and sift we can use bf or flann, akaze only use akaze
#detector=cv2.xfeatures2d.SIFT_create() #Quite long ~60secs 68sec :)
#detector = cv2.xfeatures2d.SURF_create()
detector = cv2.AKAZE_create() # ~28s as powerpoint

# This is an array, each of the elements is a name directory of image.
# Dataset array
TraingIMGArr = ["TrainingData/10000F.jpg","TrainingData/10000B.jpg",
                "TrainingData/20000F.jpg","TrainingData/20000B.jpg",
                "TrainingData/50000F.jpg","TrainingData/50000B.jpg",
                "TrainingData/100000F.jpg","TrainingData/100000B.jpg",
                "TrainingData/200000F.jpg","TrainingData/200000B.jpg",
                "TrainingData/500000F.jpg","TrainingData/500000B.jpg"
                ]

# Create an array to save all feature of dataset, this will be help to improve speed of detecting
DesArr = []
start = time.time() # this variable to calculate time of getting feature of all dataset
for i in range(len(TraingIMGArr)): 
    get_Arrimg  = TraingIMGArr[i]   # Get image one by one from Array
    read_Arrimg = cv2.imread(get_Arrimg,0) #Convert it to grayscale
    trainKP,trainDesc=detector.detectAndCompute(read_Arrimg,None) #Procedures to get feature
    DesArr.append(trainDesc) # Save to DesArr
end = time.time()
print(end - start) #Print out running time to console

np.save("feature.npy", DesArr)
#temp = np.load("data.npy")
