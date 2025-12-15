from pathlib import Path
from typing import Literal
from PIL import Image

import numpy as np
import pandas as pd

Orientation = Literal["Horizontal", "Vertical", "Square"]

def add_orientation_column(
    df: pd.DataFrame,
    abs_col: str = "absolute_path",
    new_col: str = "orientation",
) -> pd.DataFrame:
    """Добавление колонки с ориентациями изображений"""
    df_new = df.copy()
    values: list[Orientation | None] = []

    for p in df_new[abs_col]:
        path = Path(str(p))

        try:
            with Image.open(path) as img:
                img = img.convert("RGB")
                arr = np.array(img)
        except Exception as e:
            print("Не удалось открыть файл:", path, "| ошибка:", e)
            values.append(None)
            continue

        h, w = arr.shape[:2]

        if h > w:
            values.append("Vertical")
        elif h < w:
            values.append("Horizontal")
        else:
            values.append("Square")

    df_new[new_col] = values
    return df_new

def filter_by_orientation(
    df: pd.DataFrame, orientation: Orientation, orientation_col: str = "orientation"
) -> pd.DataFrame:
    """Фильтр по ориентации."""
    return df[df[orientation_col] == orientation].copy()

def sort_by(df: pd.DataFrame, col: str = "orientation") -> pd.DataFrame:
    """Сортировка по ориентации."""
    return df.sort_values(by=col)


