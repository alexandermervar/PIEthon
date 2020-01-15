from py import PieHandler, previewGui,report, functions
from datetime import date, timedelta, datetime
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLineEdit, QLabel, QComboBox,
                             QPushButton, QCalendarWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QCoreApplication, QThread
from os.path import exists, expanduser
from os import mkdir

class mainwindow(QWidget):

    def __init__(self, username, dataoptions, driver, semesters):
        self.username = username
        self.dataoptions = dataoptions
        self.driver = driver
        self.semesters = semesters
        self.subThread = submitThread(self)
        self.subThread.finished.connect(self.completed)
        super().__init__()

        self.initUI()

    def initUI(self):
        self.center()

        #add the data type label and C C C combobox
        self.datatypelabel = QLabel(self)
        self.datatypelabel.setText("Data Pull Type")
        self.datatypelabel.setAlignment(Qt.AlignCenter)

        self.datacombo = QComboBox(self)
        #Sorted by alphabet
        self.datacombo.addItems(sorted(self.dataoptions.keys()))
        self.datacombo.currentTextChanged.connect(self.combochange)

        #add the filter label
        self.filterlabel = QLabel(self)
        self.filterlabel.setText('Filters')
        self.filterlabel.setAlignment(Qt.AlignCenter)

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

        self.categorylabel = QLabel(self)
        self.categorylabel.setText("Category: ")

        self.categorycombo = QComboBox(self)
        self.statuslabels = QLabel(self)
        self.statuslabels.setText("Status: ")

        self.statuscombo = QComboBox(self)

        #add the startdate and end date calendars
        self.startcal = QCalendarWidget(self)
        self.startcal.setSelectedDate(date.today()-timedelta(days=30))
        self.startcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.startcal.setGridVisible(True)
        self.startcal.clicked.connect(self.startdatechange)

        self.startlabel = QLabel(self)
        self.startlabel.setText("Start Date: " + self.startcal.selectedDate().toString())

        self.startdroplabel = QLabel(self)
        self.startdroplabel.setText('Autoselect start of :  ')
        self.startdroplabel.setObjectName('desctext')

        self.startcombo = QComboBox(self)
        self.startcombo.addItems(self.semesters.keys())
        self.startcombo.currentTextChanged.connect(self.startcomboselect)

        self.endcal = QCalendarWidget(self)
        self.endcal.setSelectedDate(date.today())
        self.endcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.endcal.setGridVisible(True)
        self.endcal.clicked.connect(self.enddatechange)

        self.endlabel = QLabel(self)
        self.endlabel.setText("End Date: " + self.endcal.selectedDate().toString())

        self.enddroplabel = QLabel(self)
        self.enddroplabel.setText('Autoselect end of :  ')
        self.enddroplabel.setObjectName('desctext')

        self.endcombo = QComboBox(self)
        self.endcombo.addItems(self.semesters.keys())
        self.endcombo.currentTextChanged.connect(self.endcomboselect)

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
        self.submitbutton.clicked.connect(self.subThread.start)

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
        statushbox.addWidget(self.statuslabels)

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

        startdrophlayout = QHBoxLayout()
        startdrophlayout.addWidget(self.startdroplabel)
        startdrophlayout.addWidget(self.startcombo)
        startdrophlayout.setSpacing(0)
        startdrophlayout.addStretch(0)

        enddropylayout = QHBoxLayout()
        enddropylayout.addWidget(self.enddroplabel)
        enddropylayout.addWidget(self.endcombo)
        enddropylayout.setSpacing(0)
        enddropylayout.addStretch(0)

        calendarlayout = QVBoxLayout()
        calendarlayout.addWidget(self.startlabel)
        calendarlayout.addLayout(startdrophlayout)
        calendarlayout.addWidget(self.startcal)
        calendarlayout.addSpacing(10)
        calendarlayout.addWidget(self.endlabel)
        calendarlayout.addLayout(enddropylayout)
        calendarlayout.addWidget(self.endcal)
        calendarlayout.setSpacing(3)
        calendarlayout.addStretch(1)

        datapullhlayout = QHBoxLayout()
        datapullhlayout.addLayout(dataselectlayout)
        datapullhlayout.addSpacing(10)
        datapullhlayout.addLayout(calendarlayout)

        datapullvlayout =QVBoxLayout()
        datapullvlayout.addSpacing(15)
        datapullvlayout.addLayout(datapullhlayout)

        self.datapulltab.setLayout(datapullvlayout)

        #Report things?

        self.reporttab = QWidget()

        self.startrepcal = QCalendarWidget(self)
        self.startrepcal.setSelectedDate(date.today()-timedelta(days=30))
        self.startrepcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.startrepcal.setGridVisible(True)
        self.startrepcal.clicked.connect(self.startrepdatechange)

        self.startreplabel = QLabel(self)
        self.startreplabel.setText("Start Date: " + self.startrepcal.selectedDate().toString())

        self.endrepcal = QCalendarWidget(self)
        self.endrepcal.setSelectedDate(date.today())
        self.endrepcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.endrepcal.setGridVisible(True)
        self.endrepcal.clicked.connect(self.endrepdatechange)

        self.endreplabel = QLabel(self)
        self.endreplabel.setText("End Date: " + self.endrepcal.selectedDate().toString())

        self.reporttypelabel = QLabel(self)
        self.reporttypelabel.setText('Report Type')
        self.reporttypelabel.setAlignment(Qt.AlignCenter)

        self.reportdrop = QComboBox(self)
        self.reportdrop.addItems([x.name for x in report.report_list])
        self.reportdrop.currentTextChanged.connect(self.reportcombochange)

        self.reportactivelabel = QLabel(self)
        self.reportactivelabel.setText("Active")

        self.reportactive = QLabel(self)
        self.reportactive.setText("")
        self.reportactive.setObjectName('desctext')

        self.reportauthorlabel = QLabel(self)
        self.reportauthorlabel.setText("Author")

        self.reportauthor = QLabel(self)
        self.reportauthor.setText("")
        self.reportauthor.setObjectName('desctext')

        self.reportdesclabel = QLabel(self)
        self.reportdesclabel.setText("Report Description")

        self.descbox = QLabel(self)
        self.descbox.setText("")
        self.descbox.setWordWrap(True)
        self.descbox.setFixedWidth(self.usernamecombo.frameGeometry().width()+53)
        self.descbox.setObjectName('desctext')

        self.startrepdroplabel = QLabel(self)
        self.startrepdroplabel.setObjectName('desctext')
        self.startrepdroplabel.setText('Autoselect start of :  ')

        self.startrepcombo = QComboBox(self)
        self.startrepcombo.addItems(self.semesters.keys())
        self.startrepcombo.currentTextChanged.connect(self.startrepcomboselect)

        self.enddropreplabel = QLabel(self)
        self.enddropreplabel.setText('Autoselect end of :  ')
        self.enddropreplabel.setObjectName('desctext')

        self.endrepcombo = QComboBox(self)
        self.endrepcombo.addItems(self.semesters.keys())
        self.endrepcombo.currentTextChanged.connect(self.endrepcomboselect)

        newreportlayout = QVBoxLayout()

        newreportlayout.addWidget(self.reporttypelabel)
        newreportlayout.addWidget(self.reportdrop)
        verticalSpacernew = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        newreportlayout.addSpacerItem(verticalSpacernew)
        newreportlayout.addWidget(self.reportauthorlabel)
        newreportlayout.addWidget(self.reportauthor)
        verticalSpacernewest = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        newreportlayout.addSpacerItem(verticalSpacernewest)
        newreportlayout.addWidget(self.reportactivelabel)
        newreportlayout.addWidget(self.reportactive)
        verticalSpacernewer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        newreportlayout.addSpacerItem(verticalSpacernewer)
        newreportlayout.addWidget(self.reportdesclabel)
        newreportlayout.addWidget(self.descbox)
        newreportlayout.setSpacing(3)
        newreportlayout.addStretch(1)

        startrepdrophlayout = QHBoxLayout()
        startrepdrophlayout.addWidget(self.startrepdroplabel)
        startrepdrophlayout.addWidget(self.startrepcombo)
        startrepdrophlayout.setSpacing(0)
        startrepdrophlayout.addStretch(0)

        endrepdropylayout = QHBoxLayout()
        endrepdropylayout.addWidget(self.enddropreplabel)
        endrepdropylayout.addWidget(self.endrepcombo)
        endrepdropylayout.setSpacing(0)
        endrepdropylayout.addStretch(0)

        repcallayout = QVBoxLayout()
        repcallayout.addWidget(self.startreplabel)
        repcallayout.addLayout(startrepdrophlayout)
        repcallayout.addWidget(self.startrepcal)
        repcallayout.addSpacing(10)
        repcallayout.addWidget(self.endreplabel)
        repcallayout.addLayout(endrepdropylayout)
        repcallayout.addWidget(self.endrepcal)
        repcallayout.setSpacing(3)
        repcallayout.addStretch(1)

        reportouterlayout = QHBoxLayout()
        reportouterlayout.addLayout(newreportlayout)
        reportouterlayout.addSpacing(10)
        reportouterlayout.addLayout(repcallayout)

        reportouterlayoutout = QVBoxLayout()
        reportouterlayoutout.addSpacing(15)
        reportouterlayoutout.addLayout(reportouterlayout)
        self.reporttab.setLayout(reportouterlayoutout)

        self.tabs.addTab(self.datapulltab,"Data Pull")
        self.tabs.addTab(self.reporttab, "Reporting")

        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.closebutton)
        buttonlayout.addWidget(self.submitbutton)

        self.statuslabel = QLabel(self)
        self.statuslabel.setText("Ready")
        self.statuslabel.setObjectName('statuslabel')
        self.statuslabel.setAlignment(Qt.AlignRight)

        outerlayout = QVBoxLayout()
        outerlayout.addWidget(self.tabs)
        outerlayout.addSpacing(15)
        outerlayout.addLayout(buttonlayout)
        outerlayout.addWidget(self.statuslabel)
        self.setLayout(outerlayout)

        self.current_report = False
        self.dframe = False

        self.reportcombochange()
        self.combochange()
        self.setWindowTitle('PIEthon: logged in as ' + self.username)
        self.setWindowIcon(QIcon(functions.resource_path('resources\\PIEcon.png')))

        #style things
        self.setStyleSheet(open(functions.resource_path("resources\\iu_stylesheet.qss"), "r").read())
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def statusUpdate(self, newstat):
        #print('in status update')
        self.statuslabel.setText(newstat)
        QCoreApplication.processEvents()

    def startdatechange(self):
        self.startcombo.setCurrentIndex(0)
        self.startlabel.setText("Start Date:  " + self.startcal.selectedDate().toString())
        self.startreplabel.setText("Start Date:  " + self.startcal.selectedDate().toString())
        self.startrepcal.setSelectedDate(self.startcal.selectedDate())

    def enddatechange(self):
        self.endcombo.setCurrentIndex(0)
        self.endlabel.setText("End Date:  " + self.endcal.selectedDate().toString())
        self.endreplabel.setText("End Date:  " + self.endcal.selectedDate().toString())
        self.endrepcal.setSelectedDate(self.endcal.selectedDate())

    def startrepdatechange(self):
        self.startrepcombo.setCurrentIndex(0)
        self.startreplabel.setText("Start Date:  " + self.startrepcal.selectedDate().toString())
        self.startlabel.setText("Start Date:  " + self.startrepcal.selectedDate().toString())
        self.startcal.setSelectedDate(self.startrepcal.selectedDate())

    def endrepdatechange(self):
        self.endrepcombo.setCurrentIndex(0)
        self.endreplabel.setText("End Date:  " + self.endrepcal.selectedDate().toString())
        self.endlabel.setText("End Date:  " + self.endrepcal.selectedDate().toString())
        self.endcal.setSelectedDate(self.endrepcal.selectedDate())

    def startcomboselect(self):
        self.startrepcombo.setCurrentIndex(self.startcombo.currentIndex())
        conv = self.semesters[self.startcombo.currentText()].getStart()
        if conv == '':
            return
        self.startlabel.setText("Start Date:  " + conv.strftime('%a %b %d %Y'))
        self.startreplabel.setText("Start Date:  " + conv.strftime('%a %b %d %Y'))
        self.startcal.setSelectedDate(conv)
        self.startrepcal.setSelectedDate(conv)

    def endcomboselect(self):
        self.endrepcombo.setCurrentIndex(self.endcombo.currentIndex())
        conv = self.semesters[self.endcombo.currentText()].getEnd()
        if conv == '':
            return
        self.endlabel.setText("End Date:  " + conv.strftime('%a %b %d %Y'))
        self.endreplabel.setText("End Date:  " + conv.strftime('%a %b %d %Y'))
        self.endcal.setSelectedDate(conv)
        self.endrepcal.setSelectedDate(conv)

    def startrepcomboselect(self):
        self.startcombo.setCurrentIndex(self.startrepcombo.currentIndex())
        conv = self.semesters[self.startrepcombo.currentText()].getStart()
        if conv == '':
            return
        self.startreplabel.setText("Start Date:  " + conv.strftime('%a %b %d %Y'))
        self.startlabel.setText("Start Date:  " + conv.strftime('%a %b %d %Y'))
        self.startrepcal.setSelectedDate(conv)
        self.startcal.setSelectedDate(conv)

    def endrepcomboselect(self):
        self.endcombo.setCurrentIndex(self.endrepcombo.currentIndex())
        conv = self.semesters[self.endrepcombo.currentText()].getEnd()
        if conv == '':
            return
        self.endreplabel.setText("End Date:  " + conv.strftime('%a %b %d %Y'))
        self.endlabel.setText("End Date:  " + conv.strftime('%a %b %d %Y'))
        self.endrepcal.setSelectedDate(conv)
        self.endcal.setSelectedDate(conv)

    def reportcombochange(self):
        self.current_report = report.report_list[self.reportdrop.currentIndex()]
        self.descbox.setText(self.current_report.description)
        self.reportactive.setText(str(self.current_report.active))
        self.reportauthor.setText(str(self.current_report.author))

    def combochange(self):
        datatype = self.dataoptions.get(self.datacombo.currentText())

        if (datatype is None):
            return

        if (len(datatype.createdbyDict) > 1):
            self.usernamecombo.clear()
            self.usernamecombo.addItems(datatype.createdbyDict.keys())
            self.usernamecombo.setEnabled(True)
        else:
            self.usernamecombo.clear()
            self.usernamecombo.setEnabled(False)

        if (len(datatype.locationDict) > 1):
            self.locationcombo.clear()
            self.locationcombo.addItems(datatype.locationDict.keys())
            self.locationcombo.setEnabled(True)
        else:
            self.locationcombo.clear()
            self.locationcombo.setEnabled(False)

        if (len(datatype.statusDict) > 1):
            self.statuscombo.clear()
            self.statuscombo.addItems(datatype.statusDict)
            self.statuscombo.setEnabled(True)
        else:
            self.statuscombo.clear()
            self.statuscombo.setEnabled(False)

        if (len(datatype.categoryDict) > 1):
            self.categorycombo.clear()
            self.categorycombo.addItems(datatype.categoryDict.keys())
            self.categorycombo.setEnabled(True)
        else:
            self.categorycombo.clear()
            self.categorycombo.setEnabled(False)

        if (len(datatype.assignedToDict) > 1):
            self.assignedcombo.clear()
            self.assignedcombo.addItems(datatype.assignedToDict.keys())
            self.assignedcombo.setEnabled(True)
        else:
            self.assignedcombo.clear()
            self.assignedcombo.setEnabled(False)

    def completed(self):
        if self.datecheck() or self.dframe is False:
            return
        if(self.tabs.currentIndex()==0):
            self.mainwind = previewGui.preview(self.dframe, self.datacombo.currentText(), self.startcal.selectedDate().toPyDate(), self.endcal.selectedDate().toPyDate())
            self.mainwind.show()
        self.dframe = False
        self.statusUpdate('Ready')

    def datecheck(self):
        return ((self.startcal.selectedDate().daysTo(self.endcal.selectedDate()) < 0) or (self.startrepcal.selectedDate().daysTo(self.endrepcal.selectedDate()) < 0))

