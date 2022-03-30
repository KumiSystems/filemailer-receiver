from configparser import ConfigParser
from socket import gethostname
from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash


class Config:
    def __init__(self, path):
        self.config = ConfigParser()
        self.path = path
        self.config.read(path)

        self.hash_passwords()

    def hash_passwords(self):
        hasher = PasswordHasher()

        for user, password in self.config.items("USERS"):
            try:
                hasher.check_needs_rehash(password)
            except InvalidHash:
                self.config["USERS"][user] = hasher.hash(password)

        with open(self.path, "w") as configfile:
            self.config.write(configfile)

    def verify_password(self, user, password):
        hasher = PasswordHasher()

        try:
            hasher.verify(self.config["USERS"][user], password)
            return True
        except:
            return False

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