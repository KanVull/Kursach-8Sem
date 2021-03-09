import random
import pathlib
import numpy as np
from PIL import Image
from tensorflow import keras

def recognize(image, model):
    image = image.reshape(1, 400) / 255
    prediction = model.predict(image)
    return np.argmax(prediction[0])

def uploadImage(path):
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

fourNames = [
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

list_paths = [
    [x for x in pathlib.Path(paths['pathBarCars']).iterdir()],
    [x for x in pathlib.Path(paths['pathBarPlanes']).iterdir()],
    [x for x in pathlib.Path(paths['pathCars']).iterdir()],
    [x for x in pathlib.Path(paths['pathPlanes']).iterdir()]
]

fourRandomImage = [ uploadImage(random.choice(path)) for path in list_paths ] 

predictions_list = [
    classes[ recognize( fourRandomImage[0], model_Bar ) ],
    classes[ recognize( fourRandomImage[1], model_Bar ) ],
    classes[ recognize( fourRandomImage[2], model_RAW ) ],
    classes[ recognize( fourRandomImage[3], model_RAW ) ],
]

for i in range( len(fourNames) ):
    print(f'{fourNames[i]} regognized as {predictions_list[i]}')
