import torch
from PIL import Image

def build_collate_fn(processor, img_size):
    def collate_fn(batch):
        videos, labels = zip(*batch)
        processed_videos = []
        for video in videos:
            if isinstance(video, torch.Tensor):
                video = video.permute(0, 2, 3, 1).numpy()
            frames = [Image.fromarray(frame.astype("uint8")) for frame in video]
            processed_videos.append(frames)

        inputs = processor(
            processed_videos,
            return_tensors="pt",
            do_rescale=True,
            size={"height": img_size[0], "width": img_size[1]}
        )
        inputs["labels"] = torch.tensor(labels)
        return inputs

    return collate_fn