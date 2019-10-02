import seleniumHandlers
import time
import dataconverter
import users
import PIEdataVARS
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def caslogin(driver, username, password, duotype):
    driver.get("https://cas.iu.edu")

    usernamebox = seleniumHandlers.getBy(driver, 'id', 'username', 5)
    usernamebox.send_keys(username)

    passbox = seleniumHandlers.getBy(driver, 'id', 'password', 5)
    passbox.send_keys(password)

    button = driver.find_element_by_class_name('button')
    button.click()

    if duotype=="push":
        iframe = seleniumHandlers.getBy(driver,'id','duo_iframe',3)
        driver.switch_to.frame(iframe)
        button = driver.find_element_by_xpath("//*[contains(text(), 'Push')]")
        if not button is False:
            button.click()
        driver.switch_to.default_content()
    elif duotype=="call":
        iframe = seleniumHandlers.getBy(driver,'id','duo_iframe',3)
        driver.switch_to.frame(iframe)
        button = driver.find_element_by_xpath("//*[contains(text(), 'Call')]")
        if not button is False:
            button.click()
        driver.switch_to.default_content()
    else:
        print('lol you chose code, this is still in development reee')

    if(seleniumHandlers.getBy(driver, 'link_text', 'begin the logout process', 15) == False):
        return False
    else:
        return driver

def getPie(driver):
    driver.get('https://pie.iu.edu')
    piebut = seleniumHandlers.getBy(driver, 'xpath', "//*[@id=\"mainContent\"]/div/div[2]/div/div/p/button[1]", 5)
    piebut.click()
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.LINK_TEXT, "IUB TCC"))
    )

    element = driver.find_element_by_link_text("IUB TCC")
    element.click()

    time.sleep(.5)

    cookies = driver.get_cookies()

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return session

def spamPieChat(driver, message, times):
    #assumes driver is already logged in
    x=0
    while x < times:
        chatbox = seleniumHandlers.getBy(driver, 'id', 'chatMessageText', 5)
        chatbox.send_keys(message)

        sendit = seleniumHandlers.getBy(driver, 'xpath',
                                        "//*[@id=\"mainContent\"]/div/div[2]/div/div/div[1]/div[2]/div[2]/form/button",
                                        5)
        sendit.click()
        time.sleep(8)
        x += 1

def grabUsers(driver):
    framey = goandget(driver, ['https://pie.iu.edu/Api/Users?page=0&pageLimit=1000&searchTerms=&active=true&whitelistInclusiveMaskNames=Employee&fromUsersView=true&maskId=5'], PIEdataVARS.contacts)

    framey['name'] = framey['lastName'] + ', ' + framey['firstName']
    framey = framey[['id', 'username', 'name']]

    userlist = {}

    tempuser = users.user('','','')
    userlist[''] = tempuser

    for index, row in framey.iterrows():
        tempuser = users.user(row['name'], row['username'], row['id'])
        userlist[row['name']] = tempuser

    return userlist

def grabLabs(driver):
    labframe = goandget(driver, ['https://pie.iu.edu/Api/Locations?'], PIEdataVARS.contacts)

    lablist = {}
    lablist[''] = ''

    for index, row in labframe.iterrows():
        lablist[row['shortName']] = row['id']

    return lablist

def grabInvLabs(driver):
    labframe = goandget(driver,['https://pie.iu.edu/Api/InventoryLocations?page=0&pageLimit=1010'], PIEdataVARS.contacts)

    labframe = labframe[['location-shortName', 'id']]

    lablist = {}
    lablist[''] = ''
    for index, row in labframe.iterrows():
        lablist[row['location-shortName']] = row['id']

    return lablist

def goandget(driver, urllist, piedata):
    totString = ''
    counter = 1
    for url in urllist:
        r = driver.get(url)
        endcut = -1
        startcut = 1
        rawInput = r.text
        #print(rawInput)
        if len(rawInput) == 0 or not rawInput:
            continue
        if (piedata.getform()):
            #this is a form, changing startcut and endcut
            endcut=rawInput.find("questions")-3
            startcut=12
        if len(rawInput) <= 2 or (piedata.getform() and rawInput[11] =='[' and rawInput[12] == ']'):
            if counter==1:
                totString = '[' + totString
            elif counter==len(urllist):
                if totString[-1] == ",":
                    totString = totString[:-1]
                totString = totString + ']'
            counter+=1
            continue
        if (len(urllist) != 1):
            if counter == 1:
                if (piedata.getform()):
                    rawInput = rawInput[startcut-1:endcut] + ','
                else:
                    rawInput = rawInput[:endcut] + ','
            elif counter == len(urllist) or len(totString) == 0:
                if (piedata.getform()):
                    rawInput = rawInput[startcut:endcut] + ']'
                else:
                    rawInput = rawInput[startcut:]
            else:
                rawInput = rawInput[startcut:endcut] + ','
        totString = totString + rawInput
        counter+=1
    if (totString == False):
        return
    else:
        frame = dataconverter.getFrame(totString, piedata.allowbracks)
        return frame


