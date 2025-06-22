import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import request

def generate_jwt(user_data):
    encoded_jwt = jwt.encode(user_data, "nschool", algorithm="HS256")
    return encoded_jwt


def get_jwt_token():
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
       
    return auth_header.split(" ")[1]

def verify_token():
    jwt_token = get_jwt_token()

    if not jwt_token:
        return False, "Missing token"
    
    try:
        payload = jwt.decode(jwt_token, "nschool", algorithms=["HS256"])
        return True, payload
    
    except ExpiredSignatureError:
        return False, "Token expired"
    
    except InvalidTokenError:
        return False, "Invalid token"

