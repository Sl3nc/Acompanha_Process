from pathlib import Path
from time import sleep
from PIL import Image

import os
import sys
import string
import traceback
from unidecode import unidecode
from abc import abstractmethod, ABCMeta
from collections import OrderedDict

import pandas as pd
from pandas.errors import ParserError
from openpyxl import load_workbook
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
    NOME_SHEET = 'Deltaprice Judiciais'

    def __init__(self) -> None:
        self.tipos_validos = 'lsx'
        self.caminho = ''
        self.COL_TEXT = 12
        pass

    def inserir(self, button: QPushButton) -> None:
        try:
            self.caminho = askopenfilename()
            if self.caminho == '':
                return
            self.__validar_entrada()
            with open(self.caminho, 'r+'):
                ...
            button.setText(self.caminho[self.caminho.rfind('/') +1:])
            button.setIcon(QPixmap(''))

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
        except FileExistsError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

    def __validar_entrada(self) -> str:
        if self.caminho == '':
            return None
        self.__tipo()
        caminho_uni = unidecode(self.caminho)
        if self.caminho != caminho_uni:
            self.caminho = self.__renomear(caminho_uni)

    def __tipo(self) -> bool:
        if self.caminho[len(self.caminho) -3 :] != self.tipos_validos:
            ultima_barra = self.caminho.rfind('/')
            raise Exception(
                f'Formato inválido do arquivo: {self.caminho[ultima_barra+1:]}')
        return True

    def __renomear(self, caminho) -> str:
        os.renames(self.caminho, caminho)
        return caminho
    
    def envio_invalido(self) -> bool:
        return True if len(self.caminho) == 0 else False

    def ler(self) -> list:
        return pd.read_excel(self.caminho, usecols='E').dropna().values.tolist()

    def alterar(self, conteudo: OrderedDict) -> None:
        #TODO Alterar
        wb = load_workbook(self.caminho)
        ws = wb[self.NOME_SHEET]
        for index, lista_movimentos in enumerate(conteudo.values(), 2):
            #print(f'{index} - {lista_movimentos}')
            if lista_movimentos == ['']:
                continue

            if ws.cell(index, self.COL_TEXT).value == None:
                ws.cell(index, self.COL_TEXT, '')

            s = ' **'.join(str(movimento) for movimento in lista_movimentos\
                if movimento[:11] not in str(ws.cell(index, self.COL_TEXT).value))

            ws.cell(index, self.COL_TEXT).value = CellRichText(
                [TextBlock(InlineFont(b=True), s), ws.cell(index, self.COL_TEXT).value]
            )

        wb.save(self.caminho)
          
    def abrir(self) -> None:
        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        os.startfile(self.caminho)

class Browser:
    CHROME_DRIVER_PATH = resource_path('src\\drivers\\chromedriver.exe')

    def make_chrome_browser(self,*options: str, hide = True) -> webdriver.Chrome:
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

        if hide == True:
            browser.set_window_position(-10000,0)

        return browser

class Tribunal:
    TIME_TO_WAIT = 1
    WAIT_CAPTCHA = 2
    CAPTCHA = ''
    __metaclass__ = ABCMeta

    def __init__(self, browser) -> None:
        self.valor_captcha = ''
        self.browser = browser
        pass

    @abstractmethod
    def executar(self) -> list[str]:
        raise NotImplementedError("Implemente este método")
    
    @abstractmethod
    def acessar_processo(self, num: str) -> None:
        raise NotImplementedError("Implemente este método")
    
    @abstractmethod
    def conteudo(self):
        raise NotImplementedError("Implemente este método")
    
    def esperar_captcha(self):
        self.valor_captcha = ''
        while self.valor_captcha == '':
            sleep(self.WAIT_CAPTCHA)

    def preencher_captcha(self):
        self.browser.find_element(By.ID, self.CAPTCHA)\
            .send_keys(self.valor_captcha)
    
    def set_captcha(self, valor):
        self.valor_captcha = valor

class ECAC(Tribunal):
    LINK_BASE = 'https://comprot.fazenda.gov.br/comprotegov/site/index.html#ajax/processo-consulta.html'
    

