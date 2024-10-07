from PySide6.QtWidgets import QMainWindow, QApplication
from window import Ui_MainWindow
import pyautogui as pg
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()