from configparser import ConfigParser
from socket import gethostname
from pathlib import Path
from hmac import compare_digest

import crypt
import re


class Config:
    def __init__(self, path):
        self.config = ConfigParser()
        self.path = path
        self.config.read(path)

        self.hash_passwords()

    def hash_passwords(self):
        for user, password in self.config.items("USERS"):
            if not re.match(r"\$\d\$", string):
                self.config["USERS"][user] = crypt.crypt(
                    password, crypt.mksalt())

        with open(self.path, "w") as configfile:
            self.config.write(configfile)

    def verify_password(self, user, password):
        hashed = self.config["USERS"][user]
        return compare_digest(hashed, crypt.crypt(password, hashed))

    @property
    def hostname(self):
        return self.config.get("SERVER", "hostname", fallback=gethostname())

    @property
    def port(self):
        return self.config.getint("SERVER", "port", fallback=8025)

    @property
    def maildir(self):
        path = self.config.get("SERVER", "maildir", fallback="maildir")
        Path(path).mkdir(parents=True, exist_ok=True)
        return path
