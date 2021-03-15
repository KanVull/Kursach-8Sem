import sys
sys.path.append("C:\\Users\\minir\\AppData\\Roaming\\liba")

import os
import cv2
import numpy as np

import barpy as bc

c = 1
filepathCars = '../Images/Cars'
filepathPlanes = '../Images/Planes'
filepath = filepathCars
struct = []

# Для построения баркода необходиом использовать структуру Barstruct, которая инициализируется настройками
# ProcType -- как строить барокд: с 0-й яркости по 255-ю или с 255-й по 0-ю
# ColorType -- формат входного изображеия: серый, ргб (создаться 3 баркода) или адаптивный (как в изображении) 
# ComponentType -- Срутктура баркода: компонента или дыра

struct.append(bc.Barstruct(bc.ProcType.f0t255, bc.ColorType.gray,bc.ComponentType.Component))
barcodeFactory = bc.BarcodeCreator()

# -- Настройки --

# Сохранять ли банарные матрицы. Они отражают компоненты/дыры на каждой яркости
barcodeFactory.setCreateBinaryMasks(True)
# показывать процесс построения на каждом шаге
barcodeFactory.setVisualize(False)
# 0 - вернуть баркод, длины которого посчитаны по числам бетти; 1 - вернуть баркод, длины которого посчитны по времени жизни копонент
barcodeFactory.setReturnType(1)


for imagename in os.listdir(filepath):
    image = cv2.imread(filepath + "/" + imagename, 0)
    
    container = barcodeFactory.createBarcode(image, struct)
    # Получить первый объекты
    item = container.get(0)
    bar = item.getBar()

    bar.sort(key=lambda x : x.len, reverse=True)

    # Если получить 2 контейнера, то их можно будет сравнить

    binmap = np.zeros_like(image)
    keyvals = bar[0].getPoints().items()
    for p in keyvals:
        binmap[p[0].y, p[0].x] += p[1]  


    # image =  cv2.resize(image,  (400, 400))
    # binmap = cv2.resize(binmap, (400, 400))
    # showImage = np.concatenate((image, binmap), axis=1)
    # cv2.imshow('img', showImage)
    # cv2.waitKey(0)
    cv2.imwrite(f'../Images/BarCars/{c}.png', binmap)
    c += 1