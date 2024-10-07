from PySide6.QtWidgets import QMainWindow, QApplication
from tkinter.filedialog import askopenfilename
from window import Ui_MainWindow
from bs4 import BeautifulSoup 
import requests 
import abc
import sys

class Arquivo:
    def __init__(self) -> None:
        pass

    def inserir(self):
        caminho = askopenfilename()

    def alterar(self):
        self.caminho
        ...

class Tribunal:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def infos(self, soap: BeautifulSoup):
        raise NotImplementedError("Please Implement this method")
    
class STF(Tribunal):
    def infos(soap:BeautifulSoup):
        ...

class Browser:
    def __init__(self) -> None:
        self.ref_enderecos = {
            'stf' : ['', STF()]
        }

        pass

    def pesquisar(self, num_processo:str, tipo:str):
        try:
            endereco = self.ref_enderecos[tipo][0]

            # Send a GET request to the website 
            response = requests.get(
                endereco.replace({'{ num_proc }'}, num_processo))
            
            # Check if the request was successful 
            html_content = response.text 
                
            # Parse the HTML content 
            soap = BeautifulSoup(html_content, 'html.parser')

            self.ref_enderecos[tipo][1].infos(soap)
        except: 
            print(f"Failed to retrieve content: {response.status_code}") 

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

    def loading(self):
        ...

    def buscar(self):
        ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()