from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize
from src.window import Ui_MainWindow
from pathlib import Path
from time import sleep
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import sys
import os
import string
from unidecode import unidecode
from abc import abstractmethod, ABCMeta

import pandas as pd
from openpyxl import load_workbook

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

def resource_path(relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

class Arquivo:
    def __init__(self) -> None:
        self.tipos_validos = 'lsx'
        self.caminho = ''
        self.COL_INDEX = 3
        self.COL_NUM = 2
        pass

    def inserir(self, button: QPushButton):
        try:
            caminho = askopenfilename()
            if caminho == '':
                return None
            self.caminho = self.__validar_entrada(caminho)
            button.setText(caminho[caminho.rfind('/') +1:])
            button.setIcon(QPixmap(''))

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
        except FileExistsError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

    def __validar_entrada(self, caminho):
        if any(c not in string.ascii_letters for c in caminho):
            caminho = self.__formato_ascii(caminho)

        self.__tipo(caminho)
        return caminho

    def __tipo(self, caminho):
        if caminho[len(caminho) -3 :] != self.tipos_validos:
            ultima_barra = caminho.rfind('/')
            raise Exception(
                f'Formato inválido do arquivo: {caminho[ultima_barra+1:]}')

    def __formato_ascii(self, caminho):
        caminho_uni = unidecode(caminho)
        os.renames(caminho, caminho_uni)
        return caminho_uni
    
    def envio_invalido(self):
        return True if len(self.caminho) == 0 else False

    def ler(self):
        ref = {}
        arq_DF = pd.read_excel(self.caminho, usecols='A:B', header=None)
        arq_dict = arq_DF.to_dict('index')
        for arq in arq_dict.values():
            ref[arq[1]] = arq[0]
        return ref

    def alterar(self, conteudo: dict):
        wb = load_workbook(self.caminho)
        ws = wb.active

        for index, numero, valor in enumerate(conteudo.items(), 1):
            if ws.cell(index, self.COL_NUM).value == numero:
                ws.cell(index, self.COL_INDEX, valor)

        wb.save(self.caminho)

    def abrir(self):
        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        os.startfile(self.caminho)

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

        return {num_processo : conteudo}

class Juiz:
    def __init__(self) -> None:
        self.ref = {
            'pje': PJE(),
            'eproc': EPROC()
        }
        pass

    def pesquisar(self, processos: dict):
        ref = {}
        for num, nome in processos.items():
            ref[num] = self.__apurar(nome)

        for num, tribunal in ref.items():
            tribunal.exec(num)  

    def __apurar(self, nome:str):
        for key, value in self.ref.items():
            if nome == key:
                return value 
        raise Exception('Processo de tribunal não identificado')
    
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.file = Arquivo()

        self.logo.setPixmap(QPixmap(resource_path("src\\imgs\\procc-icon.ico")))
        icon = QIcon()
        icon.addFile(resource_path("src\\imgs\\upload-icon.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon)

        self.pushButton_2.clicked.connect(
            lambda: self.file.inserir(self.pushButton_2))

    def buscar(self):
        if self.file.envio_invalido():
            return Exception('Favor anexar seu relatório de processos')

        juiz = Juiz()        
        processos = self.file.ler()
        for processo in processos:
            juiz.add_processo(processo['numero'], processo['tribunal'])
        result = juiz.pesquisar()
        self.file.alterar(result)
        self.file.abrir()

    def loading(self):
        ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()