from py import PIEdata
from py import PIEdata_new

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
statusdict.append('')
statusdict.append('Resolved')
statusdict.append('Open')
statusdict.append('Decommissioned')

appointmentstatdict = []
appointmentstatdict.append('Scheduled')
appointmentstatdict.append('Started')
appointmentstatdict.append('Completed')
appointmentstatdict.append('Cancelled')

###############################
### NEW DATA STRUCTURES YAY ###
###############################

list_o_data = []

# CONTACTS
contacts_new = PIEdata_new.PIEdata('Contacts - Long', 'https://tcciub.pie.iu.edu/Api/Contacts?page=0&pageLimit=100000&searchTerms=')
contacts_new.categoryDict = contactcatdict
list_o_data.append(contacts_new)

# CONTACTS - mini (lil cutie goobers)
contacts_fast = PIEdata_new.PIEdata('Contacts', 'https://tcciub.pie.iu.edu/Api/Contacts?page=0&pageLimit=100000&searchTerms=')
contacts_fast.append = '&mini=true'
contacts_fast.categoryDict = contactcatdict
list_o_data.append(contacts_fast)

# GOLDSTARS
goldstars = PIEdata_new.PIEdata('Gold Stars', 'https://tcciub.pie.iu.edu/Api/GoldStars?page=0&pageLimit=100000&searchTerms=')
goldstars.createdbyPost = True
goldstars.statusDict=statusdict
list_o_data.append(goldstars)

# PDIs
pdis = PIEdata_new.PIEdata('PDIs', 'https://tcciub.pie.iu.edu/Api/ProfessionalDevelopmentIssues?page=0&pageLimit=100000&searchTerms=')
pdis.createdbyPost = True
pdis.statusDict = statusdict
list_o_data.append(pdis)

# LOCATIONS
locations = PIEdata_new.PIEdata('User Locations', 'https://tcciub.pie.iu.edu/Api/UserLocations?page=0&pageLimit=1000000&onlyLocation=true&searchTerms=')
locations.locationPost = True
locations.createSwitch = True
list_o_data.append(locations)

# SHIFTS
shifts = PIEdata_new.PIEdata('Shifts', 'https://tcciub.pie.iu.edu/Api/Shifts?page=0&pageLimit=100000&weekView=false')
shifts.append = '&minimal=true'
shifts.locationPost = True
list_o_data.append(shifts)

# INVENTORY REPORTS
invreports = PIEdata_new.PIEdata('Inventory Reports', 'https://tcciub.pie.iu.edu/Api/InventoryReports?')
invreports.invbool = True
invreports.chuncks = 15
invreports.createdbyPost = True
invreports.createSwitch = True
invreports.append = '&onlyCurrent=false&pageLimit=null'
list_o_data.append(invreports)

# Appointments
appointments = PIEdata_new.PIEdata('Appointments', 'https://tcciub.pie.iu.edu/Api/Appointments?page=0&pageLimit={0}&startTime={1}&endTime={2}&statuses=Completed')
appointments.statusDict = appointmentstatdict
appointments.append = '&groupByEmployee=false&instanceId=1'
list_o_data.append(appointments)

# Add Active Users
activerusers = PIEdata.PIEdata('Active Users',
                               'https://tcciub.pie.iu.edu/Api/Users?page=0&pageLimit=1000&searchTerms=&active=true&whitelistInclusiveMaskNames=Employee&fromUsersView=true&maskId=5',
                               [])

# Add Graveyard headcounts
graveyardheads = PIEdata.PIEdata('Graveyard HeadCounts',
                                 'https://tcciub.pie.iu.edu/Api/LocationEvaluations/Reports?page=0&pageLimit={0}&startTime={1}&endTime={2}&formId=176&minimal=true',
                                 ['maxreturns', 'startdate', 'enddate'])

# Add the key for form pulling
formkey = PIEdata.PIEdata('Form Key',
                          'https://tcciub.pie.iu.edu/Api/LocationEvaluationForms',
                          [])
#Add Sub Pleas
subpleas = PIEdata.PIEdata('Sub Plea',
                           'https://tcciub.pie.iu.edu/Api/SubPleas?page=0&pageLimit={0}&startTime={1}&endTime={2}',
                           ['maxreturns', 'startdate', 'enddate'])
#Add schedules
schedules = PIEdata.PIEdata('Semester Schedules',
                            'https://tcciub.pie.iu.edu/Api/Schedules?page=0&pageLimit=101',
                            [])
#Add assigned badges
assignedbadges = PIEdata.PIEdata('Assigned Badges',
                                 'https://tcciub.pie.iu.edu/Api/AssignedBadges?page=0&pageLimit={0}&startTime={1}&endTime={2}',
                                 ['maxreturns', 'startdate', 'enddate'])

#add employee meetings
employeeMeetings = PIEdata.PIEdata('Employee Meetings',
                                   'https://tcciub.pie.iu.edu/Api/EmployeeMeetings?page=0&pageLimit={0}',
                                   ['maxreturns'])

#add account checks
accountchecks = PIEdata.PIEdata('Account Checks',
                                'https://tcciub.pie.iu.edu/Api/AccountChecks?page=0&pageLimit={0}&searchTerms=&startTime={1}&endTime={2}',
                                [])

#attendance issues
attendance_issues = PIEdata.PIEdata('Attendance Issues',
                                'https://tcciub.pie.iu.edu/Api/AttendanceIssues?page=0&pageLimit={0}&startTime={1}&endTime={2}',
                                ['maxreturns', 'startdate', 'enddate'])

#chat messages
chat_messages = PIEdata.PIEdata('Chat Messages',
                                'https://tcciub.pie.iu.edu/Api/ChatMessages?page=0&pageLimit={0}&startTime={1}&endTime={2}&userId={3}',
                                ['maxreturns', 'startdate', 'enddate', 'username'])

#incident reports
incident_reports = PIEdata.PIEdata('Incident Reports',
                                'https://tcciub.pie.iu.edu/Api/IncidentReports?page=0&pageLimit={0}&startTime={1}&endTime={2}',
                                ['maxreturns', 'startdate', 'enddate'])



def buildalldatathings(userdict, labdict, invlabs):

    # buff contacts
    contacts_new.createdbyDict = userdict
    contacts_new.locationDict = labdict
    contacts_fast.createdbyDict = userdict
    contacts_fast.locationDict = labdict

    # buff goldstars
    goldstars.createdbyDict = userdict
    goldstars.assignedToDict = userdict

    # buff pdis
    pdis.createdbyDict = userdict
    pdis.assignedToDict = userdict

    # buff locations
    locations.createdbyDict = userdict
    locations.locationDict = labdict

    # buff shifts
    shifts.assignedToDict = userdict
    shifts.locationDict = labdict

    # buff inventory reports
    invreports.locationDict = invlabs
    invreports.createdbyDict = userdict

    datalist = {}
    for data in list_o_data:
        datalist[data.name] = data

    return datalist
