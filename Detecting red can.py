import cv2
import numpy as np

# Setting up Trackbar

cv2.namedWindow("myTrackbar")
cv2.resizeWindow("myTrackbar",560,240)
def empty():
    pass
cv2.createTrackbar("Hue min","myTrackbar",0,255,empty)
cv2.createTrackbar("Hue max","myTrackbar",61,255,empty)
cv2.createTrackbar("Saturation min","myTrackbar",0,255,empty)
cv2.createTrackbar("Saturation max","myTrackbar",255,255,empty)
cv2.createTrackbar("Value min","myTrackbar",75,255,empty)
cv2.createTrackbar("Value max","myTrackbar",255,255,empty)

# Contour and StackImage functions

def getContours(the_imageMasked,theDisplayingImage):
    contours,hierarchy = cv2.findContours(the_imageMasked,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area_cnt = cv2.contourArea(cnt)
        if area_cnt < 100:
            pass
        elif area_cnt > 46000:
            pass
        else:
            print(area_cnt)
            cv2.drawContours(theDisplayingImage,cnt,-1,(0,255,0),3)
            peri = cv2.arcLength(cnt,True)
            c = max(cnt, key = cv2.contourArea)
            x,y,h,w = cv2.boundingRect(c)
            cv2.rectangle(theDisplayingImage,(x,y),(x+w,y+h),(0,255,0),5)
            # approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # objCor = len(approx)
            # x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(theDisplayingImage,(x,y),(x+w,y+h),(0,255,0),5)
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

while(True):
    hue_min = cv2.getTrackbarPos("Hue min","myTrackbar")
    hue_max = cv2.getTrackbarPos("Hue max","myTrackbar")
    Saturation_min = cv2.getTrackbarPos("Saturation min","myTrackbar")
    Saturation_max = cv2.getTrackbarPos("Saturation max","myTrackbar")
    Value_min = cv2.getTrackbarPos("Value min","myTrackbar")
    Value_max = cv2.getTrackbarPos("Value max","myTrackbar")

    lowers = np.array([hue_min,Saturation_min,Value_min])
    uppers = np.array([hue_max,Saturation_max,Value_max])


#  image, cannyImage, MaskImage, Contour Image

    img = cv2.imread("C:\\Users\\hp\\OneDrive\\Desktop\\1661615959749.jpg")
    img = cv2.resize(img, (920, 720))

    imgContour = img.copy()
    imgCanny = cv2.Canny(img,50,100)
    imgMask = cv2.inRange(img,lowers,uppers)

    getContours(imgMask,imgContour)
    stacked_images = stackImages(0.4,([img,imgMask,imgContour]))
    cv2.imshow("all_images_stacked",stacked_images)
    cv2.imwrite("D:\\canImageDetection0.jpg",imgContour)
    if cv2.waitKey(1) == ord("q"):
        break





