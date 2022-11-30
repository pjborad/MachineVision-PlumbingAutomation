#Importing all the necessary libraries

import cv2
import numpy as np
import pandas as pd
import os
import time
import glob
# import xlsxwriter

# workbook = xlsxwriter.Workbook('hello.xlsx')
# worksheet = workbook.add_worksheet('Sheet1')

# Main logic to count the plumbing fittinfgs from the images
images = glob.glob('./Images/*.jpeg')  #change file name from here
for img in images:
    frame = cv2.imread(img) 
    if frame is not None:
        #frame = frame[10:,100:600] #change the cropping here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (thresh, binary) = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        erosion_image = cv2.erode(binary, kernel, iterations=2)
        contours,d = cv2.findContours(erosion_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt,True)
            if area>2000: 
                (x,y,w,h) = cv2.boundingRect(cnt)
                if 200<peri<270 and 2000<area<5000:
                    cv2.putText(frame, 'elbow', (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                else:
                    cv2.putText(frame, 'Not elbow', (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)            
        #cv2.putText(frame, 'count:'+str(counter), (20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
        cv2.imshow('erode',erosion_image)       
        cv2.imshow("contours",frame)
        # worksheet.write(I,0,counter)
        cv2.waitKey()
        cv2.destroyAllWindows()


