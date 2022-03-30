import uuid
import json

from email.utils import formatdate
from pathlib import Path


class SmtpdHandler:
    def __init__(self, config):
        self.config = config

    async def handle_MAIL(self, server, session, envelope, address, mail_options):
        if session.authenticated:
            envelope.mail_from = address
            return('250 OK')
        return('530 5.7.0 Authentication required')

    async def handle_DATA(self, server, session, envelope):
        eid = uuid.uuid4()

        try:
            with open(Path(self.config.maildir) / f"{eid}.eml", "wb") as mailfile:
                mailfile.write(
                    f"From {envelope.mail_from} {formatdate()}\n".encode())
                mailfile.write(
                    f"Received: from {session.host_name} ({session.peer[0]}) by {server.hostname} (Kumi Systems FileMailer) id {eid}; {formatdate()}\n".encode())
                mailfile.write(envelope.original_content)
            with open(Path(self.config.maildir) / f"{eid}.json", "w") as jsonfile:
                data = {
                    "sender": envelope.mail_from,
                    "recipients": envelope.rcpt_tos
                }

                json.dump(data, jsonfile)

            return('250 Message accepted for delivery')

        except:
            return('451 Requested action aborted: local error in processing')
