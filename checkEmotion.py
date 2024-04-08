import cv2
import time
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder 
import matplotlib.pyplot as plt
from twilio.rest import Client

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


percentage = .4
limit = 180

# GET INFORMATION FROM FIRESTORE DATABASE

cred = credentials.Certificate('cher-19625-firebase-adminsdk-vjqfy-f28ded84c0.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
# Reference to a Firestore collection
doc_ref = db.collection('Users').document('User1')
doc = doc_ref.get()
if doc.exists:
    data = doc.to_dict()
    to_number = data.get('PhoneNumber')
    message = data.get("Message")
    percentage = float(data.get("Percent"))/100
    limit = float(data.get("TimeLimit"))
else:
    print('Document does not exist')


# LOAD TRAINED MODEL

model = load_model('emotionDetectingModel.h5')
labels = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
le = LabelEncoder()
le.fit(labels)



# TWILIO CREDENTIALS *MAKE YOUR OWN ACCOUNT AND REPLACE FOLLOWING INFO* *I ONLY HAVE FREE TRIAL AND ITS ALMOST OUT -- I DEBUGGED TOO MUCH*

account_sid = 'REPLACE'
auth_token = 'REPLACE'
# Initialize Twilio client
client = Client(account_sid, auth_token)
# Twilio phone number 
from_number = 'REPLACE'  


# CAMERA CODE

# Open the camera
cap = cv2.VideoCapture(0)
time.sleep(1)
# Frame counters
frame_counter = 0
sad_frame_counter = 0
happy_frame_counter = 0
anger_frame_counter = 0
neutral_frame_counter = 0
lineGraphX_sad = []
lineGraphY_sad = []
sentText = False
emotion = " "
startTime = time.time()
try:
    while True:
        # Capture frames
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        frame_counter += 1  

        # Preproccess Frame 
        cv2.imshow('Frame', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray, (48, 48), interpolation=cv2.INTER_AREA)
        normalized_frame = resized_frame / 255.0
        input_frame = np.expand_dims(normalized_frame, axis=0)
        input_frame = np.expand_dims(input_frame, axis=3)

        # Predict 
        prediction = model.predict(input_frame)
        emotion_index = np.argmax(prediction)
        emotion = le.inverse_transform([emotion_index])[0]

        # Keep track of frame data
        if emotion == "Sad":
            sad_frame_counter += 1     
        print(f"Detected: {emotion}")
 
        if cv2.waitKey(30) and time.time() - startTime >= limit:
            break
finally: 
    cap.release()
    cv2.destroyAllWindows()


# Send Text to Adult
if sentText == False and  sad_frame_counter/frame_counter > percentage:
    client.messages.create(from_=from_number, to=to_number, body=message)
    print("Message sent successfully.")
    sentText = True

