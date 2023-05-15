from __future__ import annotations
import os
from clip_query import ClipQuery
import pandas as pd
from umap import UMAP


def dir_exists(path: str) -> bool:
    return os.path.isdir(path)


def is_image(file_path: str, images_file_ext=[".png", ".jpg", ".jpeg"]):
    return any(file_path.lower().endswith(ext) for ext in images_file_ext)


def image_files_iter(dir_path: str, limit=None):
    count = 0
    for root, _, files in os.walk(dir_path):
        for file in files:
            if limit and count >= limit:
                return
            if is_image(file):
                count += 1
                yield os.path.join(root, file)


class Telepathy:
    def __init__(self):
        self.clip = ClipQuery()
        self.umap = UMAP()

    def encode_images(self, image_dir: str, limit=None, cache=True):
        assert dir_exists(image_dir)
        image_paths = list(image_files_iter(image_dir, limit))
        encodings = self.clip.encode_images(image_paths)
        return encodings

    def __call__(self, text: str, image_encodings: list[list[float]]):
        scores = self.clip.query(image_encodings, text)
        image_encodings_2D = self.umap.fit_transform(image_encodings, y=self.scores)
        return image_encodings_2D, scores


if __name__ == "__main__":
    print("telepathy!")
