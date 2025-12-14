import argparse
import sys
from csv import reader, writer
from datetime import datetime
from pathlib import Path
from typing import Iterable

from icrawler.builtin import GoogleImageCrawler
EXTENSIONS = {".jpg", ".jpeg", ".png",}

def crawl_range(
    keyword: str,
    out_dir: Path,
    date_range: tuple[tuple[int, int, int], tuple[int, int, int]],
    max_num: int,
) -> None:
    """Скачивает изображения для одного диапазона дат в указанную папку."""
    out_dir.mkdir(parents=True, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": str(out_dir)})
    crawler.session.headers.update({
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
  }) #предотвращает ошибку TypeError: 'NoneType' object is not iterable в кравлере из-за блокировок
    crawler.crawl(keyword=keyword, filters={"date": date_range}, max_num=max_num)


def create_pairs(root: Path) -> list[list[str]]:
    """Создает пары путей к изображениям [abs, rel]."""
    pairs: list[list[str]] = []
    root = root.resolve()
    for fp in root.rglob("*"):
        if fp.is_file() and fp.suffix.lower() in EXTENSIONS:
            abs_path = fp.resolve()
            rel_path = abs_path.relative_to(root)
            pairs.append([str(abs_path), str(rel_path)])
    return pairs


def write_csv(csv_path: Path, pairs: Iterable[Iterable[str]]) -> None:
    """Записывает аннотацию в CSV-файл."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = writer(f, delimiter=";")
        header = ["absolute_path", "relative_path"]
        w.writerow(header)
        for row in pairs:
            if not hasattr(row, "__iter__"):
                raise TypeError(
                    f"Ошибка: элемент {row!r} не является итерируемым (не список/кортеж)."
                )
            if len(row) < 2:
                raise ValueError(
                    f"Ошибка: строка {row!r} должна содержать минимум 2 значения [abs, rel]."
                )
            abs_path = str(row[0])
            rel_path = str(row[1])
            w.writerow([abs_path, rel_path])


class PathIterator:
    """Итератор по изображениям из папки или CSV (возвращает [abs, rel])."""

    def __init__(self, source: str, root: str | None = None) -> None:
        self.items: list[list[str]] = []
        p = Path(source)
        if p.is_file() and p.suffix.lower() == ".csv":
            with p.open("r", encoding="utf-8", newline="") as f:
                r = reader(f, delimiter=";")
                first = True
                for row in r:
                    if (
                        first
                        and row
                        and len(row) >= 2
                        and row[0].strip().lower() == "absolute_path"
                        and row[1].strip().lower() == "relative_path"
                    ):
                        first = False
                        continue
                    first = False
                    if len(row) >= 2:
                        self.items.append([row[0], row[1]])
        elif p.is_dir():
            base = Path(root) if root else p
            base = base.resolve()
            for fp in p.rglob("*"):
                if fp.is_file() and fp.suffix.lower() in EXTENSIONS:
                    abs_path = fp.resolve()
                    rel_path = abs_path.relative_to(base)
                    self.items.append([str(abs_path), str(rel_path)])
        else:
            raise ValueError(
                f"source='{source}' должен быть .csv файлом или директорией"
            )
        self._index = 0

    def __iter__(self) -> "PathIterator":
        self._index = 0
        return self

    def __next__(self) -> list[str]:
        if self._index >= len(self.items):
            raise StopIteration
        val = self.items[self._index]
        self._index += 1
        return val


def download_images(args: argparse.Namespace) -> None:
    """Скачивает файлы по диапазонам и формирует CSV-аннотацию."""
    out_root = Path(args.out_dir)
    for idx, dr in enumerate(args.ranges):
        subdir = out_root / f"range_{idx+1}"
        crawl_range(args.keyword, subdir, dr, args.per_range)
    pairs = create_pairs(out_root)
    write_csv(Path(args.csv), pairs)

