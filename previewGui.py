import functions
import PieHandler
import PIEdataVARS
import mainGui
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLabel, QMessageBox, QRadioButton,
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

    def __init__(self, dframe):
        self.dframe = dframe
        super().__init__()

        self.initUI()

    def initUI(self):
        spacer = 20
        x = 800
        y = 600
        self.resize(x, y)
        self.center()

        mygroupbox = QGroupBox('Mark Columns to Keep (' +str(len(self.dframe.columns)) + ' Columns Total)')
        mygroupbox.setFixedWidth(305)
        myform = QFormLayout()

        buttonlist = []
        checklist = []

        previewform = QFormLayout()
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

        previewbox = QGroupBox('Preview')
        previewbox.setFixedWidth(305)

        previewlist = []

        for i in range(rangenum):
            previewlist.append(QLabel(''))
            previewform.addRow(previewlist[i])

        previewbox.setLayout(previewform)
        previewscroll = QScrollArea()
        previewscroll.setWidget(previewbox)
        layout.addWidget(previewscroll)

        subbox = QGroupBox('')
        subbox.setFixedWidth(150)

        radiouno = QRadioButton('Downloads')
        radiouno.setChecked(True)
        radiodos = QRadioButton('Documents')
        radiotres = QRadioButton('Desktop')

        radiolist = []

        radiolist.append(radiouno)
        radiolist.append(radiodos)
        radiolist.append(radiotres)

        subform = QFormLayout()
        subbut = QPushButton('Export')
        subbut.clicked.connect(lambda: self.export(checklist, radiolist))


        for radio in radiolist:
            subform.addWidget(radio)

        subform.addWidget(subbut)

        subbox.setLayout(subform)
        layout.addWidget(subbox)

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
        self.dframe = self.dframe.drop(columns=drops)
        self.dframe.to_csv(expath + 'export.csv')

    def statusUpdate(self, newstat):
        self.statuslabel.setText(newstat)
        QtCore.QCoreApplication.processEvents()

    def startMain(self, user, dataoptions, driver):
        self.mainwind = mainGui.mainwindow(user, dataoptions, driver)
        self.mainwind.show()

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
        self.statusUpdate('Connected to Pie')
        #print('call to users')
        self.statusUpdate('Pulling in Users')
        userlist = PieHandler.grabUsers(driver)
        self.statusUpdate('Pulling in Locations')
        lablist = PieHandler.grabLabs(driver)
        self.statusUpdate('Throwing it together')
        datalist = PIEdataVARS.buildalldatathings(userlist, lablist)

        self.startMain(user, datalist, driver)

        self.close()