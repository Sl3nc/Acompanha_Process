from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from court import Tribunal
from time import sleep
from os import remove
from PIL import Image

class EPROC(Tribunal):
    """
    Implementação do Tribunal EPROC para consulta de processos.
    """
    LINK_BASE = 'https://eproc1g.trf6.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica'
    INPUT = 'txtNumProcesso'
    CONTULTAR = 'sbmNovo'
    IMG_ELEMENT = '#lblInfraCaptcha > img'
    INPUT_ELEMENT = 'txtInfraCaptcha'
    TABLE_CONTENT = '#divInfraAreaProcesso > table > tbody'
    FRAME_PRINT = [300, 430, 430, 480]

    def __init__(self, browser: WebElement) -> None:
        super().__init__(browser)
        self.CAPTCHA = 'txtInfraCaptcha'
        pass

    def executar(self):
        """
        Executa a consulta no EPROC, tratando captcha se necessário.
        """
        if self.tentar_consulta() == False:
            self.img = self.imagem_captcha()
            return self.img
        remove(self.img)
        return self.conteudo()
    
    def acessar_processo(self, num: str) -> None:
        """
        Acessa o processo no EPROC pelo número informado.
        """
        self.browser.get(self.LINK_BASE)
        sleep(1)
        num = num.replace('.','').replace('-','')
        self.browser.find_element(By.ID, self.INPUT).send_keys(num)

    def tentar_consulta(self) -> bool:
        """
        Tenta consultar o processo, verificando se há captcha.
        """
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
        """
        Salva e recorta a imagem do captcha para exibição ao usuário.
        """
        self.browser.save_screenshot(self.NOME_IMG)
        Image.open(self.NOME_IMG).crop([300, 430, 430, 480]).save(self.NOME_IMG)
        return self.NOME_IMG

    def conteudo(self):
        """
        Extrai o conteúdo da tabela de movimentos do processo.
        """
        tbody = self.browser.find_element(By.CSS_SELECTOR, self.TABLE_CONTENT)
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        rows.pop(0)
        return [x.text[3:] for x in rows if x.text != '']