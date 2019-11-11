from py import PIEdata

# Make some variables
contactcatdict = {}
contactcatdict[''] = ''
contactcatdict['3D Printing'] = 58
contactcatdict['General'] = 56
contactcatdict['Plotter Printing'] = 57
contactcatdict['Printing'] = 14
contactcatdict['Tabling/Outreach'] = 55
contactcatdict['Technology'] = 15

statusdict = []
statusdict.append('Open')
statusdict.append('Decommissioned')
statusdict.append('Resolved')

appointmentstatdict = []
appointmentstatdict.append('Scheduled')
appointmentstatdict.append('Started')
appointmentstatdict.append('Completed')
appointmentstatdict.append('Cancelled')

# Add Contacts
contacts = PIEdata.PIEdata('Contacts',
                           'https://pie.iu.edu/Api/Contacts?page=0&pageLimit={0}&searchTerms=&startTime={1}&endTime={2}&LocationIds={3}&categories={4}&creatorIds={5}&mini=true',
                           ['maxreturns', 'startdate', 'enddate', 'location', 'category', 'username'])
contacts.setcategorydict(contactcatdict)

# Add Goldstars
goldstars = PIEdata.PIEdata('Gold Stars',
                            'https://pie.iu.edu/Api/GoldStars?page=0&pageLimit={0}&startTime={1}&endTime={2}&statuses={3}&userId={4}',
                            ['maxreturns', 'startdate', 'enddate', 'status', 'assignedto'])
goldstars.setstatusdict(statusdict)

# Add PDIs
pdis = PIEdata.PIEdata('PDIs',
                       'https://pie.iu.edu/Api/ProfessionalDevelopmentIssues?page=0&pageLimit={0}&startTime={1}&endTime={2}&statuses={3}&userId={4}',
                       ['maxreturns', 'startdate', 'enddate', 'status', 'assignedto'])
pdis.setstatusdict(statusdict)

# Add Locations
locations = PIEdata.PIEdata('User Locations',
                            'https://pie.iu.edu/Api/UserLocations?page=0&pageLimit={0}&onlyLocation=true&startTime={1}&endTime={2}&userId={3}',
                            ['maxreturns', 'startdate', 'enddate', 'username'])

# Add Shifts
shifts = PIEdata.PIEdata('Shifts',
                         'https://pie.iu.edu/Api/Shifts?page=0&pageLimit={0}&weekView=false&userId={1}&startTime={2}&endTime={3}&minimal=true',
                         ['maxreturns', 'username', 'startdate', 'enddate'])

# Add Inventory Reports
invreports = PIEdata.PIEdata('Inventory Reports',
                             'https://pie.iu.edu/Api/InventoryReports?startTime={0}&endTime={1}&inventoryLocationId={2}&onlyCurrent=false&pageLimit=null',
                             ['startdate', 'enddate', 'location'])
invreports.setinvbool(True)
invreports.setchuncks(15)

# Add Appointments
appointments = PIEdata.PIEdata('Appointments',
                               'https://pie.iu.edu/Api/Appointments?page=0&pageLimit={0}&startTime={1}&endTime={2}&statuses=Completed&groupByEmployee=false&instanceId=1',
                               ['maxreturns', 'startdate', 'enddate', 'status'])
appointments.setstatusdict(appointmentstatdict)

# Add Activer Users
activerusers = PIEdata.PIEdata('Active Users',
                               'https://pie.iu.edu/Api/Users?page=0&pageLimit=1000&searchTerms=&active=true&whitelistInclusiveMaskNames=Employee&fromUsersView=true&maskId=5',
                               [])

# Add Graveyard headcounts
graveyardheads = PIEdata.PIEdata('Graveyard HeadCounts',
                                 'https://pie.iu.edu/Api/LocationEvaluations/Reports?page=0&pageLimit={0}&startTime={1}&endTime={2}&formId=176&minimal=true',
                                 ['maxreturns', 'startdate', 'enddate'])

# Add the key for form pulling
formkey = PIEdata.PIEdata('Form Key',
                          'https://pie.iu.edu/Api/LocationEvaluationForms',
                          [])
#Add Sub Pleas
subpleas = PIEdata.PIEdata('Sub Plea',
                           'https://pie.iu.edu/Api/SubPleas?page=0&pageLimit={0}&startTime={1}&endTime={2}',
                           ['maxreturns', 'startdate', 'enddate'])
#Add schedules
schedules = PIEdata.PIEdata('Semester Schedules',
                            'https://pie.iu.edu/Api/Schedules?page=0&pageLimit=101',
                            [])
#Add assigned badges
assignedbadges = PIEdata.PIEdata('Assigned Badges',
                                 'https://pie.iu.edu/Api/AssignedBadges?page=0&pageLimit={0}&startTime={1}&endTime={2}',
                                 ['maxreturns', 'startdate', 'enddate'])

#add employee meetings
employeeMeetings = PIEdata.PIEdata('Employee Meetings',
                                   'https://pie.iu.edu/Api/EmployeeMeetings?page=0&pageLimit={0}',
                                   ['maxreturns'])

#add account checks
accountchecks = PIEdata.PIEdata('Account Checks',
                                'https://pie.iu.edu/Api/AccountChecks?page=0&pageLimit={0}',
                                ['maxreturns'])

#add account checks
contactslong = PIEdata.PIEdata('Contacts-Long',
                                'https://pie.iu.edu/Api/Contacts?page=0&pageLimit={0}&searchTerms=&startTime={1}&endtime={2}&LocationIds={3}&categoryIds={4}&creatorIds={5}',
                                ['maxreturns', 'startdate', 'enddate', 'location', 'category', 'username'])
contactslong.setcategorydict(contactcatdict)

#attendance issues
attendance_issues = PIEdata.PIEdata('Attendance Issues',
                                'https://pie.iu.edu/Api/AttendanceIssues?page=0&pageLimit={0}&startTime={1}&endTime={2}',
                                ['maxreturns', 'startdate', 'enddate'])

#chat messages
chat_messages = PIEdata.PIEdata('Chat Messages',
                                'https://pie.iu.edu/Api/ChatMessages?page=0&pageLimit={0}&startTime={1}&endTime={2}&userId={3}',
                                ['maxreturns', 'startdate', 'enddate', 'username'])

def buildalldatathings(userdict, labdict, invlabs):
    contacts.setuserdict(userdict)
    contacts.setlabdict(labdict)

    contactslong.setuserdict(userdict)
    contactslong.setlabdict(labdict)

    chat_messages.setuserdict(userdict)

    goldstars.set_assigneddict(userdict)

    pdis.set_assigneddict(userdict)

    locations.setuserdict(userdict)

    shifts.setuserdict(userdict)

    invreports.setinvlocationdict(invlabs)

    invreports.setchuncks(15)

    itemlist = [contacts, goldstars, pdis, shifts,locations, invreports, appointments, activerusers, graveyardheads, subpleas, schedules, assignedbadges, employeeMeetings, accountchecks, contactslong, attendance_issues, chat_messages]

    datalist = {}

    subpleas.setallowbracks(True)

    graveyardheads.setform(True)

    formkey.setformkey(True)

    for datathing in itemlist:
        datalist[datathing.getName()] = datathing

    return datalist