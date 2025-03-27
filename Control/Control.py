from Model.Camera import CameraControl
from Model.FaceRecognition import FaceRecognition
from Model.VoiceRecognition import VoiceRecognition
from Model.RecognizeIP import RecognizeIP

class Control:
    def __init__(self):
        self.camera = CameraControl()
        self.recognition = FaceRecognition()
        self.voiceRecognition = VoiceRecognition()
        self.recognizeIp = RecognizeIP()

    def start_camera(self):
        self.camera.start()
    
    def start_recognition(self):
        self.recognition.start()
    
    def start_voice_recognition(self):
        self.voiceRecognition.start_recognition()

    def start_recognize_ip(self):
        return self.recognizeIp.get_ip()
