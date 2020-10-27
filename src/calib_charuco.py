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

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def calibrate_camera(allCorners,allIds,imsize,board):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION",imsize)

    cameraMatrixInit = np.array([[ 4000.,    0., imsize[0]/2.],
                                 [    0., 4000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    print("CAMERA CALIBRATION",imsize)
    
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS)# + cv2.CALIB_RATIONAL_MODEL)
    (ret, camera_matrix, distortion_coefficients0,
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

def read_chessboards(images,aruco_dict,board):
    """
    Charuco base pose estimation.
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    allImages =[]
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)
        if frame is None:
            print("cannot read ",im)
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner,
                                 winSize = (20,20),
                                 zeroZone = (-1,-1),
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])
                allImages.append(im)

        decimator+=1

    imsize = gray.shape
    return allCorners,allIds,imsize,allImages

def main():
    global dictionary
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('inputs',nargs="+")
    parser.add_argument('--output')
    parser.add_argument('--rows',"-r",type=int,default=11)
    parser.add_argument('--cols',"-c",type=int,default=8)
    parser.add_argument('--markersize',"-m",type=float,default=10)
    parser.add_argument('--squaresize',"-s",type=float,default=20)
    parser.add_argument('--dictionary',"-d",default="DICT_5X5_250")
    args = parser.parse_args()

    dic = getattr(cv2.aruco,args.dictionary)
    aruco_dict = cv2.aruco.getPredefinedDictionary(dic)
    board = aruco.CharucoBoard_create(args.cols,args.rows,args.squaresize,args.markersize, aruco_dict)


    images = args.inputs
    allCorners,allIds,imsize,allImages = read_chessboards(images,aruco_dict,board)
    print(allCorners)
    print(allIds)
    print(imsize)
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize,board)
    print("result",ret,mtx,dist,rvecs,tvecs)
    if args.output:
        objPoints = []
        imgPoints=[]
        for i in range(0,len(allIds)):
            op,ip = aruco.getBoardObjectAndImagePoints(board,allCorners[i],allIds[i])
            objPoints.append(op)
            imgPoints.append(ip)
        print("mtx cam",mtx.shape,mtx.dtype)
        o = dict(result=ret,mtx=mtx,dist=dist,markers=dict(vecs=rvecs,tvecs=tvecs,objpts=objPoints,imgpts=imgPoints,corners=allCorners,ids=allIds,images=allImages),imsize=imsize)
        json.dump(o,open(args.output,"w"),indent=4,sort_keys=True,cls=NumpyEncoder)
    i=3 # select image id
    plt.figure()
    frame = cv2.imread(images[min(i,len(images)-1)])
    img_undist = cv2.undistort(frame,mtx,dist,None)
    plt.subplot(1,2,1)
    plt.imshow(frame)
    plt.title("Raw image")
    plt.axis("off")
    plt.subplot(1,2,2)
    plt.imshow(img_undist)
    plt.title("Corrected image")
    plt.axis("off")
    plt.show()
    print("result",ret)
    if False:
        for f in args.inputs:

            img = cv2.imread(f,cv2.IMREAD_GRAYSCALE)
            [markerCorners,markerIds,rejectedImgPoints] = cv2.aruco.detectMarkers(img,dictionary)

            if len(markerCorners)>0:
                [ret,charucoCorners,charucoIds] = cv2.aruco.interpolateCornersCharuco(markerCorners,markerIds,img,board)
                if charucoCorners is not None and charucoIds is not None and len(charucoCorners)>3 and decimator%3==0:
                    allCorners.append(charucoCorners)
                    allIds.append(charucoIds)

                cv2.aruco.drawDetectedMarkers(img,markerCorners,markerIds)
                cv2.aruco.drawDetectedCornersCharuco(img,charucoCorners,charucoIds)


if __name__ == '__main__':
    main()
