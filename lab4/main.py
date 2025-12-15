import sys
import argparse

from io_utils import load_annotation_csv, save_dataframe
from processing import (add_orientation_column, sort_by, filter_by_orientation)
from visualization import plot_orientation_histogram


def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Обработка изображений и анализ ориентации."
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Путь к входному CSV файлу с аннотациями",
    )

    parser.add_argument(
        "--output",
        "-o",
        default="lab4_dataframe.csv",
        help="Путь к файлу для сохранения результата (CSV)",
    )

    parser.add_argument(
        "--hist",
        "-H",
        default="orientation_hist.png",
        help="Файл для сохранения гистограммы ориентаций",
    )

    return parser.parse_args()


def main() -> None:
    """Главная функция лабораторной работы."""
    args = parse_args()

    try:
        df = load_annotation_csv(args.input)

        df = add_orientation_column(df)

        df_sorted = sort_by(df)
        df_vertical = filter_by_orientation(df_sorted, "Vertical")

        print("Количество вертикальных изображений:", len(df_vertical))

        plot_orientation_histogram(df_sorted, output_path=args.hist)
        save_dataframe(df_sorted, args.output)

        print("Прогамма выполнена успешно")
    except Exception as e:
        print("Ошибка:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
