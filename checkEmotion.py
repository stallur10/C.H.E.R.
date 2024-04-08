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

# ****GET INFORMATION FROM FIRESTORE DATABASE****

# Initialize Firebase Admin SDK
cred = credentials.Certificate('cher-19625-firebase-adminsdk-vjqfy-f28ded84c0.json')
firebase_admin.initialize_app(cred)
# Create a Firestore client
db = firestore.client()
# Reference to a Firestore collection
doc_ref = db.collection('Users').document('User1')
# Get all documents in the collection
doc = doc_ref.get()
if doc.exists:
    data = doc.to_dict()
    # Recipient's phone number
    to_number = data.get('PhoneNumber')
    message = data.get("Message")
    percentage = data.get("Percent")/100
else:
    print('Document does not exist')


# ****LOAD TRAINED MODEL****

model = load_model('emotionDetectingModel.h5')
# Initialize label encoder
# Update this list with your model's emotions in the order they were encoded
labels = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
le = LabelEncoder()
le.fit(labels)



# ****TWILIO CREDENTIALS****

account_sid = 'ACa231e013485be680cad080c458dda456'
auth_token = '9f5bbff69758c9cc2d451244f840322b'
# Initialize Twilio client
client = Client(account_sid, auth_token)
# Twilio phone number
from_number = '18775066761'  


# ****CAMERA CODE****

# Open the camera
cap = cv2.VideoCapture(0)
time.sleep(2)
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
try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        frame_counter += 1  # Increment the frame counter
        # Every 20 frames, process and predict
        if frame_counter % 1 == 0:
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Resize the grayscale frame to 48x48 as expected by the model
            resized_frame = cv2.resize(gray, (48, 48), interpolation=cv2.INTER_AREA)
            # Normalize the pixel values to be in the range [0, 1]
            normalized_frame = resized_frame / 255.0
            # Expand the frame dimensions to match the model's input shape: (1, 48, 48, 1)
            input_frame = np.expand_dims(normalized_frame, axis=0)
            input_frame = np.expand_dims(input_frame, axis=3)
            # Predict the emotion
            prediction = model.predict(input_frame)
            emotion_index = np.argmax(prediction)
            emotion = le.inverse_transform([emotion_index])[0]
            # Keep track of frame data
            if emotion == "Sad":
                sad_frame_counter += 1
            if emotion == "Happy":
                happy_frame_counter += 1
            if emotion == "Anger":
                anger_frame_counter += 1
            if emotion == "Neutral":
                neutral_frame_counter += 1
            if frame_counter == 100:
                lineGraphX_sad.append(frame_counter)
                lineGraphY_sad.append(sad_frame_counter)
            # Send Text to Adult
            if sentText == False and frame_counter > 200 and sad_frame_counter/frame_counter > .4:
                # client.messages.create(from_=from_number, to=to_number, body=message)
                print("Message sent successfully.")
                sentText = True
            print(f"Detected: {emotion}")
        # Display the resulting frame with the predicted emotion (if any)
        # if frame_counter % 1 == 0:
        #     cv2.putText(frame, f'You are feeling: {emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Frame', frame)
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally: 
    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()


# ****CREATE GRAPHS****

plt.plot(lineGraphX_sad, lineGraphY_sad, marker='o')
# Add labels and title
plt.xlabel('Total Frame')
plt.ylabel('Sad Frames')
plt.title('Line Graph Example')
# plt.xticks(range(min(0), max(2000) + 100, 1))
# Display the graph
plt.show()




