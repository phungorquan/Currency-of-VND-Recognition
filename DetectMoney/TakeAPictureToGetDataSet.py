# import the necessary packages
import RPi.GPIO as GPIO #import GPIO lib
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
GPIO.setmode(GPIO.BCM)  #Use GPIO name pin on Rasp, and not use pin number on Rasp

GPIO.setup(24, GPIO.OUT) # DETECT LED

time.sleep(0.1)
GPIO.output(24, GPIO.LOW)
camera = PiCamera() #Procedures
time.sleep(2) #delay 2sec let camera stable

# Cap a picture and save to /home/pi/DetectMoney/TrainingData with name 20000B.img
camera.capture("/home/pi/ThiGiacMayTinh/LastDetectMoney/DetectMoney/TrainingData/500000B.jpg") 
GPIO.output(24, GPIO.HIGH)
