import os
from moviepy import *

def convertir_y_borrar_avis(carpeta):
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(".avi"):
            ruta_avi = os.path.join(carpeta, archivo)
            ruta_mp4 = ruta_avi.replace(".avi", ".mp4")

            print(f"🎬 Convirtiendo: {archivo}")
            clip = None
            try:
                clip = VideoFileClip(ruta_avi)
                clip.write_videofile(ruta_mp4, codec="libx264", audio=False)
                print(f"✅ Convertido: {ruta_mp4}")
            except Exception as e:
                print(f"❌ Error con {archivo}: {e}\n")
            finally:
                if clip:
                    clip.close()

            # Intentar borrar después de cerrar
            try:
                os.remove(ruta_avi)
                print(f"🗑️ Eliminado: {ruta_avi}\n")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {ruta_avi}: {e}\n")

# Cambia esta ruta por la de tu carpeta
carpeta = r"C:/Users/Eduard_PC/OneDrive/Escritorio/VIDEOS/VIDEOS/COLOR_BODY"
convertir_y_borrar_avis(carpeta)
