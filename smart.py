"""
Biblioteca que contiene herramientas útiles para el
control autónomo de un drone usando IA.

Created on Wed Jan 22 14:15:15 2020
Universidad Nacional Autónoma de México.
Instituto de Física.

@author: Juan Daniel Soto Montes.
"""
import stadistics as s
from stadistics import *
import cv2
import serial
import time
import os
from multiprocessing import Process

class smart(object):
    """
    Clase que se encarga de realizar las tareas inteligentes
    que debe realizar un drone autónomo.
    """

    def __init__(self, media, cascade):
        self.media = media
        self.cascade = cascade
    
    def recognize(self, plot=False):
        """
        Función que realiza el reconocimiento usando una inferencia de 
        una red neuronal y encuentra todas las coincidencias.
        """
        _, imagen = self.media.read()
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        caras = self.cascade.detectMultiScale(gray, 1.3, 5)
        self.dots = np.array(caras)
        self.gray = gray
        if plot==True:
            imagen, _ = smart.draw(self, imagen=imagen, dots=caras)
        return imagen, self.dots

    def move(self, imagen, centers):
        """
        Funcion que decide como debe moverse el drone.
        
        imagen --> se usa para conocer la forma del plano
        centers --> una lista de forma (2,1)
        """
        h, w = imagen.shape[0], imagen.shape[1] 
        x, y = centers[0][0], centers[1][0]
        if (x>=0)and(x<.45*w):
            mx = "derecha"
        elif (x>=.45*w)and(x<.55*w):
            mx = "nada"
        elif (x>=.55*w)and(x<=w):
            mx = "izquierda"
        if (y>=0)and(y<.45*h):
            my = "abajo"
        elif (y>=.45*h)and(y<.55*h):
            my = "nada"
        elif (y>=.55*h)and(y<=h):
            my = "arriba"
        return mx, my

    def draw(self, imagen, dots, id=False, punto=True, diagram=False, centred=False):
        """"
        Genera los recuadros de identidad, asi como el centro del objeto detectado

        dots --> (1,4)  [x,y,w,h]
        (x,y) -> Coordenadas del punto superior izquierdo
        w, h  -> Anchura y altura 
        """
        self.imagen = imagen
        if diagram == True:
            self.imagen = smart.diagrama(self)
        centers = [[],[]]
        for (x,y,w,h) in dots:
            if id==True:
                cv2.rectangle(imagen,(x,y),(x+w,y+h),(255,255,255),2)
            x = int(x+(w/2))
            y = int(y+(h/2))
            centers[0].append(x)
            centers[1].append(y)
            if len(imagen.shape) == 3: 
                if diagram == True:
                    cv2.rectangle(self.imagen,(x,y),(x+5,y+5),(0,0,0),-2)
                else: 
                    cv2.rectangle(self.imagen,(x,y),(x+2,y+2),(0,0,255),2)
            else:
                cv2.rectangle(self.imagen,(x,y),(x+2,y+2),(255,255,255),2)
        self.centers = np.array(centers)
        if punto==True and self.centers.shape[1]>=1:
            if centred == True:
                values = regLineal(self.centers[0],self.centers[1])
                x = int(values["Y media"])
                y = int(values["X media"])
                self.centers = np.array([[x],[y]])
            if len(imagen.shape) == 3: 
                if diagram == True:
                    cv2.rectangle(self.imagen,(x,y),(x+5,y+5),(0,0,0),-2)
                else: 
                    cv2.rectangle(self.imagen,(x,y),(x+2,y+2),(0,0,255),2)
            else:
                cv2.rectangle(self.imagen,(x,y),(x+2,y+2),(255,255,255),2)
        return self.imagen, self.centers

    def diagrama(self):
        """
        Función que genera una la imagen del diagrama
        de movimiento del drone
        """
        x = self.imagen.shape[0]
        y = self.imagen.shape[1]
        self.fondo = 240*np.ones((x, y, 3),dtype=np.uint8)
        cv2.rectangle(self.fondo, (int((55*y)/100),0), (int((45*y)/100),int((45*x)/100)), (255, 100, 0), -2)
        cv2.rectangle(self.fondo, (int((55*y)/100),int((55*x)/100)), (int((45*y)/100),y), (100, 255, 0), -2)
        cv2.rectangle(self.fondo, (int((45*y)/100),int((45*x)/100)), (0, int((55*x)/100)), (0, 100, 255), -2)
        cv2.rectangle(self.fondo, (int((55*y)/100),int((45*x)/100)), (y, int((55*x)/100)), (100, 0, 255), -2)
        for line in [15, 30, 70, 85]:
            cv2.rectangle(self.fondo, (int((line*y)/100)-1,0), (int((line*y)/100)+1,x), (100, 100, 100), 2)
            cv2.rectangle(self.fondo, (0,int((line*x)/100)-1), (y,int((line*x)/100)-1), (100, 100, 100), 2)
        return self.fondo

