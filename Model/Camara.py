import cv2
import numpy as np

class ControlCamara:
    def __init__(self):
        pass

    def salir(self):
        self.captura.release()
        cv2.destroyAllWindows()
#region funciones
    def preprocesar_imagen(self, frame):
        # Convertir la imagen a escala de grises
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Redimensionar la imagen
        imagen_redimensionada = cv2.resize(gris, (128, 128)) 
        return imagen_redimensionada
    
    def detectar_rostros(self, frame):
        # Cargar el clasificador de rostros (Haar Cascade)
        clasificador_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Convertir la imagen a escala de grises para mejorar la detección
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detectar los rostros en la imagen
        rostros = clasificador_rostros.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  
        # Dibujar rectángulos alrededor de los rostros detectados
        if len(rostros) > 0:
            for (x, y, w, h) in rostros:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cantidadRostro = len(rostros)
        else:
            cantidadRostro = 0
        return frame, cantidadRostro
    
    def predecir_con_modelo(self, frame, modelo):
        # Preprocesar la imagen para que tenga el tamaño adecuado para el modelo
        imagen_redimensionada = cv2.resize(frame, (224, 224))  # Suponiendo que el modelo espera imágenes de 224x224
        imagen_redimensionada = np.expand_dims(imagen_redimensionada, axis=0)  # Añadir una dimensión para el batch
        imagen_redimensionada = imagen_redimensionada / 255.0  # Normalizar la imagen a [0, 1]
        # Realizar la predicción
        prediccion = modelo.predict(imagen_redimensionada)
        clase_predicha = np.argmax(prediccion, axis=1)
        return clase_predicha
    
    def guardar_fotograma(self, frame, ruta):
        cv2.imwrite(ruta, frame)

    def detectar_movimiento(self, frame, anterior_frame):
        # Convertir a escala de grises
        gris_actual = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gris_anterior = cv2.cvtColor(anterior_frame, cv2.COLOR_BGR2GRAY)
        # Calcular la diferencia entre los fotogramas actuales y anteriores
        diferencia = cv2.absdiff(gris_actual, gris_anterior)
        umbral = cv2.threshold(diferencia, 25, 255, cv2.THRESH_BINARY)[1]
        # Encontrar los contornos en la imagen umbralizada
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Dibujar los contornos si se detecta movimiento
        for contorno in contornos:
            if cv2.contourArea(contorno) > 500:  # Filtrar contornos pequeños
                (x, y, w, h) = cv2.boundingRect(contorno)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame
    
    def aplicar_filtro(self, frame):
        # Aplicar un filtro de desenfoque (blur)
        imagen_desfocada = cv2.GaussianBlur(frame, (15, 15), 0)
        return imagen_desfocada
#endregion
    def obtenerCaptura(self):
        captura = cv2.VideoCapture(0)
        if not captura.isOpened():
            print("no camara")
            exit()
        else:
            return captura
        
    def obtenerFotograma(self, captura):
        ret, fotograma = captura.read()
        if not ret:
            print("no captura")
            return False
        else:
            return ret,fotograma
    
    def iniciar(self):
        self.captura = self.obtenerCaptura()
        while True:
            ret, frame = self.obtenerFotograma(self.captura)
            if ret == False:
                break
            cv2.imshow(f"Captura en tiempo real", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            '''
            frame, cantidadRostro = self.detectar_rostros(frame)
            
            ret, anterior_frame = self.captura.read()
            self.detectar_movimiento(frame, anterior_frame)

            frame = self.preprocesar_imagen(frame)
            cv2.imshow("Captura en tiempo real", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
                
            frame = cv2.Canny(frame, 100, 200)
            
            self.predecir_con_modelo(frame, modelo)
            
            self.aplicar_filtro(frame)
            '''
        self.salir()