class EPROC(Tribunal):
    LINK_BASE = 'https://eproc1g.trf6.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica'
    INPUT = 'txtNumProcesso'
    CONTULTAR = 'sbmNovo'
    TABLE_CONTENT = '#divInfraAreaProcesso > table > tbody'
    FRAME_PRINT = [300, 430, 430, 480]
    NOME_IMG = 'image.png'

    def __init__(self, browser) -> None:
        super().__init__(browser)
        self.CAPTCHA = 'txtInfraCaptcha'
        pass

    def executar(self):
        if self.tentar_consulta() == False:
            self.img = self.imagem_captcha()
            return self.img
        os.remove(self.img)
        return self.conteudo()
    
    def acessar_processo(self, num: str) -> None:
        self.browser.get(self.LINK_BASE)
        self.browser.find_element(By.ID, self.INPUT).send_keys(num)

    def tentar_consulta(self) -> bool:
        self.browser.find_element(By.ID, self.CONTULTAR).click()
        sleep(self.TIME_TO_WAIT)
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

    def conteudo(self):
        tbody = self.browser.find_element(By.CSS_SELECTOR, self.TABLE_CONTENT)
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        rows.pop(0)
        return [x.text[3:] for x in rows if x.text != '']

class PJE(Tribunal):
    CLASS_ELEMENTS = 'col-sm-12'
    INPUT = 'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso'
    BTN_PESQUISAR = 'fPP:searchProcessos'
    TABELA_PROCESSO = 'fPP:processosTable:tb'
    TABELA_CONTEUDO = 'j_id134:processoEvento'
    LINK_BASE = 'https://pje-consulta-publica.tjmg.jus.br/'
    LINK_JANELA = 'https://pje-consulta-publica.tjmg.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca'

    def __init__(self, browser) -> None:
        super().__init__(browser)
        pass

    def acessar_processo(self, num_process: str) -> None:
        self.browser.get(self.LINK_BASE)
        self.browser.find_element(By.NAME, self.INPUT).send_keys(num_process)

    def executar(self) -> list[str]:
        try:
            self.browser.find_element(By.NAME, self.BTN_PESQUISAR).click()
            sleep(self.TIME_TO_WAIT)
            botao_janela = self.browser.find_element(By.ID, self.TABELA_PROCESSO)
            metodo_janela = botao_janela.find_element(By.TAG_NAME, 'a')\
                .get_attribute('onclick')
            link_janela = metodo_janela[metodo_janela.rfind('='):]
            return self.conteudo(link_janela)
        except NoSuchElementException:
            return ['~']

    def conteudo(self, endereco: str) -> list[str]:
        self.browser.get(self.LINK_JANELA + endereco[:len(endereco)-2])
        tbody = self.browser.find_element(By.ID, self.TABELA_CONTEUDO)
        return [x.text for x in tbody.find_elements(By.TAG_NAME, 'span')\
                if x.text != '' and x.text[0].isnumeric()]

class TST(Tribunal):
    LINK_BASE = 'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do?consulta=Consultar&conscsjt=&numeroTst={0}&digitoTst={1}&anoTst={2}&orgaoTst={3}&tribunalTst={4}&varaTst={5}&submit=Consultar'

    TABLE_PROCESSOS = 'body > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(32) > td > table > tbody'

    def __init__(self, browser) -> None:
        super().__init__(browser)
        self.cortes_string = [7, 9, 13, 14, 16, 20]
        pass

    def acessar_processo(self, num_process: str) -> None:
        partes = []
        posic_passada = 0
        num_process = num_process.replace('.','').replace('-','')
        for posic in self.cortes_string:
            partes.append(num_process[posic_passada : posic])
            posic_passada = posic

        self.browser.get(self.LINK_BASE.format(
            partes[0],partes[1],partes[2],partes[3],partes[4],partes[5])
        )

    def executar(self):
        try:
            tabela = self.browser.find_element(By.CSS_SELECTOR, self.TABLE_PROCESSOS)
            linhas = tabela.find_elements(By.TAG_NAME, 'tr')
            return self.conteudo(linhas)
        except NoSuchElementException:
            return ['~']
        
    def conteudo(self, rows):
        return [x.text for x in rows[1:] if x.text != '']

