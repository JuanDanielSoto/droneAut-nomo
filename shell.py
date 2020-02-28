#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 14:15:15 2020

@author: daniel
"""

import threading
import os
import time

paralelo = threading.Thread
t1 = lambda : os.system("python /home/daniel/Documents/Otros/Drone/JetsonNano/Programas/Control/flying/move.py")
t2 = lambda : os.system("python /home/daniel/Documents/Otros/Drone/JetsonNano/Programas/Control/flying/caras.py")
task1 = paralelo(target=t1)
task2 = paralelo(target=t2)
task1.start()
time.sleep(2)
task2.start()