from time import sleep
from py import dataconverter, PIEdataVARS, seleniumHandlers, users, semesters
from requests import Session
from pandas import to_numeric, DataFrame
from numpy import diff, sum
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

    if seleniumHandlers.getBy(driver,'xpath', "//*[contains(text(), 'Login unsuccessful:')]", 2) is not False:
        return 'invalidlogin'

    if duotype=="push":
        iframe = seleniumHandlers.getBy(driver, 'id', 'duo_iframe', 5)
        driver.switch_to.frame(iframe)
        button = driver.find_element_by_xpath("//*[contains(text(), 'Push')]")
        if not button is False:
            button.click()
        driver.switch_to.default_content()
    elif duotype=="call":
        iframe = seleniumHandlers.getBy(driver, 'id', 'duo_iframe', 5)
        driver.switch_to.frame(iframe)
        button = driver.find_element_by_xpath("//*[contains(text(), 'Call')]")
        if not button is False:
            button.click()
        driver.switch_to.default_content()
    else:
        iframe = seleniumHandlers.getBy(driver, 'id', 'duo_iframe', 5)
        driver.switch_to.frame(iframe)
        button = driver.find_element_by_xpath("//*[contains(text(), 'Passcode')]")
        if not button is False:
            button.click()
        inputthing = seleniumHandlers.getBy(driver, 'class', 'passcode-input', 5)
        inputthing.send_keys(duotype)
        sleep(.5)
        button = driver.find_element_by_xpath("//*[contains(text(), 'Log In')]")
        if not button is False:
            button.click()
        driver.switch_to.default_content()

    if(seleniumHandlers.getBy(driver, 'link_text', 'begin the logout process', 20) == False):
        return False
    else:
        return driver

def getPie(driver):
    driver.get('https://tcciub.pie.iu.edu')
    #piebut = seleniumHandlers.getBy(driver, 'xpath', "//*[@id=\"mainContent\"]/div/div[2]/div/div/p/button[1]", 5)
    #piebut.click()


    element = driver.find_element_by_xpath("//*[contains(text(), 'Sign In Using IU Login')]")
    element.click()

    sleep(.5)

    cookies = driver.get_cookies()

    session = Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return session

def grabUsers(driver):
    framey = goandget(driver, ['https://pie.iu.edu/Api/Users?page=0&pageLimit=1000&searchTerms=&active=true&whitelistInclusiveMaskNames=Employee&fromUsersView=true&maskId=5'], PIEdataVARS.contacts)

    framey['name'] = framey['lastName'] + ', ' + framey['firstName']
    framey = framey[['id', 'username', 'name']]

    userlist = {}

    tempuser = users.user('', '', '')
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
    labframe = goandget(driver, ['https://pie.iu.edu/Api/InventoryLocations?page=0&pageLimit=1010'], PIEdataVARS.contacts)

    labframe = labframe[['location-shortName', 'id']]

    lablist = {}
    lablist[''] = ''
    for index, row in labframe.iterrows():
        lablist[row['location-shortName']] = row['id']

    return lablist

def grabSemesters(driver):
    framey = goandget(driver, [PIEdataVARS.schedules.link], PIEdataVARS.schedules)

    framey = framey[['name', 'startTime', 'endTime']]

    semkey = {}

    tempuser = semesters.semester('', '', '')
    semkey[''] = tempuser

    for index, row in framey.iterrows():
        tempuser = semesters.semester(row['name'], row['startTime'], row['endTime'])
        semkey[row['name']] = tempuser

    return semkey

def goandget(driver, urllist, piedata):
    totString = ''
    counter = 1
    for url in urllist:
        r = driver.get(url)
        endcut = -1
        startcut = 1
        rawInput = r.text
        if len(rawInput) == 0 or not rawInput:
            continue
        if (piedata.getform()):
            #this is a form, changing startcut and endcut
            endcut=rawInput.find("questions")-3
            startcut=12
        if len(rawInput) <= 2 or (piedata.getform() and rawInput[11] =='[' and rawInput[12] == ']'):
            if counter==1 and counter==len(urllist):
                continue
            elif counter==1:
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
    if (totString == False) or (totString == ''):
        return False
    else:
        frame = dataconverter.getFrame(totString, piedata.allowbracks)
        return frame


def goandgetinv(driver, urllist, invsearch):
    supString = ''
    counter = 1
    for url in urllist:
        rawInput = driver.get(url).text
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

def invcounttwo(invframe):
    thingy = invframe.groupby(by='labname')

    lab = []
    paper = []

    for name,data in thingy:
        lab.append(name)
        counts = to_numeric(data['count']).dropna().to_numpy().astype(int)
        difs = diff(counts)
        reorderthresh = float(data[['reordernum']].mean()/1.15)
        newdifs = difs[difs < reorderthresh]
        newerdifs = newdifs[newdifs > 0]
        paper.append(sum(newerdifs))

    return DataFrame({'lab':lab,'paper_used':paper})




