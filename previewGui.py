import functions
import PieHandler
import PIEdataVARS
import mainGui
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLabel, QLineEdit, QRadioButton, QVBoxLayout,
                             QPushButton, QScrollArea, QHBoxLayout, QGroupBox, QFormLayout, QCheckBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from os.path import expanduser

iconPath = functions.createPath('PIEcon.png')


class prevButton(QPushButton):

    def __init__(self, cols, rows, form, dframe):
        super().__init__()
        self.cols = cols
        self.rows = rows
        self.form = form
        self.dframe = dframe
        self.setText('preview')
        self.clicked.connect(self.colPreview)
        self.setMinimumWidth(100)

    def getcols(self):
        return self.cols

    def getrows(self):
        return self.rows

    def getform(self):
        return self.form

    def colPreview(self):
        for i in range(self.rows):
            self.form.itemAt(i).widget().setText(str(self.dframe.iloc[i, self.cols]))


class preview(QWidget):

    def __init__(self, dframe, dtype, startdate, enddate):
        self.dframe = dframe
        self.dtype = dtype
        self.startdate = startdate
        self.enddate = enddate
        super().__init__()

        self.initUI()

    def initUI(self):
        self.center()

        mygroupbox = QGroupBox('Mark Columns to Keep (' +str(len(self.dframe.columns)) + ' Columns Total)')
        mygroupbox.setMinimumWidth(200)
        myform = QFormLayout()

        buttonlist = []
        checklist = []

        previewform = QVBoxLayout()
        rangenum = min(100, len(self.dframe))

        for i in range(len(self.dframe.columns)):
            tempcheck = QCheckBox(self.dframe.columns[i])
            checklist.append(tempcheck)
            tempbutt = prevButton(i, rangenum, previewform, self.dframe)
            buttonlist.append(tempbutt)
            myform.addRow(checklist[i], buttonlist[i])
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout = QHBoxLayout(self)
        layout.addWidget(scroll)

        previewbox = QGroupBox('Preview (' +str(len(self.dframe.index)) + ' Records Total)')
        previewbox.setMinimumWidth(200)

        previewlist = []

        for i in range(rangenum):
            previewlist.append(QLabel(' '))
            previewform.addWidget(previewlist[i])

        previewbox.setLayout(previewform)
        previewscroll = QScrollArea()
        previewscroll.setWidget(previewbox)
        layout.addWidget(previewscroll)

        subbox = QGroupBox('')
        #subbox.setFixedWidth(150)

        radiouno = QRadioButton('Downloads')
        radiouno.setChecked(True)
        radiodos = QRadioButton('Documents')
        radiotres = QRadioButton('Desktop')

        radiolist = []

        radiolist.append(radiouno)
        radiolist.append(radiodos)
        radiolist.append(radiotres)

        subform = QVBoxLayout()
        subbut = QPushButton('Export')
        subbut.clicked.connect(lambda: self.export(checklist, radiolist))


        for radio in radiolist:
            subform.addWidget(radio)

        self.exportname = QLineEdit(self)
        self.exportname.setText(str(self.dtype) + '_' + str(self.startdate) + '_' + str(self.enddate))

        exportlabel = QLabel('.csv')

        hboy = QHBoxLayout()
        hboy.addWidget(self.exportname)
        hboy.addWidget(exportlabel)

        subform.addLayout(hboy)

        subform.addWidget(subbut)

        subbox.setLayout(subform)
        layout.addWidget(subbox)

        self.setStyleSheet(open("iu_stylesheet.qss", "r").read())

        self.setWindowTitle('PIEthon')
        self.setWindowIcon(QIcon(iconPath))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def export(self, checklist, radiolist):
        expath = ''
        for radio in radiolist:
            if radio.isChecked():
                print(radio.text())
                if radio.text() == 'Downloads':
                    expath = expanduser('~/Downloads/')
                if radio.text() == 'Documents':
                    expath = expanduser('~/Documents/')
                if radio.text() == 'Desktop':
                    expath = expanduser('~/Desktop/')
        drops = []
        for widget in checklist:
            if (not widget.isChecked()):
                drops.append(widget.text())
                #self.dframe.drop(widget.text())
        newframe = self.dframe.drop(columns=drops)
        try:
            newframe.to_csv(expath + self.exportname.text() + '.csv')
        except:
            newframe.to_csv(expath + str(self.dtype) + '_' + str(self.startdate) + '_' + str(self.enddate) + '.csv')