class Juiz(QObject):
    valor = Signal(str)
    progress = Signal(int)
    fim = Signal(OrderedDict)
    WAIT_CAPTCHA = 2

    def __init__(self, num_process: list[str]) -> None:
        super().__init__()
        self.num_process = num_process
        self.valor_janela = ''
        self.browser = Browser().make_chrome_browser(hide=True)
        self.ref = {
            '13': PJE(self.browser),
            '01': EPROC(self.browser),
            '03': TST(self.browser)
        }

    def pesquisar(self):
        try:
            ref = OrderedDict(
                [(str(x[0])[:25], '') for x in self.num_process]
            )
            for index, num in enumerate(self.num_process, 1):
                num = str(num[0])[:25]
                if num == None:
                    num = ''
                self.processo(ref, num)
                self.progress.emit(index)

            self.browser.quit()
            self.fim.emit(ref)

        except Exception as err:
            traceback.print_exc()
            messagebox.showerror('Aviso', err)

    def processo(self, ref, num):
        self.tribunal_atual = self.__apurar(num)
        if self.tribunal_atual == None:
            ref[num] = ['']
        else:
            #TODO PESQUISA PROCESSO
            self.tribunal_atual.acessar_processo(num)
            resp = self.tribunal_atual.executar()
            while type(resp) == str:
                self.valor.emit(resp)
                self.tribunal_atual.esperar_captcha()
                self.tribunal_atual.preencher_captcha()
                resp = self.tribunal_atual.executar()
            ref[num] = resp
    
    def __apurar(self, num:str) -> Tribunal:
        if len(num) < 16:
            return None 
        for key, value in self.ref.items():
            if key == num.replace('-','').replace('.','')[14:16]:
                return value 
        return None

    def set_captcha(self, valor) -> None:
        self.tribunal_atual.set_captcha(valor)

class MainWindow(QMainWindow, Ui_MainWindow):
    MAX_PROGRESS = 100

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.text_aviso = [
            'Os tribunais dos seguintes processos ainda não foram implementados no programa:',
            'Os números a seguir não foram encontrados em seus respectivos sites:'
        ]

        self.file = Arquivo()
        self.setWindowTitle('Consulta Processual')
        self.setWindowIcon((QIcon(
            resource_path('src\\imgs\\procss-icon.ico'))))
        self.logo.setPixmap(QPixmap(
            resource_path('src\\imgs\\procss-hori.png')))
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
            
            list_processos = self.file.ler()
            self.posicao = self.MAX_PROGRESS / len(list_processos)

            self.exec_load(True)
            self.pushButton.setDisabled(True)

            self.juiz = Juiz(list_processos)
            self._thread = QThread()

            self.juiz.moveToThread(self._thread)
            self._thread.started.connect(self.juiz.pesquisar)
            self.juiz.fim.connect(self._thread.quit)
            self.juiz.fim.connect(self._thread.deleteLater)
            self.juiz.fim.connect(self.encerramento)
            self._thread.finished.connect(self.juiz.deleteLater)
            self.juiz.valor.connect(self.to_captcha) 
            self.juiz.progress.connect(self.to_progress)

            self._thread.start()  

        except ParserError:
            messagebox.showerror(title='Aviso', message= 'Erro ao ler o arquivo, certifique-se de ter inserido o arquivo correto')
        except Exception as err:
            traceback.print_exc()
            messagebox.showerror('Aviso', err)

    def encerramento(self, result: OrderedDict):
        #TODO encerramento
        invalidos = self.filtro(result)
        for index, i in enumerate(invalidos):
            if len(i) != 0:
                messagebox.showwarning('Aviso', \
                    f'{self.text_aviso[index]} \n {'\n'.join(f'- {x}' for x in i)}')
            
        self.file.alterar(result)
        self.file.abrir()

        self.exec_load(False, 0)
        self.pushButton.setDisabled(False)

    def filtro(self, result: OrderedDict):
        falhas = []
        invalido = []
        for key, value in result.items():
            if value == ['']:
                falhas.append(key)
            elif value == ['~']:
                invalido.append(key)
                result[key] = ''
        return [falhas , invalido]
    
    def to_captcha(self, nome_img):
        self.label_5.setPixmap(QPixmap(nome_img))
        self.exec_load(False, 2)

    def to_progress(self, valor):
        self.progressBar.setValue(self.posicao * valor)

    def enviar_resp(self):
        self.juiz.set_captcha(self.lineEdit.text())
        self.lineEdit.setText('')
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