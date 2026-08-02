import jwt
import time


JWT_SECRET = "300528ea6d4acbc36b57cdabb88fb014b1cd3c67e4a4e0bbeae5e1d31032d165"
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(email, id):
    payload = {'identifier': {'email': email, 'id': id}, 'exp': time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_jwt if decode_jwt['exp'] >= time.time() else None
    except:
        return {}
