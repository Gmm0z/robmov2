#!/usr/bin/env python
#Pablo José Cremades Garrido -- Robots Móviles Proyecto. 
import cv2
import os
import time

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define the image dimensions and frame count
img_width, img_height = 64, 64
max_frames = 100
frame_count = 0

# Create a directory to save the cropped faces
save_path = 'cropped_faces'
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Countdown timer before starting
for i in range(30, 0, -1):
    ret, frame = cap.read()
    if not ret:
        break
    cv2.putText(frame, f'Center your face and wait for {i}...', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Recording Faces', frame)
    cv2.waitKey(1)  # Wait for 1 second

# Bucle de toma de fotos durante video
while frame_count < max_frames:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Process only the largest face in each frame
    largest_face = None
    max_area = 0
    for (x, y, w, h) in faces:
        if w * h > max_area:
            max_area = w * h
            largest_face = (x, y, w, h)

    if largest_face:
        x, y, w, h = largest_face
        # Crop and resize the face
        face = frame[y:y+h, x:x+w]
        resized_face = cv2.resize(face, (img_width, img_height))

        # Save the cropped face image
        cv2.imwrite(f'{save_path}/face_{frame_count}.jpg', resized_face)
        frame_count += 1

        # Display the face being recorded with frame count
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f'Recording face {frame_count}/{max_frames}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Recording Faces', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        # Show the frame even if no face is detected
        cv2.putText(frame, 'No face detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('Recording Faces', frame)

cap.release()
cv2.destroyAllWindows()