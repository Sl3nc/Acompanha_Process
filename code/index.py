from PySide6.QtWidgets import QMainWindow, QApplication
from tkinter.filedialog import askopenfilename
from window import Ui_MainWindow
import pyautogui as pg
import sys

class Arquivo:
    def __init__(self) -> None:
        pass

    def inserir(self):
        caminho = askopenfilename()

    def alterar(self):
        self.caminho
        ...

class Browser:
    def __init__(self) -> None:
        pass

    def abrir(self):
        ...

    def pesquisa(self):
        ...

    def inserir(dado:str):
        ...
    
    def infos(self):
        ...

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

    def loading(self):
        ...

    def buscar(self):
        ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()