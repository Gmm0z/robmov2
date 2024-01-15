#!/usr/bin/env python
#Pablo José Cremades Garrido  -- Robots Móviles Proyecto. 
import cv2
from tensorflow.keras.models import load_model
import numpy as np

# Load your trained model
model = load_model('user_detection_model_video.h5')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define the image dimensions (same as used during training)
img_width, img_height = 64, 64

class_labels = ['invaliduser', 'validuser']  # replace with your actual class names

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Find the largest face as the most prominent face
    largest_face = None
    max_area = 0
    for (x, y, w, h) in faces:
        if w * h > max_area:
            max_area = w * h
            largest_face = (x, y, w, h)

    if largest_face:
        x, y, w, h = largest_face
        # Crop and preprocess the face
        face = frame[y:y+h, x:x+w]
        resized_face = cv2.resize(face, (img_width, img_height))
        reshaped_face = resized_face.reshape(1, img_width, img_height, 3) / 255.0

        # Predict using the CNN model
        prediction = model.predict(reshaped_face)
        class_index = np.argmax(prediction, axis=1)[0]
        confidence_score = np.max(prediction)

        # Display the predictions
        user = class_labels[class_index]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        text = f'User: {user}, Confidence: {confidence_score:.2f}'
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('User Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()