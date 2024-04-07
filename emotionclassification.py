# # -*- coding: utf-8 -*-
# """EmotionClassification

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/emotionclassification-67be09d0-4548-461a-af4d-19cae2edc7b7.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240405/auto/storage/goog4_request%26X-Goog-Date%3D20240405T192318Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Dab61f15bc978974842076b7b4a17d9de9be95d39018bf7351fff8ca7229d083c037b3b025cb3ed020c4bbf883ccb3bd3f64de809b251a88955abd82a287c1211d4fc6a8573dc85d87ce28096e436d5f8dfb4da2bf6d25190cd346c7548c7251d396712dbf56825dee5118eb74edb1223cab8c1fbd945b285a62823b93942a9601fe9d052c88484a99ac8a5cba4d627ce63185f1d1d8b8c4a0025852c30a35c88bbdb028e62d481c4d826eabe757a9bec7013f054afa30090fc15030c78dd88c133f74fe889d635e5f444160f323f290f42493501de7e337846a444991e23adb8da7f484f0cbb694ef38e0c9ff3d26a9e2a14d41c9ee6af25a1fe459f795a78e0
# """

# # IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# # TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# # THEN FEEL FREE TO DELETE THIS CELL.
# # NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# # ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# # NOTEBOOK.

# import os
# import sys
# from tempfile import NamedTemporaryFile
# from urllib.request import urlopen
# from urllib.parse import unquote, urlparse
# from urllib.error import HTTPError
# from zipfile import ZipFile
# import tarfile
# import shutil

# CHUNK_SIZE = 40960
# DATA_SOURCE_MAPPING = 'facial-expression-dataset:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F1060020%2F1782963%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240405%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240405T192318Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D89dccd16371c551592e0c74fd6267c634a9b59187de72c1b4a44e3512c1818440b644dc15c7bff4a7e516c22a8bfa5af9b8df185de6789d795512a9dd80752ce3a9dae97508154249bb9393104c87196ee939b00f990d0a084db54bddb0f65e584f11066d0f254d11eb8aa143a96d25c5ce8095eb445a29878f1484354edb562dc3558ec426adced114bc5fb6ecb304e24a254b3032da3315a8fbb32a04e389942cf9c2deadc79fd4dcd2f32fd7778c58fbed17efc2a189af42c92dd0d16c3306631afd5fffdf55869df0d8d7c3ee2af1623db6715080de3c359c60dac069f268be41582bf80b4360d7a0f5f26a8f90902041b684dfea319cf1e3ef94f3d836d'

# KAGGLE_INPUT_PATH='/kaggle/input'
# KAGGLE_WORKING_PATH='/kaggle/working'
# KAGGLE_SYMLINK='kaggle'

# # !umount /kaggle/input/ 2> /dev/null
# shutil.rmtree('/kaggle/input', ignore_errors=True)
# os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
# os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

# try:
#   os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
# except FileExistsError:
#   pass
# try:
#   os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
# except FileExistsError:
#   pass

# for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
#     directory, download_url_encoded = data_source_mapping.split(':')
#     download_url = unquote(download_url_encoded)
#     filename = urlparse(download_url).path
#     destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
#     try:
#         with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
#             total_length = fileres.headers['content-length']
#             print(f'Downloading {directory}, {total_length} bytes compressed')
#             dl = 0
#             data = fileres.read(CHUNK_SIZE)
#             while len(data) > 0:
#                 dl += len(data)
#                 tfile.write(data)
#                 done = int(50 * dl / int(total_length))
#                 sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
#                 sys.stdout.flush()
#                 data = fileres.read(CHUNK_SIZE)
#             if filename.endswith('.zip'):
#               with ZipFile(tfile) as zfile:
#                 zfile.extractall(destination_path)
#             else:
#               with tarfile.open(tfile.name) as tarfile:
#                 tarfile.extractall(destination_path)
#             print(f'\nDownloaded and uncompressed: {directory}')
#     except HTTPError as e:
#         print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
#         continue
#     except OSError as e:
#         print(f'Failed to load {download_url} to path {destination_path}')
#         continue

# print('Data source import complete.')

# """# **Hi Coders** Today We Are Going To Work Through A Problem Called **Face Emotion Recognition**.
# ## This is an important topic in field of ML.We Used Our Model to detect human emotion based on their photos.
# It Mainly Consist of 7 emotions -->

# `Happy` `Sad` `Anger` `Surprise` `Fear` `Neutral` `Disgust`.

# Algo Predict HumanEmotions.

# I Have Divided This Project in two parts -
# 1) Creating My Own Model.

