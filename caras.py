import smart as u
from smart import *

cam = u.smart(cv2.VideoCapture(0), cv2.CascadeClassifier('cascade/haarcascade_frontalface_alt.xml'))
while(True):
    img, faces = cam.reconize(plot=True)
    black, centers = cam.draw(img,faces, diagram=True,centred=True)
    if centers.shape == (2,1):
        mx, my = cam.move(img,centers)
        print(mx+ "\n"+my)
    cv2.imshow("Direction",black)
    #cv2.imshow('Camara',img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.VideoCapture(0).release()
cv2.destroyAllWindows()	