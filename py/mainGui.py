from py import functions, PieHandler, previewGui
import datetime
import importlib
import os
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLineEdit, QLabel, QComboBox, QMessageBox,
                             QPushButton, QCalendarWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

iconPath = functions.createPath('resources//PIEcon.png')

reports = [filename for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))) if filename.startswith("report") and filename.endswith(".py")]
reports = [x.replace('.py','') for x in reports]

#https://nikolak.com/pyqt-threading-tutorial/

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
        self.datatypelabel.setAlignment(QtCore.Qt.AlignCenter)

        self.datacombo = QComboBox(self)
        #Sorted by alphabet
        self.datacombo.addItems(sorted(self.dataoptions.keys()))
        self.datacombo.currentTextChanged.connect(self.combochange)

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

        self.categorylabel = QLabel(self)
        self.categorylabel.setText("Category: ")

        self.categorycombo = QComboBox(self)
        self.statuslabels = QLabel(self)
        self.statuslabels.setText("Status: ")

        self.statuscombo = QComboBox(self)

        #add the startdate and end date calendars
        self.startcal = QCalendarWidget(self)
        self.startcal.setSelectedDate(datetime.date.today()-datetime.timedelta(days=30))
        self.startcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.startcal.setGridVisible(True)
        self.startcal.clicked.connect(self.startdatechange)

        self.startlabel = QLabel(self)
        self.startlabel.setText("Start Date: " + self.startcal.selectedDate().toString())

        self.startdroplabel = QLabel(self)
        self.startdroplabel.setText('Autoselect start of :  ')

        self.startcombo = QComboBox(self)
        self.startcombo.addItems(self.semesters.keys())
        self.startcombo.currentTextChanged.connect(self.startcomboselect)

        self.endcal = QCalendarWidget(self)
        self.endcal.setSelectedDate(datetime.date.today())
        self.endcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.endcal.setGridVisible(True)
        self.endcal.clicked.connect(self.enddatechange)

        self.endlabel = QLabel(self)
        self.endlabel.setText("End Date: " + self.endcal.selectedDate().toString())

        self.enddroplabel = QLabel(self)
        self.enddroplabel.setText('Autoselect end of :  ')

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
        self.startrepcal.setSelectedDate(datetime.date.today()-datetime.timedelta(days=30))
        self.startrepcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.startrepcal.setGridVisible(True)
        self.startrepcal.clicked.connect(self.startrepdatechange)

        self.startreplabel = QLabel(self)
        self.startreplabel.setText("Start Date: " + self.startrepcal.selectedDate().toString())

        self.endrepcal = QCalendarWidget(self)
        self.endrepcal.setSelectedDate(datetime.date.today())
        self.endrepcal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.endrepcal.setGridVisible(True)
        self.endrepcal.clicked.connect(self.endrepdatechange)

        self.endreplabel = QLabel(self)
        self.endreplabel.setText("End Date: " + self.endrepcal.selectedDate().toString())

        self.reporttypelabel = QLabel(self)
        self.reporttypelabel.setText('Report Type')
        self.reporttypelabel.setAlignment(QtCore.Qt.AlignCenter)

        self.reportdrop = QComboBox(self)
        self.reportdrop.addItems([repo.replace('report','') for repo in reports])
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
        self.descbox.setFixedWidth(self.usernamecombo.frameGeometry().width()+54)
        self.descbox.setObjectName('desctext')

        self.startrepdroplabel = QLabel(self)
        self.startrepdroplabel.setText('Autoselect start of :  ')

        self.startrepcombo = QComboBox(self)
        self.startrepcombo.addItems(self.semesters.keys())
        self.startrepcombo.currentTextChanged.connect(self.startrepcomboselect)

        self.enddropreplabel = QLabel(self)
        self.enddropreplabel.setText('Autoselect end of :  ')

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
        self.statuslabel.setAlignment(QtCore.Qt.AlignRight)

        outerlayout = QVBoxLayout()
        outerlayout.addWidget(self.tabs)
        outerlayout.addSpacing(15)
        outerlayout.addLayout(buttonlayout)
        outerlayout.addWidget(self.statuslabel)
        self.setLayout(outerlayout)

        self.reportcombochange()
        self.combochange()
        self.setWindowTitle('PIEthon: logged in as ' + self.username)
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

    def startdatechange(self):
        self.startcombo.setCurrentIndex(0)
        self.startlabel.setText("Start Date:  " + self.startcal.selectedDate().toString())

    def enddatechange(self):
        self.endcombo.setCurrentIndex(0)
        self.endlabel.setText("End Date:  " + self.endcal.selectedDate().toString())

    def startrepdatechange(self):
        self.startrepcombo.setCurrentIndex(0)
        self.startreplabel.setText("Start Date:  " + self.startrepcal.selectedDate().toString())

    def endrepdatechange(self):
        self.endrepcombo.setCurrentIndex(0)
        self.endreplabel.setText("End Date:  " + self.endrepcal.selectedDate().toString())

    def startcomboselect(self):
        sempick = self.semesters[self.startcombo.currentText()].getStart()[:10]
        if sempick == '':
            return
        conv = datetime.datetime.strptime(sempick, '%Y-%m-%d')
        self.startlabel.setText("Start Date:  " + conv.strftime('%a %b %d %Y'))
        self.startcal.setSelectedDate(conv)

    def endcomboselect(self):
        sempick = self.semesters[self.endcombo.currentText()].getEnd()[:10]
        if sempick == '':
            return
        conv = datetime.datetime.strptime(sempick, '%Y-%m-%d')
        self.endlabel.setText("End Date:  " + conv.strftime('%a %b %d %Y'))
        self.endcal.setSelectedDate(conv)

    def startrepcomboselect(self):
        sempick = self.semesters[self.startrepcombo.currentText()].getStart()[:10]
        if sempick == '':
            return
        conv = datetime.datetime.strptime(sempick, '%Y-%m-%d')
        self.startreplabel.setText("Start Date:  " + conv.strftime('%a %b %d %Y'))
        self.startrepcal.setSelectedDate(conv)

    def endrepcomboselect(self):
        sempick = self.semesters[self.endrepcombo.currentText()].getEnd()[:10]
        if sempick == '':
            return
        conv = datetime.datetime.strptime(sempick, '%Y-%m-%d')
        self.endreplabel.setText("End Date:  " + conv.strftime('%a %b %d %Y'))
        self.endrepcal.setSelectedDate(conv)

    def reportcombochange(self):
        i = importlib.import_module('py.report' + self.reportdrop.currentText())
        self.descbox.setText(i.description)
        self.reportactive.setText(str(i.active))
        self.reportauthor.setText(str(i.author))

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

    def completed(self):
        self.mainwind = previewGui.preview(self.dframe, self.datacombo.currentText(), self.startcal.selectedDate().toPyDate(), self.endcal.selectedDate().toPyDate())
        self.mainwind.show()

