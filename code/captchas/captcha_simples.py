from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from captcha import Captcha

class CaptchaSimples(Captcha):
    def __init__(self, elem_img: str, elem_input: str, browser: WebElement):
        super().__init__(elem_img, elem_input, browser)

    def preencher(self) -> None:
        self.browser.find_element(By.ID, self.elem_input)\
            .send_keys(self.resp)

    def imagem(self) -> str:
        self.browser.find_element(By.CSS_SELECTOR, self.elem_img).screenshot(self.NOME_IMG)
        return self.NOME_IMG