from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series, DataFrame, merge
import matplotlib.pyplot as plt
from collections import Counter
import operator

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

    def iconlistcleaner(x):
        temper = []
        for icon in x:
            if icon in kingdict:
                temper.append(icon)
        return temper

    chatframe['icons'] = chatframe['colons'].map(lambda x: iconlistcleaner(x))
    chatframe = chatframe[['id', 'user-username', 'icons']]
    print(chatframe.head(30))

    chatframe['num_icons'] = chatframe['icons'].map(lambda x: len(x))
    print(chatframe.head(15))

    #total number of messages
    beefer = chatframe[['user-username', 'id']]
    totalunique = beefer.groupby(['user-username']).count()
    #totalunique.columns.names = ['user-username','total messages sent']
    print(totalunique.head(15))
    print()

    #total icons sent
    icoframe = chatframe[['user-username', 'num_icons']]
    totalicons = icoframe.groupby(['user-username']).sum()
    #totalunique.columns.names = ['user-username', 'total icons sent']
    print(totalicons.head(15))
    print()

    #fold the frames down

    def find_max(x):
        if (len(x) == 0):
            return 'N/A'
        else:
            maxer = 0
            val = 'N/A'
            for key, value in x.items():
                if value > maxer:
                    val = key
                    maxer = value
            return val + ' (' + str(maxer) + ')'

    modded = chatframe[['user-username', 'icons']]
    merged = modded.groupby('user-username').agg({'icons': 'sum'})
    merged['counts'] = merged['icons'].apply(lambda x: dict(Counter(x)))
    merged['most_used (times)'] = merged['counts'].apply(lambda x: find_max(x))
    merged['unique icons used'] = merged['counts'].apply(lambda x: len(x))
    merged = merged[['most_used (times)', 'unique icons used']]
    print(merged.head(5))

    usertable = merge(totalunique,totalicons, left_index=True, right_index=True)
    usertable = merge(usertable,merged, left_index=True,right_index=True)
    print(usertable.head(30))
    usertable['avg icons/message'] =  usertable['num_icons'] / usertable['id']
    usertable=usertable.reset_index()
    usertable.columns = ['username', 'total messages sent', 'total icons sent', 'most used (times)', 'unique icons used', 'avg icons/message']

    smaller = usertable.sort_values(by=['total messages sent'], ascending=False).head(20)
    smaller = smaller.sort_values(by=['total messages sent'], ascending=True)
    smaller = smaller[['username', 'total messages sent', 'total icons sent']]

    plt.tight_layout()
    smaller.plot(x='username',kind='barh', figsize=(8, 10), zorder=2, width=0.85)
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path + '\\totalmessages.png')

    report.add('table', 'User Icon Usage', usertable)
    report.add('graph', 'Total Messages sent', '\\totalmessages.png')

    report.makeHTML('Chat Icon Usage')

description = "Chat icon usage numbers in selected time frame"
active = True
author = 'Brian Funk'

chaticonreport = report.report('Chat Icon Usage', author,active)
chaticonreport.description = description
chaticonreport.main_run = main