import torch
import sys
from transformers.trainer_utils import get_last_checkpoint
from dataset import load_datasets
from model import load_model
from collate import build_collate_fn
from train_utils import get_training_args, build_trainer
from config import IMG_SIZE, CHECKPOINT_DIR, FINAL_MODEL_DIR

if __name__ == "__main__":
    train_ds, val_ds, test_ds, label_map = load_datasets()
    model, processor = load_model(num_labels=len(label_map))

    collate_fn = build_collate_fn(processor, IMG_SIZE)
    args = get_training_args()
    trainer = build_trainer(model, args, train_ds, val_ds, collate_fn)

    torch.cuda.empty_cache()
    checkpoint = get_last_checkpoint(CHECKPOINT_DIR)
    print("Último checkpoint encontrado:", checkpoint)

    trainer.train(resume_from_checkpoint=checkpoint)
    trainer.evaluate()
    trainer.save_model(FINAL_MODEL_DIR)
    processor.save_pretrained(FINAL_MODEL_DIR)
    sys.exit(0)