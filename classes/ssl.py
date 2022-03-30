from OpenSSL import crypto

import ssl
import tempfile

from datetime import datetime


class SSL:
    def __init__(self, hostname=None, email=None, country=None, locality=None, state=None, org=None, orgunit=None, validity=10*365*60*60*24, bits=4096):
        self.cn = hostname or "localhost"
        self.email = email or ("filemailer@%s" % (hostname or "localhost"))
        self.country = country or "AT"
        self.locality = locality or "Graz"
        self.state = state or "Steiermark"
        self.org = org or "Kumi Systems e.U."
        self.orgunit = orgunit or "FileMailer"
        self.validity = validity
        self.bits = bits

    def makeCert(self):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, self.bits)

        cert = crypto.X509()
        cert.get_subject().C = self.country
        cert.get_subject().ST = self.state
        cert.get_subject().L = self.locality
        cert.get_subject().O = self.org
        cert.get_subject().OU = self.orgunit
        cert.get_subject().CN = self.cn
        cert.get_subject().emailAddress = self.email
        cert.set_serial_number(int(datetime.now().timestamp()))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(self.validity)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')

        return cert, k

    def makeContext(self):
        cert, k = self.makeCert()

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        with tempfile.NamedTemporaryFile() as certfile, tempfile.NamedTemporaryFile() as keyfile:
            certdump = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
            certfile.write(certdump)
            certfile.flush()

            keydump = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
            keyfile.write(keydump)
            keyfile.flush()

            context.load_cert_chain(certfile.name, keyfile.name)

        return context

    @staticmethod
    def makeContextFromFiles(certfile="cert.pem", keyfile="key.pem"):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile, keyfile)
        return context