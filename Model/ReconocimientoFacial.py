import cv2
import numpy as np
import joblib
import os
import tkinter as tk
from tkinter import Entry, Label, Button
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class ReconocimientoDeRostros:
    def __init__(self):
        self.clasificador = RandomForestClassifier(n_estimators=10)
        self.encoder = LabelEncoder()
        self.datos = []  # Datos de entrenamiento (características de los rostros)
        self.etiquetas = []  # Etiquetas para cada rostro (nombre)
        self.modelo_guardado = "Data/modelo_entrenado.joblib"  # Ruta donde guardaremos el modelo
        self.encoder_guardado = "Data/encoder.joblib"  # Ruta donde guardaremos el encoder
        self.modelo_entrenado = False
        self.cargar_modelo()

    def cargar_modelo(self):
        """Cargar el modelo y el encoder si existen"""
        if os.path.exists(self.modelo_guardado) and os.path.exists(self.encoder_guardado):
            self.clasificador = joblib.load(self.modelo_guardado)
            self.encoder = joblib.load(self.encoder_guardado)
            self.modelo_entrenado = True
            print("Modelo cargado exitosamente.")
        else:
            print("No se encontró un modelo guardado. El modelo comenzará desde cero.")
    
    def obtenerNombre(self, entry):
        self.nombre = entry.get()

    def guardar_modelo(self):
        """Guardar el modelo entrenado y el encoder"""
        joblib.dump(self.clasificador, self.modelo_guardado)
        joblib.dump(self.encoder, self.encoder_guardado)
        print("Modelo guardado exitosamente.")

    def extraer_caracteristicas(self, rostro):
        """Extraer características de un rostro (promedio de píxeles en escala de grises)"""
        gris = cv2.cvtColor(rostro, cv2.COLOR_BGR2GRAY)
        return np.mean(gris)  # Un solo valor que representa la característica

    def entrenar_incremental(self, imagen, etiqueta):
        """Entrenar incrementalmente el modelo con una nueva imagen y su etiqueta"""
        caracteristicas = self.extraer_caracteristicas(imagen)
        self.datos.append([caracteristicas])  # Convertir a formato 2D (una fila, una característica)
        self.etiquetas.append(etiqueta)  # Agregar la etiqueta (nombre)
        # Convertir las etiquetas a números
        etiquetas_numericas = self.encoder.fit_transform(self.etiquetas)
        # Entrenar el modelo
        self.clasificador.fit(np.array(self.datos).reshape(len(self.datos), -1), etiquetas_numericas)
        self.modelo_entrenado = True  # El modelo está entrenado
        # Guardar el modelo después de entrenarlo
        self.guardar_modelo()

    def predecir(self, imagen):
        """Predecir el nombre de la persona basada en el rostro detectado"""
        if self.modelo_entrenado:
            caracteristicas = self.extraer_caracteristicas(imagen).reshape(1, -1)  # Asegurarse de que sea 2D
            prediccion = self.clasificador.predict(caracteristicas)
            return self.encoder.inverse_transform(prediccion)[0]  # Convertir la predicción a nombre
        else:
            print("El modelo no ha sido entrenado aún.")
            return None

    def detectar_rostros(self, frame):
        """Detectar rostros en el frame usando un clasificador Haar"""
        clasificador_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = clasificador_rostros.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return rostros

    def iniciar(self):
        """Iniciar la captura de video en tiempo real y permitir guardar rostros como modelos"""
        captura = cv2.VideoCapture(0)
        if not captura.isOpened():
            print("No se pudo acceder a la cámara")
            exit()

        while True:
            ret, frame = captura.read()
            if not ret:
                print("No se pudo capturar la imagen")
                break

            rostros = self.detectar_rostros(frame)

            for (x, y, w, h) in rostros:
                rostro = frame[y:y+h, x:x+w]  # Recortar el rostro de la imagen
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dibujar un rectángulo alrededor del rostro

                # Predicción de la persona basada en el rostro detectado
                nombre = self.predecir(rostro)
                if nombre:
                    cv2.putText(frame, nombre, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Mostrar la imagen con los rostros detectados y la predicción
            cv2.imshow("Captura en tiempo real", frame)

            # Opción para guardar el rostro como un nuevo modelo cuando se presiona 's'
            if cv2.waitKey(1) & 0xFF == ord('s'):  # Guardar nuevo rostro

                def obtenerNombre(self, entry):
                    print(entry.get())
                root = tk.Tk()
                root.title("Quien es?")
                root.geometry("500x100")
                label = Label(root,text="Quien es?")
                label.pack()
                entry = Entry(root)
                entry.pack()
                boton = Button(root, text="Agregar", command=lambda:(self.obtenerNombre(entry), root.destroyqq()))
                boton.pack()
                root.mainloop()
                for (x, y, w, h) in rostros:
                    rostro = frame[y:y+h, x:x+w]
                    self.entrenar_incremental(rostro, self.nombre)
                    print(f"Rostro de {self.nombre} guardado y modelo actualizado.")

            # Salir cuando se presiona 'q'
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar la cámara y cerrar ventanas
        captura.release()
        cv2.destroyAllWindows()
