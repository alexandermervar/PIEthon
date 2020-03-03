from py import PIEdataVARS, PieHandler, htmlbase, report
from pandas import Series, DataFrame, merge, concat, to_datetime
import datetime
import matplotlib.pyplot as plt
from collections import Counter

def main(driver, startdate, enddate, statuslabel, report):

    # okay so take active users and then do an individual query for each one on assigned badges oh gosh okay also select columns
    # so that we don't nuke the memory probably. BREAK

    #lets grab active users
    activeusers = PIEdataVARS.activerusers
    urllist = activeusers.urlList()
    ids = PieHandler.goandget(driver, urllist, activeusers)['id'].tolist()

    # find badges for each user and scooby doo them together
    badges = PIEdataVARS.assignedbadges

    frames = []

    for id in ids:
        url = [badges.link + '&userId=' + str(id)]
        print(url)
        frame = PieHandler.goandget(driver,url,badges)
        if frame is not False:
            if 'assignedBy-username' not in frame:
                frame['assignedBy-username'] = ''
            if 'badge-assignedBy' not in frame:
                frame['badge-assignedBy'] = ''
            frame = frame[['user-username','assignedBy-username','badge-assignedBy','badge-badgeCategory-description','badge-name', 'created', 'user-lastName','user-firstName']]
            frames.append(frame)

    bigo = concat(frames)
    bigo['created'] = bigo['created'].astype(str).str[:-6]
    bigo['created'] = to_datetime(bigo['created'])
    bigo['user-username'] = bigo['user-firstName'] + ' ' + bigo['user-lastName']

    bigo = bigo.sort_values(['user-username','badge-name','created'],ascending=(True,True,True))

    # find number of badges total
    totalnum = bigo[['user-username','badge-name']].groupby(['user-username']).count()
    totalnum.rename(columns={totalnum.columns[0]: "total badges"}, inplace=True)

    # total unique badges
    totalunique = bigo[['user-username','badge-name','created']].groupby(['user-username','badge-name']).count().reset_index().groupby(['user-username']).count()
    totalunique.rename(columns={totalunique.columns[0]: "total unique badges"}, inplace=True)

    #find total badges received in period
    startdate = datetime.datetime.combine(startdate, datetime.datetime.min.time())
    enddate = datetime.datetime.combine(enddate, datetime.datetime.min.time())
    totalnew = bigo[(bigo['created'] > startdate) & (bigo['created'] < enddate)]
    totalnew = totalnew[['user-username', 'badge-name']].groupby(['user-username']).count()
    totalnew.rename(columns={totalnew.columns[0]: "badges in period"}, inplace=True)

    #first time badges this month
    firsts = bigo[['user-username','badge-name','created']].groupby(['user-username','badge-name']).agg({'created':'first'})
    firsts = firsts[(firsts['created'] > startdate) & (firsts['created'] < enddate)]
    firsts = firsts.groupby(['user-username']).count()
    firsts.rename(columns={firsts.columns[0]: "first time badges in period"}, inplace=True)

    merged = merge(totalnum, totalunique, left_index=True, right_index=True,how='left')
    merged = merge(merged, totalnew, left_index=True, right_index=True,how='left')
    merged = merge(merged, firsts, left_index=True, right_index=True,how='left').reset_index()
    merged.rename(columns={merged.columns[0]: "user"}, inplace=True)
    merged.drop(['created'],axis=1,inplace=True)

    merged.sort_values(['total badges'], inplace=True, ascending=True, na_position='first')

    plt.tight_layout()
    merged.plot(x='user', y='total badges',kind='barh', figsize=(8, 10), zorder=2, width=0.85)
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path + '\\totalbadges.png')
    report.add('graph', 'Total Badges', '\\totalbadges.png')

    merged.sort_values(['total unique badges'], inplace=True, ascending=True, na_position='first')

    plt.tight_layout()
    merged.plot(x='user', y='total unique badges',kind='barh', figsize=(8, 10), zorder=2, width=0.85)
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path + '\\totalubadges.png')
    report.add('graph', 'Total Unique Badges', '\\totalubadges.png')

    merged.sort_values(['badges in period'], inplace=True, ascending=True, na_position='first')

    plt.tight_layout()
    merged.plot(x='user', y='badges in period',kind='barh', figsize=(8, 10), zorder=2, width=0.85)
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path + '\\periodbadges.png')
    report.add('graph', 'Total Badges in Period', '\\periodbadges.png')

    merged.sort_values(['first time badges in period'], inplace=True, ascending=True, na_position='first')

    plt.tight_layout()
    merged.plot(x='user', y='first time badges in period',kind='barh', figsize=(8, 10), zorder=2, width=0.85)
    plt.tight_layout()
    plt.savefig(htmlbase.figure_path + '\\firstbadges.png')
    report.add('graph', 'First Time Badges in Period', '\\firstbadges.png')

    merged.sort_values(['user'], inplace=True, ascending=True)

    report.add('table', 'Badge Report Data', merged)

    report.makeHTML('Badge Assignments')

description = "Finds the number of badges assigned to each user in a time period in various dimensions"
active = True
author = 'Brian Funk'

badgereport = report.report('Badge Assignments', author,active)
badgereport.description = description
badgereport.main_run = main