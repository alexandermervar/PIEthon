from sys import exit, argv
from py import loginGui
from PyQt5.QtWidgets import (QApplication)

#MAIN

if __name__ == '__main__':
    app = QApplication(argv)
    ex = loginGui.login()
    exit(app.exec_())
