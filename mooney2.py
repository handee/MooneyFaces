#!/usr/bin/env python

import numpy as np
import cv2
import os 
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str

help_message = '''
USAGE: mooney2.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
No arguments will just run on any attached webcam data
Creates a directory called "out" and saves a time series of images in that, which will be overwritten each run
'''

def nothing(x):
    pass
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':

    import sys, getopt
    print help_message
# set up arguments for video capture and face detection
    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "haarcascade_frontalface_alt.xml")
    cascade = cv2.CascadeClassifier(cascade_fn)
#look for output directory and create if necessary
    directory="out"
    if not os.path.exists(directory):
	    os.makedirs(directory)
#open video capture 
    cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')

# build control window
    cv2.namedWindow("controls")
    cv2.createTrackbar('Red (line)','controls',0,255,nothing)
    cv2.createTrackbar('Green (line)','controls',0,255,nothing)
    cv2.createTrackbar('Blue (line)','controls',0,255,nothing)
    cv2.createTrackbar('Width of line','controls',1,10,nothing)
    cv2.createTrackbar('Foreground grey','controls',0,255,nothing)
    cv2.createTrackbar('Background grey','controls',0,255,nothing)
    cv2.setTrackbarPos('Red (line)','controls',150)
    cv2.setTrackbarPos('Green (line)','controls',150)
    cv2.setTrackbarPos('Blue (line)','controls',150)
    cv2.setTrackbarPos('Width of line','controls',3)
    cv2.setTrackbarPos('Foreground grey','controls',255)
    cv2.setTrackbarPos('Background grey','controls',0)
   

#some constants 
    n=0
    mean_face=(126,126,126)
    face_found=0
    while True:   
 # Interaction: get trackbar positions
        r = cv2.getTrackbarPos('Red (line)','controls')
	g = cv2.getTrackbarPos('Green (line)','controls')
	b = cv2.getTrackbarPos('Blue (line)','controls')
	linewidth = cv2.getTrackbarPos('Width of line','controls')
	greyfore = cv2.getTrackbarPos('Foreground grey','controls')
	greyback = cv2.getTrackbarPos('Background grey','controls')
        if (linewidth%2==0):
           linewidth=linewidth+1

# grab a new frame and preprocess
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

# if we've not found a face look for faces
# and get hold of the mean face greylevel for moonification
        if (face_found==0):
		rects = detect(gray, cascade)
		vis = img.copy()
		if (len(rects)>=1):
			for x1, y1, x2, y2 in rects:
			    x1=x1-20
			    y1=y1-20 
			    x2=x2+20 
			    y2=y2+20 
			roi = gray[y1:y2, x1:x2] 
			mean_face=cv2.mean(roi)
			face_found=1;	

#blur, threshold and make blocky (morphology) the input 
	blur = cv2.GaussianBlur(img,(5,5),0)
 	ret, thresh=cv2.threshold(gray,mean_face[0],255,cv2.THRESH_BINARY)
        kernel = np.ones((5,5),np.uint8)
	moony= cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)

# find the edges, then blur them to give a broader edge profile
        edges=cv2.Canny(moony,100,100,apertureSize=5)	
	blur = cv2.GaussianBlur(edges,(linewidth,linewidth),0)


#bit of conversion
	bgrm= cv2.cvtColor(moony, cv2.COLOR_GRAY2BGR)
        
#colour it all in         
        linecolour= (b,g,r)
        backgroundcolour=(greyback,greyback,greyback)
        foregroundcolour=(greyfore,greyfore,greyfore)
	bgrm[moony!=0 ] =foregroundcolour 
	bgrm[moony==0 ] = backgroundcolour 
	bgrm[blur!=0 ] =linecolour 
#output
        cv2.imshow('moonyout',bgrm)
        cv2.imshow('edges', edges)
#set up filename; if you want to preserve, just change the sub string "mooney" 
# and you'll get a different time series saved to out subdirectory
        fn="out/mooney"+str(n).rjust(4,'0')+".png" 
        cv2.imwrite(fn,bgrm);
        n=n+1
 


        n=n+1
        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()
