from pickletools import uint8
import cv2
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(3,560)
capture.set(4,720)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



    
def empty():
    pass

cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar",560,240)    
cv2.createTrackbar("Hue min","TrackBar",0,255,empty)
cv2.createTrackbar("Saturation min","TrackBar",63,255,empty)
cv2.createTrackbar("Value min","TrackBar",255,255,empty)
cv2.createTrackbar("Hue max","TrackBar",255,255,empty)
cv2.createTrackbar("Saturation max","TrackBar",255,255,empty)
cv2.createTrackbar("Value max","TrackBar",255,255,empty)

while(True):

    success,frame = capture.read()

    hue_min = cv2.getTrackbarPos("Hue min","TrackBar")
    saturation_min = cv2.getTrackbarPos("Saturation min","TrackBar")
    value_min = cv2.getTrackbarPos("Value min","TrackBar")
    hue_max = cv2.getTrackbarPos("Hue max","TrackBar")
    saturation_max = cv2.getTrackbarPos("Saturation max","TrackBar")
    value_max = cv2.getTrackbarPos("Value max","TrackBar")

    print("Hue: ",hue_min,hue_max,",Saturation: ",saturation_min,saturation_max,",Value: ",value_min,value_max)

    lower = np.array([hue_min,saturation_min,value_min])
    upper = np.array([hue_max,saturation_max,value_max])

    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    HSV_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    canny_frame = cv2.Canny(frame,50,100)

    mask = cv2.inRange(HSV_frame,lower,upper)

    imgStack = stackImages(0.6,([frame,gray_frame,HSV_frame]))
    cv2.imshow("mask",mask)
    cv2.imshow("imgStack",imgStack)
    cv2.waitKey(1) 




