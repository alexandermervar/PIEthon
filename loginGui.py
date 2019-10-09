import functions
import PieHandler
import PIEdataVARS
import mainGui
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLineEdit, QLabel, QMessageBox,
                             QPushButton, QRadioButton, QApplication,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore
import reportLabBreakdown
import reportuserinfo
import reportPDIs
import reportStepouts
import time
import sys

iconPath = functions.createPath('PIEcon.png')
font = 'BentonSans'
fontsize = 9

app = QApplication(sys.argv)

screen = app.primaryScreen()
size = screen.size()
rect = screen.availableGeometry()

class login(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.resize(rect.height()/3, rect.width()/6)
        self.center()

        #add a username label and text box
        self.userlabel = QLabel(self)
        #self.userlabel.move(20, 20)
        self.userlabel.setText("Username")
        #self.userlabel.resize(80, 25)

        self.userbox = QLineEdit(self)
        #self.userbox.move(90, 20)
        #self.userbox.resize(150, 25)

        #add the password label and text box
        self.passlabel = QLabel(self)
        #self.passlabel.move(20, 55)
        self.passlabel.setText("Password")
        #self.passlabel.resize(80, 25)

        self.passbox = QLineEdit(self)
        self.passbox.setEchoMode(QLineEdit.Password)
        #self.passbox.move(90, 55)
        #self.passbox.resize(150, 25)

        #add the radio buttons
        self.pushradio = QRadioButton('Duo Push', self)
        self.pushradio.setChecked(True)
        #self.reportradio.move(50, 100)

        self.callradio = QRadioButton('Duo Call', self)
        #self.pulldata.move(165, 100)

        self.coderadio = QRadioButton('Duo Code', self)

        #add the cccccccombo box
        self.codelabel = QLabel(self)
        #self.categorylabel.move(20, 125)
        self.codelabel.setText("Duo Code:")
        #self.categorylabel.resize(80, 25)

        self.duocode = QLineEdit(self)
        self.duocode.setEnabled(False)
        #self.reportcombo.move(90, 125)
        #self.reportcombo.resize(150, 25)

        self.coderadio.toggled.connect(self.radiocheck)

        #add close button
        self.closebutton = QPushButton('Close', self)
        #self.closebutton.move(20,160)
        self.closebutton.clicked.connect(self.close)

        #add submit button
        self.submitbutton = QPushButton('Submit', self)
        #self.submitbutton.move(175,160)
        self.submitbutton.clicked.connect(self.pieLogin)

        #add the status thingy
        self.statuslabel = QLabel(self)
        #self.statuslabel.move(75, 185)
        self.statuslabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.statuslabel.setText("Ready")
        #self.statuslabel.resize(195, 13)

        userhbox = QHBoxLayout()
        userhbox.addWidget(self.userlabel)
        userhbox.addWidget(self.userbox)

        passvbox = QHBoxLayout()
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
        totalvbox.addSpacing(25)
        totalvbox.addLayout(buttonhbox)
        totalvbox.addLayout(statushbox)

        self.setLayout(totalvbox)
        self.setWindowTitle('PIEthon')
        self.setWindowIcon(QIcon(iconPath))

        #style things
        self.setStyleSheet("background-color:white;")
        self.userlabel.setFont(QFont(font, fontsize))
        self.userbox.setFont(QFont(font, fontsize))
        self.passlabel.setFont(QFont(font, fontsize))
        self.passbox.setFont(QFont(font, fontsize))
        self.pushradio.setFont(QFont(font, fontsize))
        self.callradio.setFont(QFont(font, fontsize))
        self.coderadio.setFont(QFont(font, fontsize))
        self.codelabel.setFont(QFont(font, fontsize))
        self.duocode.setFont(QFont(font, fontsize))
        self.submitbutton.setFont(QFont(font, fontsize))
        self.submitbutton.setStyleSheet("background-color:rgb(153,0,0); color:white;")
        self.closebutton.setFont(QFont(font, fontsize))
        self.closebutton.setStyleSheet("background-color:rgb(153,0,0); color:white;")
        self.statuslabel.setFont(QFont(font, fontsize, QFont.Bold))

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

    def startreports(self, driver, text):
        if text == 'Lab Breakdown':
            self.lab = reportLabBreakdown.labbreakdown(driver)
            self.lab.show()
        if text == 'Incomplete User Information':
            reportuserinfo.getinfo(driver)
        if text == 'Stepout Location Medians':
            self.lab = reportStepouts.stepoutaverages(driver)
            self.lab.show()
        if text == 'PDIs (NJ41)':
            self.lab = reportPDIs.Pdis(driver)
            self.lab.show()

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
        driver = PieHandler.caslogin(driver,user,password,duotype)
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