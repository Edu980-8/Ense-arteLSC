import io
from fastapi import UploadFile
import torch
from PIL import Image
from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor

import av 
import av.error
import numpy as np
from PIL import Image
import torch
from typing import Any, Dict, List, Optional, Tuple
import torchvision.transforms as T
import torchvision.transforms.functional as F

async def read_and_sample_video_pyav_uploadfile(file: UploadFile, num_frames: int) -> Optional[List[np.ndarray]]:
    """
    Lee un archivo de video UploadFile usando PyAV y samplea un número fijo de frames.

    Args:
        file (UploadFile): Archivo recibido desde el endpoint FastAPI.
        num_frames (int): Número de frames a samplear.

    Returns:
        Optional[List[np.ndarray]]: Lista de frames RGB como arrays de numpy, o None en caso de error.
    """
    try:
        contents = await file.read()  # Lee el archivo en memoria
        container = av.open(io.BytesIO(contents))  # Abre el archivo en memoria con PyAV

        # Decodifica todos los frames como arrays RGB
        all_frames = [frame.to_ndarray(format="rgb24") for frame in container.decode(video=0)]
        container.close()

        total_frames = len(all_frames)
        if total_frames == 0:
            print(f"Error: No se decodificaron frames del archivo subido.")
            return None

        if total_frames >= num_frames:
            indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
            sampled_frames = [all_frames[i] for i in indices]
        else:
            sampled_frames = all_frames
            while len(sampled_frames) < num_frames:
                sampled_frames.append(all_frames[-1])

        return sampled_frames

    except av.AVError as e:
        print(f"Error de PyAV al procesar archivo subido: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar archivo subido con PyAV: {e}")
        return None

async def infer_video_class(
    file: UploadFile,
    model,
    processor,
    id2label: dict
) -> List[Dict[str, Any]]:
    """
    Realiza inferencia sobre un video subido usando un modelo y procesador dados.

    Args:
        file (UploadFile): Video recibido desde el endpoint FastAPI.
        model: Modelo PyTorch para inferencia.
        processor: Procesador de frames (de transformers o personalizado).
        id2label (dict): Diccionario de mapeo de IDs a etiquetas.

    Returns:
        List[Dict[str, Any]]: Lista de predicciones top-5 con label y score.
    """
    # 1. Leer y muestrear frames
    num_frames = model.config.num_frames
    size = (processor.size["shortest_edge"], processor.size["shortest_edge"])
    frames = await read_and_sample_video_pyav_uploadfile(file, num_frames=num_frames)
    
    if frames is None:
        raise ValueError("No se pudieron leer frames del video.")

    # 2. Convertir a PIL y redimensionar
    pil_frames = [Image.fromarray(f).resize(size) for f in frames]

    # 3. Preprocesar
    inputs = processor(pil_frames, return_tensors="pt")

    # 4. Inferencia solo en CPU
    model.eval()
    model.to("cpu")
    with torch.no_grad():
        # Asegura que los tensores estén en CPU
        inputs = {k: v.to("cpu") for k, v in inputs.items()}
        outputs = model(**inputs)
        logits = outputs.logits

    probs = torch.nn.functional.softmax(logits, dim=-1)
    top5_probs, top5_indices = torch.topk(probs, k=5, dim=-1)

    results = []
    for prob, idx in zip(top5_probs[0], top5_indices[0]):
        results.append({
            "label": id2label.get(idx.item(), str(idx.item())),
            "score": round(prob.item(), 4)
        })

    return results