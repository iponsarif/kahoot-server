import jwt
from flask import abort
from datetime import datetime, timedelta


def encode(data):
    payload = {
        "data": data,
        # "exp": datetime.utcnow() + timedelta(seconds=1000),
        # "exp": datetime.utcnow(),
        # "iat": datetime.utcnow()
    }
    
    encoded = jwt.encode(payload, "kucing-merah", algorithm="HS256").decode('utf-8')
    return encoded

def decode(data):
    try:
        decoded = jwt.decode(data, "kucing-merah", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        abort(403)

    return decoded