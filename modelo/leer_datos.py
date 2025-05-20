import cv2 as cv
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

import os

path = r"C:/Users/Eduard_PC/OneDrive/Escritorio/VIDEOS/VIDEOS/COLOR_BODY/0000_0000_0000.avi"
print(os.path.exists(path))


def leer_datos(path):
    cap = cv.VideoCapture(path)

    if not cap.isOpened():
        print("❌ No se pudo abrir el video.")
        return

    print("✅ Video cargado correctamente.")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Mostrar frame (opcional)
        cv.imshow('Frame', frame)

        # Salir con 'q'
        if cv.waitKey(25) & 0xFF == ord('q'):
            break

    print(f"Total de frames leídos: {frame_count}")
    cap.release()
    cv.destroyAllWindows()


leer_datos(r"C:/Users/Eduard_PC/OneDrive/Escritorio/VIDEOS/COLOR_BODY/0000_0000_0000.avi")
