import sys
sys.path.append("C:\\Users\\minir\\AppData\\Roaming\\liba")

import cv2
import numpy as np

import barpy as bc
print(dir(bc))

import os
c = 1
filepath = 'C:/Users/minir/Downloads/archive/cars_train/cars_train'
for imagename in os.listdir(filepath):
    image = cv2.imread(filepath + "/" + imagename, 0)
    image = cv2.resize(image, (20,20))
    cv2.imwrite(f'../Images/Cars/{c}.png', image)
    c += 1