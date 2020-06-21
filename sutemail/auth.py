import os
import json
import requests

from requests.cookies import cookiejar_from_dict

import time

from bs4 import BeautifulSoup
import re


from .config import Config


class Auth(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": Config.USER_AGENT
        }

    def login_with_cookies(self):
        if os.path.isfile("./cookies.json"):
            with open("./cookies.json") as file:
                self.cookies = json.load(file)
        else:
            self.cookies = self.get_cookies()
        self.session.cookies = cookiejar_from_dict(self.cookies)

    def login_with_uid_and_passwd(self, user_id: str, password: str):
        self.login_with_cookies()
        param = {
            "action": "checkLogin",
            "nopost": "1",
            "UID_enc": self.cookies["cookie_uidenc_seted"],
            "csrf_token_check": self.cookies["cookie_csrf_token"],
            "csrf_subtoken_check": self.login_token,
            "number": user_id,
            "password": password,
            "t": str(int(time.time())),
            "_": str(int(time.time()))
        }
        req = self.session.get(
            Config.HOST + Config.INDEX,
            params=param
        )
        uid = req.text.lstrip("OK:")
        self.reissue_cookies(uid)

    def reissue_cookies(self, uid: str):
        param = {
            "action": "changeUID",
            "new_UID": uid
        }
        req = self.session.get(
            Config.HOST + Config.INDEX,
            params=param,
            allow_redirects=False
        )
        self.session.cookies.update(req.cookies.get_dict())

    def get_cookies(self) -> dict:
        req = self.session.get(
            Config.HOST,
        )
        pattern = r"csrf_subtoken_check=[a-zA-z0-9]*"
        self.login_token = re.findall(pattern, req.text)[0].lstrip("csrf_subtoken_check=")
        return req.cookies.get_dict()

    def save_cookies(self):
        with open("./cookies.json", "w") as file:
            json.dump(self.cookies, file, indent=4, ensure_ascii=False)