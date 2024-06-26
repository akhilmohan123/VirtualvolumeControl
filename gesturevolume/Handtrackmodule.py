import mediapipe as mp
import time
import cv2 as cv
class HandDetector:
    def __init__(self,mode=True,maxhand=2,detectioncon=0.5,trackingcon=0.5):
        self.mode=mode
        self.maxhand=maxhand
        self.detectioncon=detectioncon
        self.trackingcon=trackingcon
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands()
        self.mpdraw=mp.solutions.drawing_utils#drawing

    def findHand(self,img,draw=True):    
         rgb=cv.cvtColor(img,cv.COLOR_BGR2RGB)
         self.results=self.hands.process(rgb)
         if self.results.multi_hand_landmarks:
            for self.handlm in self.results.multi_hand_landmarks:
             if draw:
                self.mpdraw.draw_landmarks(img,self.handlm,self.mpHands.HAND_CONNECTIONS)
         return img 
    def findPosition(self,img,handNo=0,draw=True):
               
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNo]
            for id,lms in enumerate(myhand.landmark):
                
                 h,w,c=img.shape
                 cx,cy=int(lms.x*w),int(lms.y*h)
                 lmlist.append([id,cx,cy])
                 if draw:
                    cv.circle(img, (cx, cy), 5, (255, 0, 255), cv.FILLED)
                  

        return lmlist
        

def main():
    ctime=0.0
    ptime=0.0
    cap=cv.VideoCapture(0)
    dector=HandDetector()
    while True:
          success,img=cap.read()
          img=dector.findHand(img)
          lmlist=dector.findPosition(img,draw=False)
          if len(lmlist) !=0:
              print(lmlist[4])
          ctime=time.time()
          fps=1/(ctime-ptime)
          ptime=ctime             
          cv.putText(img,str(int(fps)),(30,70),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
          cv.imshow('image',img)
          cv.waitKey(1)



if __name__=="__main__":
    main()