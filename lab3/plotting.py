import cv2
import matplotlib.pyplot as plt
import numpy as np

from io_utils import image_size


def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    """Преобразование BGR (стандарт openCV) в RGB."""
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def print_sizes(img1: np.ndarray, img2: np.ndarray) -> None:
    """Печать размеров двух изображений."""
    w1, h1 = image_size(img1)
    w2, h2 = image_size(img2)
    print(f"Image1: width={w1}, height={h1}")
    print(f"Image2: width={w2}, height={h2}")


def display_images(
    img1_bgr: np.ndarray,
    img2_bgr: np.ndarray,
    result_bgr: np.ndarray,
) -> None:
    """Вывод исходных изображений и результата."""
    images = [bgr_to_rgb(img1_bgr),bgr_to_rgb(img2_bgr),bgr_to_rgb(result_bgr)]
    titles = ["Image 1 (bottom)","Image 2 (top)","Result (overlayed images)"]
    fig, axs = plt.subplots(1, len(images), figsize=(12, 4))
    for i in range (3):
        ax = axs[i]
        ax.imshow(images[i])
        ax.set_title(titles[i])
        ax.axis('off') 
    plt.tight_layout()
    plt.show()