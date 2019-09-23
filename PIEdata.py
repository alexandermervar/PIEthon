import datetime
import functions

class PIEdata:
    def __init__(self, name, link, variables):
        self.variables = variables
        self.name = name
        self.link = link
        self.startdate = ''
        self.enddate = ''
        self.username = ''
        self.location = ''
        self.category = ''
        self.status = ''
        self.assignedto = ''
        self.maxreturns = 100
        self.userdict = {}
        self.labdict = {}
        self.statusdict = []
        self.categorydict = {}
        self.assigneddict = {}
        self.invlocationdict = {}
        self.invbool = False
        self.chunk_size = 30
        self.form = False
        self.formkey = False
        self.allowbracks = False

    def getallowbracks(self):
        return self.allowbracks

    def setallowbracks(self, boolboy):
        self.allowbracks = boolboy

    def setformkey(self, newVal):
        self.formkey = newVal

    def getformkey(self):
        return self.formkey

    def setform(self, newVal):
        self.form = newVal

    def getform(self):
        return self.form

    def setinvlocationdict(self, newVal):
        self.invlocationdict = newVal

    def setinvbool(self, newVal):
        self.invbool = newVal

    def setchuncks(self, newVal):
        self.chunk_size = newVal

    def setuserdict(self, newVal):
        self.userdict = newVal

    def setlabdict(self, newVal):
        self.labdict = newVal

    def setstatusdict(self, newVal):
        self.statusdict = newVal

    def setcategorydict(self, newVal):
        self.categorydict = newVal

    def getName(self):
        return self.name

    def getuserdict(self):
        return self.userdict

    def getlabdict(self):
        return self.labdict

    def getstatusdict(self):
        return self.statusdict

    def getcategorydict(self):
        return self.categorydict

    def getassigneddict(self):
        return self.assigneddict

    def getstartdate(self):
        return self.startdate

    def getenddate(self):
        return self.enddate

    def getinvlocationdict(self):
        return self.invlocationdict

    def getinvbool(self):
        return self.invbool

    def set_startdate(self, newVal):
        self.startdate = newVal

    def set_enddate(self, newVal):
        self.enddate = newVal

    def set_username(self, newVal):
        self.username = newVal

    def set_location(self, newVal):
        self.location = newVal

    def set_category(self, newVal):
        self.category = newVal

    def set_maxreturns(self, newVal):
        self.maxreturns = newVal

    def set_status(self, newVal):
        self.status = newVal

    def set_assigneddict(self, newVal):
        self.assigneddict = newVal

    def set_assignedto(self, newVal):
        self.assignedto = newVal

    def getvariablelist(self):
        return self.variables

    def make_url(self):

        if self.startdate == '':
            return [self.link]

        datelist = []

        while(self.enddate-self.startdate).days > self.chunk_size:
            datelist.append(self.startdate)
            self.set_startdate(self.startdate+datetime.timedelta(days=self.chunk_size))
        datelist.append(self.startdate)
        storeend = self.enddate
        chunkcount = 1

        urllist = []
        for startdate in datelist:
            self.set_startdate(startdate)
            if(chunkcount == len(datelist)):
                self.set_enddate(storeend)
            else:
                self.set_enddate(startdate+datetime.timedelta(days=self.chunk_size))
            vardict = self.urlDict()
            newvars = []
            for thing in self.variables:
                newvars.append(vardict[thing])
            url = self.link.format(*newvars)
            urllist.append(url)
            chunkcount+=1
        return urllist

    def urlDict(self):
        vardict = {}
        vardict['startdate'] = functions.pieTimeConvert(self.startdate)
        vardict['enddate'] = functions.pieTimeConvert(self.enddate)
        if (not self.username == ''):
            vardict['username'] = self.userdict[self.username].getId()
        else:
            vardict['username'] = ''
        if (not self.location == ''):
            vardict['location'] = self.labdict[self.location]
        else:
            vardict['location'] = ''
        vardict['category'] = self.category
        vardict['maxreturns'] = self.maxreturns
        if (len(self.assignedto) > 1):
            vardict['assignedto'] = self.assigneddict[self.assignedto].getId()
        else:
            vardict['assignedto'] = ''
        vardict['status'] = self.status
        return vardict