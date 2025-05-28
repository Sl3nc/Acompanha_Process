from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from court import Tribunal

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