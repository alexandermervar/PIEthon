"""
TCC PDI Analysis Fall 2018
Nick Johnson
"""

import re
from datetime import datetime
from py import report, htmlbase, PIEdataVARS, PieHandler
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLabel, QPushButton, QRadioButton, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class Pdis(QWidget):

    def __init__(self, driver):
        self.driver = driver
        super().__init__()

        self.initUI()

    def initUI(self):
        # TODO: Resize and add username box to search by username
        self.resize(275, 125)
        self.center()

        # add the radio buttons
        self.semesterRadio = QRadioButton('Semester', self)
        self.semesterRadio.setChecked(True)
        self.semesterRadio.move(50, 25)

        self.lifeRadio = QRadioButton('Life', self)
        self.lifeRadio.move(165, 25)

        # add the cccccccombo box
        self.categorylabel = QLabel(self)
        self.categorylabel.move(20, 50)
        self.categorylabel.setText("Semesters")
        self.categorylabel.resize(80, 25)

        self.reportcombo = QComboBox(self)
        self.reportcombo.addItems(self.buildSems())
        self.reportcombo.move(90, 50)
        self.reportcombo.resize(150, 25)

        self.semesterRadio.toggled.connect(self.radiocheck)

        # add close button
        self.closebutton = QPushButton('Close', self)
        self.closebutton.move(20, 90)
        self.closebutton.clicked.connect(self.close)

        # add submit button
        self.submitbutton = QPushButton('Submit', self)
        self.submitbutton.move(175, 90)
        self.submitbutton.clicked.connect(self.getSemPdi)

        # add the status thingy
        self.statuslabel = QLabel(self)
        self.statuslabel.move(75, 110)
        self.statuslabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.statuslabel.setText("Ready")
        self.statuslabel.resize(195, 13)

        self.setWindowTitle('PIEthon - PDI Information')
        self.setWindowIcon(QIcon(iconPath))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def radiocheck(self):
        if (self.lifeRadio.isChecked()):
            self.reportcombo.setEnabled(False)
        else:
            self.reportcombo.setEnabled(True)

    # Builds the list of semesters for selection in the GUI
    def buildSems(self):
        semStruct = PIEdataVARS.schedules
        semUrl = semStruct.make_url()
        semFrame = PieHandler.goandget(self.driver, semUrl, semStruct)
        semList = []

        for index, row in semFrame.iterrows():
            semList.append(row["name"])

        return semList  # Hands the list of semesters back to Combo box

    # Builds PDI frame and returns necessary information
    def getSemPdi(self, user="all"):
        # TODO: Implement searching by user
        pd.set_option("display.max_colwidth", 1000)

        semStruct = PIEdataVARS.schedules
        semUrl = semStruct.make_url()
        semFrame = PieHandler.goandget(self.driver, semUrl, semStruct)

        semName = self.reportcombo.currentText()

        pdiStruct = PIEdataVARS.pdis

        for idx, row in semFrame.iterrows():
            if row["name"] == semName:
                pdiStruct.set_startdate(
                    datetime.fromisoformat(row["startTime"]))  # set start/end time to selected semester
                pdiStruct.set_enddate(datetime.fromisoformat(row["endTime"]))  # to build correct URL for the PDI frame
                pdiStruct.set_maxreturns(1000)
                pdiUrl = pdiStruct.make_url()
                pdiFrame = PieHandler.goandget(self.driver, pdiUrl, pdiStruct)

        # Pandas really doesn't like this method of changing the value, but it's the only way I've found that works so... too bad
        for idx, row in pdiFrame.iterrows():
            pdiFrame["behaviorDescription"][idx] = removeHTML(row["behaviorDescription"])
            pdiFrame["actionTaken"][idx] = removeHTML(row["actionTaken"])
            pdiFrame["created"][idx] = row["created"][0:10]

        # Renaming for readability
        pdiFrame.rename(
            columns={'assignedBy-username': 'Assigned By', 'user-username': 'Assigned To', 'created': 'Created',
                     'behaviorDescription': 'Behavior Description', 'recurringIssue': 'Recurring Issue',
                     'addressedIssue': 'Addressed Issue', 'actionTaken': 'Action Taken'},
            inplace=True)

        # Smallening the Frame
        pdiFrame = pdiFrame[["Assigned By", "Assigned To", "Created", "Behavior Description", "Recurring Issue",
                             "Addressed Issue", "Action Taken"]]

        # TODO: Some form of graphing maybe? Time between PDIs? Time between Recurring PDIs?
        # Converting to HTML
        resultFrame = pdiFrame.to_html()
        tableList = [resultFrame]
        pictureList = []

        outputFile = htmlbase.htmlbase('PDI Information', 'PDI Information', tableList, pictureList)
        outputFile.makeHTML('PDI Information')

        return


# TODO: Add lifetime PDIs -- Search from Active User Frame and find hire date through today


def removeHTML(string: str):  # removes HTML entities from string
    string = string.replace("\n", "")  # removes new line chars
    string = re.sub('<.*?>', "", string)  # removes HTML tags
    string = re.sub('&nbsp;|&#160', " ", string)  # removes &nbsp artifacts and replaces with a space
    string = re.sub('&apos|&#39;', "\'", string)  # removes &#39; artifacts and replaces with apostrophe
    string = re.sub('&quot;|&#34', "\"", string)  # removes &quot artifacts and replaces with double quote
    string = re.sub('&amp;|&#38;', "&", string)  # removes &amp; or &#38; and replaces with ampersand

    return string

description = "Honestly not sure what it does but it needs to be completely overhauled. Running this will crash PIEthon"
active = False
author = 'Nick Johnson'

pdireport = report.report('PDI Report',author,active)
pdireport.description = description
pdireport.main_run = False
