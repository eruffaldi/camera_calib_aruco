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
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    #parser.add_argument('--imleft')
    #parser.add_argument('--imright')
    parser.add_argument('--calleft')
    parser.add_argument('--calright')
    parser.add_argument('--output')
    parser.add_argument('--fixint',action="store_true")
    args = parser.parse_args()

    term_crit = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 1000, 1e-8)
    c1 = json.load(open(args.calleft,"r"))
    c2 = json.load(open(args.calright,"r"))

    for c in (c1,c2):
        c["mtx"] = np.array(c["mtx"],dtype=np.float64)
        c["dist"] = np.array(c["dist"],dtype=np.float64)

    s1 = dict([(os.path.split(x)[1],i) for i,x in enumerate(c1["markers"]["images"])])
    s2 = dict([(os.path.split(x)[1],i) for i,x in enumerate(c2["markers"]["images"])])
    s11 = set(s1.keys()) & set(s2.keys())
    imsize = tuple(c1["imsize"]) #np.array(c1["imsize"],dtype=np.float64)
    # go through each pair
    flags = 0
    if args.fixint:
      print ("fix intrinsics")
      flags |= cv2.CALIB_FIX_INTRINSIC
      flags |= cv2.CALIB_USE_INTRINSIC_GUESS
    elif c1["mtx"] is not None and c2["mtx"] is not None:
      flags |= cv2.CALIB_USE_INTRINSIC_GUESS

    img_points1 = []
    img_points2 = []
    obj_points = []
    images = []
    ids=[]
    print("common files",len(s11))
    for c in s11:
        s1c = s1[c]
        s2c = s2[c]
        op = c1["markers"]["objpts"][s1c]
        im1 = c1["markers"]["imgpts"][s1c]
        im2 = c2["markers"]["imgpts"][s2c]
        ids1 = [x[0] for x in c1["markers"]["ids"][s1c]]
        ids2 = [x[0] for x in c2["markers"]["ids"][s2c]]
        print(ids1)
        cc = set(ids1) & set(ids2)
        if len(cc) == 0:
            print("nomarkerincommon",c)
            continue
        print(c,len(cc))
        s1i = dict([(x,i) for i,x in enumerate(ids1)]) #identifier to index
        s2i = dict([(x,i) for i,x in enumerate(ids2)]) #identifier to index
        s1ic = [s1i[x] for x in cc] # index
        s2ic = [s2i[x] for x in cc] # index

        images.append((c1["markers"]["images"][s1c],c2["markers"]["images"][s2c]))
        ids.append(cc)
        img_points1.append(np.squeeze(np.array([im1[i] for i in s1ic],dtype=np.float32)))
        img_points2.append(np.squeeze(np.array([im2[i] for i in s2ic],dtype=np.float32)))
        obj_points.append(np.squeeze(np.array([op[i] for i in s1ic],dtype=np.float32)))




    #flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
    #flags |= cv2.CALIB_FIX_FOCAL_LENGTH
    #flags |= cv2.CALIB_FIX_ASPECT_RATIO
    #flags |= cv2.CALIB_ZERO_TANGENT_DIST
    #flags |= cv2.CALIB_SAME_FOCAL_LENGTH
    #flags |= cv2.CALIB_RATIONAL_MODEL
    #V3 imsize after

    #    stereoCalibrate(objectPoints, imagePoints1, imagePoints2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize[, R[, T[, E[, F[, flags[, criteria]]]]]]) -> retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F
    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F  = cv2.stereoCalibrate(obj_points,img_points1,img_points2,c1["mtx"],c1["dist"],c2["mtx"],c2["dist"],imsize,R=None,T=None,F=None,E=None,criteria=term_crit,flags=flags)

    print ("error is:",retval)
    print ("orig cameraMatrix1\n",c1["mtx"])
    print ("cameraMatrix1\n",cameraMatrix1)
    print ("orig cameraMatrix2\n",c2["mtx"])
    print ("cameraMatrix2\n",cameraMatrix2)
    print ("orig distCoeffs1",c1["dist"])
    print ("distCoeffs1",distCoeffs1.transpose())
    print ("orig distCoeffs1",c2["dist"])
    print ("distCoeffs1",distCoeffs2.transpose())
    print ("T\n",T)
    print ("R\n",R)

    r = dict(result=retval,cam1=dict(result=retval,mtx=cameraMatrix1,dist=distCoeffs1),cam2=dict(result=retval,mtx=cameraMatrix2,dist=distCoeffs2),stereo=dict(R=R,T=T,E=E,F=F))
    json.dump(r,open(args.output,"w"),indent=4,sort_keys=True,cls=NumpyEncoder)
    rd = dict(images=images,ids=ids,img_points1=img_points1,img_points2=img_points2,obj_points=obj_points)
    json.dump(rd,open(args.output+".images.json","w"),indent=4,sort_keys=True,cls=NumpyEncoder)

    


if __name__ == '__main__':
    main()  