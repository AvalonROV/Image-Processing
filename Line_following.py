import numpy as np
import cv2

img = cv2.VideoCapture(1)
temporary = ""

old_x = None
old_y = None
while(True):

    ret, frame = img.read()
    crop_img = frame    #################################
    offset = 50
    horizontal = crop_img[240-offset:240+offset, :]
    vertical = crop_img[:,320-offset:320+offset]
        
    h_gray = cv2.cvtColor(horizontal, cv2.COLOR_BGR2GRAY) #was crop_img instead of frame
    h_blur = cv2.GaussianBlur(h_gray, (5, 5), 0) #Gasian blur to remove unneeded stuff from the background
    h_ret, h_thresh = cv2.threshold(h_blur, 60, 255, cv2.THRESH_BINARY_INV) #threshold values https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html so we convert image to boolean (white and black pixels)
    _, h_contours, h_hierarchy = cv2.findContours(h_thresh, 1 , cv2.CHAIN_APPROX_NONE) #https://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html used to join similar pixels together. Need to be proceed on binnary image

    v_gray = cv2.cvtColor(vertical, cv2.COLOR_BGR2GRAY) #was crop_img instead of frame
    v_blur = cv2.GaussianBlur(v_gray, (5, 5), 0) #Gasian blur to remove unneeded stuff from the background
    v_ret, v_thresh = cv2.threshold(v_blur, 60, 255, cv2.THRESH_BINARY_INV) #threshold values https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html so we convert image to boolean (white and black pixels)
    _, v_contours, v_hierarchy = cv2.findContours(v_thresh, 1 , cv2.CHAIN_APPROX_NONE) 
    
    if len(h_contours) > 0:

        c = max(h_contours, key=cv2.contourArea)                #https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html

        M = cv2.moments(c)

        try:
            center_x = int(M['m10'] /M['m00'])  #take x middle coordinate
            center_y = int(M['m01'] / M['m00'])  #take y middle coordinates
        except:
            pass
        
        x, y, w, h = cv2.boundingRect(c)

        cv2.line(crop_img, (center_x , 0), (center_x , 480), (255, 0, 0), 2)  #draw vertical line

        cv2.line(crop_img, (0, center_y), (640, center_y), (255, 0, 0), 2)   #draw horizontal line

        cv2.line(crop_img, (320,0), (320, 480), (0, 0, 255), 2)

        cv2.line(crop_img, (0,240), (640, 240), (0, 0, 255), 2)


        #cv2.line(blur, (320,0), (320, 480), (0, 0, 255), 2)

        #cv2.line(blur, (0,240), (640, 240), (0, 0, 255), 2)

        #cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 2)


        x_offset = 40
        y_offset = 40

        if center_x > 320 + x_offset:
            temp_x = "Right"
        elif center_x < 320 - x_offset:
            temp_x = "Left"
        else:
             temp_x = "off"
        
        print("Horizontal: " + temp_x)
        
    else:
        print("I don't see the h_line")
    
    if len(v_contours) > 0:

        c = max(v_contours, key=cv2.contourArea)                #https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html

        M = cv2.moments(c)
        
        try:
            center_x = int(M['m10'] /M['m00'])  #take x middle coordinate
            center_y = int(M['m01'] / M['m00'])  #take y middle coordinates
        except:
            pass
        x_offset = 40
        y_offset = 40

        if center_y < 240 + y_offset:
            temp_y = "Up"
        elif center_y > 240 - y_offset:
            temp_y = "Down"
        else:
            temp_y = "off"        
   
        print("Vertical : " + temp_y)
    else:
        print("I don't see the v_line")
        
    

    cv2.imshow("Image", frame)
    #cv2.imshow("Edge",blur)
    cv2.imshow("horizontal", horizontal)
    cv2.imshow("vertical", vertical)


    #cv2.imshow("Edges", gray)
    if cv2.waitKey(1) & 0xFF == ord('`'):
        break

img.release()
cv2.destroyAllWindows()











