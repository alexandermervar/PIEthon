from datetime import datetime
from pytz import utc

class semester:
    def __init__(self, name, start, end):
        self.name = name
        if start is not '':
            self.start = datetime.strptime(start[:10], '%Y-%m-%d').replace(tzinfo=utc)
        else:
            self.start = ''

        if end is not  '':
            self.end = datetime.strptime(end[:10], '%Y-%m-%d').replace(tzinfo=utc)
        else:
            self.end = ''

    def getName(self):
        return self.name

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end