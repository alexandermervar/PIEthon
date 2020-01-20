from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series

def main(driver, startdate, enddate, statuslabel):
    activeuserstruct = PIEdataVARS.chat_messages
    urllist = activeuserstruct.make_url()
    chatframe = PieHandler.goandget(driver, urllist, activeuserstruct)

    chatframe = chatframe[['id', 'alert', 'created', 'text', 'user-username', 'user-firstName', 'user-lastName']]

    tablelist = [chatframe.to_html()]
    picturelist = []

    outputfile = htmlbase.htmlbase('Chat Icon Usage', 'Chat Icon Usage', tablelist, picturelist)
    outputfile.makeHTML('Chat Icon Usage')

description = "Chat icon usage numbers in selected time frame"
active = False
author = 'Brian Funk'

chaticonreport = report.report('Chat Icon Usage', author,active)
chaticonreport.description = description
chaticonreport.main_run = main