import functions
import PieHandler
import PIEdataVARS
import mainGui
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLineEdit, QLabel, QMessageBox,
                             QPushButton, QRadioButton, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import reportLabBreakdown
import reportVars
import reportuserinfo
import reportPDIs
import reportStepouts
import time

iconPath = functions.createPath('PIEcon.png')

class login(QWidget):

    def __init__(self):
        self.reportdict = reportVars.buildReports()
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(275, 200)
        self.center()

        #add a username label and text box
        self.userlabel = QLabel(self)
        self.userlabel.move(20, 20)
        self.userlabel.setText("Username")
        self.userlabel.resize(80, 25)

        self.userbox = QLineEdit(self)
        self.userbox.move(90, 20)
        self.userbox.resize(150, 25)

        #add the password label and text box
        self.passlabel = QLabel(self)
        self.passlabel.move(20, 55)
        self.passlabel.setText("Password")
        self.passlabel.resize(80, 25)

        self.passbox = QLineEdit(self)
        self.passbox.setEchoMode(QLineEdit.Password)
        self.passbox.move(90, 55)
        self.passbox.resize(150, 25)

        #add the radio buttons
        self.reportradio = QRadioButton('Reports', self)
        self.reportradio.setChecked(True)
        self.reportradio.move(50, 100)

        self.pulldata = QRadioButton('Pull Data', self)
        self.pulldata.move(165, 100)

        #add the cccccccombo box
        self.categorylabel = QLabel(self)
        self.categorylabel.move(20, 125)
        self.categorylabel.setText("Report Type")
        self.categorylabel.resize(80, 25)

        self.reportcombo = QComboBox(self)
        self.reportcombo.addItems(self.reportdict)
        self.reportcombo.move(90, 125)
        self.reportcombo.resize(150, 25)

        self.reportradio.toggled.connect(self.radiocheck)

        #add close button
        self.closebutton = QPushButton('Close', self)
        self.closebutton.move(20,160)
        self.closebutton.clicked.connect(self.close)

        #add submit button
        self.submitbutton = QPushButton('Submit', self)
        self.submitbutton.move(175,160)
        self.submitbutton.clicked.connect(self.pieLogin)

        #add the status thingy
        self.statuslabel = QLabel(self)
        self.statuslabel.move(75, 185)
        self.statuslabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.statuslabel.setText("Ready")
        self.statuslabel.resize(195, 13)

        self.setWindowTitle('PIEthon')
        self.setWindowIcon(QIcon(iconPath))
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
        print('hit')
        if (self.pulldata.isChecked()):
            self.reportcombo.setEnabled(False)
        else:
            self.reportcombo.setEnabled(True)

    def pieLogin(self):
        self.statusUpdate('Spinning up the driver')
        driver = functions.buildHeadless()
        self.statusUpdate('Driver built, prepare for DUO')
        user = self.userbox.text()
        password = self.passbox.text()
        driver = PieHandler.caslogin(driver,user,password)
        if(not driver):
            QMessageBox.about(self,"Error","CAS login failed!")
            return
        else:
            self.statusUpdate('DUO passed, going to Pie')
        driver = PieHandler.getPie(driver)
        time.sleep(.7)
        self.statusUpdate('Connected to Pie')
        if self.reportradio.isChecked():
            print('load reports')
            self.startreports(driver, self.reportcombo.currentText())
        else:
            self.statusUpdate('Pulling in Users')
            userlist = PieHandler.grabUsers(driver)
            self.statusUpdate('Pulling in Locations')
            lablist = PieHandler.grabLabs(driver)
            self.statusUpdate('Throwing it together')
            invlabs = PieHandler.grabInvLabs(driver)
            datalist = PIEdataVARS.buildalldatathings(userlist, lablist, invlabs)

            self.startMain(user, datalist, driver)

        self.close()