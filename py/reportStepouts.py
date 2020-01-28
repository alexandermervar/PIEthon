from py import functions, htmlbase, PIEdataVARS, PieHandler, report
from numpy import vectorize

def main(driver, startdate, enddate, statuslabel, report):
    locationstruct = PIEdataVARS.locations
    locationstruct.endDate = enddate
    locationstruct.startDate = startdate
    locationurl = locationstruct.urlList()
    locationframe = PieHandler.goandget(driver, locationurl, locationstruct)
    locationframe['staffed_minutes'] = vectorize(functions.getMinutes)(locationframe['assumedDuration-difference'])
    locationframe['abb'] = locationframe['location-shortName'].apply(lambda x: functions.getAbb(x))
    locationframe = locationframe.groupby('abb')['staffed_minutes'].median().reset_index()

    report.add('table', 'Median Stepout Times', locationframe)
    report.makeHTML('Stepout Medians')

#This is a bad report...make better lol
description = "Just give median stepout times for each lab. Honestly kinda useless. Need to make not trash"
active = True
author = 'Brian Funk'

stepoutreport = report.report('Stepout Report', author,active)
stepoutreport.description = description
stepoutreport.main_run = main