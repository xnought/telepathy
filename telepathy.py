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

    def encode_images(self, image_dir: str, limit=None):
        assert dir_exists(image_dir)
        image_paths = list(image_files_iter(image_dir, limit))
        encodings = self.clip.encode_images(image_paths)
        return encodings

    def __call__(self, text: str, image_encodings: list[list[float]]):
        scores = self.clip.query(image_encodings, text)
        image_encodings_2D = self.umap.fit_transform(image_encodings, y=self.scores)
        return image_encodings_2D, scores


class TelepathyPandas:
    def __init__(self, image_dir: str = None, limit=None, index: pd.DataFrame = None):
        assert (
            image_dir or index
        ), "you must specify either an image directory or a dataframe with encodings and image paths"
        self.clip = ClipQuery()
        self.umap = UMAP()

        # if you have a custom dataframe with encodings and image paths, you can pass it in here
        if index:
            assert isinstance(index, pd.DataFrame)
            assert "image_path" in index.columns
            assert "encoding" in index.columns
            self.df = index
        else:
            # you may have specified a directory!
            # encode the images first by looking if its cached, otherwise encodings then cacheing them for the future
            assert dir_exists(image_dir)
            self.cache_filename = os.path.join(
                image_dir, f"telepathy_cache_limit_{limit}.parquet"
            )
            if os.path.exists(self.cache_filename):
                self.df = pd.read_parquet(self.cache_filename)
            else:
                self.df = pd.DataFrame(columns=["image_path", "encoding"])
                encodings, image_paths = self._encode_images(image_dir, limit)
                self.df["image_path"] = image_paths
                self.df["encoding"] = encodings
                self.df.to_parquet(self.cache_filename)

    def _encode_images(self, image_dir: str, limit=None):
        image_paths = list(image_files_iter(image_dir, limit))
        encodings = self.clip.encode_images(image_paths)
        return encodings, image_paths

    def __call__(self, text: str, in_place=False):
        image_encodings = self.df["encoding"].tolist()
        scores = self.clip.query(image_encodings, text)
        image_encodings_2D = self.umap.fit_transform(image_encodings, y=scores)

        if in_place:
            self.df["x"] = image_encodings_2D[:, 0]
            self.df["y"] = image_encodings_2D[:, 1]
            self.df["score"] = scores
            return self.df
        else:
            out_df = pd.DataFrame(columns=["image_path", "x", "y", "score"])
            out_df["image_path"] = self.df["image_path"]
            out_df["x"] = image_encodings_2D[:, 0]
            out_df["y"] = image_encodings_2D[:, 1]
            out_df["score"] = scores
            return out_df


if __name__ == "__main__":
    print("telepathy!")
