import smart as u
from smart import *

mega = u.telemetry("ACM0",115200)
send = mega.send
time.sleep(1)
send("connect")
#Elevación
for value in range(80):             #0 --> 0%   168 -->100%
    for ch in range(3,4):
        send("ch"+str(ch)+"-"+str(value),show=True)
    time.sleep(.1)
time.sleep(5)

#Descenso
for value in list(range(80))[::-1]:
    for ch in range(3,4):
        send("ch"+str(ch)+"-"+str(value),show=True)
    time.sleep(.1)
send("disconnect",show=True)
mega.close()