import functions
import seleniumHandlers
import dataconverter
import PieHandler
import datetime
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QDesktopWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QComboBox,
                             QPushButton, QApplication, QCalendarWidget)
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
import previewGui
import time

iconPath = functions.createPath('PIEcon.png')

class mainwindow(QWidget):

    def __init__(self, username, dataoptions, driver):
        self.username = username
        self.dataoptions = dataoptions
        self.driver = driver
        super().__init__()

        self.initUI()

    def initUI(self):
        x = 380
        y = 900
        leftspace = 20
        labellen = 70
        minspace = 5
        filterlen = x - leftspace - leftspace - labellen - minspace
        itemheight = 25
        callabelspace = 25
        spacer = 40
        labelspace = 60
        itemsbefore = 1

        self.resize(x, y)
        self.center()

        #add a username label and text box
        self.userlabel = QLabel(self)
        self.userlabel.move(x-285, y-25)
        self.userlabel.setText("Logged in as: " + self.username)
        self.userlabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.userlabel.resize(275, itemheight)

        #add the data type label and C C C combobox
        self.datatypelabel = QLabel(self)
        self.datatypelabel.move(leftspace, leftspace)
        self.datatypelabel.setText("Data Type: ")
        self.datatypelabel.resize(labellen, itemheight)

        self.datacombo = QComboBox(self)
        self.datacombo.addItems(self.dataoptions.keys())
        self.datacombo.move(leftspace + labellen + minspace, leftspace)
        self.datacombo.resize(filterlen, itemheight)
        self.datacombo.currentTextChanged.connect(self.combochange)

        itemsbefore+=1

        #add the filter label
        self.filterlabel = QLabel(self)
        self.filterlabel.move(0, 60)
        self.filterlabel.setText('Filters')
        #self.filterlabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.filterlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.filterlabel.resize(355, 25)

        #add all of the other filter things
        self.usernamelabel = QLabel(self)
        self.usernamelabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.usernamelabel.setText("Created By: ")
        self.usernamelabel.resize(labellen, itemheight)

        self.usernamecombo = QComboBox(self)
        #self.usernamecombo.addItems()
        self.usernamecombo.move(leftspace + labellen + minspace, leftspace + itemsbefore*spacer)
        self.usernamecombo.resize(filterlen, itemheight)

        itemsbefore+=1

        self.assignedlabel = QLabel(self)
        self.assignedlabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.assignedlabel.setText("Assigned To: ")
        self.assignedlabel.resize(labellen, itemheight)

        self.assignedcombo = QComboBox(self)
        #self.usernamecombo.addItems()
        self.assignedcombo.move(leftspace+labellen + minspace, leftspace + itemsbefore*spacer)
        self.assignedcombo.resize(filterlen, itemheight)

        itemsbefore+=1

        self.locationlabel = QLabel(self)
        self.locationlabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.locationlabel.setText("Location: ")
        self.locationlabel.resize(labellen, itemheight)

        self.locationcombo = QComboBox(self)
        #self.locationcombo.addItems(self.labs)
        self.locationcombo.move(leftspace+labellen + minspace, leftspace + itemsbefore*spacer)
        self.locationcombo.resize(filterlen, itemheight)

        itemsbefore+=1

        self.categorylabel = QLabel(self)
        self.categorylabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.categorylabel.setText("Category: ")
        self.categorylabel.resize(labellen, itemheight)

        self.categorycombo = QComboBox(self)
        #self.categorycombo.addItems(self.labs)
        self.categorycombo.move(leftspace+labellen + minspace, leftspace + itemsbefore*spacer)
        self.categorycombo.resize(filterlen, itemheight)

        itemsbefore+=1

        self.statuslabel = QLabel(self)
        self.statuslabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.statuslabel.setText("Status: ")
        self.statuslabel.resize(labellen, itemheight)

        self.statuscombo = QComboBox(self)
        #self.statuscombo.addItems(self.labs)
        self.statuscombo.move(leftspace+labellen + minspace, leftspace + itemsbefore*spacer)
        self.statuscombo.resize(filterlen, itemheight)

        itemsbefore+=1

        #add the startdate and end date calendars
        self.startcal = QCalendarWidget(self)
        self.startcal.move(x/2 - 157, leftspace + itemsbefore*spacer + callabelspace)
        self.startcal.setSelectedDate(datetime.date.today()-datetime.timedelta(days=30))
        self.startcal.clicked.connect(self.startdatechange)

        self.startlabel = QLabel(self)
        self.startlabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.startlabel.setText("Start Date: " + self.startcal.selectedDate().toString())
        self.startlabel.resize(labellen+150, itemheight)

        itemsbefore+=5.5

        self.endcal = QCalendarWidget(self)
        self.endcal.move(x/2 - 157, leftspace + itemsbefore*spacer + callabelspace)
        self.endcal.setSelectedDate(datetime.date.today())
        self.endcal.clicked.connect(self.enddatechange)

        self.endlabel = QLabel(self)
        self.endlabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.endlabel.setText("End Date: " + self.endcal.selectedDate().toString())
        self.endlabel.resize(labellen+150, itemheight)


        itemsbefore+=5.5

        #create the maxreturns things
        self.maxlabel = QLabel(self)
        self.maxlabel.move(leftspace, leftspace + itemsbefore*spacer)
        self.maxlabel.setText("Max Returns: ")
        self.maxlabel.resize(labellen, itemheight)

        self.maxbox = QLineEdit(self)
        self.maxbox.move(leftspace+labellen + minspace, leftspace + itemsbefore*spacer)
        self.maxbox.resize(filterlen, itemheight)
        self.maxbox.setText('1000')

        #add close button
        self.closebutton = QPushButton('Close', self)
        self.closebutton.move(leftspace,y-50)
        self.closebutton.clicked.connect(self.close)

        #add submit button
        self.submitbutton = QPushButton('Submit', self)
        self.submitbutton.move(x-99,y-50)
        self.submitbutton.clicked.connect(self.submititboy)

        self.combochange()

        self.setWindowTitle('PIEthon')
        self.setWindowIcon(QIcon(iconPath))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startdatechange(self):
        print(self.startcal.selectedDate())
        self.startlabel.setText("Start Date:  " + self.startcal.selectedDate().toString())

    def enddatechange(self):
        self.endlabel.setText("End Date:  " + self.endcal.selectedDate().toString())

    def combochange(self):
        datatype = self.dataoptions.get(self.datacombo.currentText())

        if (datatype is None):
            return

        if (not datatype.getuserdict() == {}):
            self.usernamecombo.clear()
            self.usernamecombo.addItems(datatype.getuserdict().keys())
            self.usernamecombo.setEnabled(True)
        else:
            self.usernamecombo.clear()
            self.usernamecombo.addItems(datatype.getuserdict().keys())
            self.usernamecombo.setEnabled(False)

        if (not datatype.getlabdict() == {}):
            self.locationcombo.clear()
            self.locationcombo.addItems(datatype.getlabdict().keys())
            self.locationcombo.setEnabled(True)
        else:
            self.locationcombo.clear()
            self.locationcombo.setEnabled(False)

        if (not datatype.getstatusdict() == []):
            self.statuscombo.clear()
            self.statuscombo.addItems(datatype.getstatusdict())
            self.statuscombo.setEnabled(True)
        else:
            self.statuscombo.clear()
            self.statuscombo.setEnabled(False)

        if (not datatype.getcategorydict() == {}):
            self.categorycombo.clear()
            self.categorycombo.addItems(datatype.getcategorydict().keys())
            self.categorycombo.setEnabled(True)
        else:
            self.categorycombo.clear()
            self.categorycombo.setEnabled(False)

        if (not datatype.getassigneddict() == {}):
            self.assignedcombo.clear()
            self.assignedcombo.addItems(datatype.getassigneddict().keys())
            self.assignedcombo.setEnabled(True)
        else:
            self.assignedcombo.clear()
            self.assignedcombo.setEnabled(False)

    def startPreview(self, dframe):
        self.mainwind = previewGui.preview(dframe)
        self.mainwind.show()

    def submititboy(self):
        datatype = self.dataoptions.get(self.datacombo.currentText())
        datatype.set_maxreturns(self.maxbox.text())
        datatype.set_enddate(self.endcal.selectedDate().toPyDate())
        datatype.set_startdate(self.startcal.selectedDate().toPyDate())
        datatype.set_username(self.usernamecombo.currentText())
        datatype.set_assignedto(self.assignedcombo.currentText())
        datatype.set_location(self.locationcombo.currentText())
        datatype.set_category(self.categorycombo.currentText())
        datatype.set_status(self.statuscombo.currentText())

        url = datatype.make_url()
        frameboy = PieHandler.goandget(self.driver, url, datatype)
        self.startPreview(frameboy)