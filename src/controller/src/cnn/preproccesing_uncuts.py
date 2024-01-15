import cv2
import os
import glob

def detect_and_crop_face(input_path, output_path):
    # Load the pre-trained Haar Cascade model for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Process each image in the input directory
    for img_file in glob.glob(input_path + '/*.jpg'):  # adjust the pattern to your file type
        # Read the image
        img = cv2.imread(img_file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Crop the image to the face area
            face = img[y:y+h, x:x+w]
            # Save the cropped image
            cv2.imwrite(os.path.join(output_path, os.path.basename(img_file)), face)
            break  # Only save the first face; remove this line to save all detected faces

# Define your input and output paths
input_path = '/home/palko/robmov2/src/controller/src/cnn/uncut_pictures/invalidusers'
output_path = '/home/palko/robmov2/src/controller/src/cnn/pictures/invalidusers'

# Run the face detection and cropping
detect_and_crop_face(input_path, output_path)
