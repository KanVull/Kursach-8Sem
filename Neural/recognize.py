import random
import pathlib
import numpy as np
from PIL import Image
from tensorflow import keras

def recognize(image, model):
    '''
    image - PIL.Image object. Size must be (20, 20). GrayScale
    model - tensorflow.keras.model object
    
    returns number of recognized class
    '''
    image = image.reshape(1, 400) / 255
    prediction = model.predict(image)
    return np.argmax(prediction[0])

def uploadImage(path: pathlib.Path):
    '''
    path - pathlib.Path object. Absolute path of image
    
    returns image as PIL.Image object
    '''
    image = Image.open(path)
    data = np.asarray(image)
    return data    

models_names = [
    'BarPy_model.h5',
    'RAW_model.h5',
]

classes = [ 'Car', 'Plane' ]

model_Bar = keras.models.load_model( models_names[0] )
model_RAW = keras.models.load_model( models_names[1] )

Names = [
    'BarCar',
    'BarPlane',
    'RAWCar',
    'RAWPlane',
]

paths = {
    'pathCars': '../Images/Cars/',
    'pathPlanes': '../Images/Planes/',
    'pathBarCars': '../Images/BarCars/',
    'pathBarPlanes': '../Images/BarPlanes/',
}

# Getting all paths of all images
# [ [paths to Bar Cars], [paths to Bar Planes], [paths to Cars], [paths to Planes] ]
list_paths = [
    [x for x in pathlib.Path(paths['pathBarCars']).iterdir()],
    [x for x in pathlib.Path(paths['pathBarPlanes']).iterdir()],
    [x for x in pathlib.Path(paths['pathCars']).iterdir()],
    [x for x in pathlib.Path(paths['pathPlanes']).iterdir()]
]

# count of images of every classes
numberOfImages = 50

# Loading lists of images
# [ 
#   [PIL.Image, .., PIL.Image], 
#   [PIL.Image, .., PIL.Image], 
#   [PIL.Image, .., PIL.Image], 
#   [PIL.Image, .., PIL.Image] 
# ]
RandomImages = [ [uploadImage(pathOfImage) for pathOfImage in random.sample(path, numberOfImages)] for path in list_paths ] 

# Getting predictions by model for every image + expected answer as Names element
# [ 
#   [ (recognized, expected), .. , (recognized, expected) ],
#   [ (recognized, expected), .. , (recognized, expected) ],
#   [ (recognized, expected), .. , (recognized, expected) ],
#   [ (recognized, expected), .. , (recognized, expected) ], 
# ]
predictions_list = [
    [ (classes[recognize( image, model_Bar )], classes[0]) for image in RandomImages[0] ],
    [ (classes[recognize( image, model_Bar )], classes[1]) for image in RandomImages[1] ],
    [ (classes[recognize( image, model_RAW )], classes[0]) for image in RandomImages[2] ],
    [ (classes[recognize( image, model_RAW )], classes[1]) for image in RandomImages[3] ],
]

for i in range(4):
    err = 0
    for p in predictions_list[i]:
        print(f'{Names[i]} regognized as {p[0]}')
        if p[0] != p[1]:
            err += 1
    print(f'\tError: { (err / numberOfImages) * 100 }%')        
