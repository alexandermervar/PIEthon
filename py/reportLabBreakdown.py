from py import functions, htmlbase, PIEdataVARS, PieHandler, report
from PyQt5.QtCore import QCoreApplication
from numpy import vectorize
from pandas import merge
import matplotlib.pyplot as plt

def main(driver, startdate, enddate, statuslabel, report):
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
        struct.endDate = enddate
        struct.startDate = startdate

    statusUpdate(statuslabel, 'Loading contacts, please be patient')

    #CONTACTS
    contacturl = contactstruct.urlList()
    contactframe = PieHandler.goandget(driver, contacturl, contactstruct)
    testy = contactframe['locationName'].value_counts().reset_index()
    testy.rename(columns={'locationName': 'contacts', 'index': 'locationName'}, inplace=True)
    testy['abb'] = testy['locationName'].apply(lambda x: functions.getAbb(x))
    testy = testy.groupby('abb')['contacts'].sum().reset_index()

    #LOCATIONS
    statusUpdate(statuslabel, 'Loading locations, please keep being patient')
    locationurl = locationstruct.urlList()
    locationframe = PieHandler.goandget(driver, locationurl, locationstruct)
    locationframe['staffed_hours'] = vectorize(functions.getSeconds)(locationframe['assumedDuration-difference'])
    locationframe['abb'] = locationframe['location-shortName'].apply(lambda x: functions.getAbb(x))
    locationframe = locationframe.groupby('abb')['staffed_hours'].sum().reset_index()
    locationframe = locationframe[['abb', 'staffed_hours']]
    supaframe = merge(locationframe, testy, left_on='abb', right_on='abb', how='outer')
    supaframe['contacts_per_hour'] = supaframe['contacts']/supaframe['staffed_hours']
    statusUpdate(statuslabel, 'Loading inventory reports, thanks for sticking around')

    #INVENTORY REPORTS
    inventoryurl = inventoryreportstruct.urlList()
    invframe = PieHandler.goandgetinv(driver, inventoryurl, 'Letter(8.5" x 11")')
    invuseframe = PieHandler.invcounttwo(invframe)

    #PUTTING THINGS TOGETHER
    invuseframe['abb'] = invuseframe['lab'].apply(lambda x: functions.getAbb(x))

    invuseframe = invuseframe.groupby('abb')['paper_used'].sum().reset_index()
    supadupaframe = merge(supaframe, invuseframe, on='abb', how='outer')
    supadupaframe = supadupaframe[['abb', 'staffed_hours', 'contacts', 'contacts_per_hour', 'paper_used']]
    supadupaframe['overall_score']=supadupaframe['contacts_per_hour']*supadupaframe['paper_used']
    supadupaframe.sort_values(by=['overall_score'], ascending=False, inplace=True)
    supadupaframe = supadupaframe.reset_index(drop=True)
    report.add('table', 'Lab Contacts/Hour and Paper Usage (Reams)', supadupaframe)


    #APPOINTMENTS
    statusUpdate(statuslabel, 'Moving on to appointments now. This will be worth it I swear.')
    appointmenturl = appointmentstruct.urlList()
    appointmentframe = PieHandler.goandget(driver, appointmenturl, appointmentstruct)

    shiftlocationframe = appointmentframe['shiftType-name'].value_counts().to_frame()
    plt.tight_layout()
    shiftlocationframe.plot.pie(y='shiftType-name',autopct=functions.make_autopct(shiftlocationframe['shiftType-name'].tolist()), fontsize=15, figsize=(8, 8))
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path+ '\\shiftlocations.png')
    report.add('graph', 'Appointment Assignments', '\\shiftlocations.png')

    buildingframe = appointmentframe['ticket-residence-building-name'].value_counts().to_frame()
    plt.tight_layout()
    buildingframe.plot.bar(figsize=(8,8))
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path + '\\appointmentlocals.png')
    report.add('graph', 'Appointment Locations', '\\appointmentlocals.png')

    appointmentframe['month'] = appointmentframe['scheduledStartTime'].apply(lambda x: functions.getMonth(x))
    smallboi = appointmentframe[['month', 'shiftType-shortName']]
    pivoto = smallboi.pivot_table(index='month', columns='shiftType-shortName', values='shiftType-shortName', aggfunc=len)

    statusUpdate(statuslabel, 'GeneratingReport')

    plt.tight_layout()
    pivoto.plot.bar()
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path + '\\timeandbuilding.png')
    report.add('graph', 'Appointment Months', '\\timeandbuilding.png')

    report.makeHTML('Lab Breakdown')

def statusUpdate(label, newstat):
    label.setText(newstat)
    QCoreApplication.processEvents()

description = "This report lists contacts per staffed hour and paper usage for each lab, as well as graphs for appointment history. This report is used for prioritizing labs in Lab Breakdown"
active = True
author = 'Brian Funk'

labbreakreport = report.report('Lab Breakdown', author, active)
labbreakreport.description = description
labbreakreport.main_run = main
