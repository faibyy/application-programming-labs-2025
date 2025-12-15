import argparse

from overlay import overlay
from io_utils import read_image, save_image
from plotting import print_sizes, display_images

def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Наложение одного изображения на другое.",
    )
    parser.add_argument(
        "img1",
        type=str,
        help="Путь к нижнему изображению",
    )
    parser.add_argument(
        "img2",
        type=str,
        help="Путь к верхнему изображению",
    )
    parser.add_argument(
        "out",
        type=str,
        help="Путь для сохранения результата",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.5,
        help="Прозрачность верхнего изображения, по умолчанию 0.5",
    )
    return parser.parse_args()

def main() -> None:
    """Основная логика программы."""
    args = parse_args()
    try:
        img1 = read_image(args.img1)
        img2 = read_image(args.img2)
        print_sizes(img1, img2)

        result = overlay(img1, img2, alpha=args.alpha)

        display_images(img1, img2, result)
        save_image(args.out, result)
        print(f"Результат: {args.out}")
    except ValueError as exc:
        print(f"[Неверные параметры] {exc}")
    except Exception as exc: 
        print(f"[Ошибка] {exc}")


if __name__ == "__main__":
    main()