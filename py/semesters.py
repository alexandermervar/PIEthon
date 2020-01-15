from datetime import datetime

class semester:
    def __init__(self, name, start, end):
        self.name = name
        if start is not '':
            self.start = datetime.strptime(start[:10], '%Y-%m-%d')
        else:
            self.start = ''

        if end is not  '':
            self.end = datetime.strptime(end[:10], '%Y-%m-%d')
        else:
            self.end = ''

    def getName(self):
        return self.name

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def match(self,datein):
        print('starting match')
        return self.start < datein < self.end