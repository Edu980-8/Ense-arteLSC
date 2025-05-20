import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset
import random

class VideoDataset(Dataset):
    def __init__(self, root_dir, num_frames=16, size=(224, 224), augment=True):
        self.samples = []
        self.labels = []
        self.label_map = {}
        self.num_frames = num_frames
        self.size = size
        self.augment = augment

        for archivo in sorted(os.listdir(root_dir)):
            if archivo.endswith(".mp4"):
                clase_id = archivo.split("_")[0]
                if clase_id not in self.label_map:
                    self.label_map[clase_id] = len(self.label_map)
                label = self.label_map[clase_id]
                self.samples.append(os.path.join(root_dir, archivo))
                self.labels.append(label)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        for offset in range(len(self.samples)):
            try:
                video_path = self.samples[(idx + offset) % len(self.samples)]
                label = self.labels[(idx + offset) % len(self.samples)]
                frames = self._load_video(video_path)
                return frames, label
            except Exception as e:
                print(f"⚠️ Skipping video {video_path}: {e}")
        raise RuntimeError("❌ No se pudo cargar ningún video válido.")

    def _load_video(self, path):
        cap = cv2.VideoCapture(path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total < self.num_frames:
            raise ValueError(f"{path} has only {total} frames")

        interval = total // self.num_frames
        frames = []

        for i in range(0, total, interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            frame = cv2.resize(frame, self.size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if frame.shape != (self.size[1], self.size[0], 3):
                print(f"❌ Frame con forma inválida en {path}: {frame.shape}")
                continue

            frames.append(frame.astype(np.uint8))
            if len(frames) == self.num_frames:
                break

        cap.release()

        if len(frames) < self.num_frames:
            raise ValueError(f"{path} tiene solo {len(frames)} frames válidos")

        output = np.stack(frames, axis=0)  # (T, H, W, C)

        if output.shape != (self.num_frames, self.size[1], self.size[0], 3):
            print(f"🛑 Video mal formado antes de retornar: {output.shape} en {path}")
            raise ValueError(f"⚠️ Video corrupto: {output.shape} en {path}")

        # Aplicar augmentación si está habilitada
        if self.augment:
            output = self._augment_video(output)

        return output

    def _augment_video(self, frames):
        """Aplica augmentaciones simples de video frame por frame."""
        augmented = []

        for frame in frames:
            # Flip horizontal aleatorio
            if random.random() < 0.5:
                frame = cv2.flip(frame, 1)

            # Rotación aleatoria
            if random.random() < 0.3:
                angle = random.uniform(-10, 10)
                M = cv2.getRotationMatrix2D((frame.shape[1]//2, frame.shape[0]//2), angle, 1.0)
                frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

            # Brillo aleatorio
            if random.random() < 0.3:
                factor = random.uniform(0.7, 1.3)
                frame = np.clip(frame * factor, 0, 255).astype(np.uint8)

            augmented.append(frame)

        return np.stack(augmented, axis=0)
