from pathlib import Path

import cv2
import numpy as np
from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def list_images(input_dir: Path) -> list[Path]:
    return sorted(f for f in input_dir.iterdir() if f.suffix.lower() in SUPPORTED)


def load_image_cv2(path: Path) -> np.ndarray:
    return cv2.imread(str(path), cv2.IMREAD_UNCHANGED)


def save_image_cv2(path: Path, img: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        cv2.imwrite(str(path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])
    elif ext == ".webp":
        cv2.imwrite(str(path), img, [cv2.IMWRITE_WEBP_QUALITY, 95])
    else:
        cv2.imwrite(str(path), img)


def save_image_pil(path: Path, img: Image.Image, fmt: str = "PNG") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(path), fmt)