class submitThread(QThread):

    def __init__(self, window):
        self.window = window
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        if self.window.datecheck():
            self.window.statusUpdate("ERROR: Start date is after end date")
            self.window.statuslabel.setStyleSheet("color: red;")
            return
        self.window.setDisabled(True)
        self.window.statuslabel.setStyleSheet("color: black;")
        if (self.window.tabs.currentIndex() == 0):
            self.window.dframe = False
            self.window.statusUpdate("Preparing Data Structure")

            datatype = self.window.dataoptions.get(self.window.datacombo.currentText())
            datatype.endDate = self.window.endcal.selectedDate().toPyDate()
            datatype.startDate = self.window.startcal.selectedDate().toPyDate()
            datatype.createdby = self.window.usernamecombo.currentText()
            datatype.assignedTo = self.window.assignedcombo.currentText()
            datatype.location = self.window.locationcombo.currentText()
            datatype.category = self.window.categorycombo.currentText()
            datatype.status = self.window.statuscombo.currentText()
            url = datatype.urlList()
            datatype.reset()

            self.window.statusUpdate("Pulling from Pie")
            frameboy = PieHandler.goandget(self.window.driver, url, datatype)
            if frameboy is False:
                self.window.statusUpdate("ERROR: No results returned")
                self.window.statuslabel.setStyleSheet("color: red;")
                self.window.setDisabled(False)
                return
            else:
                self.window.statusUpdate("Post-processing...")
                frameboy = datatype.postFilter(frameboy, self.window.semesters)
                self.window.statusUpdate("Complete")
                self.window.dframe = frameboy
                self.window.setDisabled(False)
        else:
            if self.window.current_report.active is False:
                self.window.statusUpdate("ERROR: Report is not active")
                self.window.statuslabel.setStyleSheet("color: red;")
                self.window.setDisabled(False)
                return

            if not exists(expanduser('~/Documents/PIEthon')):
                mkdir(expanduser('~/Documents/PIEthon'))
            if not exists(expanduser('~/Documents/PIEthon/reports')):
                mkdir(expanduser('~/Documents/PIEthon/reports'))
            if not exists(expanduser('~/Documents/PIEthon/figures')):
                mkdir(expanduser('~/Documents/PIEthon/figures'))

            self.window.statusUpdate("Starting Report")
            self.window.current_report.run_main(self.window.driver,self.window.startrepcal.selectedDate().toPyDate(), self.window.endrepcal.selectedDate().toPyDate(), self.window.statuslabel)
            self.window.setDisabled(False)
