import smart as u
from smart import *

cam = u.smart(cv2.VideoCapture(2), cv2.CascadeClassifier('cascade/haarcascade_frontalface_alt.xml'))
mega = u.telemetry("ACM0",115200)
send = mega.comand
open("/home/daniel/Documents/Otros/Drone/JetsonNano/Programas/Control/flying/closeMain.sh","w").write("kill "+str(os.getpid()))
open("/home/daniel/Documents/Otros/Drone/JetsonNano/Programas/Control/flying/closeMain.sh","w").close()
#time.sleep(2)
mega.elevar(40,vel=.1)
#time.sleep(3)
#mega.send("ch3-0")
#os.system("rm topic/log.txt")
while(True):
    img, faces = cam.recognize(plot=True)
    black, centers = cam.draw(img,faces, diagram=True,centred=True)
    if centers.shape == (2,1):
        try:
            p1.kill()
            p2.kill()
        except Exception:
            None
        mx, my = cam.move(img,centers)
        p1 = Process(target=send(mx))
        p2 = Process(target=send(my))
        p1.start()
        p2.start()
    #cv2.imshow("Direction",black)
    cv2.imshow('Camara',img)
    key = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(1) & 0xFF == ord('q'):
        os.system("kill "+str(os.getppid()))
        break

cv2.VideoCapture(0).release()
cv2.destroyAllWindows()	
