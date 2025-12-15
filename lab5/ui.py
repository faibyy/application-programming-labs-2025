
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    """Описание интерфейса главного окна."""

    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 700)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralWidget")

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 25, 800, 600))
        self.graphicsView.setObjectName("graphicsView")

        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(850, 125, 100, 35))
        self.nextButton.setObjectName("nextButton")

        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(850, 50, 100, 35))
        self.openButton.setObjectName("openButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 650, 900, 20))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Просмотр датасета"))
        self.nextButton.setText(_translate("MainWindow", "Следущее"))
        self.openButton.setText(_translate("MainWindow", "Открыть"))
        self.label.setText(_translate("MainWindow", "Имя файла:"))
