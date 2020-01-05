from __future__ import print_function   #Use newest way to print if has new version in future
from __future__ import division         #Use newest way to division if has new version in future

from time import sleep  #import sleep lib as delay in Microcontroller
from picamera.array import PiRGBArray   #import camera lib
from picamera import PiCamera #import camera lib
import RPi.GPIO as GPIO #import GPIO lib
#import serial           #import Serial(UART) lib , need enable hardware uart in Rasp's setting

import numpy as np
import cv2              #import opencv lib
import smbus
import time

# LCD CODE

# Define some device parameters
I2C_ADDR  = 0x3F # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LCD_BACKLIGHT  = 0x08  # On
LCD_NO_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD,LCD_BACKLIGHT) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD,LCD_BACKLIGHT) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD,LCD_BACKLIGHT) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD,LCD_BACKLIGHT) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD,LCD_BACKLIGHT) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD,LCD_BACKLIGHT) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode, ledonoff):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | ledonoff
  bits_low = mode | ((bits<<4) & 0xF0) | ledonoff

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line,ledonoff):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD,LCD_BACKLIGHT)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR,ledonoff)

lcd_init()


###############DETECT CODE###########################################################################

lower1 = np.array([81,35,141])
upper1 = np.array([157,255,255])

lower2 = np.array([49,113,70])
upper2 = np.array([206,255,109])

Ratio = 0.90            # Rate of distance, greater will be checked easier

GPIO.setmode(GPIO.BCM)  #Use GPIO name pin on Rasp, and not use pin number on Rasp

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Setup pullup internal resistor input 
GPIO.setup(5, GPIO.OUT, initial=False)  # CAMERA led
GPIO.output(5,False)  # Turn off camera led

GPIO.setup(24, GPIO.OUT) # White led inside box
GPIO.output(24, GPIO.HIGH) # Turn off white led 

# With surf and sift we can use bf or flann, akaze only use akaze
#detector=cv2.xfeatures2d.SIFT_create()
#detector = cv2.xfeatures2d.SURF_create()
detector = cv2.AKAZE_create()

#FLANN
FLANN_INDEX_KDITREE=0   #Procedures
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)   #Procedures
flann=cv2.FlannBasedMatcher(flannParam,{})  #Procedures

#BF
#BF = cv2.BFMatcher()

#AKAZE
AKAZE = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)

# This is an array, each of the elements is a name directory of image.
# Dataset array
TraingIMGArr = ["TrainingData/10000F.jpg","TrainingData/10000B.jpg",
                "TrainingData/20000F.jpg","TrainingData/20000B.jpg",
                "TrainingData/50000F.jpg","TrainingData/50000B.jpg",
                "TrainingData/100000F.jpg","TrainingData/100000B.jpg",
                "TrainingData/200000F.jpg","TrainingData/200000B.jpg",
                "TrainingData/500000F.jpg","TrainingData/500000B.jpg"
                ]

# Use to print to console and LCD
PrintingElement = ["10000","10000",
                    "20000","20000",
                    "50000","50000",
                    "100000","100000",
                    "200000","200000",
                    "500000","500000"
                    ]

print("WAITING TO GET FEATURE ...") #Print to console

#Print to LCD 
lcd_string("GETTING FEATURE",LCD_LINE_1,LCD_BACKLIGHT)
lcd_string("WAITING RESPONSE",LCD_LINE_2,LCD_BACKLIGHT)

#Loading features of dataset to DesArr 
DesArr = np.load("feature.npy") 

print("START - PRESS BUTTON TO TAKE A PICTURE TO DETECT") #Print to console
#Print to LCD 
lcd_string(" WAITING BUTTON",LCD_LINE_1,LCD_BACKLIGHT)
lcd_string("",LCD_LINE_2,LCD_BACKLIGHT)

