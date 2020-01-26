from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series

def main(driver, startdate, enddate, statuslabel):
    chats = PIEdataVARS.chat_messages
    chats.startDate = startdate
    chats.endDate = enddate
    urllist = chats.urlList()
    chatframe = PieHandler.goandget(driver, urllist, chats)

    chatframe = chatframe[['id', 'alert', 'created', 'text', 'user-username', 'user-firstName', 'user-lastName']]

    #find counts of messages sent
    message_counts = chatframe.groupby('user-username').count()
    print(message_counts.columns)

    tablelist = [message_counts.to_html()]
    picturelist = []

    outputfile = htmlbase.htmlbase('Chat Icon Usage', 'Chat Icon Usage', tablelist, picturelist)
    outputfile.makeHTML('Chat Icon Usage')

description = "Chat icon usage numbers in selected time frame"
active = False
author = 'Brian Funk'

chaticonreport = report.report('Chat Icon Usage', author,active)
chaticonreport.description = description
chaticonreport.main_run = main