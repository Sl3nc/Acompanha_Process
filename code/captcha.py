from selenium.webdriver.remote.webelement import WebElement
from abc import abstractmethod
from time import sleep

class Captcha:
    WAIT = 2
    NOME_IMG = 'image.png'

    def __init__(self, elem_img: str, elem_input: str, browser: WebElement):
        self.resp = ''
        self.browser = browser
        self.elem_input = elem_input
        self.elem_img = elem_img

    @abstractmethod
    def preencher(self) -> None:
        return NotImplementedError("Implemente este método")

    @abstractmethod
    def imagem(self) -> str:
        return NotImplementedError("Implemente este método")

    def esperar(self) -> None:
        self.resp = ''
        while self.resp == '':
            sleep(self.WAIT)

    def set_valor(self, valor) -> None:
        self.resp = valor
