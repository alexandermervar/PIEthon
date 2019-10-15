from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def getBy(driverIn, byType, key, delay):
    if (byType== 'id'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.ID, key)))
            return myElem
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif (byType == 'xpath'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.XPATH, key)))
            return myElem
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif (byType == 'class'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.CLASS_NAME, key)))
            return myElem
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif (byType == 'name'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.NAME, key)))
            return myElem
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif (byType == 'css'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, key)))
            return myElem
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif (byType == 'tag'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.TAG_NAME, key)))
            return myElem
        except TimeoutException:
            print("Loading took too much time!")
            return False
    elif (byType == 'link_text'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.LINK_TEXT, key)))
            return myElem
        except TimeoutException:
            print("Loading took too much time!")
            return False
    else:
        print("Please use a valid byType")
        return False