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
statusdict.append('')
statusdict.append('Resolved')
statusdict.append('Open')
statusdict.append('Decommissioned')

appointmentstatdict = []
appointmentstatdict.append('')
appointmentstatdict.append('Completed')
appointmentstatdict.append('Scheduled')
appointmentstatdict.append('Started')
appointmentstatdict.append('Cancelled')

###############################
### NEW DATA STRUCTURES YAY ###
###############################

list_o_data = []

# CONTACTS
contacts_long = PIEdata.PIEdata('Contacts - Long', 'https://tcciub.pie.iu.edu/Api/Contacts?page=0&pageLimit=100000&searchTerms=')
contacts_long.categoryDict = contactcatdict
list_o_data.append(contacts_long)

# CONTACTS - mini (lil cutie goobers)
contacts = PIEdata.PIEdata('Contacts', 'https://tcciub.pie.iu.edu/Api/Contacts?page=0&pageLimit=100000&searchTerms=')
contacts.append = '&mini=true'
contacts.categoryDict = contactcatdict
list_o_data.append(contacts)

# GOLDSTARS
goldstars = PIEdata.PIEdata('Gold Stars', 'https://tcciub.pie.iu.edu/Api/GoldStars?page=0&pageLimit=100000&searchTerms=')
goldstars.createdbyPost = True
goldstars.statusDict=statusdict
list_o_data.append(goldstars)

# PDIs
pdis = PIEdata.PIEdata('PDIs', 'https://tcciub.pie.iu.edu/Api/ProfessionalDevelopmentIssues?page=0&pageLimit=100000&searchTerms=')
pdis.createdbyPost = True
pdis.statusDict = statusdict
list_o_data.append(pdis)

# LOCATIONS
locations = PIEdata.PIEdata('User Locations', 'https://tcciub.pie.iu.edu/Api/UserLocations?page=0&pageLimit=1000000&onlyLocation=true&searchTerms=')
locations.locationPost = True
locations.createSwitch = True
list_o_data.append(locations)

# Labs
labs = PIEdata.PIEdata('Active Labs', 'https://pie.iu.edu/Api/Locations?')
labs.allowDates = False
# list_o_data.append(labs)

# Inventory Labs
inv_labs = PIEdata.PIEdata('Active Inventory Labs', 'https://pie.iu.edu/Api/InventoryLocations?page=0&pageLimit=1010')
inv_labs.allowDates = False
# list_o_data.append(inv_labs)

# SHIFTS
shifts = PIEdata.PIEdata('Shifts', 'https://tcciub.pie.iu.edu/Api/Shifts?page=0&pageLimit=100000&weekView=false')
shifts.append = '&minimal=true'
shifts.locationPost = True
list_o_data.append(shifts)

# INVENTORY REPORTS
invreports = PIEdata.PIEdata('Inventory Reports', 'https://tcciub.pie.iu.edu/Api/InventoryReports?')
invreports.invbool = True
invreports.chuncks = 15
invreports.createdbyPost = True
invreports.createSwitch = True
invreports.append = '&onlyCurrent=false&pageLimit=null'
list_o_data.append(invreports)

# APPOINTMENTS
appointments = PIEdata.PIEdata('Appointments', 'https://tcciub.pie.iu.edu/Api/Appointments?page=0&pageLimit=10000000')
appointments.statusDict = appointmentstatdict
appointments.append = '&groupByEmployee=false&instanceId=1'
appointments.assignedToPost = True
list_o_data.append(appointments)

# ACTIVE USERS
activerusers = PIEdata.PIEdata('Active Users', 'https://tcciub.pie.iu.edu/Api/Users?page=0&pageLimit=1000&searchTerms=&active=true&whitelistInclusiveMaskNames=Employee&fromUsersView=true&maskId=5')
activerusers.allowDates = False
list_o_data.append(activerusers)

# GRAVEYARD HEADCOUNTS
graveyardheads = PIEdata.PIEdata('Graveyard HeadCounts', 'https://tcciub.pie.iu.edu/Api/LocationEvaluations/Reports?page=0&pageLimit=10000000')
graveyardheads.append = '&formId=176&minimal=true'
list_o_data.append(graveyardheads)

# FORM KEY
formkey = PIEdata.PIEdata('Form Key', 'https://tcciub.pie.iu.edu/Api/LocationEvaluationForms')

# SUB PLEAS
subpleas = PIEdata.PIEdata('Sub Plea', 'https://tcciub.pie.iu.edu/Api/SubPleas?page=0&pageLimit=1000000')
list_o_data.append(subpleas)

# SCHEDULES
schedules = PIEdata.PIEdata('Semester Schedules', 'https://tcciub.pie.iu.edu/Api/Schedules?page=0&pageLimit=101')
schedules.allowDates = False
list_o_data.append(schedules)

# ASSIGNED BADGES
assignedbadges = PIEdata.PIEdata('Assigned Badges', 'https://tcciub.pie.iu.edu/Api/AssignedBadges?page=0&pageLimit=1000000')
assignedbadges.createdbyPost = True
assignedbadges.assignedToPost = True
list_o_data.append(assignedbadges)

# EMPLOYEE MEETINGS
employeeMeetings = PIEdata.PIEdata('Employee Meetings', 'https://tcciub.pie.iu.edu/Api/EmployeeMeetings?page=0&pageLimit=10000000')
employeeMeetings.employeeswitch = True
list_o_data.append(employeeMeetings)

# ACCOUNT CHECKS
accountchecks = PIEdata.PIEdata('Account Checks', 'https://tcciub.pie.iu.edu/Api/AccountChecks?page=0&pageLimit=1000000')
accountchecks.createdbyPost = True
accountchecks.startPost = True
accountchecks.endPost = True
accountchecks.locationPost = True
list_o_data.append(accountchecks)

# ATTENDANCE ISSUES
attendance_issues = PIEdata.PIEdata('Attendance Issues', 'https://tcciub.pie.iu.edu/Api/AttendanceIssues?page=0&pageLimit=1000000')
attendance_issues.assignedToPost = True
list_o_data.append(attendance_issues)

# CHAT MESSAGES
chat_messages = PIEdata.PIEdata('Chat Messages', 'https://tcciub.pie.iu.edu/Api/ChatMessages?page=0&pageLimit=1000000')
chat_messages.createSwitch = True
list_o_data.append(chat_messages)

# INCIDENT REPORTS
incident_reports = PIEdata.PIEdata('Incident Reports', 'https://tcciub.pie.iu.edu/Api/IncidentReports?page=0&pageLimit=1000000')
incident_reports.createdbyPost = True
incident_reports.startPost = True
incident_reports.endPost = True
incident_reports.createSwitch = True
list_o_data.append(incident_reports)

def buildalldatathings(userdict, labdict, invlabs):

    # buff contacts
    contacts_long.createdbyDict = userdict
    contacts_long.locationDict = labdict
    contacts.createdbyDict = userdict
    contacts.locationDict = labdict

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

    # buff appointments
    appointments.assignedToDict = userdict

    # buff account checks
    accountchecks.createdbyDict = userdict
    accountchecks.locationDict = labdict

    # buff assigned badges
    assignedbadges.assignedToDict = userdict
    assignedbadges.createdbyDict = userdict

    # buff attendance issues
    attendance_issues.assignedToDict = userdict

    # buff chat messages
    chat_messages.createdbyDict = userdict

    # buff employee meetings
    employeeMeetings.createdbyDict = userdict
    employeeMeetings.assignedToDict = userdict

    # buff incident reports
    incident_reports.createdbyDict = userdict

    datalist = {}
    for data in list_o_data:
        datalist[data.name] = data

    return datalist
