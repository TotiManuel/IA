import cv2
import numpy as np

class CameraControl:
    def __init__(self):
        pass

    def exit(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def preprocess_image(self, frame):
        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize the image
        resized_image = cv2.resize(gray, (128, 128)) 
        return resized_image
    
    def detect_faces(self, frame):
        # Load the face classifier (Haar Cascade)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Convert the image to grayscale to improve detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  
        # Draw rectangles around detected faces
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_count = len(faces)
        else:
            face_count = 0
        return frame, face_count
    
    def predict_with_model(self, frame, model):
        # Preprocess the image to the correct size for the model
        resized_image = cv2.resize(frame, (224, 224))  # Assuming the model expects 224x224 images
        resized_image = np.expand_dims(resized_image, axis=0)  # Add a dimension for the batch
        resized_image = resized_image / 255.0  # Normalize the image to [0, 1]
        # Make the prediction
        prediction = model.predict(resized_image)
        predicted_class = np.argmax(prediction, axis=1)
        return predicted_class
    
    def save_frame(self, frame, path):
        cv2.imwrite(path, frame)

    def detect_motion(self, frame, previous_frame):
        # Convert to grayscale
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
        # Calculate the difference between the current and previous frames
        difference = cv2.absdiff(current_gray, previous_gray)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Draw the contours if movement is detected
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filter small contours
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame
    
    def apply_filter(self, frame):
        # Apply a blur filter
        blurred_image = cv2.GaussianBlur(frame, (15, 15), 0)
        return blurred_image

    def get_capture(self):
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            exit()
        else:
            return capture
        
    def get_frame(self, capture):
        ret, frame = capture.read()
        if not ret:
            return False
        else:
            return ret, frame

    def start(self):
        self.capture = self.get_capture()
        while True:
            ret, frame = self.get_frame(self.capture)
            if ret == False:
                break
            cv2.imshow(f"Real-time Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.exit()

'''
Implementations
frame, face_count = self.detect_faces(frame)
            
ret, previous_frame = self.capture.read()
self.detect_motion(frame, previous_frame)

frame = self.preprocess_image(frame)
cv2.imshow("Real-time Capture", frame)
if cv2.waitKey(1) & 0xFF == ord("q"):
    break
                
frame = cv2.Canny(frame, 100, 200)
            
self.predict_with_model(frame, model)
            
self.apply_filter(frame)
'''
