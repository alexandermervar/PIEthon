import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def buildHeadless():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    #here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #here = here.replace('\\','/')
    #prefs = {'download.default_directory': here}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(
        executable_path='resources//chromedriver.exe',
        chrome_options=chrome_options)

    return driver

def pieTimeConvert(date):
    fordate = date.strftime('%Y-%m-%d')
    temp = fordate + 'T04%3A00%3A00.000Z'
    return temp

def getSeconds(time):
    if time.count('.') > 1:
        return 0
    sep = '.'
    rest = time.split(sep, 1)[0]
    h, m, s = rest.split(':')
    secs = int(h) * 3600 + int(m) * 60 + int(s)
    hours = secs / 3600
    return hours

def getMinutes(time):
    if time.count('.') > 1:
        return 0
    sep = '.'
    rest = time.split(sep, 1)[0]

    h, m, s = rest.split(':')

    secs = int(h) * 3600 + int(m) * 60 + int(s)
    hours = secs / 60
    return hours

def getAbb(abb):
    badlist = ['RI', '(s', 'FL', 'TR']
    if (abb[:2] in badlist):
        return ''
    if (not abb[:2] == 'LI'):
        return abb[:2]
    else:
        return abb[:3]

def getMonth(date):
    return date[5:7]

def make_autopct(values):
    print(values)
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct