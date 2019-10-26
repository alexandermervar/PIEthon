from py import mainGui, functions, PIEdataVARS, PieHandler
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLineEdit, QLabel, QMessageBox,
                             QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import time

iconPath = functions.createPath('resources//PIEcon.png')

qss="iu_stylesheet.qss"

class login(QWidget):

    def __init__(self):
        super().__init__()
        self.subThread = submitThread(self)
        self.subThread.finished.connect(self.completed)
        self.initUI()

    def initUI(self):
        self.center()

        self.semesters = ''

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
        self.submitbutton.clicked.connect(self.subThread.start)

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
        self.mainwind = mainGui.mainwindow(user, dataoptions, driver, self.semesters)
        #print('time to show')
        self.mainwind.show()

    def radiocheck(self):
        if (not self.coderadio.isChecked()):
            self.duocode.setEnabled(False)
        else:
            self.duocode.setEnabled(True)

    def keyPressEvent(self, qKeyEvent):
        if (qKeyEvent.key() == QtCore.Qt.Key_Return or qKeyEvent.key() == QtCore.Qt.Key_Enter) and (self.userbox.hasFocus() or self.passbox.hasFocus()):
            self.subThread.start()
        else:
            super().keyPressEvent(qKeyEvent)

    def completed(self):
        if self.userbox.text() == '' or self.passbox.text() == '':
            return
        self.startMain(self.userbox.text(), self.datalist, self.driver)
        self.close()

class submitThread(QtCore.QThread):

    def __init__(self, window):
        self.window = window
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        if self.window.userbox.text() == '':
            self.window.statusUpdate("ERROR: Please provide a username")
            self.window.statuslabel.setStyleSheet("color: red;")
            return
        if self.window.passbox.text() == '':
            self.window.statusUpdate("ERROR: Please enter a password")
            self.window.statuslabel.setStyleSheet("color: red;")
            return
        self.window.setDisabled(True)
        self.window.statuslabel.setStyleSheet("color: black;")
        self.window.statusUpdate('Spinning up the driver')
        driver = functions.buildHeadless()
        self.window.statusUpdate('Driver built, prepare for DUO')
        user = self.window.userbox.text()
        password = self.window.passbox.text()
        if self.window.pushradio.isChecked():
            duotype = 'push'
        elif self.window.callradio.isChecked():
            duotype = 'call'
        else:
            duotype = self.window.duocode.text()
        driver = PieHandler.caslogin(driver, user, password, duotype)
        if(not driver):
            QMessageBox.about(self.window,"Error","CAS login failed!")
            self.window.setDisabled(False)
            return
        else:
            self.window.statusUpdate('DUO passed, going to Pie')
        driver = PieHandler.getPie(driver)
        time.sleep(.7)
        self.window.statusUpdate('Connected to Pie')
        self.window.statusUpdate('Pulling in Users')
        userlist = PieHandler.grabUsers(driver)
        self.window.statusUpdate('Pulling in Locations')
        lablist = PieHandler.grabLabs(driver)
        invlabs = PieHandler.grabInvLabs(driver)
        self.window.statusUpdate('Grabbing Semesters')
        self.window.semesters = PieHandler.grabSemesters(driver)
        self.window.statusUpdate('Throwing it together')
        datalist = PIEdataVARS.buildalldatathings(userlist, lablist, invlabs)
        self.window.datalist = datalist
        self.window.driver = driver
        self.window.statusUpdate('Starting Main Window')
        return