# 2) Using a pretrained Model.

# Obviously Second Work Going to work A Lot Better. I Have Not Even Created A Very Deep Learning Neural Network of my own.
# Like Follwing a Research paper but if you want to go I Will Suggest To Look at these  **Mollahosseini** and **Lopes**.Because My Semester Exams Are Coming 🥲.
# Maybe in Future I Will  Work On `Mollahosseini` CNN  Model .

# On A Tough Intution He Did Follwoing Things-->
# ## 1) Data Preprocessing:
# * Facial landmarks were extracted from the images.
# * The images were then resized to 48x48 pixels.
# * Augmentation techniques were applied to the data. Augmentation can involve operations like rotation, scaling, flipping, etc., to artificially increase the size of the training dataset and improve the model's generalization.

# ## 2) Network Architecture:
# * In Conv Layers They Use Two Max Pooling Layers And And Two Conv2D Layer.
# * And After That They Use `Inception-Style Modules`With Filters With 1x1 and 3x3 and 5x5.

# ### The Dataset we have Taken Is `Facial-Expression-dataset` on Kaggle

# ### Importing The Neccessary Libraries
# """

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import os
import random
import warnings
import seaborn as sns

from keras.utils import load_img



warnings.filterwarnings("ignore")

print(tf.__version__)

"""### Load The Dataset `Train` And `Test`"""

TRAIN_DIR="train"
TEST_DIR="test"

def load_datasets(directory):

    image_paths=[]
    labels=[]
    for label in os.listdir(directory):
        for filename in os.listdir(directory+"/"+label):
            for file in os.listdir(directory+"/"+label+"/"+filename):
                image_path=os.path.join(directory,label,filename,file)
                image_paths.append(image_path)
                labels.append(filename)
            print(filename,"Completed\n")
    return image_paths,labels

"""### Converting Them Into Train Dataframe"""

train=pd.DataFrame()
train["image"],train["label"]=load_datasets(TRAIN_DIR)

train.sample(4)

"""### Converting Them Into Test Dataframe"""

test=pd.DataFrame()
test["image"],test["label"]=load_datasets(TEST_DIR)

test.sample(4)

train=train.sample(frac=1).reset_index(drop=True)

train.head(4)

"""### Basic `EDA`"""

train["label"].value_counts().values

sns.countplot(x=train["label"])
plt.show()

from PIL import Image
img=Image.open(train["image"][10])
plt.imshow(img,cmap="gray")
plt.title(train["label"][10])
plt.show()

plt.figure(figsize=(25,25))
files=train.iloc[0:25]
for index,file,label in files.itertuples():
#     print(index)
    plt.subplot(5,5,index+1)
    img=Image.open(file)
    plt.imshow(img,cmap="gray")
    plt.title(label)
    plt.axis("off")
#     plt.show()

"""What below Fuction are doing is just they looping through all my image converting them into gray_scale  and converting them into a numpy array and creating a list which contains all images in an array format and after that converting that list into a numpy array and then reshaping into shapes of total_images,48,48,1 where 48 are height and width and 1 is channel you can use 3 for `rgb` values

"""

def load_img_grayscale(path):
    img = Image.open(path)
    img = img.convert('L')
    return img


def extract_feature_images(images):
    features = []
    for image in images:
        img = load_img_grayscale(image)
        img = np.array(img)
        features.append(img)
    features = np.array(features)
    features = features.reshape(len(features), 48, 48, 1)
    return features

train_features=extract_feature_images(train["image"])

train_features[0][0][0]

test_features=extract_feature_images(test["image"])
test_features[0][0][0]

"""we are dividing those all values by 255.

Basically We Are MinMaxScaling Are Values to be in form 0 and 1.

`0` means `Black` and `1` means `White`
"""

X_train=train_features/255.0
X_test=test_features/255.0

X_train[0][0][0]

"""## Label Encoding
### to convert values like Happy Sad etc. to 0,1 etc.
"""

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
le.fit(train["label"])
y_train=le.transform(train["label"])
y_test=le.transform(test["label"])

y_train

y_test

input_shape=(48,48,1)
output_classes=7

"""Converting all values into categorical column to help our `CNN Layers`
to `one_hot_encode` them
"""

from keras.utils import to_categorical

y_train=to_categorical(y_train,num_classes=7)

y_train[0]

y_test=to_categorical(y_test,num_classes=7)

y_test

"""# Making Our Deep CNN Model

"""

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D,LSTM,AveragePooling2D

model = Sequential()


model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(output_classes, activation="softmax"))

model.compile(optimizer="adam", metrics=["accuracy"], loss="categorical_crossentropy")

