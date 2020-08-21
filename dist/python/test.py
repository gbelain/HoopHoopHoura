# -*- coding: utf-8 -*-

from ball_tracking import processVideo

a, b = processVideo("test_video.MOV")
print "le resultat final est " + \
    str(a) + "tirs effectues et " + str(b) + "tir reussis"
