import sys
from py import loginGui
from PyQt5.QtWidgets import (QApplication)

#MAIN

k=input("on initial thing")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = loginGui.login()
    sys.exit(app.exec_())

k = input("on two")