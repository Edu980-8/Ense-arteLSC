from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor
import torch

class VideoMAEModelSingleton:
    _instance = None

    def __new__(cls, model_ckpt: str):
        if cls._instance is None:
            cls._instance = super(VideoMAEModelSingleton, cls).__new__(cls)
            cls._instance._load(model_ckpt)
        return cls._instance

    def _load(self, model_ckpt: str):
        # Cargar modelo en CPU
        self.model = VideoMAEForVideoClassification.from_pretrained(model_ckpt, torch_dtype=torch.float32)
        self.model.to("cpu")
        self.model.eval()
        self.processor = VideoMAEImageProcessor.from_pretrained(model_ckpt)
        # Cargar el mapeo id2label del modelo
        self.id2label = self.model.config.id2label if hasattr(self.model.config, "id2label") else {}

# Función global para obtener el singleton cargado
def get_model_components(model_ckpt: str):
    instance = VideoMAEModelSingleton(model_ckpt)
    return instance.model, instance.processor, instance.id2label

# Ejemplo de uso en el backend:
# model, processor, id2label = get_model_components(r"results/videomae-LSC-finetuned")