from py import mainGui, functions, PIEdataVARS, PieHandler
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLineEdit, QLabel, QMessageBox,
                             QPushButton, QRadioButton, QApplication,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import time
import sys

iconPath = functions.createPath('resources//PIEcon.png')
font = 'BentonSans'
fontsize = 9

app = QApplication(sys.argv)

screen = app.primaryScreen()
size = screen.size()
rect = screen.availableGeometry()

qss="iu_stylesheet.qss"

class login(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.resize(rect.height()/3, rect.width()/6)
        self.center()

        #add a username label and text box
        self.userlabel = QLabel(self)
        self.userlabel.setObjectName('bigboi')
        self.userlabel.setText("Username")

        self.userbox = QLineEdit(self)
        self.userbox.setObjectName("important")


        #add the password label and text box
        self.passlabel = QLabel(self)
        self.passlabel.setObjectName('bigboi')
        self.passlabel.setText("Password")

        self.passbox = QLineEdit(self)
        self.passbox.setEchoMode(QLineEdit.Password)
        self.passbox.setObjectName("important")

        #add the radio buttons
        self.pushradio = QRadioButton('Duo Push', self)
        self.pushradio.setChecked(True)

        self.callradio = QRadioButton('Duo Call', self)

        self.coderadio = QRadioButton('Duo Code', self)

        self.codelabel = QLabel(self)
        self.codelabel.setText("Duo Code:")

        self.duocode = QLineEdit(self)
        self.duocode.setEnabled(False)

        self.coderadio.toggled.connect(self.radiocheck)

        #add close button
        self.closebutton = QPushButton('Close', self)
        self.closebutton.clicked.connect(self.close)

        #add submit button
        self.submitbutton = QPushButton('Submit', self)
        self.submitbutton.clicked.connect(self.pieLogin)

        #add the status thingy
        self.statuslabel = QLabel(self)
        self.statuslabel.setObjectName('statuslabel')
        self.statuslabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.statuslabel.setText("Ready")

        userhbox = QVBoxLayout()
        userhbox.addWidget(self.userlabel)
        userhbox.addWidget(self.userbox)

        passvbox = QVBoxLayout()
        passvbox.addWidget(self.passlabel)
        passvbox.addWidget(self.passbox)

        radiobox = QHBoxLayout()
        radiobox.addWidget(self.pushradio)
        radiobox.addWidget(self.callradio)
        radiobox.addWidget(self.coderadio)

        combohbox = QHBoxLayout()
        combohbox.addWidget(self.codelabel)
        combohbox.addWidget(self.duocode)

        buttonhbox = QHBoxLayout()
        buttonhbox.addWidget(self.closebutton)
        buttonhbox.addWidget(self.submitbutton)

        statushbox = QHBoxLayout()
        statushbox.addWidget(self.statuslabel)

        totalvbox = QVBoxLayout()
        totalvbox.addSpacing(10)
        totalvbox.addLayout(userhbox)
        totalvbox.addLayout(passvbox)
        totalvbox.addSpacing(15)
        totalvbox.addLayout(radiobox)
        totalvbox.addLayout(combohbox)
        totalvbox.addSpacing(30)
        totalvbox.addLayout(buttonhbox)
        totalvbox.addLayout(statushbox)

        self.setLayout(totalvbox)
        self.setWindowTitle('PIEthon')
        self.setWindowIcon(QIcon(iconPath))

        #style things
        self.setStyleSheet(open("resources//iu_stylesheet.qss", "r").read())

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def statusUpdate(self, newstat):
        #print('in status update')
        self.statuslabel.setText(newstat)
        QtCore.QCoreApplication.processEvents()

    def startMain(self, user, dataoptions, driver):
        #print('here we go')
        self.mainwind = mainGui.mainwindow(user, dataoptions, driver)
        #print('time to show')
        self.mainwind.show()

    def radiocheck(self):
        if (not self.coderadio.isChecked()):
            self.duocode.setEnabled(False)
        else:
            self.duocode.setEnabled(True)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return or qKeyEvent.key() == QtCore.Qt.Key_Enter:
            self.pieLogin()
        else:
            super().keyPressEvent(qKeyEvent)

    def pieLogin(self):
        self.statusUpdate('Spinning up the driver')
        driver = functions.buildHeadless()
        self.statusUpdate('Driver built, prepare for DUO')
        user = self.userbox.text()
        password = self.passbox.text()
        if self.pushradio.isChecked():
            duotype = 'push'
        elif self.callradio.isChecked():
            duotype = 'call'
        else:
            duotype = self.duocode.text()
        driver = PieHandler.caslogin(driver, user, password, duotype)
        if(not driver):
            QMessageBox.about(self,"Error","CAS login failed!")
            return
        else:
            self.statusUpdate('DUO passed, going to Pie')
        driver = PieHandler.getPie(driver)
        time.sleep(.7)
        self.statusUpdate('Connected to Pie')
        self.statusUpdate('Pulling in Users')
        userlist = PieHandler.grabUsers(driver)
        self.statusUpdate('Pulling in Locations')
        lablist = PieHandler.grabLabs(driver)
        self.statusUpdate('Throwing it together')
        invlabs = PieHandler.grabInvLabs(driver)
        datalist = PIEdataVARS.buildalldatathings(userlist, lablist, invlabs)

        self.startMain(user, datalist, driver)

        self.close()