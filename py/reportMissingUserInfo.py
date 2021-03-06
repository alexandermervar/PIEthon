from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series

def main(driver, startdate, enddate, statuslabel, report):
    activeuserstruct = PIEdataVARS.activerusers
    urllist = activeuserstruct.urlList()
    userframe = PieHandler.goandget(driver, urllist, activeuserstruct)

    searchlist = ['address', 'emergencyName', 'emergencyRelationship', 'emergencyPhoneNumber', 'phone']

    missinghold = []

    for index, row in userframe.iterrows():
        temparray = []
        if yikescheck(row['address']):
            temparray.append('address')
        if yikescheck(row['emergencyName']):
            temparray.append('emergencyName')
        if yikescheck(row['emergencyRelationship']):
            temparray.append('emergencyRelationship')
        if yikescheck(row['emergencyPhoneNumber']):
            temparray.append('emergencyPhoneNumber')
        if yikescheck(row['phoneNumber']):
            temparray.append('phoneNumber')

        missinghold.append(temparray)

    se = Series(missinghold)
    userframe['Missing Attributes'] = se.values

    userframe = userframe[['lastName', 'firstName', 'username', 'Missing Attributes']]

    report.add('table', 'Missing User Info', userframe)

    report.makeHTML('Missing User Info')

def yikescheck(val):
    #might need to check if the value is a string
    if val is None:
        return False
    val = "".join(val.split())
    if val == "" or val == 'None' or val == ',':
        return True
    else:
        return False

description = "Goes through active users and lists if they are missing any contact information on their Pie profile page"
active = True
author = 'Brian Funk'

missinginforeport = report.report('Missing User Info', author,active)
missinginforeport.description = description
missinginforeport.main_run = main