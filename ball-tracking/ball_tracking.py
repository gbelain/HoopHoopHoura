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


def findHoopLocation(vs):
    vs.set(1, 5)
    boleen, frame = vs.read()

    frame = imutils.resize(frame, width=600)
    cv2.imwrite("la frame de base"+'.jpg', frame)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    cv2.imwrite("la frame blurred"+'.jpg', blurred)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imwrite("la frame hsv"+'.jpg', hsv)

    mask = cv2.inRange(hsv, redLower, redUpper)
    cv2.imwrite("le mask"+'.jpg', mask)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imwrite("le mask apres traitement"+'.jpg', mask)

    # cnts = cv2.findContours(
    #     mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # center = None

    # only proceed if at least one contour was found
    # if len(cnts) > 0:
    #     # find the largest contour in the mask, then use
    #     # it to compute the minimum enclosing circle and
    #     # centroid
    #     c = max(cnts, key=cv2.contourArea)
    #     ((x, y), radius) = cv2.minEnclosingCircle(c)
    #     M = cv2.moments(c)
    #     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    #     # only proceed if the radius meets a minimum size
    #     if radius > 10:
    #         # draw the circle and centroid on the frame,
    #         # then update the list of tracked points
    #         cv2.circle(frame, (int(x), int(y)), int(radius),
    #                    (0, 255, 255), 2)
    #         cv2.circle(frame, center, 5, (0, 0, 255), -1)


def findAndShowBallLocation(frame, orangeLower, orangeUpper):
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


######################################################################################

# define the lower and upper boundaries of the "orange"
# ball in the HSV color space, then initialize the
# list of tracked points
orangeLower = (7, 100, 20)
orangeUpper = (22, 250, 255)

redLower = (0, 150, 20)
redUpper = (5, 255, 255)

dequeLength = 64
videoName = "test_video.MOV"

pts = deque(maxlen=dequeLength)

vs2 = cv2.VideoCapture(videoName)
time.sleep(2.0)

findHoopLocation(vs2)

vs2.release()

# grab a reference to the video file
vs = cv2.VideoCapture(videoName)

# allow the camera or video file to warm up
time.sleep(2.0)

# hoopLocation = findHoopLocation(vs)

while True:
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture
    frame = frame[1]
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    findAndShowBallLocation(frame, orangeLower, orangeUpper)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# release the video/camera
vs.release()
# close all windows
cv2.destroyAllWindows()
