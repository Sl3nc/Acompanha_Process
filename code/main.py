from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QPixmap, QIcon, QMovie
from PySide6.QtCore import QThread, QSize

from src.window_process import Ui_MainWindow
from pandas.errors import ParserError
from collections import OrderedDict
from traceback import print_exc
from tkinter import messagebox
from pathlib import Path
from file import Arquivo
from judge import Juiz
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Classe principal da interface gráfica. Gerencia as interações do usuário e o fluxo do programa.
    """
    MAX_PROGRESS = 100

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.text_aviso = [
            'Os tribunais dos seguintes processos ainda não foram implementados no programa:',
            'Os números a seguir não foram encontrados em seus respectivos sites:'
        ]

        self.file = Arquivo()
        self.setWindowTitle('Consulta Processual')
        self.setWindowIcon((QIcon(
            (Path(__file__).parent/'src'/'imgs'/'procss-icon.ico').__str__())))
        self.logo.setPixmap(QPixmap(
            (Path(__file__).parent/'src'/'imgs'/'procss-hori.png').__str__()))
        icon = QIcon()
        icon.addFile(
            (Path(__file__).parent/'src'/'imgs'/'upload-icon.png').__str__(),
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off
        )
        self.pushButton_2.setIcon(icon)
        self.movie = QMovie(
            (Path(__file__).parent/'src'/'imgs'/'load.gif').__str__()
        )
        self.gif_load.setMovie(self.movie)

        self.pushButton_2.clicked.connect(
            lambda: self.file.inserir(self.pushButton_2)
        )
        self.pushButton.clicked.connect(self.hard_work)
        self.enviar_captcha.clicked.connect(self.enviar_resp)

    def hard_work(self):
        """
        Inicia o processamento dos processos em uma thread separada.
        """
        try:
            if self.file.envio_invalido():
                raise Exception('Favor anexar seu relatório de processos')
            
            list_processos = self.file.ler()
            self.posicao = self.MAX_PROGRESS / len(list_processos)

            self.exec_load(True)
            self.pushButton.setDisabled(True)

            self.juiz = Juiz(list_processos)
            self._thread = QThread()

            self.juiz.moveToThread(self._thread)
            self._thread.started.connect(self.juiz.pesquisar)
            self.juiz.fim.connect(self._thread.quit)
            self.juiz.fim.connect(self._thread.deleteLater)
            self.juiz.fim.connect(self.encerramento)
            self._thread.finished.connect(self.juiz.deleteLater)
            self.juiz.valor.connect(self.to_captcha) 
            self.juiz.progress.connect(self.to_progress)

            self._thread.start()  

        except ParserError:
            messagebox.showerror(title='Aviso', message= 'Erro ao ler o arquivo, certifique-se de ter inserido o arquivo correto')
        except Exception as err:
            print_exc()
            messagebox.showerror('Aviso', err)

    def encerramento(self, result: OrderedDict):
        """
        Finaliza o processamento, exibe avisos e abre o arquivo gerado.
        """
        #TODO encerramento
        invalidos = self.filtro(result)
        for index, i in enumerate(invalidos):
            if len(i) != 0:
                messagebox.showwarning('Aviso', \
                    f'{self.text_aviso[index]} \n {'\n'.join(f'- {x}' for x in i)}')
            
        self.file.alterar(result)
        self.file.abrir()

        self.exec_load(False, 0)
        self.pushButton.setDisabled(False)

    def filtro(self, result: OrderedDict):
        """
        Filtra processos inválidos ou não encontrados.
        """
        falhas = []
        invalido = []
        for key, value in result.items():
            if value == ['']:
                falhas.append(key)
            elif value == ['~']:
                invalido.append(key)
                result[key] = ''
        return [falhas , invalido]
    
    def to_captcha(self, nome_img):
        """
        Exibe a imagem do captcha para o usuário.
        """
        self.label_5.setPixmap(QPixmap(nome_img))
        self.exec_load(False, 2)

    def to_progress(self, valor):
        """
        Atualiza a barra de progresso.
        """
        self.progressBar.setValue(self.posicao * valor)

    def enviar_resp(self):
        """
        Envia a resposta do captcha informada pelo usuário.
        """
        self.juiz.set_captcha(self.lineEdit.text())
        self.lineEdit.setText('')
        self.exec_load(True)

    def exec_load(self, action: bool, to = 1):
        """
        Controla a exibição do GIF de carregamento e troca de telas.
        """
        if action == True:
            self.movie.start()
            self.stackedWidget.setCurrentIndex(to)
        else:
            self.movie.stop()
            self.stackedWidget.setCurrentIndex(to)


if __name__ == '__main__':
    """
    Ponto de entrada do programa. Inicializa a aplicação Qt.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()