from py import functions, htmlbase, PIEdataVARS, PieHandler, report
from PyQt5 import QtCore
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main(driver, startdate, enddate, statuslabel):
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
        struct.set_enddate(enddate)
        struct.set_startdate(startdate)
        struct.set_maxreturns(100000)

    statusUpdate(statuslabel, 'Loading contacts, please be patient')

    #CONTACTS
    contacturl = contactstruct.make_url()
    contactframe = PieHandler.goandget(driver, contacturl, contactstruct)
    testy = contactframe['locationName'].value_counts().reset_index()
    testy.rename(columns={'locationName': 'contacts', 'index': 'locationName'}, inplace=True)
    testy['abb'] = testy['locationName'].apply(lambda x: functions.getAbb(x))
    testy = testy.groupby('abb')['contacts'].sum().reset_index()

    #LOCATIONS
    statusUpdate(statuslabel, 'Loading locations, please keep being patient')
    locationurl = locationstruct.make_url()
    locationframe = PieHandler.goandget(driver, locationurl, locationstruct)
    locationframe['staffed_hours'] = np.vectorize(functions.getSeconds)(locationframe['assumedDuration-difference'])
    locationframe['abb'] = locationframe['location-shortName'].apply(lambda x: functions.getAbb(x))
    locationframe = locationframe.groupby('abb')['staffed_hours'].sum().reset_index()
    locationframe = locationframe[['abb', 'staffed_hours']]
    supaframe = pd.merge(locationframe, testy, left_on='abb', right_on='abb', how='outer')
    supaframe['contacts_per_hour'] = supaframe['contacts']/supaframe['staffed_hours']
    statusUpdate(statuslabel, 'Loading inventory reports, thanks for sticking around')

    #INVENTORY REPORTS
    inventoryurl = inventoryreportstruct.make_url()
    invframe = PieHandler.goandgetinv(driver, inventoryurl, 'Letter(8.5" x 11")')
    invuseframe = PieHandler.invcounttwo(invframe)

    #PUTTING THINGS TOGETHER
    invuseframe['abb'] = invuseframe['lab'].apply(lambda x: functions.getAbb(x))

    invuseframe = invuseframe.groupby('abb')['paper_used'].sum().reset_index()
    supadupaframe = pd.merge(supaframe, invuseframe, on='abb', how='outer')
    supadupaframe = supadupaframe[['abb', 'staffed_hours', 'contacts', 'contacts_per_hour', 'paper_used']]
    supadupaframe['overall_score']=supadupaframe['contacts_per_hour']*supadupaframe['paper_used']
    supadupaframe.sort_values(by=['overall_score'], ascending=False, inplace=True)
    supadupaframe = supadupaframe.reset_index(drop=True)
    labbreakhtml = supadupaframe.to_html()

    #APPOINTMENTS
    statusUpdate(statuslabel, 'Moving on to appointments now. This will be worth it I swear.')
    appointmenturl = appointmentstruct.make_url()
    appointmentframe = PieHandler.goandget(driver, appointmenturl, appointmentstruct)

    shiftlocationframe = appointmentframe['shiftType-name'].value_counts().to_frame()
    plt.tight_layout()
    shiftlocationframe.plot.pie(y='shiftType-name',autopct=functions.make_autopct(shiftlocationframe['shiftType-name'].tolist()), fontsize=15, figsize=(8, 8))
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path() + '\\shiftlocations.png')

    buildingframe = appointmentframe['ticket-residence-building-name'].value_counts().to_frame()
    plt.tight_layout()
    buildingframe.plot.bar(figsize=(8,8))
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path() + '\\appointmentlocals.png')

    appointmentframe['month'] = appointmentframe['scheduledStartTime'].apply(lambda x: functions.getMonth(x))
    smallboi = appointmentframe[['month', 'shiftType-shortName']]
    pivoto = smallboi.pivot_table(index='month', columns='shiftType-shortName', values='shiftType-shortName', aggfunc=len)

    statusUpdate(statuslabel, 'GeneratingReport')

    plt.tight_layout()
    pivoto.plot.bar()
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path() + '\\timeandbuilding.png')

    tablelist = [labbreakhtml]
    picturelist = [htmlbase.figure_path() + '\\shiftlocations.png', htmlbase.figure_path() + '\\appointmentlocals.png', htmlbase.figure_path() + '\\timeandbuilding.png'brfun]

    outputfile = htmlbase.htmlbase('Lab Breakdown', 'Lab Breakdown', tablelist, picturelist)
    outputfile.makeHTML('LabBreakdown')

def statusUpdate(label, newstat):
    label.setText(newstat)
    QtCore.QCoreApplication.processEvents()

description = "This report lists contacts per staffed hour and paper usage for each lab, as well as graphs for appointment history. This report is used for prioritizing labs in Lab Breakdown"
active = True
author = 'Brian Funk'

labbreakreport = report.report('Lab Breakdown', author, active)
labbreakreport.description = description
labbreakreport.main_run = main
