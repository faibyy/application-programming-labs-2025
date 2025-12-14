import argparse
import sys
from csv import reader, writer
from datetime import datetime
from pathlib import Path
from typing import Iterable

from crawler import PathIterator, download_images


def parse_range(s: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Преобразует строку дат в кортеж."""
    a, b = s.split(":")
    mindate = datetime.strptime(a, "%Y-%m-%d").date()
    maxdate = datetime.strptime(b, "%Y-%m-%d").date()
    if mindate > maxdate:
        mindate, maxdate = maxdate, mindate
    return (mindate.year, mindate.month, mindate.day), (maxdate.year, maxdate.month, maxdate.day)


def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Скачать изображения по диапазонам дат и создать CSV-аннотацию."
    )
    parser.add_argument(
        "--keyword",
        default="bear",
        help='Ключевое слово для поиска (по умолчанию "bear").',
    )
    parser.add_argument(
        "--out-dir", required=True, help="Папка для сохранения результатов."
    )
    parser.add_argument("--csv", required=True, help="Путь к итоговому CSV (abs;rel).")
    parser.add_argument(
        "--range",
        dest="ranges",
        action="append",
        type=parse_range,
        required=True,
        help="Диапазон(ы) дат YYYY-MM-DD:YYYY-MM-DD",
    )
    parser.add_argument(
        "--per-range",
        type=int,
        required=True,
        help="Количество изображений на диапазон",
    )
    return parser.parse_args()


def check_range(per_range: int) -> None:
    """Проверяет количество изображений на диапазон."""
    if not (50 <= per_range <= 1000):
        raise ValueError("Ошибка: --per-range должен быть в диапазоне [50, 1000].")


def main() -> None:
    try:
        args = parse_args()
        check_range(args.per_range)
        download_images(args)
        source_for_iter = args.csv if Path(args.csv).exists() else args.out_dir
        pathIterator = PathIterator(source_for_iter, root=args.out_dir)
        for path in pathIterator:
            print(path)
        
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
