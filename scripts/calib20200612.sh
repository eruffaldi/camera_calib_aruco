#!/bin/bash
SS=5.5
ROWS=8
COLS=5
MS=2.2
SL=/Users/eruffaldi/Documents/tasks/mitaka/capture-2020-06-12/calib1/Left
SR=/Users/eruffaldi/Documents/tasks/mitaka/capture-2020-06-12/calib1/Right
python calib_charuco.py --rows $ROWS --cols $COLS --markersize $MS --squaresize $SS --output camleft.json $SL/* 
python calib_charuco.py --rows $ROWS --cols $COLS --markersize $MS --squaresize $SS --output camright.json $SR/* 
#python calib_stereo.py --calleft camleft.json --calright camright.json --imleft $SL --imright $SR --output stereo.json
#/Users/eruffaldi/Documents/tasks/mitaka/capture-2020-06-12/calib1/Right/*

# Right
# 6.15 -> 9.31091267013404
# 5.5 -> 6.34578640152167
#

# Left
# 6.15 -> 12.036
# 5.5 -> 7.53
# 4.8087 5.0
# 4.5 -> 2.77
# 4.2 -> 2.0
# 4.0 -> 1.69
#
# joint 
# 5.5 -> 6.961348325108881
# 4.5 -> 3.0822671983379264
# 4.0 -> 1.977305506527398