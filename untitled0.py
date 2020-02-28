#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:17:39 2020

@author: daniel
"""

import stadistics as s
from stadistics import *

centers = [[339,6], [233,85]]
val = regLineal(centers[0], centers[1], graph=True)
print(val)