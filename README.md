# Currency-of-VND-Recognition
Special thanks to my lecturer gave me solution to recognize currency as fastest as possible, and thanks to Codacus channel give me tutorial about object recognition

# Tools
  - OpenCV 3.4.3
  - Python3
  - Raspberry library (GPIO,I2C,Camera,..)
  - SIFT/SURF/AKAZE algorithm in contribution library of OpenCV (Recommend install OpenCv by Cmake, not recommend use pip install)
  
# Operating steps:
  1. Run 'TestCamerabyStreamVideo.py' to check camera 
  2. Input money, then while opening file above to make sure money in good position
  3. Open 'TakeAPictureToGetDataSet.py' to edit corresponding directory with money type
  4. Run 'TakeAPictureToGetDataSet.py' to take picture and save to directory you edited
  5. Open 'CreateFeatureFile.py' to edit corresponding directory in array, change get feature recognition algorithm if necessary
  6. Run 'CreateFeatureFile.py' and wait until it finised and export 'feature.npy' file in the current folder
  7. Open 'Detect.py' to edit corresponding directory in array, change recognition algorithm if necessary
  8. Run 'Detect.py' then enjoy the project

# Devices
  - Raspberry Pi 3B+
  - Camera Pi 5M
  - LCD I2C 16x02
  - Accessories (Carton, button , wires,…)

# Time comparision
  - Watch my video to see it : https://youtu.be/NwosF7BgHX8

# Reference 
  - https://thecodacus.com/object-recognition-using-opencv-python/
