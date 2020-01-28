from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

def main(driver, startdate, enddate, statuslabel, report):
    chats = PIEdataVARS.chat_messages
    chats.startDate = startdate
    chats.endDate = enddate
    urllist = chats.urlList()
    chatframe = PieHandler.goandget(driver, urllist, chats)

    chatframe = chatframe[['id', 'alert', 'created', 'text', 'user-username', 'user-firstName', 'user-lastName']]

    #find counts of messages sent
    message_counts = chatframe[['user-username', 'id']]
    message_counts = message_counts.groupby('user-username').count()

    def parseIcons(message):
        # first count number of colons in message
        iconsused = []
        count = message.count(':')
        if count < 2:
            return iconsused
        if (count % 2) == 0:
            # even number = good
            split = message.split(':')
            return split[1:]
        else:
            # odd number = bad
            split = message.split(':')
            return split[1:]

    chatframe['colons'] = chatframe['text'].map(lambda x: parseIcons(x))
    badlist = [' ', '  ', 'https']
    iconlist = chatframe['colons'].tolist()
    kingdict = {}
    for icons in iconlist:
        for icon in icons:
            icon = icon.strip()
            if len(icon) > 20 or len(icon) < 3:
                continue
            if icon in badlist:
                continue
            if icon in kingdict:
                kingdict[icon] = kingdict[icon] + 1
            else:
                kingdict[icon] = 1

    finaldict = {}
    for icon,count in kingdict.items():
        if count > 10:
            finaldict[icon] = count

    #chatframe = chatframe[['id', 'colons']].head(200)
    counts = DataFrame.from_dict(finaldict,orient='index').reset_index()
    counts.columns = ['icon', 'count']
    counts = counts.sort_values(by='count', ascending=False)

    report.add('table', 'Count of Icon Usage', counts)

    #do the cool thing
    plt.rcdefaults()
    fig, ax = plt.subplots()

    ax.barh(counts['icon'], counts['count'],align='center')
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Count of Icon Usage')

    plt.savefig(htmlbase.figure_path + '\\iconuse.png')

    report.add('graph', 'Icon Use Counts', '\\iconuse.png')

    report.makeHTML('Chat Icon Usage')

description = "Chat icon usage numbers in selected time frame"
active = True
author = 'Brian Funk'

chaticonreport = report.report('Chat Icon Usage', author,active)
chaticonreport.description = description
chaticonreport.main_run = main