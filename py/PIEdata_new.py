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
            baseurl = baseurl + '&creatorIds=' + str(self.createdbyDict[self.createdby].getId())
        if (self.assignedToDict is not {} and not self.assignedToPost and self.assignedTo is not ''):
            baseurl = baseurl + '&userId=' + str(self.assignedToDict[self.assignedTo].getId())
        if (self.locationDict is not {} and not self.locationPost and self.location is not ''):
            baseurl = baseurl + '&LocationIds=' + str(self.locationDict[self.location])
        if (self.categoryDict is not {} and not self.categoryPost and self.category is not ''):
            baseurl = baseurl + '&categoryIds=' + str(self.categoryDict[self.category])
        if (self.statusDict is not {} and not self.statusPost and self.status is not ''):
            baseurl = baseurl + '&statuses=' + str(self.statusDict[self.status])
        if 'mini' in self.name:
            baseurl = baseurl + '&mini=true'
        print(baseurl)
        return baseurl

    def reset(self):
        self.createdby = ''
        self.assignedTo = ''
        self.location = ''
        self.category = ''
        self.status = ''