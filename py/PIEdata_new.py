from datetime import timedelta, date, datetime
from py import functions
import pandas as pd
import numpy as np

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
            baseurl = baseurl + '&statuses=' + self.status
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
        self.startDate = ''
        self.endDate = ''

    def postFilter(self, frame, semesters):
        print(self.createdbyPost)
        print(self.createdby)

        #helper for getting things?
        def semesterMatch(x):
            for name,semester in semesters.items():
                if name is '':
                    continue
                if semester.start <= x.replace(tzinfo=None) <= semester.end:
                    return name
            return None

        #limit semesters to info I care about?
        # nah

        #attempt to parse creation date into a dope super cool columns thing
        try:
            frame['created'] = pd.to_datetime(frame['created'], utc=True)
            frame['created-year'] = pd.DatetimeIndex(frame['created']).year
            frame['created-month'] = pd.DatetimeIndex(frame['created']).month
            frame['created-week'] = pd.DatetimeIndex(frame['created']).week
            frame['created-day'] = pd.DatetimeIndex(frame['created']).day
            frame['created-weekday'] = pd.DatetimeIndex(frame['created']).weekday
            frame['created-hour'] = pd.DatetimeIndex(frame['created']).hour
            # semester time oh boy
            frame['semester'] = frame['created'].map(lambda x: semesterMatch(x))

        except:
            print('could not parse date information')

        #true post processing - epic gamer moment incoming

        if (self.startPost and self.startDate is not ''):
            # filter frame to after startdate
            try:
                frame = frame[frame['created'] >= self.startDate]
            except:
                print('cannot post-filter on start date')
        if (self.endPost and self.endDate is not ''):
            # filter frame to before enddate
            print('temp')
        if (self.createdbyPost and self.createdby is not ''):
            # filter frame to created by
            createdbyid = self.createdbyDict[self.createdby].getId()
            try:
                frame = frame[frame['assignedBy-id'] == createdbyid]
            except:
                print('cannot post filter on createdby')
        if (self.assignedToPost and self.assignedTo is not ''):
            # filter frame to assigned to
            print('temp')
        if (self.locationPost and self.location is not ''):
            # filter frame to location
            print('temp')
        if (self.categoryPost and self.category is not ''):
            # filter frame to category
            print('temp')
        if (self.statusPost and self.status is not ''):
            # filter frame to status
            print('temp')
        return frame