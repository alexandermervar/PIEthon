import PIEdataVARS
import functions
import PieHandler
import PIEdataVARS
import datetime
import sys
import mainGui
from PyQt5.QtWidgets import (QWidget, QToolTip, QDesktopWidget, QLineEdit, QLabel, QPushButton, QMessageBox,
                             QPushButton, QApplication, QRadioButton, QComboBox, QCalendarWidget)
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import htmlbase

iconPath = functions.createPath('PIEcon.png')

class labbreakdown(QWidget):

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
        self.warninglabel.setText("HEADS UP - This will take a while to run. Pie's fault, not Brian's :)")
        self.warninglabel.resize(670, 25)

        self.setWindowTitle('PIEthon - Lab Breakdown')
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
        self.statuslabel.setText(newstat)
        QtCore.QCoreApplication.processEvents()

    def startMain(self, user, dataoptions, driver):
        self.mainwind = mainGui.mainwindow(user, dataoptions, driver)
        self.mainwind.show()

    def labbreakwork(self):
        contactstruct = PIEdataVARS.contacts
        locationstruct = PIEdataVARS.locations
        inventoryreportstruct = PIEdataVARS.invreports
        appointmentstruct = PIEdataVARS.appointments

        container = []

        container.append(contactstruct)
        container.append(locationstruct)
        container.append(inventoryreportstruct)
        container.append(appointmentstruct)

        for struct in container:
            struct.set_enddate(self.endcal.selectedDate().toPyDate())
            struct.set_startdate(self.startcal.selectedDate().toPyDate())
            struct.set_maxreturns(100000)

        self.statusUpdate('Loading contacts, please be patient')

        #CONTACTS
        contacturl = contactstruct.make_url()
        contactframe = PieHandler.goandget(self.driver, contacturl, contactstruct)
        testy = contactframe['locationName'].value_counts().reset_index()
        testy.rename(columns={'locationName': 'contacts', 'index': 'locationName'}, inplace=True)
        testy['abb'] = testy['locationName'].apply(lambda x: functions.getAbb(x))
        testy = testy.groupby('abb')['contacts'].sum().reset_index()

        #LOCATIONS
        self.statusUpdate('Loading locations, please keep being patient')
        locationurl = locationstruct.make_url()
        locationframe = PieHandler.goandget(self.driver, locationurl, locationstruct)
        locationframe['staffed_hours'] = np.vectorize(functions.getSeconds)(locationframe['assumedDuration-difference'])
        locationframe['abb'] = locationframe['location-shortName'].apply(lambda x: functions.getAbb(x))
        locationframe = locationframe.groupby('abb')['staffed_hours'].sum().reset_index()
        locationframe = locationframe[['abb', 'staffed_hours']]
        supaframe = pd.merge(locationframe, testy, left_on='abb', right_on='abb', how='outer')
        supaframe['contacts_per_hour'] = supaframe['contacts']/supaframe['staffed_hours']
        self.statusUpdate('Loading inventory reports, thanks for sticking around')

        #INVENTORY REPORTS
        inventoryurl = inventoryreportstruct.make_url()
        invframe = PieHandler.goandgetinv(self.driver, inventoryurl, 'Letter(8.5" x 11")')
        paperdict = PieHandler.findinvused(invframe)
        usedict = PieHandler.usepapdict(paperdict)
        toframe = {}
        locas = []
        nums = []
        for key,val in usedict.items():
            locas.append(key)
            nums.append(val)
        toframe['locationName'] = locas
        toframe['paper_used'] = nums
        invuseframe = pd.DataFrame(data=toframe)

        #PUTTING THINGS TOGETHER
        invuseframe['abb'] = invuseframe['locationName'].apply(lambda x: functions.getAbb(x))

        invuseframe = invuseframe.groupby('abb')['paper_used'].sum().reset_index()
        supadupaframe = pd.merge(supaframe, invuseframe, on='abb', how='outer')
        supadupaframe = supadupaframe[['abb', 'staffed_hours', 'contacts', 'contacts_per_hour', 'paper_used']]
        supadupaframe['overall_score']=supadupaframe['contacts_per_hour']*supadupaframe['paper_used']
        supadupaframe.sort_values(by=['overall_score'], ascending=False, inplace=True)
        supadupaframe = supadupaframe.reset_index(drop=True)
        labbreakhtml = supadupaframe.to_html()

        """
        #APPOINTMENTS
        self.statusUpdate('Moving on to appointments now. This will be worth it I swear.')
        appointmenturl = appointmentstruct.make_url()
        appointmentframe = PieHandler.goandget(self.driver, appointmenturl, appointmentstruct)

        shiftlocationframe = appointmentframe['shiftType-name'].value_counts().to_frame()
        plt.tight_layout()
        shiftlocationframe.plot.pie(y='shiftType-name',autopct=functions.make_autopct(shiftlocationframe['shiftType-name'].tolist()), fontsize=15, figsize=(8, 8))
        plt.tight_layout()
        plt.savefig('reports/figures/shiftlocations.png')

        buildingframe = appointmentframe['ticket-residence-building-name'].value_counts().to_frame()
        plt.tight_layout()
        buildingframe.plot.bar(figsize=(8,8))
        plt.tight_layout()
        plt.savefig('reports/figures/appointmentlocals.png')

        appointmentframe['month'] = appointmentframe['scheduledStartTime'].apply(lambda x: functions.getMonth(x))
        smallboi = appointmentframe[['month', 'shiftType-shortName']]
        pivoto = smallboi.pivot_table(index='month', columns='shiftType-shortName', values='shiftType-shortName', aggfunc=len)

        plt.tight_layout()
        pivoto.plot.bar()
        plt.tight_layout()
        plt.savefig('reports/figures/timeandbuilding.png')
        """

        tablelist = [labbreakhtml]
        #picturelist = ['figures/shiftlocations.png', 'figures/appointmentlocals.png', 'figures/timeandbuilding.png']
        picturelist = []

        outputfile = htmlbase.htmlbase('Lab Breakdown', 'Lab Breakdown', tablelist, picturelist)
        outputfile.makeHTML('LabBreakdown')

        #supadupaframe.to_csv('labbreakdown.csv')
        self.close()

def mainrun(driver):
    newboy = labbreakdown(driver)
    newboy.show()

    return
