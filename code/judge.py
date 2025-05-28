from courts.eproc import EPROC
from courts.pje import PJE
from courts.tst import TST

from selenium.common.exceptions import NoSuchElementException
from captchas.captcha_simples import CaptchaSimples
from PySide6.QtCore import Signal, QObject
from tkinter.messagebox import showerror
from collections import OrderedDict
from traceback import print_exc
from browser import Browser
from court import Tribunal


class Juiz(QObject):
    """
    Classe responsável por orquestrar a consulta dos processos em diferentes tribunais.
    Utiliza multithreading para não travar a interface gráfica.
    """
    valor = Signal(str)
    progress = Signal(int)
    fim = Signal(OrderedDict)
    WAIT_CAPTCHA = 2

    def __init__(self, num_process: list[str]) -> None:
        super().__init__()
        self.num_process = num_process
        self.browser = Browser().make_chrome_browser(hide=False)
        self.ref = {
            '13': PJE(self.browser),
            '01': EPROC(self.browser),
            '03': TST(self.browser)
        }

    def pesquisar(self):
        """
        Realiza a pesquisa dos processos, emitindo sinais de progresso e resultado.
        """
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

        except NoSuchElementException as err:
            print_exc()
            showerror('Aviso', f'Erro na busca por elementos no site, favor comunicar o desenvolvedor. Erro: \n {err}')
        except Exception as err:
            print_exc()
            showerror('Aviso', err)
        finally:
            self.browser.close()
            self.fim.emit(ref)

    def processo(self, ref, num):
        """
        Realiza a consulta de um processo específico, tratando captcha se necessário.
        """
        tribunal_atual = self.__apurar(num)
        if tribunal_atual == None:
            ref[num] = ['']
        else:
            tribunal_atual.acessar_processo(num)
            resp = tribunal_atual.executar()
            while type(resp) == CaptchaSimples:
                self.captcha = resp
                self.valor.emit(self.captcha.imagem())
                self.captcha.esperar()
                self.captcha.preencher()
                resp = tribunal_atual.executar()
            ref[num] = resp
    
    def __apurar(self, num:str) -> Tribunal:
        """
        Determina o tribunal responsável pelo processo a partir do número.
        """
        if len(num) < 16:
            return None 
        for key, value in self.ref.items():
            if key == num.replace('-','').replace('.','')[14:16]:
                return value 
        return None

    def set_captcha(self, valor) -> None:
        """
        Define o valor do captcha para o tribunal atual.
        """
        self.tribunal_atual.set_captcha(valor)