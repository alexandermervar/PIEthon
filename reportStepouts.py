import PIEdataVARS
import functions
import PieHandler
import PIEdataVARS
import datetime
import htmlbase
import sys
import mainGui
from PyQt5.QtWidgets import (QWidget, QToolTip, QDesktopWidget, QLineEdit, QLabel, QPushButton, QMessageBox,
                             QPushButton, QApplication, QRadioButton, QComboBox, QCalendarWidget)
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
import numpy as np
import pandas as pd

iconPath = functions.createPath('PIEcon.png')

class stepoutaverages(QWidget):

    def __init__(self, driver):
        self.driver = driver
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(670, 300)
        self.center()

        #add the startdate and end date calendars
        self.startcal = QCalendarWidget(self)
        self.startcal.move(20, 40)
        self.startcal.setSelectedDate(datetime.date.today()-datetime.timedelta(days=30))
        self.startcal.clicked.connect(self.startdatechange)

        self.startlabel = QLabel(self)
        self.startlabel.move(20,20)
        self.startlabel.setText("Start Date: " + self.startcal.selectedDate().toString())
        self.startlabel.resize(200, 25)

        self.endcal = QCalendarWidget(self)
        self.endcal.move(340, 40)
        self.endcal.setSelectedDate(datetime.date.today())
        self.endcal.clicked.connect(self.enddatechange)

        self.endlabel = QLabel(self)
        self.endlabel.move(340, 20)
        self.endlabel.setText("End Date: " + self.endcal.selectedDate().toString())
        self.endlabel.resize(200, 25)

        #add close button
        self.closebutton = QPushButton('Close', self)
        self.closebutton.move(20,260)
        self.closebutton.clicked.connect(self.close)

        #add submit button
        self.submitbutton = QPushButton('Submit', self)
        self.submitbutton.move(570,260)
        self.submitbutton.clicked.connect(self.labbreakwork)

        #add the status thingy
        self.statuslabel = QLabel(self)
        self.statuslabel.move(0, 280)
        self.statuslabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.statuslabel.setText("Ready")
        self.statuslabel.resize(665, 25)

        self.warninglabel = QLabel(self)
        self.warninglabel.move(0, 230)
        self.warninglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.warninglabel.setText("This shouldn't take too long to run")
        self.warninglabel.resize(670, 25)

        self.setWindowTitle('PIEthon - Stepout Report')
        self.setWindowIcon(QIcon(iconPath))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startdatechange(self):
        self.startlabel.setText("Start Date:  " + self.startcal.selectedDate().toString())

    def enddatechange(self):
        self.endlabel.setText("End Date:  " + self.endcal.selectedDate().toString())

    def statusUpdate(self, newstat):
        #print('in status update')
        self.statuslabel.setText(newstat)
        QtCore.QCoreApplication.processEvents()

    def startMain(self, user, dataoptions, driver):
        #print('here we go')
        self.mainwind = mainGui.mainwindow(user, dataoptions, driver)
        #print('time to show')
        self.mainwind.show()

    def labbreakwork(self):
        locationstruct = PIEdataVARS.locations
        locationstruct.set_enddate(self.endcal.selectedDate().toPyDate())
        locationstruct.set_startdate(self.startcal.selectedDate().toPyDate())
        locationstruct.set_maxreturns(100000)
        locationurl = locationstruct.make_url()
        locationframe = PieHandler.goandget(self.driver, locationurl, locationstruct)
        locationframe['staffed_minutes'] = np.vectorize(functions.getMinutes)(locationframe['assumedDuration-difference'])
        locationframe['abb'] = locationframe['location-shortName'].apply(lambda x: functions.getAbb(x))
        locationframe = locationframe.groupby('abb')['staffed_minutes'].median().reset_index()

        tablelist = [locationframe.to_html()]
        picturelist = []

        outputfile = htmlbase.htmlbase('Stepout Medians', 'Stepout Medians', tablelist, picturelist)
        outputfile.makeHTML('StepoutMedians')