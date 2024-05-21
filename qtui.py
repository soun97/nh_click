import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic.properties import QtGui, QtCore

from scheduler import start_scheduler
from datetime import datetime, timedelta

form_class = uic.loadUiType("MARKET_TIME.ui")[0]

IS_DEBUG = True

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.start_time_edit: QTimeEdit
        self.end_time_edit: QTimeEdit

        if IS_DEBUG:
            self.start_time_edit.setDateTime(datetime.now() + timedelta(minutes=1))
            self.end_time_edit.setDateTime(datetime.now() + timedelta(minutes=30))

        self.okButton: QPushButton
        self.okButton.clicked.connect(self.buttonClick)

        self.statusTextEdit: QTextEdit

    def buttonClick(self):
        # self.okButton.setDisabled()  # button disabled
        start_time=(self.start_time_edit.time())
        time_string = start_time.toString("hh:mm")
        self.statusTextEdit.append(time_string)
        end_time=(self.end_time_edit.time())
        time_string2 = end_time.toString("hh:mm")
        self.statusTextEdit.append(time_string2)
        start_scheduler(time_string, time_string2, self.log_print)

    def log_print(self, text):
        self.statusTextEdit.append(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()