from passlib.context import CryptContext


password_context = CryptContext(schemes=['sha256_crypt'])


class Hasher:
    @staticmethod
    def get_hashed_password(password):
        return password_context.hash(password)

    @staticmethod
    def verify_passwrod(password, hashed_password):
        return password_context.verify(password, hashed_password)