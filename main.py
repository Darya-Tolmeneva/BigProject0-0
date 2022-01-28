import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import uic

# SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("des.ui", self)
        self.initUI()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.dolg},{self.sh}&spn={self.masht},{self.masht}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setWindowTitle('Отображение карты')
        self.pushButton.clicked.connect(self.click)

    def click(self):
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text():
            self.sh = self.lineEdit.text()
            self.dolg = self.lineEdit_2.text()
            self.masht = self.lineEdit_3.text()
            self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.label_4.move(80, 190)
        self.label_4.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())