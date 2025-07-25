import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import request
from functools import wraps
import re
from app import g
from datetime import datetime

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
                    
            if 'vendor_id' not in payload:
                return {"success":False, "message":"Vendor_id is null."}
            
            return func(self, payload, *args, **kwargs)
        
        except ExpiredSignatureError:
            return {"success":False, "message":"Token expired."} 
        
        except InvalidTokenError:
            return {"success":False, "message":"Invalid token."}
        
           
    return wrapper


class CheckData:

    def check_register_member_args(self, account, password, email, phone):
        result, message =  self.check_account(account)
        if not result:
            return False, message
        
        result, message =  self.check_password(password)
        if not result:
            return False, message
        
        result, message =  self.check_email(email)
        if not result:
            return False, message
        
        result, message =  self.check_phone(phone)
        if not result:
            return False, message
        
        return True, None
    
    def check_register_verdor_args(self, store_phone, store_reg_no):

        result, message = self.check_phone(store_phone)
        if not result:
            return False, message
        
        result, message = self.check_store_reg_no(store_reg_no)
        if not result:
            return False, message
        
        return True, None

    def check_store_reg_no(self, store_reg_no):
        g.cur.execute("SELECT EXISTS(SELECT 1 FROM vendor where store_reg_no = %s)",(str(store_reg_no),))
        
        if g.cur.fetchone()['exists']:
            message = "Store_reg_no already exists."
            return False, message
        
        return True, None

    def check_member_id(self, member_id):
        g.cur.execute("SELECT EXISTS(SELECT 1 FROM member where id = %s)",(int(member_id),))
        result = g.fetchone()['exists']
        if not result:
            return False, "Invalid id"
        
        return True, None

    def check_account(self, account):
        if not 4 <= len(account) <= 20 :
            message = "Account must be 4 to 20 characters."
            return False, message
        
        g.cur.execute("SELECT EXISTS(SELECT 1 FROM member WHERE account = %s)",(str(account),))
       
        if g.cur.fetchone()["exists"]:
            
            message = "Account already exists."
            return False, message
        
        return True, None
    
    def check_password(self, password):
        if not 6 <= len(password) <= 20:
            message = "Password must be 6 to 20 characters."
            return False, message

        if not re.search(r"[A-Z]", password):
            message = "Password must have capital English"
            return False, message

        if not re.search(r"[a-z]", password):
            message = "Password must have lowercase English"
            return False, message
        
        return True, None

    def check_user_name(self, user_name):
        if not user_name.strip():
            message = "User_name can't be empty."
            return False, message
       
        return True, None

    def check_email(self, email):
        if not re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email):
            message = "Ivaild email"
            return False, message
        
        return True, None
    
    def check_phone(self, phone):
        if not re.search(r'09\d{8}', phone):
            message = 'Ivaild phone'
            return False, message
        
        return True, None
    

    def check_datetime(self, value):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid datetime format. Expected ISO8601.")