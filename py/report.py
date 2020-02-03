from py import htmlbase

class report:
    def __init__(self, name, author, active):
        self.name = name
        self.author = author
        self.active = active
        self.description = ''
        self.main_run = False
        self.htmlbase = htmlbase.htmlbase()

    def run_main(self, driver, startdate,enddate,statuslabel):
        if self.main_run is False:
            print('Main not initialized')
            return
        else:
            self.main_run(driver, startdate,enddate,statuslabel, self)

    def add(self, type, title, info):
        self.htmlbase.add(type,title,info)

    def makeHTML(self, filename):
        self.htmlbase.makeHTML(filename)

    def reset(self):
        self.htmlbase = htmlbase.htmlbase()

from py import reportLabBreakdown, reportMissingUserInfo, reportPDIs, reportStepouts, reportChatIcons

report_list = [reportLabBreakdown.labbreakreport,
               reportMissingUserInfo.missinginforeport,
               reportPDIs.pdireport,
               reportStepouts.stepoutreport,
               reportChatIcons.chaticonreport]