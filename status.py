from smart import *
import os 

print("Analizando caja negra...")
open("closeStats.sh","w").write("kill "+str(os.getpid()))
open("closeStats.sh","w").close()
try:
    with open("/home/daniel/Documents/Otros/Drone/JetsonNano/Programas/Control/flying/topic/log.txt", "r") as file:
        lines = file.readlines()
        print(lines.pop(0))
        ch = [[],[],[],[]]
        for line in lines:
            i = line.split(",")
            for ix, value in enumerate(i):
                ch[ix].append(int(value))
    for c in ch:
        plt.plot(c)
    plt.legend(("Canal 1", "Canal 2", "Canal 3", "Canal 4"))
    plt.show()
except Exception:
    print("No existe el archivo de la caja negra.")