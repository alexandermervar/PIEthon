from datetime import timedelta, date
from py import functions

class PIEdata:
    def __init__(self, name, link):

        #core properties
        self.name = name
        self.link = link
        self.chunk_size = 30

        #filters
        self.createdby = ''
        self.createdbyDict = {}
        self.assignedTo = ''
        self.assignedToDict = {}
        self.location = ''
        self.locationDict = {}
        self.category = ''
        self.categoryDict = {}
        self.status = ''
        self.statusDict = {}
        self.startDate = date.today() - timedelta(days=30)
        self.endDate = date.today()
        self.maxreturns = 10000000

        #flags
        self.createdbyPost = False
        self.assignedToPost = False
        self.locationPost = False
        self.categoryPost = False
        self.statusPost = False
        self.startPost = False
        self.endPost = False

        self.invbool = False
        self.form = False
        self.formkey = False
        self.allowbracks = False

    def urlList(self):
        if self.startDate == '':
            return [self.genURL('')]

        urllist = []
        tempdate = self.startDate

        while (self.endDate - tempdate).days > self.chunk_size:
            urllist.append(self.genURL(tempdate))
            tempdate = tempdate + timedelta(days=self.chunk_size)

        urllist.append(self.genURL(tempdate))

        return urllist

    def genURL(self, startdate):
        #take a startdate and create a url for it
        baseurl = self.link
        if (not self.startPost and self.startDate is not ''):
            baseurl = baseurl + '&startTime=' + str(startdate)
        if (not self.endPost and self.endDate is not ''):
            baseurl = baseurl + '&endTime=' + str(startdate + timedelta(days=self.chunk_size))
        if (self.createdbyDict is not {} and not self.createdbyPost and self.createdby is not ''):
            baseurl = baseurl + '&creatorIds=' + self.createdby
        if (self.assignedToDict is not {} and not self.assignedToPost and self.assignedTo is not ''):
            baseurl = baseurl + '&userId=' + self.assignedTo
        if (self.locationDict is not {} and not self.locationPost and self.location is not ''):
            baseurl = baseurl + '&LocationIds=' + self.location
        if (self.categoryDict is not {} and not self.categoryPost and self.category is not ''):
            baseurl = baseurl + '&categoryIds=' + self.category
        if (self.statusDict is not {} and not self.statusPost and self.status is not ''):
            baseurl = baseurl + '&statuses=' + self.status
        print(baseurl)
        return baseurl


        
    def make_url(self):

        if self.startDate == '':
            return [self.link]

        datelist = []

        while(self.endDate-self.startDate).days > self.chunk_size:
            datelist.append(self.startDate)
            self.set_startDate(self.startDate+timedelta(days=self.chunk_size))
        datelist.append(self.startDate)
        storeend = self.endDate
        chunkcount = 1

        urllist = []
        for startDate in datelist:
            self.set_startDate(startDate)
            if(chunkcount == len(datelist)):
                self.set_endDate(storeend)
            else:
                self.set_endDate(startDate+timedelta(days=self.chunk_size))
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
        vardict['startDate'] = functions.pieTimeConvert(self.startDate)
        vardict['endDate'] = functions.pieTimeConvert(self.endDate)
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
