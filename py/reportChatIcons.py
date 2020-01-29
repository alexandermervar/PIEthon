from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series, DataFrame, merge
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

    def iconlistcleaner(x):
        temper = []
        for icon in x:
            if icon in kingdict:
                temper.append(icon)
        return temper

    chatframe['icons'] = chatframe['colons'].map(lambda x: iconlistcleaner(x))
    chatframe = chatframe[['id', 'user-username', 'icons']]

    melted =\
    chatframe.icons.apply(Series) \
        .merge(chatframe, right_index=True, left_index=True) \
        .drop(["icons"], axis=1) \
        .melt(id_vars=['id', 'user-username'], value_name="icon") \
        .drop("variable", axis=1) \
        .dropna()

    chatframe = chatframe.sort_values(by='id', ascending=False)

    #total number of messages
    totalsent = melted[['user-username', 'id']]
    totalunique = totalsent.groupby(['user-username']).nunique().drop('user-username',axis=1)
    print(totalunique.head(10))
    print()

    #total icons sent
    totalicons = totalsent.groupby(['user-username']).count()
    print(totalicons.head(10))
    print()

    #find average number of icons/message
    chatframe['num_icons'] = chatframe['icons'].map(lambda x: len(x))
    averages = chatframe[['user-username', 'num_icons']]
    averages = averages.groupby(['user-username']).mean()
    print(averages.head(10))
    print()

    usertable = merge(totalunique,totalicons, left_index=True, right_index=True)
    usertable = merge(usertable, averages, left_index=True, right_index=True).reset_index()
    #usertable.columns.names = ['user-username', 'total messages', 'total icons', 'icons/message']
    print(usertable.head(10))

    report.add('table', 'Count of Icon Usage', usertable)
    """
    #do the cool thing
    plt.rcdefaults()
    fig, ax = plt.subplots()

    ax.barh(counts['icon'], counts['count'],align='center')
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Count of Icon Usage')

    plt.savefig(htmlbase.figure_path + '\\iconuse.png')

    report.add('graph', 'Icon Use Counts', '\\iconuse.png')
    """

    report.makeHTML('Chat Icon Usage')

description = "Chat icon usage numbers in selected time frame"
active = True
author = 'Brian Funk'

chaticonreport = report.report('Chat Icon Usage', author,active)
chaticonreport.description = description
chaticonreport.main_run = main