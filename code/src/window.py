# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(478, 279)
        MainWindow.setMinimumSize(QSize(478, 279))
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

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Shadow.Plain)
        self.line_3.setLineWidth(4)
        self.line_3.setMidLineWidth(2)
        self.line_3.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line_3, 5, 1, 1, 2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Verdana"])
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 2, 1, 2)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(22)
        font1.setItalic(True)
        self.pushButton_2.setFont(font1)
        icon = QIcon()
        icon.addFile(u"../imgs/upload-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QSize(75, 75))

        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 3)

        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName(u"logo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy2)
        self.logo.setMaximumSize(QSize(100, 100))
        self.logo.setPixmap(QPixmap(u"../imgs/procc-icon.ico"))
        self.logo.setScaledContents(True)

        self.gridLayout.addWidget(self.logo, 0, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        font2 = QFont()
        font2.setFamilies([u"Arial Rounded MT"])
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setItalic(False)
        self.label_2.setFont(font2)
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(False)

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.pushButton.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(accessibility)
        self.pushButton.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Executar", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Acompanha processos", None))
        self.pushButton_2.setText("")
        self.logo.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Insira aqui seu relat\u00f3rio de processos", None))
    # retranslateUi

