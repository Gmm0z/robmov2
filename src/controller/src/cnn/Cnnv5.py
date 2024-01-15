#!/usr/bin/env python
#Pablo José Cremades Garrido -- Robots Móviles Proyecto. 

# Import necessary libraries from TensorFlow and Keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# Define the path to the dataset containing facial images
dataset_path = '/home/palko/robmov2/src/controller/src/cnn/pictures'

# Set the dimensions for the input images
img_width, img_height = 64, 64

# Initialize ImageDataGenerator for data augmentation and preprocessing
data_generator = ImageDataGenerator(
    rescale=1. / 255,  # Rescaling factor for image normalization
    validation_split=0.1,  # Proportion of data to be used for validation
    rotation_range=30,  # Range of random rotations in degrees
    brightness_range=[0.1, 2.5],  # Range for random brightness adjustments
    width_shift_range=0.1,  # Range for random horizontal shifts
    height_shift_range=0.1,  # Range for random vertical shifts
    shear_range=0.15,  # Shearing intensity
    horizontal_flip=True  # Enable random horizontal flips
)


# Load and preprocess training data
train_data = data_generator.flow_from_directory(
    dataset_path,
    target_size=(img_width, img_height),
    batch_size=16,
    class_mode='categorical',
    subset='training'  # Specify subset as training data
)

# Load and preprocess validation data
valid_data = data_generator.flow_from_directory(
    dataset_path,
    target_size=(img_width, img_height),
    batch_size=16,
    class_mode='categorical',
    subset='validation'  # Specify subset as validation data
)

# Configure early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='min')

# Extract class labels from the training data
class_labels = [class_name for class_name, index in train_data.class_indices.items()]

# Define the architecture of the Convolutional Neural Network (CNN)
model = Sequential()
model.add(Conv2D(64, (3, 3), input_shape=(img_width, img_height, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Dropout(0.5))  # Dropout layer to reduce overfitting
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(units=256, activation='relu'))

model.add(Dense(units=len(class_labels), activation='softmax'))  # Output layer

# Compile the model with loss function and optimizer
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(
train_data,
steps_per_epoch=train_data.samples // 16,
validation_data=valid_data,
validation_steps=valid_data.samples // 16,
epochs=50, # Increased epochs because of early stopping
callbacks=[early_stopping]
)

# Save the trained model
model.save('user_detection_model_video.h5')
