import numpy as np
import cv2

cap = cv2.VideoCapture(1)
temporary = ""

old_x = None
old_y = None

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
            '''
            condition_1 = current_direction == 0 and x != 2
            condition_2 = current_direction == 1 and x != 3
            condition_3 = current_direction == 2 and x != 0
            condition_4 = current_direction == 3 and x != 1
            
            if condition_1 and condition_2 and condition_3 and condition_4:
                current_direction = x
            '''
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
    
'''
    x=0
    for frame in croped_sections:        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #was crop_img instead of frame
        blur = cv2.GaussianBlur(gray, (5, 5), 0) #Gasian blur to remove unneeded stuff from the background
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV) #threshold values https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html so we convert image to boolean (white and black pixels)
        contours, hierarchy = cv2.findContours(thresh, 1 , cv2.CHAIN_APPROX_NONE) #https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html used to join similar pixels together. Need to be proceed on binnary image

        x += 1
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            
            print(str(x) , str(c))
        



    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #was frame instead of frame
    blur = cv2.GaussianBlur(frame, (5, 5), 0) #Gasian blur to remove unneeded stuff from the background
    ret, thresh = cv2.threshold(frame, 60, 255, cv2.THRESH_BINARY_INV) #threshold values https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html so we convert image to boolean (white and black pixels)
    im2, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
    
    cv2.line(frame, (320,0), (320, 480), (0, 0, 255), 2)
    cv2.line(frame, (0,240), (640, 240), (0, 0, 255), 2)
    
    if len(h_contours) > 0:

        c = max(h_contours, key=cv2.contourArea)                #https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html

        M = cv2.moments(c)

        try:
            center_x = int(M['m10'] /M['m00'])  #take x middle coordinate
            center_y = int(M['m01'] / M['m00'])  #take y middle coordinates
        except:
            pass
        
        cv2.line(frame, (center_x , 0), (center_x , 480), (255, 0, 0), 2)

        x_offset = 40
        y_offset = 40

        if center_x > 320 + x_offset:
            temp_x = "Right"
        elif center_x < 320 - x_offset:
            temp_x = "Left",
        else:
             temp_x = "off"
        
        print("Horizontal: " + str(temp_x))
        
    else:
        print("I don't see the h_line")
    
    if len(v_contours) < 0:

        c = max(v_contours, key=cv2.contourArea)                #https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html

        M = cv2.moments(c)

        try:
            center_x = int(M['m10'] /M['m00'])  #take x middle coordinate
            center_y = int(M['m01'] / M['m00'])  #take y middle coordinates
        except:
            pass
        
        cv2.line(frame, (0, center_y), (640, center_y), (255, 0, 0), 2) 
        
        x_offset = 40
        y_offset = 40

        if center_y < 240 + y_offset:
            temp_y = "Up"
        elif center_y > 240 - y_offset:
            temp_y = "Down"
        else:
            temp_y = "off"        
   
        print("Vertical : " + str(temp_y))
    else:
        print("I don't see the v_line")
        
    

    cv2.imshow("Image", frame)
    cv2.imshow("Edge",blur)
    cv2.imshow("horizontal", horizontal)
    cv2.imshow("vertical", vertical)


    #cv2.imshow("Edges", gray)
    if cv2.waitKey(1) & 0xFF == ord('`'):
        break
'''




