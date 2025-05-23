# VideoPreprocessing.py

import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset

class VideoDataset(Dataset):
    def __init__(self, root_dir, num_frames=8, size=(224, 224), augment=False):
        self.samples = []
        self.labels = []
        self.label_map = {}
        self.num_frames = num_frames
        self.size = size
        self.augment = augment

        for filename in sorted(os.listdir(root_dir)):
            if filename.endswith(".mp4"):
                label = filename.split("_")[0]
                if label not in self.label_map:
                    self.label_map[label] = len(self.label_map)
                full_path = os.path.join(root_dir, filename)
                self.samples.append(full_path)
                self.labels.append(self.label_map[label])

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        video_path = self.samples[idx]
        label = self.labels[idx]
        frames = self._load_video(video_path)
        return frames, label

    def _load_video(self, path):
        cap = cv2.VideoCapture(path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_idxs = np.linspace(0, total_frames - 1, self.num_frames, dtype=np.int32)

        frames = []
        for i in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            if i in frame_idxs:
                frame = cv2.resize(frame, self.size)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)

        cap.release()

        if len(frames) < self.num_frames:
            last_frame = frames[-1] if frames else np.zeros((*self.size, 3), dtype=np.uint8)
            while len(frames) < self.num_frames:
                frames.append(last_frame)

        frames_np = np.stack(frames)  # (T, H, W, C)
        frames_tensor = torch.from_numpy(frames_np).permute(0, 3, 1, 2)  # (T, C, H, W)

        return frames_tensor
