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

        #flags
        self.createdbyPost = False
        self.assignedToPost = False
        self.locationPost = False
        self.categoryPost = False
        self.statusPost = False
        self.startPost = False
        self.endPost = False
        self.createSwitch = False
        self.employeeswitch = False
        self.allowDates = True

        self.invbool = False
        self.form = False
        self.formkey = False
        self.allowbracks = False
        self.append = ''

    def urlList(self):
        if self.startDate == '' or self.startPost:
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
        if (not self.startPost and self.startDate is not '' and self.allowDates):
            baseurl = baseurl + '&startTime=' + str(startdate.strftime('%Y-%m-%d'))
        if (not self.endPost and self.endDate is not '' and self.allowDates):
            baseurl = baseurl + '&endTime=' + str((startdate + timedelta(days=self.chunk_size)).strftime('%Y-%m-%d'))
        if (self.createdbyDict is not {} and not self.createdbyPost and self.createdby is not ''):
            if not self.createSwitch:
                if len(self.categoryDict) > 1:
                    baseurl = baseurl + '&creatorIds=' + str(self.createdbyDict[self.createdby].getId())
                else:
                    baseurl = baseurl + '&creatorId=' + str(self.createdbyDict[self.createdby].getId())
            else:
                baseurl = baseurl + '&userId=' + str(self.createdbyDict[self.createdby].getId())
        if (self.assignedToDict is not {} and not self.assignedToPost and self.assignedTo is not ''):
            if not self.employeeswitch:
                baseurl = baseurl + '&userId=' + str(self.assignedToDict[self.assignedTo].getId())
            else:
                baseurl = baseurl + '&employeeId=' + str(self.assignedToDict[self.assignedTo].getId())
        if (self.locationDict is not {} and not self.locationPost and self.location is not ''):
            if not self.invbool:
                baseurl = baseurl + '&LocationIds=' + str(self.locationDict[self.location])
            else:
                baseurl = baseurl + '&inventoryLocationId=' + str(self.locationDict[self.location])
        if (self.categoryDict is not {} and not self.categoryPost and self.category is not ''):
            baseurl = baseurl + '&categoryIds=' + str(self.categoryDict[self.category])
        if (self.statusDict is not {} and not self.statusPost and self.status is not ''):
            baseurl = baseurl + '&statuses=' + self.status
        baseurl = baseurl + self.append
        #print(baseurl)
        return baseurl

    def reset(self):
        self.createdby = ''
        self.assignedTo = ''
        self.location = ''
        self.category = ''
        self.status = ''
        self.startDate = date.today() - timedelta(days=30)
        self.endDate = date.today()

    def postFilter(self, frame, semesters):

        #helper for getting things?
        def semesterMatch(x):
            for name,semester in semesters.items():
                if name is '':
                    continue
                if semester.start <= x <= semester.end:
                    return name
            return None

        #attempt to parse creation date into a dope super cool columns thing
        try:
            if 'created' in frame:
                frame['created'] = pd.to_datetime(frame['created'], utc=True)
                frame['created-year'] = pd.DatetimeIndex(frame['created']).year
                frame['created-month'] = pd.DatetimeIndex(frame['created']).month
                frame['created-week'] = pd.DatetimeIndex(frame['created']).week
                frame['created-day'] = pd.DatetimeIndex(frame['created']).day
                frame['created-weekday'] = pd.DatetimeIndex(frame['created']).weekday
                frame['created-hour'] = pd.DatetimeIndex(frame['created']).hour
                frame['semester'] = frame['created'].map(lambda x: semesterMatch(x))

            if 'startTime' in frame:
                frame['startTime'] = pd.to_datetime(frame['startTime'], utc=True)
                frame['startTime-year'] = pd.DatetimeIndex(frame['startTime']).year
                frame['startTime-month'] = pd.DatetimeIndex(frame['startTime']).month
                frame['startTime-week'] = pd.DatetimeIndex(frame['startTime']).week
                frame['startTime-day'] = pd.DatetimeIndex(frame['startTime']).day
                frame['startTime-weekday'] = pd.DatetimeIndex(frame['startTime']).weekday
                frame['startTime-hour'] = pd.DatetimeIndex(frame['startTime']).hour
                frame['startTime-semester'] = frame['startTime'].map(lambda x: semesterMatch(x))

            if 'endTime' in frame:
                frame['endTime'] = pd.to_datetime(frame['endTime'], utc=True)
                frame['endTime-year'] = pd.DatetimeIndex(frame['endTime']).year
                frame['endTime-month'] = pd.DatetimeIndex(frame['endTime']).month
                frame['endTime-week'] = pd.DatetimeIndex(frame['endTime']).week
                frame['endTime-day'] = pd.DatetimeIndex(frame['endTime']).day
                frame['endTime-weekday'] = pd.DatetimeIndex(frame['endTime']).weekday
                frame['endTime-hour'] = pd.DatetimeIndex(frame['endTime']).hour
                frame['endTime-semester'] = frame['endTime'].map(lambda x: semesterMatch(x))

        except:
            print('could not parse date information')

        #true post processing - epic gamer moment incoming

        if (self.startPost and self.startDate is not ''):
            # filter frame to after startdate
            if 'created' in frame:
                frame = frame[frame['created'] >= self.startDate]
            else:
                print('cannot post-filter on start date')
        if (self.endPost and self.endDate is not ''):
            if 'created' in frame:
                frame = frame[frame['created'] < self.endDate]
            else:
                print('cannot post-filter on end date')
        if (self.createdbyPost and self.createdby is not ''):
            # filter frame to created by
            createdbyid = self.createdbyDict[self.createdby].getId()
            if 'assignedBy-id' in frame:
                frame = frame[frame['assignedBy-id'] == createdbyid]
            elif 'user-id' in frame and self.createSwitch:
                frame = frame[frame['user-id'] == createdbyid]
            elif 'creator-id' in frame:
                frame = frame[frame['creator-id'] == createdbyid]
        if (self.assignedToPost and self.assignedTo is not ''):
            # filter frame to assigned to
            assignedtoid = self.assignedToDict[self.assignedTo].getId()
            if 'user-id' in frame:
                frame = frame[frame['user-id'] == assignedtoid]
            elif 'attendingEmployee-id' in frame:
                frame = frame[frame['attendingEmployee-id'] == assignedtoid]
        if (self.locationPost and self.location is not ''):
            # filter frame to location
            locationid = self.locationDict[self.location]
            if 'location-id' in frame:
                frame = frame[frame['location-id'] == locationid]
            elif 'shiftGroup-shiftType-baseLocation-id' in frame:
                frame = frame[frame['shiftGroup-shiftType-baseLocation-id'] == locationid]
        if (self.categoryPost and self.category is not ''):
            # filter frame to category
            print('temp')
        if (self.statusPost and self.status is not ''):
            # filter frame to status
            print('temp')
        return frame