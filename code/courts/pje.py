from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from court import Tribunal
from time import sleep

class PJE(Tribunal):
    """
    Implementação do Tribunal PJE para consulta de processos.
    """
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
        """
        Acessa o processo no PJE pelo número informado.
        """
        self.browser.get(self.LINK_BASE)
        self.browser.find_element(By.NAME, self.INPUT).send_keys(num_process)

    def executar(self) -> list[str]:
        """
        Executa a consulta no PJE e retorna os movimentos do processo.
        """
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
        """
        Extrai o conteúdo da tabela de eventos do processo.
        """
        self.browser.get(self.LINK_JANELA + endereco[:len(endereco)-2])
        tbody = self.browser.find_element(By.ID, self.TABELA_CONTEUDO)
        return [x.text for x in tbody.find_elements(By.TAG_NAME, 'span')\
                if x.text != '' and x.text[0].isnumeric()]