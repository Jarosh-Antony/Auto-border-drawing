import cv2 as cv
import sys
import numpy as np
from rembg import remove
import argparse


def correct(img,cb,v):
    T=0
    D=img.shape[0]
    L=0
    R=img.shape[1]
    t=cb[1] 
    d=cb[3]
    l=cb[0]
    r=cb[2]
    if t>d:
        t,d=d,t 
    if l>r:
        l,r=r,l
    l-=v
    t-=v
    d+=v 
    r+=v 
    if t<0:
        t=0
    if d>D:
        d=D
    if l<0:
        l=0
    if r>R:
        r=R
    return [l,t,r,d]
    
 
 
def makeBorder(img,cb):
    
    #img boundaries
    T=0
    D=img.shape[0]
    L=0
    R=img.shape[1]
    
    cb=correct(img,cb,0)
    #crop boundaries
    t=cb[1] #top
    d=cb[3] #bottom
    l=cb[0] #left
    r=cb[2] #right
    
        
    cropped=img[t:d,l:r]
    nbg=remove(cropped)
    
    red=np.array([0,0,255]) #red pixel
    bg=np.zeros(4)
    #bg=np.ones(4)
    bg+=100 #tolerating value of background pixel till 100(nearly black)
    #rather than 0(exact black) to smoothen the drawn border
    
    #horizontal processing
    for h in range(t,d):
        B=C=0  #B --> black pixel and C --> coloured pixel
        
        for w in range(l,r):
        
            if np.ndarray.all(np.less(nbg[h-t][w-l],bg)):  #checks if a pixel is nearly black
                B+=1
                if C>9:
                    C=0
                    for i in range(10):
                        if w+i<R:
                            img[h][w+i]=red
                
            else :
                C+=1
                if B>9:
                    B=0
                    for i in range(10):
                        if w-i>=L:
                            img[h][w-i]=red
                
    
    #vertical processing
    for w in range(l,r):
    
        B=C=0
        for h in range(t,d):
        
            if np.ndarray.all(np.less(nbg[h-t][w-l],bg)):
                B+=1
                if C>9:
                    C=0
                    for i in range(10):
                        if h+i<D:
                            img[h+i][w]=red
                        
            else :
                C+=1
                if B>9:
                    B=0
                    for i in range(10):
                        if h-i>=T:
                            img[h-i][w]=red
                        
    return img.copy()
    
# instead of using the default technique of replacing the entire region,
# we only replace the drawn portion of the image which is faster and visually smooth than the selectROI provided by cv2
def redo(oldcb,image,drawn):
    oldcb=correct(image,oldcb,6)
    image[oldcb[1]:oldcb[3],oldcb[0]:oldcb[2]]=drawn[oldcb[1]:oldcb[3],oldcb[0]:oldcb[2]]
    

# my version of simplified selectROI to implement q-->quit, c-->clear functionality smoothly
# mainly to override behaviour of clicking c in cv.selectROI
def selectROI(event,x,y,flags,param):
    global ix,iy,drawing,image,cb,oldcb
    blue=np.array([255,0,0])
    if event == cv.EVENT_LBUTTONDOWN:
        if len(oldcb)==4:
            redo(oldcb,image,drawn)    
        drawing = True
        ix,iy = x,y
        cb=[x,y]
        oldcb=[x,y]
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if len(oldcb)==4:
                redo(oldcb,image,drawn)
            cv.rectangle(image,(ix,iy),(x,y),(255,0,0),5)
            oldcb=[ix,iy,x,y]
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if len(oldcb)==4:
            redo(oldcb,image,drawn)
        cv.rectangle(image,(ix,iy),(x,y),(255,0,0),5)
        oldcb=[ix,iy,x,y]
        if((x,y)==(ix,iy)):
            cb=[]
            oldcb=[]
        else:
            cb.append(x)
            cb.append(y)
 


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help ="Path to the image")
args = vars(ap.parse_args())

cb=[] #crop_boundaries
oldcb=[]
drawing = False
ix,iy = -1,-1
f=args['image'].split('.')
filename=f[0]
extension=f[1]
output=filename+'_output.'+extension

try:
    image=cv.imread(args['image'])
except:
    sys.exit('Failed to load image')
    
print('Use mouse to select a region by "click and drag"')
print('Press "ENTER" button to validate the region drawn by mouse')
print('Press "c" button to delete all borders and load original image')
print('Press "s" button to save the image with border')
print('Press "q" button to close or quit the script')

drawn=image.copy()
original=image.copy()
cv.namedWindow('image',cv.WINDOW_NORMAL)
cv.setMouseCallback('image',selectROI)
while(True):
    cv.imshow("image", image)
    k=cv.waitKey(1)
    if k==ord('q') or k==ord('Q'):
        break
    elif k==13 and len(cb)==4:
        image=drawn.copy()
        drawn=makeBorder(image,cb)
        
    elif k==ord('c') or k==ord('C'):
        image=original.copy()
        drawn=original.copy()
        
    elif k==ord('s') or k==ord('S'):
        cv.imwrite(output,drawn)


cv.destroyAllWindows()

