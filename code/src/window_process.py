# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window_process.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(679, 459)
        MainWindow.setMinimumSize(QSize(679, 459))
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_1 = QFrame(self.centralwidget)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShadow(QFrame.Shadow.Plain)
        self.line_1.setLineWidth(4)
        self.line_1.setMidLineWidth(2)
        self.line_1.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line_1, 1, 1, 1, 3)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Shadow.Plain)
        self.line_3.setLineWidth(4)
        self.line_3.setMidLineWidth(2)
        self.line_3.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line_3, 5, 1, 1, 2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.pushButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton, 5, 3, 1, 1)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_2 = QVBoxLayout(self.page_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.page_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Arial Rounded MT"])
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(False)

        self.verticalLayout_2.addWidget(self.label_2)

        self.pushButton_2 = QPushButton(self.page_3)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(22)
        font1.setItalic(True)
        self.pushButton_2.setFont(font1)
        icon = QIcon()
        icon.addFile(u"../imgs/upload-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QSize(65, 63))

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_4 = QGridLayout(self.page_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.label_4 = QLabel(self.page_4)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        font2 = QFont()
        font2.setFamilies([u"Arial Rounded MT"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.label_4.setFont(font2)

        self.gridLayout_4.addWidget(self.label_4, 1, 1, 1, 1)

        self.gif_load = QLabel(self.page_4)
        self.gif_load.setObjectName(u"gif_load")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.gif_load.sizePolicy().hasHeightForWidth())
        self.gif_load.setSizePolicy(sizePolicy4)
        self.gif_load.setMinimumSize(QSize(100, 100))
        self.gif_load.setMaximumSize(QSize(100, 100))
        self.gif_load.setPixmap(QPixmap(u"../imgs/load.gif"))
        self.gif_load.setScaledContents(True)

        self.gridLayout_4.addWidget(self.gif_load, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.progressBar = QProgressBar(self.page_4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout_4.addWidget(self.progressBar, 3, 0, 1, 3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 1, 2, 1, 1)

        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_3 = QGridLayout(self.page_5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.enviar_captcha = QPushButton(self.page_5)
        self.enviar_captcha.setObjectName(u"enviar_captcha")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.enviar_captcha.sizePolicy().hasHeightForWidth())
        self.enviar_captcha.setSizePolicy(sizePolicy5)
        self.enviar_captcha.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout_3.addWidget(self.enviar_captcha, 2, 2, 1, 1)

        self.label_6 = QLabel(self.page_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)

        self.gridLayout_3.addWidget(self.label_6, 1, 1, 1, 1)

        self.label_5 = QLabel(self.page_5)
        self.label_5.setObjectName(u"label_5")
        sizePolicy4.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy4)
        self.label_5.setScaledContents(True)

        self.gridLayout_3.addWidget(self.label_5, 0, 1, 1, 2)

        self.lineEdit = QLineEdit(self.page_5)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_3.addWidget(self.lineEdit, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_5)

        self.gridLayout.addWidget(self.stackedWidget, 4, 1, 1, 3)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logo = QLabel(self.widget)
        self.logo.setObjectName(u"logo")
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setPixmap(QPixmap(u"../imgs/procss-hori.png"))
        self.logo.setScaledContents(True)

        self.verticalLayout.addWidget(self.logo)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setFamilies([u"Verdana"])
        font3.setPointSize(22)
        font3.setBold(True)
        font3.setItalic(False)
        font3.setStrikeOut(False)
        font3.setKerning(True)
        self.label.setFont(font3)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)


        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.pushButton.setDefault(True)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(accessibility)
        self.pushButton.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Executar", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Insira aqui seu relat\u00f3rio de processos", None))
        self.pushButton_2.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Carregando...", None))
        self.gif_load.setText("")
        self.progressBar.setFormat(QCoreApplication.translate("MainWindow", u"%p% conclu\u00eddo", None))
        self.enviar_captcha.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Favor preencher o exame CAPTCHA acima", None))
        self.label_5.setText("")
        self.logo.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Consulta Processual", None))
    # retranslateUi

