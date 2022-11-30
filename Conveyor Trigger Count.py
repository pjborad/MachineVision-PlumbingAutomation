import cv2
import numpy as np
from scipy.io import savemat
import pyfirmata
import sys

def main(area1,area2,peri1,peri2,threshold):
    Board = pyfirmata.Arduino('COM3')
    it = pyfirmata.util.Iterator(Board)  
    it.start()
    Board.digital[4].mode = pyfirmata.INPUT
    Board.digital[13].mode = pyfirmata.OUTPUT
    cap = cv2.VideoCapture(0)
    counter =0
    while True:   
        stat, frame = cap.read()
        cv2.imshow('frame',frame)
        Status = cv2.waitKey(25) 
        Board.digital[13].write(1)   
        if Board.digital[4].read()==1:        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (thresh, binary) = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            erosion_image = cv2.erode(binary, kernel, iterations=2)
            contours,d = cv2.findContours(erosion_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                peri = cv2.arcLength(cnt,True)
                if area>2000: 
                    (x,y,w,h) = cv2.boundingRect(cnt)
                    if peri1<peri<peri2 and area1<area<area2:
                        cv2.putText(frame, 'elbow', (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                        counter = counter+1
                    else:
                        cv2.putText(frame, 'Not elbow', (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)            
            cv2.putText(frame, 'count:'+str(counter), (20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
            cv2.imshow('erode',erosion_image)       
            cv2.imshow("contours",frame)
            i = 0
            for i in range(1000000):
                i = i+0
        if Status == 27: #esc key for destroy all the windows
            break
    return counter,frame

if __name__ == "__main__":
    area1 = float(sys.argv[1])
    area2 = float(sys.argv[2])
    peri1 = float(sys.argv[3])
    peri2 = float(sys.argv[4])
    threshold = float(sys.argv[5])
    sys.stdout.write(str(main(area1,area2,peri1,peri2,threshold)))

 
