import sys
import loginGui
from PyQt5.QtWidgets import (QApplication)
import os
#MAIN
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = loginGui.login()
    sys.exit(app.exec_())