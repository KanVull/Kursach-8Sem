# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import sys
import numpy as np
import cv2

# Путь к модулю (непосредсвенно к папке), т.е. сама библиотека расположена по пути
#                D:\\Programs\\C++\\Barcode\\x64\\Python\barpy.pyd
sys.path.append("C:\\Users\\minir\\AppData\\Roaming\\liba")
# sys.path.append('D:\\Programs\\Python\\BARPY')

# сам модуль
import barpy as bc

# Вывести все объекты (классы) из библиотеки
print(dir(bc))

struct = []

# Для построения баркода необходиом использовать структуру Barstruct, которая инициализируется настройками
# ProcType -- как строить барокд: с 0-й яркости по 255-ю или с 255-й по 0-ю
# ColorType -- формат входного изображеия: серый, ргб (создаться 3 баркода) или адаптивный (как в изображении) 
# ComponentType -- Срутктура баркода: компонента или дыра

struct.append(bc.Barstruct(bc.ProcType.f0t255, bc.ColorType.gray,bc.ComponentType.Component))

# В список можно доавить сразу несколько конфигураций, тогда вернётся не один, а 2 баркода. 
# struct.append(bc.Barstruct(bc.ProcType.f0t255,bc.ColorType.gray,bc.ComponentType.Hole))

# Фабрика для пострроения баркодов
barcodeFactory = bc.BarcodeCreator()

# -- Настройки --

# Сохранять ли банарные матрицы. Они отражают компоненты/дыры на каждой яркости
barcodeFactory.setCreateBinaryMasks(True)
# показывать процесс построения на каждом шаге
barcodeFactory.setVisualize(False)
# 0 - вернуть баркод, длины которого посчитаны по числам бетти; 1 - вернуть баркод, длины которого посчитны по времени жизни копонент
barcodeFactory.setReturnType(1)

# Закгрузка изображения
img = cv2.imread(imgpath, 0)
cv2.imshow("source", img)
cv2.waitKey(1)
# Запуск построения баркода с помощью функции createBarcode. Передаётся изображение и структура построения
# Вернётся объект класса BarcodeContainer. Он хранит в себе объекты типа BarItem, именно в них хранятся выходные бакркоды. 
containet = barcodeFactory.createBarcode(img, struct)

# Получить первый объекты
item = containet.get(0)

# Функции баркода
print(dir(item))

# Получить линии баркода (класс BLine). У них есть 2 поля: start и len
bar = item.getBar()

bar.sort(key=lambda x : x.len, reverse=True)

# Если получить 2 контейнера, то их можно будет сравнить

binmap = np.zeros(img.shape, np.uint8)
keyvals = bar[0].getPoints().items()
for p in keyvals:
    binmap[p[0].y,p[0].x] += p[1]

# for bl in bar:
#     # Получаем значения из словаря. Они будут хранитсья в виде
#     # {(key, value),(key, value),(key, value)...}
#     # key - это позиция, т.е. point, у которого есть 'x' и 'y', value - это значения яркости
#     keyvals = bl.getPoints().items()
#     for p in keyvals:
#         binmap[p[0].y,p[0].x] += p[1]

# Особенность востановления: результирующее изображение необходимо вычесть из 255
binmap = img.max() - binmap
cv2.imshow("Restored image",binmap)
cv2.waitKey(0)
