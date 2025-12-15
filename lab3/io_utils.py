from pathlib import Path
from typing import Tuple

import cv2
import numpy as np



def read_image(path: str | Path) -> np.ndarray:
    """Чтение изображение из файла как ndarray."""
    p = Path(path)
    if not p.is_file() or not p.exists():
        raise Exception(f"Файл не найден: {p}")
    img = cv2.imread(str(p), cv2.IMREAD_COLOR)
    if img is None:
        raise Exception(f"Пустое изображение: {p}")
    return img


def save_image(path: str | Path, image: np.ndarray) -> None:
    """Сохранение изображения."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(p), image):
        raise IOError(f"Не удалось сохранить изображение: {p}")


def image_size(image: np.ndarray) -> Tuple[int, int]:
    """Размеры изображения."""
    h, w = image.shape[:2]
    return w, h