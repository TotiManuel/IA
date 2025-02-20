import speech_recognition as sr

class ReconocimientoVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def iniciarMicrofono(self):
        with sr.Microphone() as self.source:
            print("Ajustando el ruido ambiente...")
            self.recognizer.adjust_for_ambient_noise(self.source)
            print("Di algo...")
            self.escucharMicrofono()
            self.reconocerAudio()
    
    def escucharMicrofono(self):
        self.audio = self.recognizer.listen(self.source)

    def reconocerAudio(self):
        try:
            print("Reconociendo...")
            text = self.recognizer.recognize_google(self.audio, language="es-ES")  # También puedes usar "en-US" para inglés
            print(f"Lo que dijiste: {text}")
        except sr.UnknownValueError:
            print("No pude entender lo que dijiste")
        except sr.RequestError:
            print("No se pudo conectar al servicio de reconocimiento de voz")

    def iniciarReconocimiento(self):
        self.iniciarMicrofono()
