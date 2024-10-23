from pathlib import Path
from time import sleep
from PIL import Image

import os
import sys
import string
import traceback
from unidecode import unidecode
from abc import abstractmethod, ABCMeta

import pandas as pd
from openpyxl import load_workbook

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout,QPushButton, QLineEdit
)
from PySide6.QtGui import QPixmap, QIcon, QMovie
from PySide6.QtCore import QThread, QObject, Signal, QSize
from src.window_process import Ui_MainWindow

from tkinter import messagebox
from tkinter.filedialog import askopenfilename

def resource_path(relative_path: str):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Arquivo:
    def __init__(self) -> None:
        self.tipos_validos = 'lsx'
        self.caminho = ''
        self.COL_TEXT = 2
        self.COL_NUM = 1
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

    def __formato_ascii(self, caminho) -> str:
        caminho_uni = unidecode(caminho)
        os.renames(caminho, caminho_uni)
        return caminho_uni
    
    def envio_invalido(self) -> bool:
        return True if len(self.caminho) == 0 else False

    def ler(self) -> list:
        return pd.read_excel(self.caminho, usecols='A', header=None)[0]\
            .values.tolist()

    def alterar(self, conteudo: dict) -> None:
        wb = load_workbook(self.caminho)
        ws = wb.active
        for index, lista_movimentos in enumerate(conteudo.values(), 1):
            valor_novo = ''
            for movimento in lista_movimentos:
                if movimento not in ws.cell(index, self.COL_NUM).value:
                    valor_novo = f'{valor_novo} §#§ {movimento}'

            if ws.cell(index, self.COL_TEXT).value == None:
                ws.cell(index, self.COL_TEXT, '')
            ws.cell(index, self.COL_TEXT).value = \
                ws.cell(index, self.COL_TEXT).value + valor_novo

        wb.save(self.caminho)

    def abrir(self) -> None:
        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        os.startfile(self.caminho)

class Browser:
    ROOT_FOLDER = Path(__file__).parent
    CHROME_DRIVER_PATH = ROOT_FOLDER / 'src' / 'drivers' / 'chromedriver.exe'

    def __init__(self, options = (), hide = True) -> webdriver.Chrome:
        if hide == True:
            self.browser.set_window_position(-10000,0)
            
        return self.make_chrome_browser(*options)

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
    TIME_TO_WAIT = 1
    __metaclass__ = ABCMeta

    def __init__(self, browser) -> None:
        self.valor_captcha = ''
        self.browser = browser
        pass

    @abstractmethod
    def executar(self, num_processo):
        raise NotImplementedError("Implemente este método")
    
    def set_captcha(self, valor):
        self.valor_captcha = valor

class EPROC(Tribunal):
    LINK_BASE = 'https://eproc1g.trf6.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica'
    INPUT = 'txtNumProcesso'
    CAPTCHA = 'txtInfraCaptcha'
    CONTULTAR = 'sbmNovo'
    TABLE_CONTENT = '#divInfraAreaProcesso > table > tbody'
    TIME_TO_WAIT = 1
    WAIT_CAPTCHA = 2
    FRAME_PRINT = [300, 430, 430, 480]
    NOME_IMG = 'image.png'

    def __init__(self, browser) -> None:
        super().__init__(browser)
        pass

    def executar(self, num_process: str):
        self.inserir_valor(num_process)
        while self.tentar_consulta() == False:
            self.valor_captcha = ''
            img = self.imagem_captcha()
            self.valor.emit(img)
            while self.valor_captcha == '':
                sleep(self.WAIT_CAPTCHA)
            self.preencher_captcha(self.valor_captcha)
            
        os.remove(img)
        return self.conteudo()
    
    def inserir_valor(self, num_process) -> None:
        self.browser.get(self.LINK_BASE)
        self.browser.find_element(By.ID, self.INPUT).send_keys(num_process)

    def tentar_consulta(self) -> bool:
        self.browser.find_element(By.ID, self.CONTULTAR).click()
        try:
            #Se dar erro é porque não tem o captcha, senão o contrário
            alert = WebDriverWait(self.browser, self.TIME_TO_WAIT)\
                .until(EC.alert_is_present())
            alert.accept() 
            self.browser.find_element(By.ID, self.CAPTCHA)
        except:
            return True
        return False
        
    def imagem_captcha(self):
        self.browser.save_screenshot(self.NOME_IMG)
        Image.open(self.NOME_IMG).crop([300, 430, 430, 480]).save(self.NOME_IMG)
        return self.NOME_IMG

    def preencher_captcha(self, valor):
        self.browser.find_element(By.ID, 'txtInfraCaptcha').send_keys(valor)

    def conteudo(self):
        tbody = self.browser.find_element(By.CSS_SELECTOR, self.TABLE_CONTENT)
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        rows.pop(0)
        return rows

