import speech_recognition as sr
from tkinter import messagebox

class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def start_microphone(self):
        with sr.Microphone() as self.source:
            self.recognizer.adjust_for_ambient_noise(self.source)
            messagebox.showinfo("Voice Recognition", "Say something...")
            self.listen_microphone()
            self.recognize_audio()
    
    def listen_microphone(self):
        self.audio = self.recognizer.listen(self.source)

    def recognize_audio(self):
        try:
            text = self.recognizer.recognize_google(self.audio, language="es-ES")  # You can also use "en-US" for English
            messagebox.showinfo("Voice Recognition", f"You said: {text}")
        except sr.UnknownValueError:
            messagebox.showinfo("Voice Recognition","I couldn't understand what you said")
        except sr.RequestError:
            messagebox.showinfo("Voice Recognition","Could not connect to the speech recognition service")

    def start_recognition(self):
        self.start_microphone()