class telemetry(object):
    """
    Clase que contiene funciones útiles para una
    comunicación de telemetría.
    """
    def __init__(self, puerto, baud):
        self.puerto = "/dev/tty"+puerto
        self.baud = baud
        self.nano = serial.Serial(port = self.puerto,
                         baudrate = self.baud,
                         bytesize = serial.EIGHTBITS,
                         parity   = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE)
        time.sleep(1)

    def send(self, frase, show=False):
        """
        Función que envia un mensaje a través
        de un puerto serial.
        """ 
        frase = frase+"\r"
        if show ==True:
            print(frase.encode())
        self.nano.write(frase.encode())

    def comand(self, comand):
        """
        Función que genera movimientos compuestos
        deacuardo a un comando de entrada.
        """
        if comand == "nada":
            return
        elif comand == "arriba":
            self.ch = telemetry.reader(self)
            if self.ch[2] >= 168:
                telemetry.send(self,"ch3-"+str(168),show=show)
                self.ch[2] = 168
                telemetry.log(self, self.ch)
            elif self.ch[2] < 168:
                value = self.ch[2] + 1
                telemetry.send(self,"ch3-"+str(value),show=show)
                self.ch[2] = value
                telemetry.log(self,self.ch)
                time.sleep(.1)
        elif comand == "abajo":
            self.ch = telemetry.reader(self)
            if self.ch[2] <= 0:
                telemetry.send(self,"ch3-"+str(0),show=show)
                self.ch[2] = 0
                telemetry.log(self, self.ch)
            elif self.ch[2] > 0:
                value = self.ch[2] - 1
                telemetry.send(self,"ch3-"+str(value),show=show)
                self.ch[2] = value
                telemetry.log(self,self.ch)
                time.sleep(.1)
        elif comand == "derecha":
            self.ch = telemetry.reader(self)
            if self.ch[1] < 106:
                for value in range (self.ch[1], 106):
                    telemetry.send(self, "ch2-"+str(value), show=show)
                    self.ch[1] = value
                    telemetry.log(self, self.ch)
                    time.sleep(.05)
                time.sleep(.1)
                for value in list(range (86,self.ch[1]))[::-1]:
                    telemetry.send(self, "ch2-"+str(value), show=show)
                    self.ch[1] = value
                    telemetry.log(self, self.ch)
                    time.sleep(.05)
            else:
                for value in list(range (86,self.ch[1]))[::-1]:
                    telemetry.send(self, "ch2-"+str(value), show=show)
                    self.ch[1] = value
                    telemetry.log(self, self.ch)
                    time.sleep(.05)
        elif comand == "izquierda":
            self.ch = telemetry.reader(self)
            if self.ch[1] > 66:
                for value in list(range (self.ch[1], 66))[::-1]:
                    telemetry.send(self, "ch2-"+str(value), show=show)
                    self.ch[1] = value
                    telemetry.log(self, self.ch)
                    time.sleep(.05)
                time.sleep(.1)
                for value in range (self.ch[1],86):
                    telemetry.send(self, "ch2-"+str(value), show=show)
                    self.ch[1] = value
                    telemetry.log(self, self.ch)
                    time.sleep(.05)
            else:
                for value in range (self.ch[1],86):
                    telemetry.send(self, "ch2-"+str(value), show=show)
                    self.ch[1] = value
                    telemetry.log(self, self.ch)
                    time.sleep(.05)
        return

    def close(self):
        """
        Función que se desconecta de el drone
        automáticamente.
        """
        telemetry.send(self,"disconnect")
        self.nano.close()
    
    def log(self,ch):
        """
        Función que guarda en un archivo log
        el estado actual de cada canal.
        """
        self.ch=ch
        with open("/home/daniel/Documents/Otros/Drone/JetsonNano/Programas/Control/flying/topic/log.txt", "a") as file:    
            file.write("\n"
            +str(self.ch[0])+","
            +str(self.ch[1])+","
            +str(self.ch[2])+","
            +str(self.ch[3]) 
            )

    def reader(self):
        """
        Función que verifica el archivo log
        o en su defecto crea las lista con los
        valores iniciales de los canales.
        """
        try:
            with open("/home/daniel/Documents/Otros/Drone/JetsonNano/Programas/Control/flying/topic/log.txt", "r") as file:
                chains = file.readlines()[-1].split(",")
                self.ch = [int(x) for x in chains]
        except Exception:
            self.ch = []
            for _ in range(4):
                self.ch.append(84) 
            self.ch[2] = 0
        return np.array(self.ch)

    def elevar(self, altura=80, vel=.1):
        """
        Función que eleva el drone hasta una altura indicada
        en porcentaje.
        """
        telemetry.send(self, "connect", show=True)
        time.sleep(1)
        telemetry.reader(self)
        if self.ch[2] <= int((altura*168)/100):
            for ch3 in range(self.ch[2], int((altura*168)/100)):
                telemetry.send(self,"ch3-"+str(ch3),show=show)
                self.ch[2] = ch3
                telemetry.log(self,self.ch)
                time.sleep(vel)
        else:
            for ch3 in list(range(int((altura*168)/100), self.ch[2]))[::-1]:
                telemetry.send(self,"ch3-"+str(ch3))
                self.ch[2] = ch3
                telemetry.log(self,self.ch)
                time.sleep(vel)

