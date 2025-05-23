import os
import time
import torch
import optuna
from optuna.pruners import HyperbandPruner

from dataset import load_datasets
from model import load_model
from collate import build_collate_fn
from train_utils import build_trainer
from config import IMG_SIZE

def objective(trial):
    # Detectar si hay GPU
    use_cuda = torch.cuda.is_available()
    print("🖥️ GPU disponible:", use_cuda)

    # Sugerimos hiperparámetros
    learning_rate = trial.suggest_float("learning_rate", 1e-5, 5e-4, log=True)
    batch_size = trial.suggest_categorical("batch_size", [4, 8])
    num_epochs = trial.suggest_int("num_train_epochs", 3, 10)
    weight_decay = trial.suggest_float("weight_decay", 0.0, 0.3)

    # Cargar datos
    train_ds, val_ds, _, label_map = load_datasets()
    model, processor = load_model(num_labels=len(label_map), freeze_backbone=True)
    collate_fn = build_collate_fn(processor, IMG_SIZE)

    # Ruta específica para el trial
    output_dir = f"./optuna_checkpoints/trial_{trial.number}"

    args = get_training_args(
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        num_train_epochs=num_epochs,
        weight_decay=weight_decay,
        output_dir=output_dir
    )

    # Construir trainer con control de pin_memory (en collate_fn ya está integrado)
    trainer = build_trainer(model, args, train_ds, val_ds, collate_fn)

    print(f"🚀 Trial {trial.number} - lr={learning_rate:.5f}, batch={batch_size}, epochs={num_epochs}, wd={weight_decay:.3f}")
    start = time.time()

    trainer.train()
    metrics = trainer.evaluate()

    end = time.time()
    print(f"✅ Trial {trial.number} done in {round(end - start, 2)}s → accuracy={metrics.get('eval_accuracy', 0):.4f}")
    print(f"📁 Checkpoints saved at: {output_dir}")

    return metrics.get("eval_accuracy", 0)


# TrainingArguments con parámetros dinámicos
from transformers import TrainingArguments

def get_training_args(
    learning_rate=3e-4,
    per_device_train_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.05,
    output_dir="./optuna_checkpoints"
):
    return TrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",  # como prefieres
        save_strategy="epoch",
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_train_batch_size,
        num_train_epochs=num_train_epochs,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        logging_dir=os.path.join(output_dir, "logs"),
        report_to=["none"],
        disable_tqdm=True,
        metric_for_best_model="accuracy",
        load_best_model_at_end=True,
        overwrite_output_dir=True,
        dataloader_pin_memory=torch.cuda.is_available(),  # ✅ evita warning
    )

if __name__ == "__main__":
    study = optuna.create_study(
        direction="maximize",
        pruner=HyperbandPruner(),
        study_name="vivit_hyperparam_search",
        storage="sqlite:///vivit_optuna.db",
        load_if_exists=True
    )

    study.optimize(objective, n_trials=20)

    print("🏆 Best trial:")
    print(study.best_trial.params)
