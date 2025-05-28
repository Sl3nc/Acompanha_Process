from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from pathlib import Path

class Browser:
    """
    Classe utilitária para criar e configurar uma instância do navegador Chrome via Selenium.
    """
    CHROME_DRIVER_PATH = Path(__file__).parent / 'src'/'drivers'/'chromedriver.exe'

    def make_chrome_browser(self,*options: str, hide = True) -> webdriver.Chrome:
        """
        Cria uma instância do navegador Chrome com as opções fornecidas.
        """
        chrome_options = webdriver.ChromeOptions()

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