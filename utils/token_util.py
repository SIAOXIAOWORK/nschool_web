import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import request
from functools import wraps


def generate_jwt(user_data):
    encoded_jwt = jwt.encode(user_data, "nschool", algorithm="HS256")
    return encoded_jwt


def get_jwt_token():
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
       
    return auth_header.split(" ")[1]

def verify_token(func):
    def wrapper(self, *args, **kwargs):
        jwt_token = get_jwt_token()

        if not jwt_token:
            return {"success":False, "message":"Missing token."}
        
        try:
            payload = jwt.decode(jwt_token, "nschool", algorithms=["HS256"])
                    
            if 'vendor_id' not in payload or not payload["vendor_id"] :
                return {"success":False, "message":"Vendor_id is null."}
            
            return func(self, payload, *args, **kwargs)
        
        except ExpiredSignatureError:
            return {"success":False, "message":"Token expired."} 
        
        except InvalidTokenError:
            return {"success":False, "message":"Invalid token."}
        
        
    
    return wrapper

