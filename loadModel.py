import cv2
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

# Load the trained model
model = load_model('savedModelFile.h5')

# Initialize label encoder
# Update this list with your model's emotions in the order they were encoded
labels = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
le = LabelEncoder()
le.fit(labels)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Frame counter
frame_counter = 0

# Emotion detected
emotion = ""

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        frame_counter += 1  # Increment the frame counter
        
        # Every 20 frames, process and predict
        if frame_counter % 20 == 0:
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
            
            print(f"Predicted Emotion: {emotion}")
        
        # Display the resulting frame with the predicted emotion (if any)
        if frame_counter % 1 == 0:
            cv2.putText(frame, f'Emotion: {emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Frame', frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()
