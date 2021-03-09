from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import utils
from tensorflow.keras.preprocessing import image
import random
import numpy as np
import pathlib
import os
from PIL import Image

def uploadImage(path):
    image = Image.open(path)
    data = np.asarray(image)
    return data

def GetImages_Names(path, name):
    images = []
    names = []
    count = 0
    for imageName in pathlib.Path(path).iterdir():
        image = uploadImage( str(imageName.resolve()) ) 
        if image is not None:
            images.append(image)
            names.append(name)
            count += 1
            if count % 1000 == 0:
                print(f'{count} images of {name} is loaded') 
    print(f'Loading {name} Done')               
    return images, names        

paths = {
    'pathCars': '../Images/Cars/',
    'pathPlanes': '../Images/Planes/',
    'pathBarCars': '../Images/BarCars/',
    'pathBarPlanes': '../Images/BarPlanes/',
}

path = paths['pathCars']
images_train, names_train = GetImages_Names(path, 0)

path = paths['pathPlanes']
a, b = GetImages_Names(path, 1)
images_train += a
names_train += b

images_train = np.array(images_train).reshape(len(images_train), 400)
images_train = images_train / 255

random_image_position = random.randint(0, len(images_train))
images_test = images_train[random_image_position].reshape(1, 400)
names_test = names_train[random_image_position]

print(names_train[0])

names_train = utils.to_categorical(names_train, num_classes=2)

print(names_train[0])

model = Sequential()
model.add(Dense(400, input_dim=400, activation="relu"))
model.add(Dense(2, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])

print(model.summary())

history = model.fit(images_train, names_train, 
                    batch_size=200, 
                    epochs=50,  #иначе 100
                    verbose=1)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
model.save('RAW_model.h5')

predictions = model.predict(images_test)
n = 0
print(predictions[n])

print(np.argmax(predictions[n]))
print(names_test)
