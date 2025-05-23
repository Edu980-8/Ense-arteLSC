import torch
from torch.utils.data import random_split
from VideoPreprocessing import VideoDataset
from config import VIDEO_DIR, NUM_FRAMES, IMG_SIZE, TRAIN_SPLIT, VAL_SPLIT, SEED

def load_datasets():
    dataset = VideoDataset(root_dir=VIDEO_DIR, num_frames=NUM_FRAMES, size=IMG_SIZE, augment=True)
    total_len = len(dataset)
    train_len = int(TRAIN_SPLIT * total_len)
    val_len = int(VAL_SPLIT * total_len)
    test_len = total_len - train_len - val_len

    train_ds, val_ds, test_ds = random_split(
        dataset, [train_len, val_len, test_len], generator=torch.Generator().manual_seed(SEED)
    )
    return train_ds, val_ds, test_ds, dataset.label_map
