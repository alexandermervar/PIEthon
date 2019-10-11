import functions
import PieHandler
import datetime
import importlib
import os
from PyQt5.QtWidgets import (QWidget, QToolTip, QDesktopWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QComboBox,
                             QPushButton, QApplication, QCalendarWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
import previewGui
import time

iconPath = functions.createPath('PIEcon.png')
font = 'BentonSans'
fontsize = 9

reports = [filename for filename in os.listdir('.') if filename.startswith("report") and filename.endswith(".py")]
reports = [x.strip('.py') for x in reports]

class mainwindow(QWidget):

    def __init__(self, username, dataoptions, driver):
        self.username = username
        self.dataoptions = dataoptions
        self.driver = driver
        super().__init__()

        self.initUI()

    def initUI(self):
        self.center()

        #add the data type label and C C C combobox
        self.datatypelabel = QLabel(self)
        self.datatypelabel.setText("Data Pull Type")
        self.datatypelabel.setAlignment(QtCore.Qt.AlignCenter)

        self.datacombo = QComboBox(self)
        #Sorted by alphabet
        self.datacombo.addItems(sorted(self.dataoptions.keys()))
        self.datacombo.currentTextChanged.connect(self.combochange)

        #itemsbefore+=1

        #add the filter label
        self.filterlabel = QLabel(self)
        self.filterlabel.setText('Filters')
        self.filterlabel.setAlignment(QtCore.Qt.AlignCenter)

        #add all of the other filter things
        self.usernamelabel = QLabel(self)
        self.usernamelabel.setText("Created By: ")

        self.usernamecombo = QComboBox(self)

        self.assignedlabel = QLabel(self)
        self.assignedlabel.setText("Assigned To: ")

        self.assignedcombo = QComboBox(self)

        self.locationlabel = QLabel(self)
        self.locationlabel.setText("Location: ")

        self.locationcombo = QComboBox(self)

        #itemsbefore+=1

        self.categorylabel = QLabel(self)
        self.categorylabel.setText("Category: ")

        self.categorycombo = QComboBox(self)
        self.statuslabel = QLabel(self)
        self.statuslabel.setText("Status: ")

        self.statuscombo = QComboBox(self)

        #add the startdate and end date calendars
        self.startcal = QCalendarWidget(self)
        self.startcal.setSelectedDate(datetime.date.today()-datetime.timedelta(days=30))
        self.startcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.startcal.setGridVisible(True)
        self.startcal.clicked.connect(self.startdatechange)

        self.startlabel = QLabel(self)
        self.startlabel.setText("Start Date: " + self.startcal.selectedDate().toString())

        self.endcal = QCalendarWidget(self)
        self.endcal.setSelectedDate(datetime.date.today())
        self.endcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.endcal.setGridVisible(True)
        self.endcal.clicked.connect(self.enddatechange)

        self.endlabel = QLabel(self)
        self.endlabel.setText("End Date: " + self.endcal.selectedDate().toString())

        #create the maxreturns things
        self.maxlabel = QLabel(self)
        self.maxlabel.setText("Max Returns: ")
        self.maxlabel.hide()

        self.maxbox = QLineEdit(self)
        self.maxbox.setText('10000000')
        self.maxbox.hide()

        #add close button
        self.closebutton = QPushButton('Close', self)
        self.closebutton.clicked.connect(self.close)

        #add submit button
        self.submitbutton = QPushButton('Submit', self)
        self.submitbutton.clicked.connect(self.submititboy)

        self.tabs = QTabWidget()

        #everything for the data pull tab
        self.datapulltab = QWidget()

        datatypelabhbox = QHBoxLayout()
        datatypelabhbox.addWidget(self.datatypelabel)

        datatypehbox = QHBoxLayout()
        datatypehbox.addWidget(self.datacombo)

        filternamehbox = QHBoxLayout()
        filternamehbox.addWidget(self.filterlabel)

        usernamehbox = QHBoxLayout()
        usernamehbox.addWidget(self.usernamelabel)

        assignedhbox = QHBoxLayout()
        assignedhbox.addWidget(self.assignedlabel)

        locationhbox = QHBoxLayout()
        locationhbox.addWidget(self.locationlabel)

        categoryhbox = QHBoxLayout()
        categoryhbox.addWidget(self.categorylabel)

        statushbox = QHBoxLayout()
        statushbox.addWidget(self.statuslabel)

        dataselectlayout = QVBoxLayout()
        dataselectlayout.addLayout(datatypelabhbox)
        dataselectlayout.addLayout(datatypehbox)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        dataselectlayout.addSpacerItem(verticalSpacer)
        dataselectlayout.addLayout(filternamehbox)
        dataselectlayout.addLayout(usernamehbox)
        dataselectlayout.addWidget(self.usernamecombo)
        dataselectlayout.addLayout(assignedhbox)
        dataselectlayout.addWidget(self.assignedcombo)
        dataselectlayout.addLayout(locationhbox)
        dataselectlayout.addWidget(self.locationcombo)
        dataselectlayout.addLayout(categoryhbox)
        dataselectlayout.addWidget(self.categorycombo)
        dataselectlayout.addLayout(statushbox)
        dataselectlayout.addWidget(self.statuscombo)
        dataselectlayout.setSpacing(3)
        dataselectlayout.addStretch(1)

        calendarlayout = QVBoxLayout()
        calendarlayout.addWidget(self.startlabel)
        calendarlayout.addWidget(self.startcal)
        calendarlayout.addWidget(self.endlabel)
        calendarlayout.addWidget(self.endcal)
        calendarlayout.setSpacing(3)
        calendarlayout.addStretch(1)

        datapullhlayout = QHBoxLayout()
        datapullhlayout.addLayout(dataselectlayout)
        datapullhlayout.addLayout(calendarlayout)

        self.datapulltab.setLayout(datapullhlayout)

        #Report things?

        self.reporttab = QWidget()

        self.startrepcal = QCalendarWidget(self)
        self.startrepcal.setSelectedDate(datetime.date.today()-datetime.timedelta(days=30))
        self.startrepcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.startrepcal.clicked.connect(self.startrepdatechange)

        self.startreplabel = QLabel(self)
        self.startreplabel.setText("Start Date: " + self.startrepcal.selectedDate().toString())

        self.endrepcal = QCalendarWidget(self)
        self.endrepcal.setSelectedDate(datetime.date.today())
        self.endrepcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.endrepcal.clicked.connect(self.endrepdatechange)

        self.endreplabel = QLabel(self)
        self.endreplabel.setText("End Date: " + self.endrepcal.selectedDate().toString())

        self.reporttypelabel = QLabel(self)
        self.reporttypelabel.setText('Report Type')

        self.reportdrop = QComboBox(self)
        self.reportdrop.addItems([repo.strip('report') for repo in reports])

        reportreportlayout = QHBoxLayout()
        #reportreportlayout.addStretch(1)
        reportreportlayout.setAlignment(QtCore.Qt.AlignLeft)
        reportreportlayout.addWidget(self.reporttypelabel)
        reportreportlayout.addWidget(self.reportdrop)

        reportcallablayout = QHBoxLayout()
        reportcallablayout.addWidget(self.startreplabel)
        reportcallablayout.addWidget(self.endreplabel)

        reportcallayout = QHBoxLayout()
        reportcallayout.addWidget(self.startrepcal)
        reportcallayout.addWidget(self.endrepcal)

        reportvlayout = QVBoxLayout()
        reportvlayout.addLayout(reportreportlayout)
        reportvlayout.addSpacing(10)
        reportvlayout.addLayout(reportcallablayout)
        reportvlayout.addLayout(reportcallayout)

        self.reporttab.setLayout(reportvlayout)

        self.tabs.addTab(self.datapulltab,"Data Pull")
        self.tabs.addTab(self.reporttab, "Reporting")

        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.closebutton)
        buttonlayout.addWidget(self.submitbutton)

        self.statuslabel = QLabel(self)
        self.statuslabel.setText("Ready")
        self.statuslabel.setAlignment(QtCore.Qt.AlignRight)

        outerlayout = QVBoxLayout()
        outerlayout.addWidget(self.tabs)
        outerlayout.addLayout(buttonlayout)
        outerlayout.addWidget(self.statuslabel)
        self.setLayout(outerlayout)

        self.combochange()
        self.setWindowTitle('PIEthon: Logged In As ' + self.username)
        self.setWindowIcon(QIcon(iconPath))

        #style things
        #self.setStyleSheet("background-color:white;")
        self.datatypelabel.setFont(QFont(font, fontsize))
        self.datacombo.setFont(QFont(font, fontsize))
        self.filterlabel.setFont(QFont(font, fontsize))
        self.usernamelabel.setFont(QFont(font, fontsize))
        self.usernamecombo.setFont(QFont(font, fontsize))
        self.assignedlabel.setFont(QFont(font, fontsize))
        self.assignedcombo.setFont(QFont(font, fontsize))
        self.locationlabel.setFont(QFont(font, fontsize))
        self.locationcombo.setFont(QFont(font, fontsize))
        self.categorylabel.setFont(QFont(font, fontsize))
        self.categorycombo.setFont(QFont(font, fontsize))
        self.statuslabel.setFont(QFont(font, fontsize))
        self.statuscombo.setFont(QFont(font, fontsize))
        self.startlabel.setFont(QFont(font, fontsize))
        self.endlabel.setFont(QFont(font, fontsize))
        self.submitbutton.setFont(QFont(font, fontsize))
        self.submitbutton.setStyleSheet("background-color:rgb(153,0,0); color:white;")
        self.closebutton.setFont(QFont(font, fontsize))
        self.closebutton.setStyleSheet("background-color:rgb(153,0,0); color:white;")
        self.startcal.setStyleSheet('QSpinBox{'
                                  'background-color:rgb(153,0,0);'
                                  'selection-background-color: rgb(153, 0, 0);'
                                  'selection-color: white;'
                                  'color:white;}'

                                  'QToolButton{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'

                                  'QWidget#qt_calendar_navigationbar{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'

                                  'QMenu{'
                                  'background-color:rgb(153,0,0);}'
                                  )
        self.endcal.setStyleSheet('QSpinBox{'
                                  'background-color:rgb(153,0,0);'
                                  'selection-background-color: rgb(153, 0, 0);'
                                  'selection-color: white;'
                                  'color:white;}'
                                  
                                  'QToolButton{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'
                                  
                                  'QWidget#qt_calendar_navigationbar{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'
                                  
                                  'QMenu{'
                                  'background-color:rgb(153,0,0);}'
                                  )
        """
        self.endcal.setStyleSheet('QWidget#qt_calendar_navigationbar{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'

                                  'QMenu{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'

                                  'QSpinBox{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'

                                  'QWidget{'
                                  'alternate-background-color:rgb(153,0,0);'
                                  'color:white;}'

                                  'QPrevNextCalButton#qt_calendar_prevmonth{'
                                  'alternate-background-color:rgb(153,0,0);'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'

                                  'QMenu{'
                                  'background-color:rgb(153,0,0);'
                                  'color:white;}'
                                  )
        """
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

    def startdatechange(self):
        self.startlabel.setText("Start Date:  " + self.startcal.selectedDate().toString())

    def enddatechange(self):
        self.endlabel.setText("End Date:  " + self.endcal.selectedDate().toString())

    def startrepdatechange(self):
        self.startreplabel.setText("Start Date:  " + self.startrepcal.selectedDate().toString())

    def endrepdatechange(self):
        self.endreplabel.setText("End Date:  " + self.endrepcal.selectedDate().toString())

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
        self.mainwind = previewGui.preview(dframe, self.datacombo.currentText(), self.startcal.selectedDate().toPyDate(), self.endcal.selectedDate().toPyDate())
        self.mainwind.show()

    def submititboy(self):
        if (self.tabs.currentIndex() == 0):

            self.statusUpdate("Preparing Data Structure")

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

            self.statusUpdate("Pulling from Pie")

            frameboy = PieHandler.goandget(self.driver, url, datatype)

            self.statusUpdate("Complete")

            self.startPreview(frameboy)
        else:
            self.statusUpdate("Starting Report")
            i = importlib.import_module('report' + self.reportdrop.currentText())
            i.main('start', 'end', self.statuslabel)
