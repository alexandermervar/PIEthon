import PieHandler
import PIEdataVARS
import pandas as pd

def getinfo(driver):
    activeuserstruct = PIEdataVARS.activerusers
    urllist = activeuserstruct.make_url()
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

    se = pd.Series(missinghold)
    userframe['Missing Attributes'] = se.values

    userframe = userframe[['lastName', 'firstName', 'username', 'Missing Attributes']]

    for index, row in userframe.iterrows():
        if not row["Missing Attributes"]  == []:
            print(str(row['firstName']) + ' ' + str(row['lastName']) + ' is missing ' + str(row['Missing Attributes']))

def yikescheck(val):
    #might need to check if the value is a string
    if val is None:
        return False
    val = "".join(val.split())
    if val == "" or val == 'None' or val == ',':
        return True
    else:
        return False