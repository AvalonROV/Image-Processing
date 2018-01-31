# SKIP FRAMES to increase the speed

import cv2
import numpy as np
import math
cap=cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
# If use an image, then not infinite loop and also use imread instead of Frame


def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)
    
scale=2
#HSV better than RGB, Each value in HSV are format, but in RGB these are dependent. V- Color Value, S - Satuation like intensity and H - hue -This dictates the color
# This function are responsible for filtering colour
lower_red=np.array([150,150,0])
upper_red=np.array([180,255,255])

# You can apply filters which literally just blurs the images, thus ignoring any distrurbances
lower_blue=np.array([100,150,0])
upper_blue=np.array([140,255,255])

lower_yellow=np.array([20, 100, 100])
upper_yellow=np.array([30, 255, 255])

def changeFrameColour(lower_value,upper_value):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_value,upper_value)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    median_value=cv2.medianBlur(res,15)
    return median_value
    
def areaCalculate(median_value):
    edges=cv2.Canny(median_value,100,200)
    canny2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for plc,contour in enumerate(contours):
        area=cv2.contourArea(contour)
        if area>300:
            return 1
        else:
            return 2

def shapeIdentifier(median_value,name_tri,name_rectangle):
        edges=cv2.Canny(median_value,100,200) # CHANGE THE 'FRAME' TO 'RES' FOR THE ORIGINAL CODE
        canny2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for i in range(0,len(contours)):
            #approximate the contour with accuracy proportional to
            #the contour perimeter
            approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)
            #Skip small or non-convex objects
            if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):
                continue
    
            #triangle
            if(len(approx)==3):
                x,y,w,h = cv2.boundingRect(contours[i])
                cv2.putText(frame,name_tri,(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            
            elif(len(approx)>=4 and len(approx)<=6):
                vtc = len(approx)
                cos = []
                for j in range(2,vtc+1):
                    cos.append(angle(approx[j%vtc],approx[j-2],approx[j-1]))
            #sort ascending cos
                cos.sort()
            #get lowest and highest
                mincos = cos[0]
                maxcos = cos[-1]

            #Use the degrees obtained above and the number of vertices
            #to determine the shape of the contour
                x,y,w,h = cv2.boundingRect(contours[i])
                #Rectangle
                if(vtc==4):
                    cv2.putText(frame,name_rectangle,(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            else:
                None
     
while True:
    _,frame=cap.read() #'_' is a value returned to this function, but we don't care about that value

    median_red=changeFrameColour(lower_red,upper_red)
    area_red=areaCalculate(median_red)
    
    median_blue=changeFrameColour(lower_blue,upper_blue)
    area_blue=areaCalculate(median_blue)
    
    median_yellow=changeFrameColour(lower_yellow,upper_yellow)
    area_yellow=areaCalculate(median_yellow)
    
    #Using elif instead of multiple If's as the program should detect only one colour at a time
    if(area_red==1): #MAKE THE CONDITION THAT ONLY DETECT ONE COLOUR  AT TIME , X==1 AND Y!=1 AND Z!=1
        cv2.imshow('median',median_red)
        median_value=median_red
        shapeIdentifier(median_value,'TRI_R','RECT_R')
    elif(area_blue==1):
        #cv2.imshow('median',median_blue)
        median_value=median_blue
        shapeIdentifier(median_value,'TRI_B','RECT_B')
    if(area_yellow==1):
        #cv2.imshow('median',median_yellow)
        median_value=median_yellow
        shapeIdentifier(median_value,'TRI_Y','RECT_Y')
    else:
        #print('')
        None
    
    cv2.imshow('frame',frame)
    cv2.waitKey(10)

    
cv2.destroyAllWindows()
cap.release()