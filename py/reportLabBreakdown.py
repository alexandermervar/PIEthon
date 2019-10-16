from py import functions, htmlbase, PIEdataVARS, PieHandler
from PyQt5 import QtCore
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

def main(driver, startdate, enddate, statuslabel):
    print("in reportmain")
    contactstruct = PIEdataVARS.contacts
    locationstruct = PIEdataVARS.locations
    inventoryreportstruct = PIEdataVARS.invreports
    appointmentstruct = PIEdataVARS.appointments

    container = []

    container.append(contactstruct)
    container.append(locationstruct)
    container.append(inventoryreportstruct)
    container.append(appointmentstruct)

    print("container complete")

    for struct in container:
        struct.set_enddate(enddate)
        struct.set_startdate(startdate)
        struct.set_maxreturns(100000)

    print("structs updates")

    statusUpdate(statuslabel, 'Loading contacts, please be patient')

    print(startdate)

    #CONTACTS
    contacturl = contactstruct.make_url()
    print("url made")
    contactframe = PieHandler.goandget(driver, contacturl, contactstruct)
    print("frame obtained")
    testy = contactframe['locationName'].value_counts().reset_index()
    testy.rename(columns={'locationName': 'contacts', 'index': 'locationName'}, inplace=True)
    testy['abb'] = testy['locationName'].apply(lambda x: functions.getAbb(x))
    testy = testy.groupby('abb')['contacts'].sum().reset_index()
    print("contacts done")

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
    print("locations done")

    #INVENTORY REPORTS
    inventoryurl = inventoryreportstruct.make_url()
    invframe = PieHandler.goandgetinv(driver, inventoryurl, 'Letter(8.5" x 11")')
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
    print("inventory reports done")

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

def statusUpdate(label, newstat):
    label.setText(newstat)
    QtCore.QCoreApplication.processEvents()
