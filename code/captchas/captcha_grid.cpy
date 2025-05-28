from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium import webdriver

from PIL import Image, ImageFont, ImageDraw
from captcha import Captcha

class CaptchaGrid(Captcha):
    def __init__(self, elem_img: str, elem_input: str, browser: WebElement):
        super().__init__(elem_img, elem_input, browser)

        self.cord_resp = [
            [-100,-100], [0,-100], [100,-100],
            [-100,0], [0,0], [100,0],
            [-100,100], [0,100], [100,100]
        ] 

        #Horizontal, Vertical
        self.cord_img = {
            '1':(5, 0),
            '2':(110, 0),
            '3':(220, 0),
            '4':(5, 100),
            '5':(110, 100),
            '6':(220, 100),
            '7':(5, 205),
            '8':(110, 205),
            '9':(220, 205),
        }

    def preencher(self):
        el = self.browser.find_element(By.CSS_SELECTOR, self.CAPTCHA2)
        action = webdriver.common.action_chains.ActionChains(self.browser)

        for var1, var2 in [[0,100], [100,100]]:
            action.move_to_element_with_offset(el, var1, var2)
            action.click()
            action.perform()

    def imagem(self):
        self.browser.find_element(By.CSS_SELECTOR, '#root > div > form > div:nth-child(3) > div > div:nth-child(2) > canvas').screenshot(self.nome_img)

        font = ImageFont.truetype("C:\\Windows\\Fonts\\Verdanab.ttf", 50)
        img = Image.open(self.nome_img)
        draw = ImageDraw.Draw(img)

        for number, posic in self.ref_img.items():
            draw.text(posic, number, 'red', font=font)

        return self.nome_img      