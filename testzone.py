import sys
from PyQt5.QtWidgets import (QApplication)

import loginGui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = loginGui.login()
    sys.exit(app.exec_())