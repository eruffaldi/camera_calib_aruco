#import pandas as pd
#import numpy as np
#import pandas as pd
#import numpy as np
import argparse
import os
import sys
import json
import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import argparse
import os
import sys


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def compute_stereo_rectification_maps(c1mtx,c1dist,c2mtx,c2dist, im_size, size_factor):
    new_size = (int(im_size[1] * size_factor), int(im_size[0] * size_factor))
    rotation1, rotation2, pose1, pose2 = \
        cv2.stereoRectify(cameraMatrix1=c1mtx,
                          distCoeffs1=c1dist,
                          cameraMatrix2=c2mtx,
                          distCoeffs2=c2dist,
                          imageSize=(im_size[1], im_size[0]),
                          R=R,
                          T=T,
                          flags=cv2.CALIB_ZERO_DISPARITY,
                          newImageSize=new_size
                          )[0:4]
    map1x, map1y = cv2.initUndistortRectifyMap(c1mtx,
                                               c1dist,
                                               rotation1, pose1, new_size, cv2.CV_32FC1)
    map2x, map2y = cv2.initUndistortRectifyMap(c2mtx,
                                               c2dist,
                                               rotation2, pose2, new_size, cv2.CV_32FC1)
    return map1x, map1y, map2x, map2y 

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    #parser.add_argument('--imleft')
    #parser.add_argument('--imright')
    parser.add_argument('--stereo')
    parser.add_argument('--images')
    parser.add_argument('--output-dir')

    # load calib
    # undistort
    # rectify
    c = json.load(open(args.stereo,"r"))
    #r = dict(result=retval,cam1=dict(result=retval,mtx=cameraMatrix1,dist=distCoeffs1),cam2=dict(result=retval,mtx=cameraMatrix2,dist=distCoeffs2),stereo=dict(R=R,T=T,E=E,F=F))
    for q in (c["cam1"],c["cam2"]):
        q["mtx"] = np.array(q["mtx"],dtype=np.float64)
        q["dist"] = np.array(q["dist"],dtype=np.float64)

    det = json.load(open(args.images,"r"))
    #images=images,ids=ids,img_points1=img_points1,img_points2=img_points2,obj_points=obj_points
    for i in range(0,len(images)):

