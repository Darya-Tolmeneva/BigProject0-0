import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import Qt


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("des.ui", self)
        self.initUI()

    def getImage(self):
        self.label_5.setText("")
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.dolg},{self.sh}&spn={str(self.masht)},{str(self.masht)}&l={self.map}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            self.label_5.setText("Ой, проверьте данные")

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.map_file = " "
        self.map = "-"
        self.setWindowTitle('Отображение карты')
        self.pushButton.clicked.connect(self.click)
        self.radioButton.toggled.connect(self.onClicked)
        self.radioButton_2.toggled.connect(self.onClicked)
        self.radioButton_3.toggled.connect(self.onClicked)


    def keyPressEvent(self, ev):
        k = ev.key()
        if k == Qt.Key_U:
            try:
                self.masht = float(self.masht) + 0.1
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
                self.lineEdit_3.setText(str(self.masht))
            except FloatingPointError:
                pass
        elif k == Qt.Key_D:
            try:
                self.masht = float(self.masht) - 0.1
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
                self.lineEdit_3.setText(str(self.masht))
            except FloatingPointError:
                pass
        elif k == Qt.Key_I:
            try:
                self.sh = float(self.sh) + float(self.masht)
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
                self.lineEdit.setText(str(self.sh))
            except FloatingPointError:
                pass
        elif k == Qt.Key_M:
            try:
                self.sh = float(self.sh) - float(self.masht)
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
                self.lineEdit.setText(str(self.sh))
            except FloatingPointError:
                pass
        elif k == Qt.Key_J:
            try:
                self.dolg = float(self.dolg) - float(self.masht)
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
                self.lineEdit_2.setText(str(self.dolg))
            except FloatingPointError:
                pass
        elif k == Qt.Key_K:
            try:
                self.dolg = float(self.dolg) + float(self.masht)
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
                self.lineEdit_2.setText(str(self.dolg))
            except FloatingPointError:
                pass

    def click(self):
        self.label_5.setText("")
        if self.lineEdit.text() != "" and self.lineEdit_2.text() != "" and self.lineEdit_3.text() != "":
            self.sh = self.lineEdit.text()
            self.dolg = self.lineEdit_2.text()
            self.masht = self.lineEdit_3.text()
            try:
                self.sh = float(self.sh)
                self.dolg = float(self.dolg)
                self.masht = float(self.masht)
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
            except ValueError:
                self.label_5.setText("Ой, проверьте данные")
        else:
            pass

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.text() == "схема":
                self.map = "map"
            elif radioButton.text() == "спутник":
                self.map = "sat"
            elif radioButton.text() == "гибрид":
                self.map = "sat,skl"


    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        if self.map_file != " ":
            os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())