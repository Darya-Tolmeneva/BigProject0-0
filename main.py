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
        if not self.need_point:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.dolg},{self.sh}&spn={str(self.masht)},{str(self.masht)}&l={self.map}"
        else:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.dolg},{self.sh}&spn={str(self.masht)},{str(self.masht)}&l={self.map}&pt={self.need_point[0]},{self.need_point[1]},pmwtm1"
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
        self.need_point = False
        self.setWindowTitle('Отображение карты')
        self.pushButton.clicked.connect(self.click)
        self.radioButton.toggled.connect(self.onClicked)
        self.radioButton_2.toggled.connect(self.onClicked)
        self.radioButton_3.toggled.connect(self.onClicked)
        self.pushButton_2.clicked.connect(self.find)
        self.lineEdit_3.setText('1')
        self.map = "map"
        self.radioButton.setDown(True)
        self.pushButton_3.clicked.connect(self.clean_pt)

    def clean_pt(self):
        self.need_point = False
        self.click()

    def find(self):
        if self.lineEdit_4.text():
            if self.lineEdit_3.text():
                self.need_point = False
                self.masht = self.lineEdit_3.text()
                geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
                geocoder_params = {
                    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                    "geocode": self.lineEdit_4.text(),
                    "format": "json",
                }
                response = requests.get(geocoder_api_server, params=geocoder_params)
                if not response:
                    print("Ошибка выполнения запроса:")
                    print(response)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    self.label_5.setText("Ой, проверьте данные")
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]
                toponym_coodrinates = toponym["Point"]["pos"].split()
                self.need_point = toponym_coodrinates
                self.dolg, self.sh = toponym_coodrinates[0], toponym_coodrinates[1]
                self.lineEdit.setText(toponym_coodrinates[1])
                self.lineEdit_2.setText(toponym_coodrinates[0])
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
            else:
                self.label_5.setText("Введите масштаб")
        else:
            self.label_5.setText("Ой, проверьте данные")

    def keyPressEvent(self, ev):
        k = ev.key()
        if k == Qt.Key_PageDown:
            try:

                self.masht = float(self.masht) + (float(self.masht) * 0.5)
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
            except FloatingPointError:
                pass
        elif k == Qt.Key_PageUp:
            try:
                self.masht = float(self.masht) - (float(self.masht) * 0.5)
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.label_4.move(80, 190)
                self.label_4.setPixmap(self.pixmap)
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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
