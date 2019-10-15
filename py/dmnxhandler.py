from py import seleniumHandlers
import time
import fnmatch
import pandas as pd
import os

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

    time.sleep(.5)

    expando = seleniumHandlers.getBy(driver, 'id', 'isc_1Copen_icon_11', 10)
    expando.click()

    time.sleep(.5)

    expando = seleniumHandlers.getBy(driver, 'id', 'isc_1Cicon_13', 10)
    expando.click()

    time.sleep(.5)

    expando = seleniumHandlers.getBy(driver, 'id', 'isc_25', 10)
    expando.click()

    time.sleep(.5)

def gettable(driver) :
    buttonguy = seleniumHandlers.getBy(driver, 'name', 'isc_2Xicon', 20)
    buttonguy.click()

    time.sleep(1)

    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.csv'):
            dataframeo = pd.read_csv(file, header=4)
            os.remove(file)

    return dataframeo