while(1):

    if GPIO.input(23) == False: # If press button
        while GPIO.input(23) == False: # While press button (don't do anything)
            {}
        # Get start time
        start = time.time()
        # Print to LCD 
        lcd_string("",LCD_LINE_2,LCD_BACKLIGHT)
        lcd_string(" GETTING IMAGE! ",LCD_LINE_1,LCD_BACKLIGHT)

        # Turn on WHITE LED inside box (set LOW because i'm using LOW trigger for turn ON led)
        GPIO.output(24, GPIO.LOW)

        # Print to LCD 
        print("DETECTING ....... ")
        
        # Ready to take a picture
        camera = PiCamera() #Procedures
        sleep(1) #delay 2sec let camera stable
        camera.capture("userimg.jpg") # Cap a picture with name userimg.img
        camera.close() #Turn off camera

        # Turn off WHITE LED
        GPIO.output(24, GPIO.HIGH)
        
        # Read image has just taken
        Raw_usr_img=cv2.imread("userimg.jpg") #Read img from user (captured from raspberry)
        PhotoDetect = cv2.resize(Raw_usr_img, (640,480))
        PhotoDetect=PhotoDetect[130:420,40:630]
        hsv_img = cv2.cvtColor(PhotoDetect, cv2.COLOR_BGR2HSV)   # HSV image
        
        mask_sub1 = cv2.inRange(hsv_img , lower1, upper1)
        mask_sub2 = cv2.inRange(hsv_img , lower2, upper2)
        mask = cv2.bitwise_or(mask_sub1,mask_sub2)
        _,contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        suma=0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            suma=suma+area
        result=suma/(PhotoDetect.shape[0]*PhotoDetect.shape[1])*100
        #print(result)
        if result>120:
            print ("PHOTO MONEY")
            lcd_string(" PHOTO MONEY :) ",LCD_LINE_1,LCD_BACKLIGHT)
        else:
            Raw_usr_img=cv2.imread("userimg.jpg") #Read img from user (captured from raspberry)
            queryKP,queryDesc=detector.detectAndCompute(Raw_usr_img,None) #Procedures to get feature from this picture
        
            max_point = 0; # Max point
            index_element_arr = 0; # Index which picture are detecting or detected to print out LCD or console

            # Print to LCD
            lcd_string("   DETECTING:   ",LCD_LINE_1,LCD_BACKLIGHT)

            for i in range(len(TraingIMGArr)):            
                matches=AKAZE.knnMatch(queryDesc,DesArr[i],k=2) #Procedures 

                print("DETECTING - " + PrintingElement[i]) #Print to console which image are being processed
                lcd_string("   "+PrintingElement[i] + " VND ",LCD_LINE_2,LCD_BACKLIGHT) #Print to LCD

                Match_Count = 0 # Create a variable to count match points from 2 images
                for m,n in matches:
                    if(m.distance < Ratio * n.distance):   #If match 
                        Match_Count += 1    #increase by 1
                print(Match_Count)  #Print to console, comment if don't need it
                if Match_Count >= max_point: # If the Match_Count greater than max_point
                    max_point = Match_Count  # Assign max_point again
                    index_element_arr = i;   # Assign idex to print to console and LCD 
            # Get end time
            end = time.time()
            print(end - start)
            
            #If box is empty, the match count usually < 30 MatchPoint
            if Match_Count > 24:
                #Print running time
                print("THAT IS - " + PrintingElement[index_element_arr]) #After run all dataset, print to console which money was detected
        
                #Print to LCD
                lcd_string("    THAT IS:    ",LCD_LINE_1,LCD_BACKLIGHT)
                lcd_string("   "+PrintingElement[index_element_arr] + " VND ",LCD_LINE_2,LCD_BACKLIGHT)
            else:
                print("BOX IS EMPTY")
                lcd_string("  BOX IS EMPTY  ",LCD_LINE_1,LCD_BACKLIGHT)
                lcd_string(" ",LCD_LINE_2,LCD_BACKLIGHT)
            
            