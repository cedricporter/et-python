#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#

import random
import numpy as np


LOOP = 10
N = 50000000
width = 1
pi_list = []

for i in xrange(LOOP):
    x_list = np.random.uniform(-width, width, N)
    y_list = np.random.uniform(-width, width, N)

    distance_list = (x_list ** 2 + y_list ** 2) ** 0.5

    inner = distance_list[distance_list < width]
    area = width ** 2 * float(len(inner)) / len(distance_list)

    r = width / 2.0
    pi = area / r ** 2
    print(i, pi)
    pi_list.append(pi)

pi_list = np.array(pi_list)
pi = pi_list.mean()
print(pi)
