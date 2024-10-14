from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize
from tkinter.filedialog import askopenfilename
from src.window import Ui_MainWindow
from pathlib import Path
from time import sleep

import sys
import os
from abc import abstractmethod, ABCMeta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def resource_path(relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

class Arquivo:
    def __init__(self) -> None:
        pass

    def inserir(self):
        caminho = askopenfilename()

    def alterar(self):
        self.caminho
        ...

# Chrome Options
# https://peter.sh/experiments/chromium-command-line-switches/

class Browser:
    ROOT_FOLDER = Path(__file__).parent
    CHROME_DRIVER_PATH = ROOT_FOLDER / 'drivers' / 'chromedriver.exe'

    def __init__(self, options = '') -> None:
        self.browser = self.make_chrome_browser(*options)
        pass

    def make_chrome_browser(self,*options: str) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument('--headless')
        if options is not None:
            for option in options:
                chrome_options.add_argument(option)

        chrome_service = Service(
            executable_path=str(self.CHROME_DRIVER_PATH),
        )

        browser = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options
        )

        return browser

class Tribunal:
    TIME_TO_WAIT = 10
    __metaclass__ = ABCMeta

    def __init__(self, link, option = '') -> None:
        self.browser = Browser(option)
        self.browser.get(link)
        pass

    @abstractmethod
    def exec(self, num_processo):
        raise NotImplementedError("Implemente este método")
    
class EPROC(Tribunal):
    def __init__(self) -> None:
        super().__init__('https://eproc1g.trf6.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica')
        pass
    
    def exec(self):
        ...

class PJE(Tribunal):
    CLASS_ELEMENTS = 'col-sm-12'

    def __init__(self) -> None:
        super().__init__('https://pje-consulta-publica.tjmg.jus.br/')
        pass

    def exec(self, num_processo):
        self.browser.find_element(By.NAME, 
            'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso').send_keys(num_processo)


        self.browser.find_element(By.NAME, 'fPP:searchProcessos').click()

        sleep(self.TIME_TO_WAIT)

        self.browser.find_element(By.CSS_SELECTOR,'#fPP\\:processosTable\\:632256959\\:j_id245 > a').click()

class Juiz:
    def __init__(self) -> None:
        self.processos = {}

        self.ref = {
            'pje': PJE(),
        }
        pass

    def add_processo(self, num:str, nome:str):
        self.processos[num, self.__apurar(nome)]

    def __apurar(self, nome:str):
        for key, value in self.ref.items():
            if nome == key:
                return value 
        raise Exception('Processo de tribunal não identificado')
    
    def pesquisar(self):
        for num, tribunal in self.processos.items():
            tribunal.exec(num)           

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.logo.setPixmap(QPixmap(resource_path("src\\imgs\\procc-icon.ico")))
        icon = QIcon()
        icon.addFile(resource_path("src\\imgs\\upload-icon.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon)


    def loading(self):
        ...

    def buscar(self):
        ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()