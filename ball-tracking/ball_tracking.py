# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
# list-like data structure for storing the past x,y locations of the ball
from collections import deque
from imutils.video import VideoStream
# install with : $ pip install --upgrade imutils
import numpy as np
import argparse
import cv2
import imutils
import time

######################################################################################


def findHoopCenterLocation(vs):
    vs.set(1, 5)
    boleen, frame = vs.read()
    frame = imutils.resize(frame, width=600)
    # cv2.imwrite("la frame de base"+'.jpg', frame)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    # cv2.imwrite("la frame blurred"+'.jpg', blurred)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # cv2.imwrite("la frame hsv"+'.jpg', hsv)
    mask = cv2.inRange(hsv, redLower, redUpper)
    # cv2.imwrite("le mask"+'.jpg', mask)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # blurredMask = cv2.GaussianBlur(mask, (11, 11), 0)
    # cv2.imwrite("le mask apres traitement"+'.jpg', mask)
    cnts = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # countShapesSides = 10
        circleContour = None
        # for c in cnts:
        #     # compute the center of the contour
        #     # M = cv2.moments(c)
        #     # cX = int(M["m10"] / M["m00"])
        #     # cY = int(M["m01"] / M["m00"])

        #     peri = cv2.arcLength(c, True)
        #     approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        #     print len(approx)
        #     if len(approx) < countShapesSides:
        #         countShapesSides = len(approx)
        #         circleContour = c
        circleContour = max(cnts, key=cv2.contourArea)
        # draw the contour and center of the shape on the image

        M = cv2.moments(circleContour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.drawContours(frame, [circleContour], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX+16, cY-14), 3, (255, 255, 255), -1)
        # show the image
        cv2.imshow("les contours", frame)
        cv2.waitKey(0)
        return (cX+16, cY-14)
    else:
        print "pas de contour trouve"
        return None


def findBallLocation(frame, orangeLower, orangeUpper):
    global pts
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "orange", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    # raw_input("Press Enter to continue...")
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(dequeLength / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)


def IsTakingAShot(xBall):
    global shotTaken
    global shotCount
    if xBall < xHoop:
        if not shotTaken:
            shotTaken = True
            shotCount += 1
    else:
        if shotTaken:
            shotTaken = False
    return None


######################################################################################

    # define the lower and upper boundaries of the "orange"
    # ball in the HSV color space, then initialize the
    # list of tracked points
orangeLower = (7, 100, 20)
orangeUpper = (22, 250, 255)

redLower = (0, 100, 20)
redUpper = (10, 255, 255)

dequeLength = 64
videoName = "test_video.MOV"

pts = deque(maxlen=dequeLength)

vsHoop = cv2.VideoCapture(videoName)
# allow the camera or video file to warm up
time.sleep(2.0)
(xHoop, yHoop) = findHoopCenterLocation(vsHoop)
vsHoop.release()

vs = cv2.VideoCapture(videoName)
time.sleep(2.0)

shotTaken = False
shotCount = 0
while True:
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture
    frame = frame[1]
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    findBallLocation(frame, orangeLower, orangeUpper)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# release the video/camera
vs.release()
# close all windows
cv2.destroyAllWindows()
