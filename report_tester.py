import py.functions as functions
import py.PieHandler as PieHandler
from PyQt5.QtWidgets import QLabel, QApplication
import datetime
import sys

"""

This file is meant to be used only for development purposes. It will test reports without needing to re-run the gui and go through all the hoops.

Report type, dates, and DUO authentication method are all decided in the file variables, and username/password are a separate file to avoid accidentally uploading credentials to git

"""

# import report here
from py.report import report_list

# other variables (default times are Fall 2019)
report_name = 'Badge Assignments'
duotype = 'push'
startdate = datetime.date(2019, 8, 25)
enddate = datetime.date(2020, 1, 12)

for temp in report_list:
    if temp.name == report_name:
        report = temp

# create random qlabel
app = QApplication(sys.argv)
randlabel = QLabel('na')

# get username and password info from file
f = open("credentials.txt",'r')
lines = f.readlines()
username = lines[0]
password = lines[1]

#run driver and such
driver = functions.buildHeadless()
print('sent info prepare for duo')
driver = PieHandler.caslogin(driver, username, password, duotype)
driver = PieHandler.getPie(driver)

report.run_main(driver,startdate,enddate,randlabel)
