from aiosmtpd.controller import Controller as SmtpdController
from aiosmtpd.smtp import AuthResult

import asyncio
import logging

from classes.smtpdhandler import SmtpdHandler
from classes.config import Config
from classes.authenticator import Authenticator
from classes.ssl import SSL

if __name__ == "__main__":
    log = logging.basicConfig()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    config = Config("settings.ini")
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
