import cv2
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')

output_file = cv2.VideoWriter('ProBlackScreen.avi' , fourcc , 20.0 , (640 , 480))

#Start the camera
cam = cv2.VideoCapture(0)

#Allow the camera to read the background by sleeping for 2 seconds
time.sleep(2)
bg = 0

#Capture the background for 60 frames
for i in range (60) :
    ret , bg = cam.read()
bg = np.flip(bg , axis = 1)

#Reading the captured frame till the camera is open
while (cam.isOpened()) :
    ret , img = cam.read()
    if not ret :
        break
    #Flip the image
    img = np.flip(img , axis = 1)

    #Convert the colour from BGR to HSV
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #Generate Mask to find red color
    Ublack = np.array([8, 8, 8])
    Lblack = np.array([74, 72, 72])
    mask_1 = cv2.inRange(hsv , Ublack , Lblack)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255 , 255])
    mask_2 = cv2.inRange(hsv , lower_red , upper_red)

    mask_1 = mask_1+ mask_2

    #Open and expand the image where there is mask 1
    mask_1 = cv2.morphologyEx(mask_1 , cv2.MORPH_OPEN , np.ones((3,3),np.uint8))
    mask_1 = cv2.morphologyEx(mask_1 , cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    #Select the part that does not have the mask 1 (red colour) and save in mask two
    mask_2 = cv2.bitwise_not(mask_1)

    #Keep the part of images without red color
    res_1 = cv2.bitwise_and(img , img , mask = mask_2)

    #Keep the part of images with red color
    res_2 = cv2.bitwise_and(bg, bg , mask = mask_1)

    #File merging res1 , res2 
    final_output = cv2.addWeighted(res_1 , 1 , res_2 , 1 , 0)
    output_file.write(final_output)
    #Display the output
    cv2.imshow("Pragna's cloak" , final_output)
    cv2.waitKey(1)

cam.release()
out.release()
cv2.destroyAllWindows()








