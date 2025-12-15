import cv2
import numpy as np


def resize(bottom: np.ndarray, top: np.ndarray) -> np.ndarray:
    """Меняет размер top на размер bottom."""
    height, width = bottom.shape[:2]
    return cv2.resize(top, (width, height), interpolation=cv2.INTER_LINEAR)


def overlay(bottom: np.ndarray, top: np.ndarray, alpha: float,
) -> np.ndarray:
    """Наложение top на bottom с прозрачностю alpha."""
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("alpha должен быть в диапазоне[0, 1].")

    if bottom.shape[:2] != top.shape[:2]:
        top = resize(bottom, top)

    return cv2.addWeighted(bottom, 1.0 - alpha, top, alpha, 0.0)