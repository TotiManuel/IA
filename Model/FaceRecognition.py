import cv2
import numpy as np
import joblib
import os
import tkinter as tk
from tkinter import Entry, Label, Button, messagebox
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class FaceRecognition:
    def __init__(self):
        self.classifier = RandomForestClassifier(n_estimators=10)
        self.encoder = LabelEncoder()
        self.data = []  # Training data (features of faces)
        self.labels = []  # Labels for each face (name)
        self.saved_model = "Data/trained_model.joblib"  # Path where we will save the model
        self.saved_encoder = "Data/encoder.joblib"  # Path where we will save the encoder
        self.model_trained = False

    def load_model(self):
        """Load the model and encoder if they exist"""
        if os.path.exists(self.saved_model) and os.path.exists(self.saved_encoder):
            self.classifier = joblib.load(self.saved_model)
            self.encoder = joblib.load(self.saved_encoder)
            self.model_trained = True
            messagebox.showinfo("Camera","Model loaded successfully.")
        else:
            messagebox.showinfo("Camera","No saved model found. The model will start from scratch.")
    
    def get_name(self, entry):
        self.name = entry.get()

    def save_model(self):
        """Save the trained model and encoder"""
        joblib.dump(self.classifier, self.saved_model)
        joblib.dump(self.encoder, self.saved_encoder)
        messagebox.showinfo("Model","Model saved successfully.")

    def extract_features(self, face):
        """Extract features from a face (average pixel value in grayscale)"""
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        return np.mean(gray)  # A single value representing the feature

    def incremental_train(self, image, label):
        """Incrementally train the model with a new image and its label"""
        features = self.extract_features(image)
        self.data.append([features])  # Convert to 2D format (one row, one feature)
        self.labels.append(label)  # Add the label (name)
        # Convert the labels to numbers
        numeric_labels = self.encoder.fit_transform(self.labels)
        # Train the model
        self.classifier.fit(np.array(self.data).reshape(len(self.data), -1), numeric_labels)
        self.model_trained = True  # The model is trained
        # Save the model after training
        self.save_model()

    def predict(self, image):
        """Predict the name of the person based on the detected face"""
        if self.model_trained:
            features = self.extract_features(image).reshape(1, -1)  # Ensure it's 2D
            prediction = self.classifier.predict(features)
            return self.encoder.inverse_transform(prediction)[0]  # Convert prediction to name
        else:
            return None

    def detect_faces(self, frame):
        """Detect faces in the frame using a Haar classifier"""
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def start(self):
        self.load_model()
        """Start real-time video capture and allow saving faces as models"""
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            messagebox.showinfo("Camera","Unable to access the camera")
            exit()

        while True:
            ret, frame = capture.read()
            if not ret:
                messagebox.showinfo("Model","Unable to capture the image")
                break

            faces = self.detect_faces(frame)

            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]  # Crop the face from the image
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw a rectangle around the face

                # Predict the person based on the detected face
                name = self.predict(face)
                if name:
                    cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the image with the detected faces and prediction
            cv2.imshow("Real-time Capture", frame)

            # Option to save the face as a new model when 's' is pressed
            if cv2.waitKey(1) & 0xFF == ord('s'):  # Save new face

                root = tk.Tk()
                root.title("Who is it?")
                root.geometry("500x100")
                label = Label(root, text="Who is it?")
                label.pack()
                entry = Entry(root)
                entry.pack()
                button = Button(root, text="Add", command=lambda: (self.get_name(entry), root.destroy()))
                button.pack()
                root.mainloop()
                for (x, y, w, h) in faces:
                    face = frame[y:y+h, x:x+w]
                    self.incremental_train(face, self.name)
                    messagebox.showinfo("Face",f"Face of {self.name} saved and model updated.")

            # Exit when 'q' is pressed
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close windows
        capture.release()
        cv2.destroyAllWindows()
