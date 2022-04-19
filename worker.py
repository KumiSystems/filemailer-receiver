from aiosmtpd.controller import Controller as SmtpdController
from aiosmtpd.smtp import AuthResult

import asyncio
import logging

from argparse import ArgumentParser

from classes.smtpdhandler import SmtpdHandler
from classes.config import Config
from classes.authenticator import Authenticator
from classes.ssl import SSL

if __name__ == "__main__":
    log = logging.basicConfig()

    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to config file", default="settings.ini")
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = Config(args.config)
    authenticator = Authenticator(config)
    handler = SmtpdHandler(config)

    smtpd = SmtpdController(handler, hostname=config.hostname,
                            port=config.port, authenticator=authenticator,
                            ident="Kumi Systems FileMailer", 
                            auth_require_tls=False)

    smtpd.start()

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