class PJE(Tribunal):
    CLASS_ELEMENTS = 'col-sm-12'
    TIME_TO_WAIT = 300
    INPUT = 'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso'
    BTN_PESQUISAR = 'fPP:searchProcessos'
    JANELA_PROCESSO = '#fPP\\:processosTable\\:632256959\\:j_id245 > a'
    TABELA_CONTEUDO = 'j_id134:processoEvento'
    LINK_BASE = 'https://pje-consulta-publica.tjmg.jus.br/'
    LINK_JANELA = 'https://pje-consulta-publica.tjmg.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca'

    def __init__(self, browser) -> None:
        super().__init__(browser)
        pass

    def exec(self, num_processo):
        self.browser.get(self.LINK_BASE)

        self.browser.find_element(By.NAME, self.INPUT).send_keys(num_processo)

        self.browser.find_element(By.NAME, self.BTN_PESQUISAR).click()

        sleep(self.TIME_TO_WAIT)

        metodo_janela = self.browser.find_element(By.CSS_SELECTOR, self.JANELA_PROCESSO).get_attribute('onclick')

        link_janela = metodo_janela[metodo_janela.rfind('='):]

        return {num_processo: self.__valor_janela(link_janela)}

    def __valor_janela(self, endereco: str):
        self.browser.get(self.LINK_JANELA + endereco[:len(endereco)-2])

        sleep(self.TIME_TO_WAIT)

        tbody = self.browser.find_element(By.ID, self.TABELA_CONTEUDO)
        results = tbody.find_elements(By.TAG_NAME, 'span')
        for value in results:
            print(value.text)
        return results

class Juiz(QObject):
    valor = Signal(str)
    fim = Signal(dict)
    WAIT_CAPTCHA = 2

    def __init__(self, num_process: list[str]) -> None:
        super().__init__()
        self.num_process = num_process
        self.valor_janela = ''
        self.browser = Browser()
        self.ref = {
            '13': PJE(self.browser),
            '01': EPROC(self.browser)
        }

    def pesquisar(self) -> dict:
        ref = {}
        for num in self.num_processos:
            self.tribunal_atual = self.__apurar(str(num))
            if self.tribunal_atual == None:
                ref[num] = None
            else:
                ref[num] = self.tribunal_atual.exec(str(num))

        self.fim.emit(ref)
    
    def __apurar(self, num:str) -> Tribunal:
        for key, value in self.ref.items():
            if key == num.replace('-','').replace('.','')[14:16]:
                return value 
        return None

    def set_captcha(self, valor):
        self.tribunal_atual.set_captcha(valor)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.file = Arquivo()

        self.logo.setPixmap(QPixmap(resource_path('src\\imgs\\procc-icon.ico')))
        icon = QIcon()
        icon.addFile(resource_path("src\\imgs\\upload-icon.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon)
        self.movie = QMovie(resource_path("src\\imgs\\load.gif"))
        self.gif_load.setMovie(self.movie)

        self.pushButton_2.clicked.connect(
            lambda: self.file.inserir(self.pushButton_2)
        )
        self.pushButton.clicked.connect(self.hard_work)
        self.enviar_captcha.clicked.connect(self.enviar_resp)

    def hard_work(self):
        try:
            if self.file.envio_invalido():
                raise Exception('Favor anexar seu relatório de processos')
            
            self.exec_load(True)
            self.pushButton.setDisabled(True)

            self.juiz = Juiz(self.file.ler())
            self._thread = QThread()

            self.juiz.moveToThread(self._thread)
            self._thread.started.connect(self.juiz.executar)
            self.juiz.fim.connect(self._thread.quit)
            self.juiz.fim.connect(self._thread.deleteLater)
            self.juiz.fim.connect(self.encerramento)
            self._thread.finished.connect(self.juiz.deleteLater)
            self.juiz.valor.connect(self.progress) 

            self._thread.start()  
        except Exception as err:
            traceback.print_exc()
            messagebox.showerror('Aviso', err)

    def encerramento(self, result: dict):
        invalidos = self.filtra_invalido(result)
        if len(invalidos) != 0:
            for key in invalidos:
                result.pop(key)
                
            messagebox.showerror('Aviso', \
                f'Os tribunais dos seguintes processos ainda não foram implementados no programa: \n\n \
                    {'\n - '.join(str(x) for x in invalidos)}')

        self.file.alterar(result)
        self.file.abrir()

        self.exec_load(False, 0)
        self.pushButton.setDisabled(False)

    def filtra_invalido(self, result: dict):
        falhas = []
        for key, value in result.items():
            if value == None:
                falhas.append(key)
        return falhas
    
    def progress(self, nome_img):
        self.label_5.setPixmap(QPixmap(nome_img))
        self.exec_load(False, 2)

    def enviar_resp(self):
        self.juiz.set_captcha(self.lineEdit.text())
        self.exec_load(True)

    def exec_load(self, action: bool, to = 1):
        if action == True:
            self.movie.start()
            self.stackedWidget.setCurrentIndex(to)
        else:
            self.movie.stop()
            self.stackedWidget.setCurrentIndex(to)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()