from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series, DataFrame, merge
import matplotlib.pyplot as plt
from collections import Counter

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
            if not icon[0].isalpha():
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

    chatframe['num_icons'] = chatframe['icons'].map(lambda x: len(x))

    #total number of messages
    beefer = chatframe[['user-username', 'id']]
    totalunique = beefer.groupby(['user-username']).count()

    #total icons sent
    icoframe = chatframe[['user-username', 'num_icons']]
    totalicons = icoframe.groupby(['user-username']).sum()
    #totalunique.columns.names = ['user-username', 'total icons sent']

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

    usertable = merge(totalunique,totalicons, left_index=True, right_index=True)
    usertable = merge(usertable,merged, left_index=True,right_index=True)
    usertable['avg icons/message'] = usertable['num_icons'] / usertable['id']
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

    # now do the exact same thing, but with icons. Will need to melt.
    #make new version of chatframe that only has what I care about
    iconframe = chatframe[['id', 'user-username', 'icons']]
    melted = iconframe.explode('icons')

    # find total messages appeared in
    iconappearance = melted.groupby(['id','icons']).count().groupby(['icons']).count()
    iconappearance.rename(columns={iconappearance.columns[0]: "messages appeared in"}, inplace=True)

    # find total uses
    uses = melted.groupby('icons').count()
    uses.rename(columns={uses.columns[1]: "times used"}, inplace = True)
    uses = uses[['times used']]

    # most used by
    usedby = melted.groupby(['icons','user-username'], as_index=False)['id'].count()
    inner = usedby.groupby(['icons']).agg({'id':'max'}).reset_index()
    usedby = merge(left = usedby, right=inner, how='inner', left_on=['icons','id'], right_on=['icons','id'])
    usedby = usedby.set_index('icons')

    usedby['most used by (times)'] = usedby['user-username'] + ' (' + usedby['id'].astype(str) + ')'
    usedby = usedby[['most used by (times)']]
    usedby = usedby.groupby(['icons']).agg({'most used by (times)':'first'})

    # unique users
    uniqueusers = melted.groupby(['icons','user-username'], as_index=False)['id'].count().groupby(['icons']).agg({'user-username':'count'})
    uniqueusers.rename(columns={uniqueusers.columns[0]: "unique users"}, inplace=True)

    # join em all into a biggy wiggy
    merged = merge(iconappearance,uses, left_index=True, right_index=True)
    merged = merge(merged,usedby,left_index=True,right_index=True)
    merged = merge(merged, uniqueusers, left_index=True, right_index=True).reset_index()
    merged.rename(columns={merged.columns[0]: "icon name"}, inplace=True)

    report.add('table', 'Icon User Usage', merged)


    report.makeHTML('Chat Icon Usage')

description = "Chat icon usage numbers in selected time frame"
active = True
author = 'Brian Funk'

chaticonreport = report.report('Chat Icon Usage', author,active)
chaticonreport.description = description
chaticonreport.main_run = main