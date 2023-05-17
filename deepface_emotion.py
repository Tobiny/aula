import cv2
from deepface import DeepFace
import time
import requests

# Umbral de confianza para las emociones
emotion_confidence_threshold = 30

# URL donde se enviarán las emociones
url = 'http://localhost:5000/emotions'

# Saltar n-1 fotogramas para reducir la carga de procesamiento
frame_skip_rate = 5
frame_count = 0

while True:
    # Capturar el fotograma de la cámara web
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Detección de rostros y análisis de emociones
    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

    # Identificación de la emoción dominante
    emotion_counts = {}
    for face in result:
        dominant_emotion = face['dominant_emotion']
        if dominant_emotion in emotion_counts:
            emotion_counts[dominant_emotion] += 1
        else:
            emotion_counts[dominant_emotion] = 1

    if emotion_counts:
        # Determinar la emoción predominante
        max_emotion = max(emotion_counts, key=emotion_counts.get)
        print(f"Emoción predominante: {max_emotion}")

        # Enviar la emoción predominante al servidor
        r = requests.post(url, json={'emotion': max_emotion})

    # Esperar 15 minutos 900 segundos es 15 minutos
    time.sleep(6)
