import os
import json
import requests
import sys


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


    def login_with_cookies(self, random: bool=False):
        if random:
            self.cookies = self.get_cookies()
        elif os.path.isfile("./cookies.json"):
            with open("./cookies.json") as file:
                self.cookies = json.load(file)
        else:
            self.cookies = self.get_cookies()
        """
            dictオブジェクトをcookiesオブジェクトに変換
        """
        self.session.cookies = cookiejar_from_dict(self.cookies)
        self.save_cookies()


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
        if req.status_code == 200:
            uid = req.text.lstrip("OK:")
            self.reissue_cookies(uid)
        else:
            print(f"failed {sys._getframe().f_code.co_name} with statu code {req.status_code}")


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
        if req.status_code == 200:
            """
                重複するcookiesをなくすために一度辞書にする
            """
            self.session.cookies.update(req.cookies.get_dict())
            self.session.cookies = cookiejar_from_dict(self.session.cookies.get_dict())
        else:
            print(f"failed {sys._getframe().f_code.co_name} with statu code {req.status_code}")
        self.save_cookies()


    def get_cookies(self) -> dict:
        req = self.session.get(
            Config.HOST,
        )
        if req.status_code == 200:
            pattern = r"csrf_subtoken_check=[a-zA-z0-9]*"
            self.login_token = re.findall(pattern, req.text)[0].lstrip("csrf_subtoken_check=")
            soup = BeautifulSoup(req.text, "html.parser")
            self.passwd = re.findall(r"[0-9]*", soup.find("td", id="area_passwordview").string)[11]
            self.userID = re.findall(r"[0-9]*", soup.find("td", id="area_numberview").string)[12]
            print(f"""アカウントの作成に成功
userid : {self.userID}
passwd : {self.passwd}""")
            return req.cookies.get_dict()
        else:
            print(f"failed {sys._getframe().f_code.co_name} with statu code {req.status_code}")

    def save_cookies(self):
        with open("./cookies.json", "w") as file:
            json.dump(self.cookies, file, indent=4, ensure_ascii=False)