"""### Using `Early Stopping`"""

from keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor='val_loss',
                               patience=5,
                               restore_best_weights=True)

# history=model.fit(x=X_train,y=y_train,batch_size=32,epochs=100,validation_data=(X_test,y_test),callbacks=[early_stopping])
history=model.fit(x=X_train,y=y_train,batch_size=32,epochs=5,validation_data=(X_test,y_test),callbacks=[early_stopping])

"""### Plotting the accuracy and val_accuracy graph"""

plt.plot(history.history["accuracy"],"b",label="accuracy")
plt.plot(history.history["val_accuracy"],"r",label="val_accuracy")
plt.title("Accuracy Score")
plt.show()

"""### Plotting the loss and val_loss graph"""

plt.plot(history.history["loss"],"b",label="loss")
plt.plot(history.history["val_loss"],"r",label="val_loss")
plt.title("Loss")
plt.show()

"""## Evaluation our model
Using `Accuracy` `Precision` `Recall` `F1` and `hinge loss`
"""

from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

preds=model.predict(X_test)
preds=np.argmax(preds,axis=1)
preds

preds_cat=to_categorical(preds,num_classes=7)

preds_cat

accuracy_score(y_test,preds_cat)

precision_score(y_test,preds_cat,average="weighted")

recall_score(y_test,preds_cat,average="weighted")

f1_score(y_test,preds_cat,average="weighted")

from sklearn.metrics import hamming_loss

hamming_loss_val = hamming_loss(y_test,preds_cat)
print("Hamming Loss:", hamming_loss_val)

len(X_test)

import random
image_index=random.randint(0,len(X_test))
print("Original Output:", test['label'][image_index])
pred=model.predict(X_test[image_index].reshape(1, 48, 48, 1))
prediction_label = le.inverse_transform([pred.argmax()])[0]
print("Predicted Output:", prediction_label)
plt.imshow(X_test[image_index].reshape(48, 48), cmap='gray');

image_index=random.randint(0,len(X_test))
print("Original Output:", test['label'][image_index])
pred=model.predict(X_test[image_index].reshape(1, 48, 48, 1))
prediction_label = le.inverse_transform([pred.argmax()])[0]
print("Predicted Output:", prediction_label)
plt.imshow(X_test[image_index].reshape(48, 48), cmap='gray');

image_index=random.randint(0,len(X_test))
print("Original Output:", test['label'][image_index])
pred=model.predict(X_test[image_index].reshape(1, 48, 48, 1))
prediction_label = le.inverse_transform([pred.argmax()])[0]
print("Predicted Output:", prediction_label)
plt.imshow(X_test[image_index].reshape(48, 48), cmap='gray');

# model.save('savedModel')
tf.saved_model.save(model, 'C:\\Users\\User\\OneDrive\\Desktop\\eve\\savedModel')


"""# Using Pretrained Network **Efficient Net**

Efficient Net Mainly follow an approact to improve model accuracy using 3 things mainly `Depth` of a neural network.`Width` of a network i.e.; channels and `Resultion` of An Image

"""

# !pip install efficientnet

from keras.models import Model
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from efficientnet.tfkeras import EfficientNetB0

"""### Performing Data Augmentation"""

train_datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator()

X_train_rgb = np.repeat(X_train[..., np.newaxis], 3, -1)
X_test_rgb = np.repeat(X_test[..., np.newaxis], 3, -1)

"""### Building Model"""

base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(48, 48, 3))
base_model.trainable = False

pretrained_model = Sequential([
    base_model,
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])

pretrained_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

X_train_rgb = np.squeeze(X_train_rgb, axis=-2)
X_test_rgb = np.squeeze(X_test_rgb, axis=-2)

batch_size = 32
# epochs = 40
epochs = 5


train_generator = train_datagen.flow(X_train_rgb, y_train, batch_size=batch_size)
test_generator = test_datagen.flow(X_test_rgb, y_test, batch_size=batch_size)

pretrained_history = pretrained_model.fit(train_generator, epochs=epochs, validation_data=test_generator)

"""### Checking Accuracy and loss of Model"""

plt.plot(pretrained_history.history["accuracy"],"b",label="accuracy")
plt.plot(pretrained_history.history["val_accuracy"],"r",label="val_accuracy")
plt.title("Accuracy Score")
plt.show()

plt.plot(pretrained_history.history["loss"],"b",label="loss")
plt.plot(pretrained_history.history["val_loss"],"r",label="val_loss")
plt.title("Loss Score")
plt.show()

"""# My Model Performed Well on the Data So I Am Going to use it"""
