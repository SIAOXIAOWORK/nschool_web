from app import g
import hashlib
from utils.token_util import create_jwt
import time
import re

class LoginServer:

    def check_login_args(self, account, password):
        hash_password = hashlib.md5(password.encode()).hexdigest()
        g.cur.execute("SELECT id, user_name FROM member where account = %s and password = %s",(str(account), str(hash_password)))
        data = g.cur.fetchone()
        if data:
            id, user_name = data
            token_args = {"id":id, "user_name":user_name, "exp":time.time()}
            token = create_jwt(token_args)
            return True, token
        return False, None
    


class RegisterServer:
    
    def check_register_args(self, account, password, user_name, email, phone):
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


    def check_account(self, account):
        if not 4 <= len(account) <= 20 :
            message = "Account must be 4 to 20 characters."
            return False, message
        
        g.cur.execute("SELECT EXISTS(SELECT 1 FROM member WHERE account = %s)",(str(account),))
        
        if g.cur.fetchone()[0]:
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

    def register_member(self, account, password, user_name, email, phone):
        
        result, message = self.check_register_args(account, password, user_name, email, phone)

        if result:
            hash_password = hashlib.md5(password.encode()).hexdigest()
            g.cur.execute("INSERT INTO member(account, password, user_name, email, phone) VALUES(%s, %s, %s, %s, %s)",(account, hash_password, user_name, email, phone))
            g.conn.commit()
            return True, None
        
        return False, message