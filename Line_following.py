#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:36:36 2019

@author: Marwan Taher 
"""

import numpy as np
import cv2

cap = cv2.VideoCapture(1)

depth = 60
width = 80

x_centre = 320
y_centre = 240

current_direction = None

directions = ["Top", "Right", "Bottom", "Left"]

while(True):
    ret, main_frame = cap.read()
    
    croped_frame = [
            main_frame [0:depth, x_centre-width:x_centre+width], #Top
            main_frame [y_centre-width:y_centre+width, 639-depth:639], #Right
            main_frame [479-depth:479, x_centre-width:x_centre+width], #Bottom
            main_frame [y_centre-width:y_centre+width, 0:depth] #Left
            ]
    
    cv2.line(main_frame, (320,0), (320, 480), (0, 0, 255), 2)
    cv2.line(main_frame, (0,240), (640, 240), (0, 0, 255), 2)
    cv2.line(main_frame, (x_centre,0), (x_centre, 480), (0, 240, 0), 2)
    cv2.line(main_frame, (0,y_centre), (640, y_centre), (0, 240, 0), 2)
    
    '''
    cv2.imshow("Top",croped_frame[0])
    cv2.imshow("Right", croped_frame[1])
    cv2.imshow("Bottom", croped_frame[2])
    cv2.imshow("Left", croped_frame[3])
    '''
    
    for x in range(4):        
        gray = cv2.cvtColor(croped_frame[x], cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0) 
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, 1 , cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            cv2.drawContours(croped_frame[x], contours, -1, (0, 100, 0), 2)
            if current_direction == None:
                current_direction = x
                break
            #else:
                #print("Triggered: " + directions[current_direction])    
            
            if current_direction +2 != x and current_direction-2 != x:
                current_direction = x
                #print("Triggered: " + directions[current_direction])
                break

    cv2.imshow("Main_frame", main_frame)

    
    if current_direction == 0: #Top
        x_centre = 320
        y_centre = 80
        
    elif current_direction == 1: #Right
        x_centre = 559
        y_centre = 240
        
    elif current_direction == 2: #Bottom
        x_centre = 320
        y_centre = 399
        
    elif current_direction == 3: #Left
        x_centre = 80
        y_centre = 240

    
    if current_direction != None:
        print(directions[current_direction])
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
    