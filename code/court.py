from selenium.webdriver.remote.webelement import WebElement
from captchas.captcha_simples import CaptchaSimples
from selenium.webdriver.common.by import By
from abc import ABCMeta, abstractmethod
from time import sleep

class Tribunal:
    """
    Classe abstrata base para tribunais. Define a interface para consulta de processos.
    """
    TIME_TO_WAIT = 1
    __metaclass__ = ABCMeta

    def __init__(self, browser: WebElement) -> None:
        self.browser = browser
        pass

    @abstractmethod
    def executar(self) -> list[str] | CaptchaSimples:
        """
        Executa a consulta do processo no tribunal.
        """
        raise NotImplementedError("Implemente este método")
    
    @abstractmethod
    def acessar_processo(self, num: str) -> None:
        """
        Acessa a página do processo no tribunal.
        """
        raise NotImplementedError("Implemente este método")
    
    @abstractmethod
    def conteudo(self):
        """
        Extrai o conteúdo relevante do processo.
        """
        raise NotImplementedError("Implemente este método")
    
    def esperar_captcha(self):
        """
        Aguarda o usuário informar o valor do captcha.
        """
        self.valor_captcha = ''
        while self.valor_captcha == '':
            sleep(self.WAIT_CAPTCHA)

    def preencher_captcha(self):
        """
        Preenche o captcha no campo correspondente do site.
        """
        self.browser.find_element(By.ID, self.CAPTCHA)\
            .send_keys(self.valor_captcha)
    
    def set_captcha(self, valor):
        """
        Define o valor do captcha informado pelo usuário.
        """
        self.valor_captcha = valor