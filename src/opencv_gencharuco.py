
#import pandas as pd
#import numpy as np
import argparse
import os
import sys
import cv2
import cv2.aruco as aruco

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--output',"-o")
    parser.add_argument('--rows',"-r",type=int,default=11)
    parser.add_argument('--cols',"-c",type=int,default=8)
    parser.add_argument('--width',"-W",type=int,default=4000)
    parser.add_argument('--height',"-H",type=int,default=4000)
    parser.add_argument('--markersize',"-m",type=int,default=10)
    parser.add_argument('--squaresize',"-s",type=int,default=20)
    parser.add_argument('--dictionary',"-d",default="DICT_4X4_50")
    #parser.add_argument('output')
    parser.add_argument('-x',action="store_true")
    args = parser.parse_args()

    dic = getattr(cv2.aruco,args.dictionary)
    aruco_dict = cv2.aruco.getPredefinedDictionary(dic)
    board = aruco.CharucoBoard_create(args.cols,args.rows,args.squaresize,args.markersize, aruco_dict)
    mboard = board.draw((args.width, args.height))
    if args.output is None:
        cv2.imshow("image",mboard)
        cv2.waitKey(0) #any key
    else:
        cv2.imwrite(args.output,mboard)

if __name__ == '__main__':
    main()
