import sys
import json
import os
import time
import zipfile
import platform

import urllib.request

try:
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import Chrome
except ImportError:
    print("we cant find selenium module\ndownloading selenium module...\n\n")
    os.system("pip install selenium")
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import Chrome

from .const import Const
from .auth import Auth
from .mail import Mail


class MailClient(Auth, Mail):
    def __init__(self, user_id: str=None, passwd: str=None, random: bool=False, driver_path: str="chromedriver"):
        Auth.__init__(self)
        if user_id and passwd:
            self.login_with_uid_and_passwd(user_id, passwd)
        else:
            self.login_with_cookies(random=random)
        self.start_chrome_driver(driver_path)
        Mail.__init__(self)

    def start_chrome_driver(self, path):
        options = Options()
        # options.add_argument("--headless")
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('--log-level=3')
        print("starting chrome")
        self.driver = Chrome(options=options, executable_path=path)


def check_driver():
    system = platform.system()
    if os.path.isfile(Const.driver_path[system]):
        return Const.driver_path[system]
    elif "chromedriver" not in os.environ:
        path = "./chromedriver.zip"
        print("We can't find chromedriver in your environ\ninstalling chrome driver....")

        urllib.request.urlretrieve(Const.driver_urls[system], path)

        print(f"success download\nunpacking zip...\n")

        with zipfile.ZipFile(path) as zip_file:
            zip_file.extractall()

        print("success\n")
        os.remove(path)
        return Const.driver_path[system]
    else:
        return "chromedriver"
