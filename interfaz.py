from tkinter import *
import os
from multiprocessing import Process

ventana=Tk()
ventana.title("Control de Operaciones")
ventana.geometry("450x400")
ventana.configure(background="Skyblue")
color_boton=("gray77")

def main():
    Process(target=os.system("python main.py")).start()
    return 
def mainClose():
    Process(target=os.system("python main.py")).kill()
    return
def status():
    Process(target=os.system("python status.py")).start()
    return 
def statusClose():
    Process(target=os.system("python status.py")).kill
    return

l = Label(ventana, font=('arial',22,'bold'),text="Acciones con el 'drone'", bg="Skyblue").place(x=20,y=20)
Boton0=Button(ventana,font=('arial',18,'bold'),text="Lanzamiento",height=3, width=20 , bg=color_boton,command=lambda:main()).place(x=20,y=100)
Boton1=Button(ventana,font=('arial',18,'bold'),text="Stop",height=3, bg=color_boton,command=lambda:mainClose()).place(x=350,y=100)
Boton2=Button(ventana,font=('arial',18,'bold'),text="Movimiento del Drone",height=3,bg=color_boton,command=lambda:status()).place(x=20,y=250)
Boton3=Button(ventana,font=('arial',18,'bold'),text="Stop",height=3,bg=color_boton,command=lambda:statusClose()).place(x=350,y=250)

ventana.mainloop()
