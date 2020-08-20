# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py
# import the necessary packages
# list-like data structure for storing the past x,y locations of the ball
import time
import imutils
import cv2
import argparse
import numpy as np
from imutils.video import VideoStream
from collections import deque
# install with : $ pip install --upgrade imutils

######################################################################################


def findHoopCenterLocation(frame):
    frameCopy = imutils.resize(frame.copy(), width=600)
    # cv2.imwrite("la frame de base"+'.jpg', frame)
    blurred = cv2.GaussianBlur(frameCopy, (11, 11), 0)
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
        # cv2.drawContours(frame, [circleContour], -1, (0, 255, 0), 2)
        # cv2.circle(frame, (cX+16, cY-14), 3, (255, 255, 255), -1)
        # # show the image
        # cv2.imshow("les contours", frame)
        # cv2.waitKey(0)
        return (cX+16, cY-14)
    else:
        print "pas de contour trouve"
        return None


def findBallLocation(frame, orangeLower, orangeUpper):
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
    ballCenter = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        ballCenter = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, ballCenter, 5, (0, 0, 255), -1)

    return frame, ballCenter


def IsTakingAShot(xBall):
    global shotTaken
    global shotTakenCount
    global thisShotWasMade
    if xBall < hoopLocation[0]-75:
        if not shotTaken:
            shotTaken = True
            shotTakenCount += 1
    elif xBall > hoopLocation[0]+60:
        if shotTaken:
            shotTaken = False
            thisShotWasMade = False
    return None


def ShotMade(ballCenter, hoopLocation):
    global shotMadeCount
    global thisShotWasMade
    if (ballCenter[1] > hoopLocation[1]-13 and ballCenter[1] < hoopLocation[1]+13) and (ballCenter[0] > hoopLocation[0]-4 and ballCenter[0] < hoopLocation[0]+10) and not thisShotWasMade:
        shotMadeCount += 1
        thisShotWasMade = True
        print "panier marque"
    return None


def CheckTrajectory(whileCount, ballCenter, pts):
    if whileCount >= 2 and ballCenter is not None and pts[0] is not None:
        positionBallonPrec = pts[0]
        if positionBallonPrec != ballCenter:
            trajectoireBallon = (pow((ballCenter[1]-positionBallonPrec[1]), 2) +
                                 pow((ballCenter[0]-positionBallonPrec[0]), 2))**0.5
            # print abs(trajectoireBallon)
            # distance maxmimale acceptable entre 2 localisation du ballon
            if abs(trajectoireBallon) > 140:
                ballCenter = positionBallonPrec
    return ballCenter


def DisplayTrackingOnFrame(pts, shotTaken, thisShotWasMade, hoopLocation, frame):
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

    if shotTaken:
        cv2.putText(frame, " en train de tirer", (425, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 255, 255), 2)
    # show the frame to our screen
    cv2.line(frame, (hoopLocation[0], hoopLocation[1]-13),
             (hoopLocation[0], hoopLocation[1]+13), (255, 0, 0), 5)
    # cv2.line(frame, (hoopLocation[0]-75, 1),
    #          (hoopLocation[0]-75, 500), (0, 0, 255), 2)
    # cv2.line(frame, (hoopLocation[0]+60, 1),
    #  (hoopLocation[0]+60, 500), (0, 0, 255), 2)
    if thisShotWasMade:
        cv2.putText(frame, "PANIER MARQUE !!", (420, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 2)
    return frame


######################################################################################
# define the lower and upper boundaries of the "orange"
# ball in the HSV color space, then initialize the
# list of tracked points
orangeLower = (7, 100, 20)
orangeUpper = (22, 250, 255)

redLower = (0, 100, 20)
redUpper = (10, 255, 255)

dequeLength = 20
videoName = "test_video.MOV"

vs = cv2.VideoCapture(videoName)
time.sleep(2.0)

pts = deque(maxlen=dequeLength)
shotTaken = False
shotTakenCount = 0
shotMadeCount = 0
hoopLocation = None
whileCount = 0
thisShotWasMade = False

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("outputVideo.avi", fourcc, 20, (600, 337), True)

while True:
    # grab the current frame and handle the frame from VideoCapture
    frame = vs.read()
    frame = frame[1]
    # if we are viewing a video and we did not grab a frame,then we have reached the end of the video
    if frame is None:
        break
    hoopLocation = findHoopCenterLocation(frame)
    frame, ballCenter = findBallLocation(frame, orangeLower, orangeUpper)
    # check trajectory and update the points queue
    pts.appendleft(CheckTrajectory(whileCount, ballCenter, pts))

    if not ballCenter == None:
        IsTakingAShot(ballCenter[0])
        ShotMade(ballCenter, hoopLocation)

    frame = DisplayTrackingOnFrame(
        pts, shotTaken, thisShotWasMade, hoopLocation, frame)

    cv2.imshow("Frame", frame)
    out.write(frame)
    whileCount += 1
    # if the 'q' key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

out.release()
# release the video/camera
vs.release()
# close all windows
cv2.destroyAllWindows()


print "tirs effectues : " + str(shotTakenCount)
print "tirs reussis : " + str(shotMadeCount)
print "pourcentage de reussite : " + \
    str((float(shotMadeCount)/float(shotTakenCount))*100)
