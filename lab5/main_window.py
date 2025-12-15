import os
import sys
from pathlib import Path
from typing import Optional

import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from crawler import PathIterator
from ui import Ui_MainWindow


os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
    os.path.dirname(PyQt5.__file__),
    "Qt",
    "plugins",
    "platforms",
)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Главное окно приложения. Выбор папки с изображением/файла аннотации; просмотр изображений; изменение их размеров
    """

    def __init__(self, parent: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.iterator: Optional[PathIterator] = None

        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        self.nextButton.clicked.connect(self.next_image)
        self.openButton.clicked.connect(self.open_source) 


    def open_source(self) -> None:
        """
        Открывает папку с изображениями
        """
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите CSV-файл или любое изображение из папки датасета",
        )

        if not path_str:
            return

        p = Path(path_str)

        if p.is_file() and p.suffix.lower() == ".csv":
            source = str(p) 
        else:
            source = str(p.parent) 

        try:
            self.iterator = PathIterator(source)
            self.iterator = iter(self.iterator)
            self.label.setText(f"Источник: {source}")
            self.next_image()
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать итератор:\n{exc}")
            self.iterator = None

    def next_image(self) -> None:
        """
        Отображает следующее изображение из итератора
        с сохранением пропорций.
        """
        if self.iterator is None:
            QMessageBox.information(
                self,
                "Нет данных",
                "Сначала откройте CSV-файл или папку датасета.",
            )
            return

        try:
            abs_path, rel_path = next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.iterator)
            abs_path, rel_path = next(self.iterator)
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка итератора:\n{exc}")
            return

        pixmap = QPixmap(abs_path)
        if pixmap.isNull():
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не удалось открыть изображение:\n{abs_path}",
            )
            return

        target_size = self.graphicsView.viewport().size()
        scaled = pixmap.scaled(
            target_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(scaled))

        self.label.setText(f"Файл: {abs_path}")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
