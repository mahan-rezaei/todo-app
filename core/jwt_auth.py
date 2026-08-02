import jwt
import time


def token_response(token: str):
    return {"access_token": token}


def sighn_jwt(email, id):
    payload = {'identifier': {'email': email, 'id': id}, 'exp': time.time() + 600}
    token = jwt.encode(payload)
    return token_response(token)


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token)
        return decode_jwt if decode_jwt['exp'] >= time.time() else None
    except:
        return {}
