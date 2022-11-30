import cv2
import numpy as np
import pandas as pd

cap = cv2.VideoCapture('elbow_24.mp4')

def CheckEntranceLineCrossing(x, CoorXEntranceLine):
   AbsDistance = abs(x - CoorXEntranceLine)	
   if ((AbsDistance <= 9) and (x <= CoorXEntranceLine)): #change here 5 based on frame rate
      return 1
   else:
      return 0
"""
def CheckExitLineCrossing(x,CoorXExitLine):
   AbsDistance = abs(x - CoorXExitLine)	
   if ((AbsDistance <= 50) and (x < CoorXExitLine)):
	   return 1
   else:
	   return 0
"""
counter = 0
EntranceCounter = 0
ExitCounter = 0

while True:
   i = 0
   for i in range(500000):   #for delay in frames
      i = i+1
   ret,frame = cap.read()
   #frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
   #frame = cv2.resize(frame,(310,375))
   #frame = frame[95:405,0:375]
   frame = frame[10:,100:600]
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   #(thresh, binary) = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
   (thresh, binary) = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
   #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   #lower_blue = np.array([40,0,130])
   #upper_blue = np.array([255,255,255])
   #mask = cv2.inRange(hsv, lower_blue, upper_blue)
   kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
   erosion_image = cv2.erode(binary, kernel, iterations=5)
   #dilation_image = cv2.dilate(binary, kernel, iterations=2)
   #morph = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
   contours,d = cv2.findContours(erosion_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
   CoorXEntranceLine =  50
   CoorXExitLine = 200
   cv2.line(frame, (CoorXEntranceLine,0), (CoorXEntranceLine,700), (255, 0, 0), 2)
   #cv2.line(frame, (CoorXExitLine,0), (CoorXExitLine,310), (0, 0, 255), 2)
   for cnt in contours:
      area = cv2.contourArea(cnt)
      if 1000 <area< 4000:
      #if 100<area<900:

         (x,y,w,h) = cv2.boundingRect(cnt)
         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
         CoordXCentroid = int((x+x+w)/2)
         CoordYCentroid = int((y+y+h)/2)
         ObjectCentroid = (CoordXCentroid,CoordYCentroid)
         cv2.circle(frame, ObjectCentroid, 1, (0, 0, 255), 7)      
         if (CheckEntranceLineCrossing(CoordXCentroid,CoorXEntranceLine))==1 :
            ExitCounter += 1 

   count = "Counts:"+str(ExitCounter)
   cv2.putText(frame, count, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
   cv2.imshow("frame",erosion_image)
   cv2.imshow("contours",frame)
   key = cv2.waitKey(1)
   if key == 27:  #esc key for destroy all the windows
      break

cap.release()
cv2.destroyAllWindows()

    