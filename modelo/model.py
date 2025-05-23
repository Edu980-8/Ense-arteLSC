import torch
from transformers import VivitImageProcessor, AutoConfig, AutoModelForVideoClassification
from config import MODEL_NAME

from transformers import AutoModelForVideoClassification, VideoMAEImageProcessor

def load_model(num_labels=50, freeze_backbone=True):
    model = AutoModelForVideoClassification.from_pretrained(
        "google/vivit-b-16x2-kinetics400",
        num_labels=num_labels,
        ignore_mismatched_sizes=True
    )
    processor = VideoMAEImageProcessor.from_pretrained("google/vivit-b-16x2-kinetics400")

    if freeze_backbone:
        for param in model.vivit.parameters():
            param.requires_grad = False
        print("🔒 ViViT backbone frozen (only classifier will be trained).")

    return model, processor
