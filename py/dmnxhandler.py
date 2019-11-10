from py import seleniumHandlers
from time import sleep
from fnmatch import fnmatch
from pandas import read_csv
from os import listdir, remove

def getdmnx(driver, username, password):
    driver.get('https://dmnx.print.iu.edu:51433/index.html')
    usernamebox = seleniumHandlers.getBy(driver, 'name', 'username', 5)
    usernamebox.send_keys(username)

    passbox = seleniumHandlers.getBy(driver, 'name', 'password', 5)
    passbox.send_keys(password)

    button = driver.find_element_by_class_name('buttonRounded')
    button.click()

    expando = seleniumHandlers.getBy(driver, 'id', 'isc_1Copen_icon_9', 10)
    expando.click()

    sleep(.5)

    expando = seleniumHandlers.getBy(driver, 'id', 'isc_1Copen_icon_11', 10)
    expando.click()

    sleep(.5)

    expando = seleniumHandlers.getBy(driver, 'id', 'isc_1Cicon_13', 10)
    expando.click()

    sleep(.5)

    expando = seleniumHandlers.getBy(driver, 'id', 'isc_25', 10)
    expando.click()

    sleep(.5)

def gettable(driver):
    buttonguy = seleniumHandlers.getBy(driver, 'name', 'isc_2Xicon', 20)
    buttonguy.click()

    sleep(1)

    for file in listdir('.'):
        if fnmatch(file, '*.csv'):
            dataframeo = read_csv(file, header=4)
            remove(file)

    return dataframeo







