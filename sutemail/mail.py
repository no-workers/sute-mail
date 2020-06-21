
import time
import sys
from bs4 import BeautifulSoup
from typing import List
import random
import re

from .config import Config


class Mail(object):
    def __init__(self):
        self.get_domains()

    def get_mail_list(self) -> List[str]:
        param = {
            "t": str(int(time.time())),
            "_": str(int(time.time())),
            "nopost": "1"
        }
        req = self.session.get(
            Config.HOST + Config.ADDRLIST,
            params=param
        )
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            return [
                span.text for span in soup.find_all('span') if span.text
            ]
        else:
            print(f"failed {sys._getframe().f_code.co_name} with statu code {req.status_code}")

    def get_domains(self):
        res = self.session.get(Config.HOST)
        soup = BeautifulSoup(res.text, 'html.parser')
        for input_element in soup.find_all('input'):
            if input_element['type'] == 'radio':
                Config.DOMINS.add(input_element["value"])

    def issue_new_custom_mail(self, name: str, domain: str, safe=False) -> str:
        if domain not in Config.DOMINS:
            if safe:
                domain = random.choice(Config.DOMINS)
            else:
                raise Exception("そんなドメインないです")
        if self.checkNewMail(name, domain):
            params = {
                "action": "addMailAddrByManual",
                "nopost": "1",
                "by_system": "1",
                "UID_enc": self.cookies['cookie_uidenc_seted'],
                "csrf_token_check": self.cookies['cookie_csrf_token'],
                "newdomain": domain,
                "newuser": name,
                "_": str(int(time.time()))
            }
            r = self.session.get(
                Config.HOST + Config.INDEX,
                params=params
            )
            if r.status_code == 200:
                return f"{name}@{domain}"
        raise Exception("できなかったってさ")

    def check_new_mail(self, name: str, domain: str) -> bool:
        params = {
            "action": "checkNewMailUser",
            "nopost": "1",
            "UID_enc": self.cookies["cookie_uidenc_seted"],
            "csrf_token_check": self.cookies["cookie_csrf_token"],
            "newdomain": domain,
            "newuser": name,
            "_": str(int(time.time()))
        }
        r = self.session.get(
            Config.HOST,
            params=params
        )
        if r.text == "OK":
            return True
        raise Exception("もうそのメアド誰かにとられてるよ")

    def issue_new_random_mail(self) -> str:
        params = {
            "action": "addMailAddrByAuto",
            "nopost": "1",
            "UID_enc": self.cookies["cookie_uidenc_seted"],
            "csrf_token_check": self.cookies['cookie_csrf_token'],
            "_": str(int(time.time()))
        }
        r = self.session.get(
            Config.HOST + Config.INDEX,
            params=params
        )
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.u.string

    def fetch_mails(self) -> dict:
        params = {
            "nopost": "1",
            "_": str(int(time.time()))
        }
        r = self.session.get(
            Config.HOST + Config.RECV,
            params=params
        )
        soup = BeautifulSoup(r.text, "html.parser")
        if soup.h3:
            return False
        num_key = {}
        for sp in soup.find_all("script"):
            if "openMailData" in str(sp.string):
                data = re.findall(r"openMailData.*", sp.string)
                numkey = re.findall(r"(?<=').*?(?='){7,}", data[0])
                num_key[numkey[0]] = numkey[2]
        return num_key

    def get_mail(self, mail_key: str, mail_num: str):
        pass
