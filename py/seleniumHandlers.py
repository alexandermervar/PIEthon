from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from errno import ENOENT, EACCES
from os.path import basename
from platform import system
import subprocess
from time import sleep
from warnings import warn
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome import service, webdriver, remote_connection

#https://stackoverflow.com/questions/33983860/hide-chromedriver-console-in-python

def getBy(driverIn, byType, key, delay):
    if (byType== 'id'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.ID, key)))
            return myElem
        except TimeoutException:
            return False
    elif (byType == 'xpath'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.XPATH, key)))
            return myElem
        except TimeoutException:
            return False
    elif (byType == 'class'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.CLASS_NAME, key)))
            return myElem
        except TimeoutException:
            return False
    elif (byType == 'name'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.NAME, key)))
            return myElem
        except TimeoutException:
            return False
    elif (byType == 'css'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, key)))
            return myElem
        except TimeoutException:
            return False
    elif (byType == 'tag'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.TAG_NAME, key)))
            return myElem
        except TimeoutException:
            return False
    elif (byType == 'link_text'):
        try:
            myElem = WebDriverWait(driverIn, delay).until(EC.presence_of_element_located((By.LINK_TEXT, key)))
            return myElem
        except TimeoutException:
            return False
    else:
        print("Please use a valid byType")
        return False

class HiddenChromeService(service.Service):

    def start(self):
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())

            if system() == 'Windows':
                info = subprocess.STARTUPINFO()
                info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = 0  # SW_HIDE (6 == SW_MINIMIZE)
            else:
                info = None

            self.process = subprocess.Popen(
                cmd, env=self.env,
                close_fds=system() != 'Windows',
                startupinfo=info,
                stdout=self.log_file,
                stderr=self.log_file,
                stdin=subprocess.PIPE)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            elif err.errno == EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "Executable %s must be in path. %s\n%s" % (
                    basename(self.path), self.start_error_message,
                    str(e)))
        count = 0
        while True:
            self.assert_process_still_running()
            if self.is_connectable():
                break
            count += 1
            sleep(1)
            if count == 30:
                raise WebDriverException("Can't connect to the Service %s" % (
                    self.path,))


class HiddenChromeWebDriver(webdriver.WebDriver):
    def __init__(self, executable_path="chromedriver", port=0,
                options=None, service_args=None,
                desired_capabilities=None, service_log_path=None,
                chrome_options=None, keep_alive=True):
        if chrome_options:
            warn('use options instead of chrome_options',
                        DeprecationWarning, stacklevel=2)
            options = chrome_options

        if options is None:
            # desired_capabilities stays as passed in
            if desired_capabilities is None:
                desired_capabilities = self.create_options().to_capabilities()
        else:
            if desired_capabilities is None:
                desired_capabilities = options.to_capabilities()
            else:
                desired_capabilities.update(options.to_capabilities())

        self.service = HiddenChromeService(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=remote_connection.ChromeRemoteConnection(
                    remote_server_addr=self.service.service_url,
                    keep_alive=keep_alive),
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise
        self._is_remote = False