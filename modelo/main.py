import os
import torch
from torch.utils.data import DataLoader, random_split
from transformers import (
    VivitImageProcessor,
    AutoConfig,
    AutoModelForVideoClassification,
    TrainingArguments,
    Trainer,
)
from VideoPreprocessing import VideoDataset
from transformers.trainer_utils import get_last_checkpoint
import sys
from transformers import EarlyStoppingCallback

# ---------------------- Configuración ----------------------
VIDEO_DIR = r"C:\Users\Eduard_PC\OneDrive\Escritorio\VIDEOS\VIDEOS\COLOR_BODY"
MODEL_NAME = "google/vivit-b-16x2-kinetics400"
NUM_FRAMES = 32
IMG_SIZE = (224, 224)
EPOCHS = 15
BATCH_SIZE = 2
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.2
SEED = 42

device = "cuda" if torch.cuda.is_available() else "cpu"

# ---------------------- Dataset ----------------------------
dataset = VideoDataset(root_dir=VIDEO_DIR, num_frames=NUM_FRAMES, size=IMG_SIZE, augment=True)

total_len = len(dataset)
train_len = int(TRAIN_SPLIT * total_len)
val_len = int(VAL_SPLIT * total_len)
test_len = total_len - train_len - val_len

train_ds, val_ds, test_ds = random_split(
    dataset, [train_len, val_len, test_len], generator=torch.Generator().manual_seed(SEED)
)

# ---------------------- DataLoaders ------------------------
train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, pin_memory=True)
val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, pin_memory=True)

# ---------------------- Modelo y procesador ----------------
processor = VivitImageProcessor.from_pretrained(MODEL_NAME)
processor.num_frames = NUM_FRAMES

config = AutoConfig.from_pretrained(MODEL_NAME)
config.num_labels = len(dataset.label_map)

model = AutoModelForVideoClassification.from_pretrained(
    MODEL_NAME,
    config=config,
    ignore_mismatched_sizes=True,
).to(device)

# ✅ Descongelar solo las dos últimas capas del encoder y el clasificador
for name, param in model.named_parameters():
    if any(k in name for k in ["vivit.encoder.layer.10", "vivit.encoder.layer.11", "classifier"]):
        param.requires_grad = True
    else:
        param.requires_grad = False

# ---------------------- Collate Function -------------------
def collate_fn(batch):
    videos, labels = zip(*batch)
    processed_videos = []
    for video in videos:
        frames = [video[i] for i in range(video.shape[0])]
        processed_videos.append(frames)

    inputs = processor(
        processed_videos,
        return_tensors="pt",
        do_rescale=True,
        size={"height": 224, "width": 224}
    )
    inputs["labels"] = torch.tensor(labels)
    return inputs

# ---------------------- Training Setup ---------------------
args = TrainingArguments(
    output_dir="./vivit_sign_checkpoints",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    learning_rate=3e-4,
    weight_decay=0.05,
    logging_dir="./logs",
    report_to=["tensorboard"],  # 👈 Habilita logs de TensorBoard
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
     greater_is_better=True,  # 👈 esta es la que te faltaba
    fp16=False,
)

from evaluate import load
accuracy_metric = load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(-1)
    return accuracy_metric.compute(predictions=preds, references=labels)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    data_collator=collate_fn,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)


# ---------------------- Entrenamiento ----------------------


if __name__ == "__main__":
    torch.cuda.empty_cache()
    checkpoint = get_last_checkpoint("./vivit_sign_checkpoints")
    print("Último checkpoint encontrado:", checkpoint)

    trainer.train(resume_from_checkpoint=checkpoint)  # ✅ reanuda bien sin argumentos extra
    trainer.evaluate()
    trainer.save_model("./vivit_sign_final")
    processor.save_pretrained("./vivit_sign_final")
    sys.exit(0)
