import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import os
import random
import warnings
import seaborn as sns

warnings.filterwarnings("ignore")

print(tf.__version__)

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

#Converting Them Into Train Dataframe

train=pd.DataFrame()
train["image"], train["label"]=load_datasets(TRAIN_DIR)

train.sample(4)

#Converting Them Into Test Dataframe

test=pd.DataFrame()
test["image"], test["label"]=load_datasets(TEST_DIR)

test.sample(4)

train=train.sample(frac=1).reset_index(drop=True)

train.head(4)

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

X_train=train_features/255.0
X_test=test_features/255.0

X_train[0][0][0]

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
le.fit(train["label"])
y_train=le.transform(train["label"])
y_test=le.transform(test["label"])

y_train

y_test

input_shape=(48,48,1)
output_classes=7

from keras.utils import to_categorical

y_train=to_categorical(y_train,num_classes=7)

y_train[0]

y_test=to_categorical(y_test,num_classes=7)

y_test



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

#Using Early Stopping

from keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor='val_loss',
                               patience=5,
                               restore_best_weights=True)

history=model.fit(x=X_train,y=y_train,batch_size=32,epochs=5,validation_data=(X_test,y_test),callbacks=[early_stopping])

# Plotting the accuracy and val_accuracy graph

plt.plot(history.history["accuracy"],"b",label="accuracy")
plt.plot(history.history["val_accuracy"],"r",label="val_accuracy")
plt.title("Accuracy Score")
plt.show()

# Plotting the loss and val_loss graph

plt.plot(history.history["loss"],"b",label="loss")
plt.plot(history.history["val_loss"],"r",label="val_loss")
plt.title("Loss")
plt.show()

# Evaluation our model

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

tf.saved_model.save(model, 'C:\\Users\\shrey\\OneDrive\\Documents\\GitHub\\eve\\savedModel')
