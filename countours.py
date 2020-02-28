import cv2

def bordes(imagen,smoth=11):
    bn = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(bn,(smoth,smoth), 0)
    canny = cv2.Canny(gauss, 50, 150)
    (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imagen,contornos,-1,(255,255,255), 2)
    return canny

cap = cv2.VideoCapture("/home/daniel/Videos/theBigBang/1x5.mp4")
while(True):
    ret, img = cap.read()
    if ret== True:
        cv2.imshow("Original",img)
        cv2.imshow("Bordes",bordes(img,1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