class submitThread(QtCore.QThread):

    def __init__(self, window):
        self.window = window
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.window.setDisabled(True)
        if (self.window.tabs.currentIndex() == 0):
            self.window.statusUpdate("Preparing Data Structure")

            datatype = self.window.dataoptions.get(self.window.datacombo.currentText())
            datatype.set_maxreturns(self.window.maxbox.text())
            datatype.set_enddate(self.window.endcal.selectedDate().toPyDate())
            datatype.set_startdate(self.window.startcal.selectedDate().toPyDate())
            datatype.set_username(self.window.usernamecombo.currentText())
            datatype.set_assignedto(self.window.assignedcombo.currentText())
            datatype.set_location(self.window.locationcombo.currentText())
            datatype.set_category(self.window.categorycombo.currentText())
            datatype.set_status(self.window.statuscombo.currentText())
            url = datatype.make_url()

            self.window.statusUpdate("Pulling from Pie")

            frameboy = PieHandler.goandget(self.window.driver, url, datatype)
            if frameboy is False:
                QMessageBox.about(self.window, "Error", "No Results Returned!")
                self.window.setDisabled(False)
                return
            else:
                self.window.statusUpdate("Complete")
                self.window.dframe = frameboy
                self.window.setDisabled(False)
        else:
            self.window.statusUpdate("Starting Report")
            i = importlib.import_module('py.report' + self.window.reportdrop.currentText())
            i.main(self.window.driver,self.window.startrepcal.selectedDate().toPyDate(), self.window.endrepcal.selectedDate().toPyDate(), self.window.statuslabel)
            self.window.setDisabled(False)
