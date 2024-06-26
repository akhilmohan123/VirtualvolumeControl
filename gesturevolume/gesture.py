import mediapipe as mp
import cv2 as cv
import numpy as np
import time
import math
import Handtrackmodule as ht
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

iw,ih=640,480
cap=cv.VideoCapture(0)
cap.set(3,iw)
cap.set(4,ih)
detector=ht.HandDetector(trackingcon=0.7)
ptime=0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()
volbar=0
volper=0
maxvol=volrange[0]
minvol=volrange[1]
print(volrange)
while True:
    success,img=cap.read()
    img=detector.findHand(img)
    lmlist=detector.findPosition(img,draw=False)
   
    if len(lmlist) !=0:
       x1,y1=lmlist[4][1],lmlist[4][2]
       x2,y2=lmlist[8][1],lmlist[8][2]
       cx,cy=(x1+x2)//2,(y1+y2)//2
       cv.circle(img,(x1,y1),15,(255,0,255),cv.FILLED)
       cv.circle(img,(x2,y2),15,(255,0,255),cv.FILLED)
       cv.line(img,(x1,y1),(x2,y2),(255,0,0),3)
       cv.circle(img,(cx,cy),15,(255,255,0),cv.FILLED)
       length=math.hypot(x2-x1,y2-y1)
       print(length)
       if length<50:
           cv.circle(img,(cx,cy),15,(0,0,255),cv.FILLED)
       vol=np.interp(length,[50,300],[minvol,maxvol])
       volbar=np.interp(length,[50,300],[400,150])
       volper=np.interp(length,[50,300],[0,100])
       print(vol)
       volume.SetMasterVolumeLevel(vol, None)
       cv.rectangle(img,(50,150),(85,400),(0,255,0),3)
       cv.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv.FILLED)
       cv.putText(img, f'{int(volper)} %', (40, 450), cv.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv.putText(img,f'Fps:{str(int(fps))}',(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv.imshow('image',img)
    cv.waitKey(1)

    