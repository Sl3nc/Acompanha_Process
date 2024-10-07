# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(423, 279)
        MainWindow.setMinimumSize(QSize(423, 279))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setFamilies([u"Rockwell"])
        font.setBold(True)
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 5, 1, 1, 2)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 6, 2, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Verdana"])
        font1.setPointSize(14)
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setLineWidth(4)
        self.line_2.setMidLineWidth(2)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 4)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 6, 1, 1, 1)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.comboBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(4)
        self.line.setMidLineWidth(2)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line, 4, 1, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Executar", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Tipo de processo", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Relat\u00f3rio de processos", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Acompanha processos", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Inserir", None))
#if QT_CONFIG(accessibility)
        self.comboBox.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.comboBox.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
    # retranslateUi

