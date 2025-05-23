from transformers import TrainingArguments, Trainer, EarlyStoppingCallback
from config import EPOCHS, BATCH_SIZE, CHECKPOINT_DIR
from metrics import compute_metrics

def get_training_args(
    learning_rate=3e-4,
    weight_decay=0.05,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
):
    return TrainingArguments(
        output_dir=CHECKPOINT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        num_train_epochs=num_train_epochs,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        logging_dir="./logs",
        report_to=["tensorboard"],
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        gradient_accumulation_steps=8,
        fp16=False,
    )

def build_trainer(model, args, train_ds, val_ds, collate_fn):
    return Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=collate_fn,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
