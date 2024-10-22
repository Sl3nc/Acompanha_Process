from pathlib import Path
from time import sleep
import keyboard
from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from PIL import Image
import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout,QPushButton, QLineEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QThread, QObject, Signal
from src.window_process import Ui_MainWindow

class Browser:
    ROOT_FOLDER = Path(__file__).parent
    CHROME_DRIVER_PATH = ROOT_FOLDER / 'src' / 'drivers' / 'chromedriver.exe'

    def __init__(self, options = (), hide = True) -> None:
        self.browser = self.make_chrome_browser(*options)
        if hide == True:
            self.browser.set_window_position(-10000,0)
            
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

class EPROC(Browser):
    LINK_BASE = 'https://eproc1g.trf6.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica'
    INPUT = 'txtNumProcesso'
    CAPTCHA = 'txtInfraCaptcha'
    CONTULTAR = 'sbmNovo'
    TABLE_CONTENT = '#divInfraAreaProcesso > table > tbody'
    TIME_TO_WAIT = 1
    WAIT_CAPTCHA = 2
    FRAME_PRINT = [300, 430, 430, 480]

    def __init__(self) -> None:
        super().__init__(hide=False)
        pass

    def inserir_valor(self, num_process) -> None:
        self.browser.get(self.LINK_BASE)
        self.browser.find_element(By.ID, self.INPUT).send_keys(num_process)

    def tentar_consulta(self) -> bool:
        self.browser.find_element(By.ID, self.CONTULTAR).click()
        keyboard.press_and_release('enter')
        sleep(self.TIME_TO_WAIT)
        try:
            #Se dar erro é porque não tem o captcha, senão o contrário 
            self.browser.find_element(By.ID, self.CAPTCHA)
        except:
            return True
        return False
        
    def imagem_captcha(self):
        self.browser.save_screenshot(self.NOME_IMG)
        Image.open(self.NOME_IMG).crop([300, 430, 430, 480]).save(self.NOME_IMG)
        return self.NOME_IMG

    def preencher_captcha(self, valor):
        self.browser.find_element(By.ID, 'txtInfraCaptcha')\
            .text(valor)

    def conteudo(self):
        tbody = self.browser.find_element(By.CSS_SELECTOR, self.TABLE_CONTENT)
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        rows.pop(0)
        return rows

class PJE(Browser):
    CLASS_ELEMENTS = 'col-sm-12'
    TIME_TO_WAIT = 300
    INPUT = 'fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso'
    BTN_PESQUISAR = 'fPP:searchProcessos'
    JANELA_PROCESSO = '#fPP\\:processosTable\\:632256959\\:j_id245 > a'
    TABELA_CONTEUDO = 'j_id134:processoEvento'
    LINK_BASE = 'https://pje-consulta-publica.tjmg.jus.br/'
    LINK_JANELA = 'https://pje-consulta-publica.tjmg.jus.br/pje/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca'

    def __init__(self) -> None:
        super().__init__()
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

class Worker(QObject):
    inicio = Signal(str)
    valor = Signal(str)
    fim = Signal(str)

    def __init__(self, num_process) -> None:
        super().__init__()
        self.num_process = num_process
        self.ref = {
            'eproc': self.acao_eproc
        }

    def executar(self):
        for num in self.num_process:
            result_apuragem = self.__apurar()
            for key, method in self.ref.items():
                if key == result_apuragem:
                    method(num)
                    # PJE().exec('5147698-10.2023.8.13.0024')
    
    def __apurar(self):
        return 'pje'

    def acao_eproc(self, num):
        tribunal = EPROC()
        tribunal.inserir_valor(num)
        while tribunal.tentar_consulta() == False:
            img = tribunal.imagem_captcha()
            self.valor.emit(img)
            while len(self.valor_janela) != 4:
                print('esperando resp')
                sleep(self.WAIT_CAPTCHA)
            print('resposta recebida')
            tribunal.preencher_captcha(self.valor_janela)
            print('preencheu captcha')
            sleep(3)
            
        return tribunal.conteudo()

    def set_captcha(self, valor):
        self.valor_janela = valor

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.hard_work)
        self.enviar_captcha.clicked.connect(self.enviar_resp)

    def hard_work(self):
        self.worker = Worker(['5147698-10.2023.8.13.0024'])
        self._thread = QThread()

        self.worker.moveToThread(self._thread)
        self._thread.started.connect(self.worker.executar)
        self.worker.fim.connect(self._thread.quit)
        self.worker.fim.connect(self._thread.deleteLater)
        self._thread.finished.connect(self.worker.deleteLater)
        self.worker.valor.connect(self.progress) 
        #######################################
        self._thread.start()  

    def progress(self, nome_img):
        self.label.setPixmap(QPixmap(nome_img))
        self.stackedWidget.setCurrentIndex(2)

    def enviar_resp(self):
        self.worker.set_captcha(self.lineEdit.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()