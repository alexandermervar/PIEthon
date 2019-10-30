class report:
    def __init__(self, name, author, active):
        self.name = name
        self.author = author
        self.active = active
        self.description = ''
        self.main_run = False

    def run_main(self, driver, startdate,enddate,statuslabel):
        if self.main_run is False:
            print('Main not initialized')
            return
        else:
            self.main_run(driver, startdate,enddate,statuslabel)

from py import reportLabBreakdown, reportMissingUserInfo, reportPDIs, reportStepouts

report_list = [reportLabBreakdown.labbreakreport,
               reportMissingUserInfo.missinginforeport,
               reportPDIs.pdireport,
               reportStepouts.stepoutreport]