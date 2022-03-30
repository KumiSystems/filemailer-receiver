from aiosmtpd.smtp import AuthResult

class Authenticator:
    def __init__(self, config):
        self.config = config

    def __call__(self, server, session, envelope, mechanism, auth_data):
        return AuthResult(success=self.config.verify_password(auth_data.login.decode(), auth_data.password.decode()), handled=True)