def goandgetinv(driver, urllist, invsearch):
    supString = ''
    counter = 1
    for url in urllist:
        driver.get(url)
        rawInput = seleniumHandlers.getBy(driver, 'tag', 'body', 5).text
        if (len(urllist) != 1):
            if counter == 1:
                rawInput = rawInput[1:]
                #rawInput = rawInput[:-1]
                #rawInput = rawInput + ','
            elif counter == len(urllist):
                rawInput = rawInput[:-1]
                rawInput = rawInput + ','
            else:
                rawInput = rawInput[1:]
                rawInput = rawInput[:-1]
                rawInput = rawInput + ','
        supString = rawInput + supString
        counter+=1
    if (rawInput == False):
        return
    else:
        frame = dataconverter.invedit(supString, invsearch)
        return frame

def findinvused(frame):
    paperdict = {}

    for index, row in frame.iterrows():
        if row['labname'] not in paperdict:
            templist = []
            templist.append(row['reordernum'])
            paperdict[row['labname']] = templist
        else:
            paperdict[row['labname']] = [row['count']] + paperdict.get(row['labname'])

    return paperdict

def usepapdict(paperdict):
    usagedict = {}
    for key,val in paperdict.items():
        if (len(val) < 5) or (key == 'EG100'):
            usagedict[key] = ''
            continue
        val = list(filter(None,val))
        if key == 'TV250':
            reorder = 6
        elif key == 'UE020':
            reorder = 11
        else:
            reorder = val[-1]
        usage = invloop(val,reorder,0, key)
        usagedict[key] = usage
    negativevals = []
    for key, val in usagedict.items():
        if type(val) is not int:
            negativevals.append(key)
            continue
        if (val<0):
            negativevals.append(key)
    for valer in negativevals:
        usagedict[valer] = 0
    return usagedict


def invloop(listthing, reorder, used, key):
    starting = findstart(listthing[:5], reorder)
    prev = starting
    jumpthresh = 8
    dropthresh = 1.3
    if key == 'LC114':
        jumpthresh = 12
        dropthresh = 2
    jumpcheck = 0
    jumplist = []
    dropcheck = 0
    droplist = []
    lastvalid = starting
    for x in range(0, len(listthing) - 1):
        if (prev <= reorder) and ((listthing[x] - prev) > reorder):
            print('found a big jump below reorder')
            used = used + (starting - prev)
            return invloop(listthing[x:],reorder, used, key)
        elif (prev + jumpthresh < listthing[x]):
            print('jump up')
            jumpcheck+=1
            jumplist.append(listthing[x])
            if jumpcheck == 3:
                print('three jumps in a row')
                used = used + starting - lastvalid
                starting = max(jumplist)
                prev = listthing[x]
        elif (prev-listthing[x]) > (reorder/dropthresh):
            print('drop down')
            dropcheck+=1
            droplist.append(listthing[x])
            if dropcheck == 3:
                print('three drops in a row')
                used = used + starting - lastvalid
                starting = max(droplist)
                prev = listthing[x]
        else:
            jumpcheck = 0
            jumplist = []
            dropcheck = 0
            droplist = []
            prev = listthing[x]
            lastvalid = listthing[x]
    used = used + (starting - prev)
    return used

def findstart(listthing, reorder):
    thing = reorder * 11
    if listthing == []:
        print("RUH ROW SHAGGYjljlkjlkjl;kj;kjhkljguytiguyilyygulihybujhkhjooiubjuj")
        return
    if max(listthing) is None:
        return listthing[0]
    if max(listthing) <= (reorder*11):
        return max(listthing)
    else:
        listthing.remove(max(listthing))
        return findstart(listthing, reorder)
