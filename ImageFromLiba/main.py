import sys
sys.path.append("C:\\Users\\minir\\AppData\\Roaming\\liba")

import cv2
import numpy as np

import barpy as bc
print(dir(bc))

import os
c = 1
for imagename in os.listdir('../Images/planesnet'):
    if imagename[0] == '1':
        image = cv2.imread('../Images/planesnet/' + imagename, 0)
        cv2.imwrite(f'../Images/Planes/{c}.png', image)


        c += 1