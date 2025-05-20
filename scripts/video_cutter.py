import os
from moviepy import VideoFileClip  # Importación correcta en v2.x+ :contentReference[oaicite:3]{index=3}

def split_video_by_duration(video_path: str,
                            output_dir: str,
                            segment_duration: float):
    """
    Divide un video en segmentos de duración fija y los guarda en output_dir.
    Cada segmento recibe el sufijo _i donde i es su índice.
    """
    base = os.path.splitext(os.path.basename(video_path))[0]
    clip = VideoFileClip(video_path)        # Carga del video :contentReference[oaicite:4]{index=4}
    total_dur = clip.duration               # Duración total en segundos

    os.makedirs(output_dir, exist_ok=True)
    full_segments = int(total_dur // segment_duration)

    # Fragmentos completos
    for i in range(full_segments):
        start = i * segment_duration
        end = start + segment_duration
        sub = clip.subclipped(start, end)      # Método subclipped(start, end) :contentReference[oaicite:5]{index=5}
        out = f"{base}_{i+1}.mp4"
        sub.write_videofile(os.path.join(output_dir, out),
                            codec="libx264", audio_codec="aac")  # Guardado :contentReference[oaicite:6]{index=6}

    # Fragmento final (sobrante)
    if total_dur % segment_duration != 0:
        start = full_segments * segment_duration
        sub = clip.subclipped(start, total_dur)
        out = f"{base}_{full_segments+1}.mp4"
        sub.write_videofile(os.path.join(output_dir, out),
                            codec="libx264", audio_codec="aac")

def process_folder(input_folder: str = "to_cut",
                   output_folder: str = "cuted",
                   segment_duration: float = 2.0):
    """Procesa todos los videos de input_folder y guarda los cortes en output_folder."""
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        if file.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            print(f"Procesando {file}...")
            split_video_by_duration(os.path.join(input_folder, file),
                                    output_folder,
                                    segment_duration)

if __name__ == "_main_":
    process_folder(input_folder="to_cut",
                   output_folder="cuted",
                   segment_duration=2.0)  # Ajusta aquí la duración deseada
