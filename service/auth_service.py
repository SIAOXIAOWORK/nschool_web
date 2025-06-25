from app import g
import hashlib
from utils.token_util import generate_jwt
import time
import re
from flask import request

class LoginServer:

    def check_login_args(self, account, password):
        hash_password = hashlib.md5(password.encode()).hexdigest()
        g.cur.execute("SELECT id, user_name FROM member where account = %s and password = %s",(str(account), str(hash_password)))
        data = g.cur.fetchone()
        if data:
            member_id = data["id"] 
            user_name = data["user_name"]
            vendor_id = None
            
            g.cur.execute("SELECT id FROM vendor where member_id = %s", (member_id,))
            vendor_data = g.cur.fetchone()
            if vendor_data:
                print(vendor_data)
                vendor_id = vendor_data["id"]


            token_args = {"id":member_id, "user_name":user_name, "vendor_id":vendor_id, "exp":int(time.time())+3600}
            token = generate_jwt(token_args)
            return True, token
        return False, None
    


class RegisterServer:
    
    def register_member(self, account, password, user_name, email, phone):
        checkdata = CheckData()
        
        result, message = checkdata.check_register_member_args(account, password, email, phone)

        if result:
            hash_password = hashlib.md5(password.encode()).hexdigest()
            g.cur.execute("INSERT INTO member(account, password, user_name, email, phone) VALUES(%s, %s, %s, %s, %s)",(account, hash_password, user_name, email, phone))
            g.conn.commit()
            return True, None
        
        return False, message
    
    def register_vendor(self, member_id, store_name, store_address, store_phone, store_reg_no):


        checkdata = CheckData()

        result, message = checkdata.check_register_verdor_args(store_phone, store_reg_no)
        if not result:
            return False, message
        
        g.cur.execute("INSERT INTO vendor(member_id, store_name, store_address, store_phone, store_reg_no) VALUES (%s, %s, %s, %s, %s)",(member_id, store_name, store_address, store_phone, store_reg_no))
        g.conn.commit()

        return True, None
        

            

    

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
        
        if g.cur.fetchone()[0]:
            message = "Store_reg_no already exists."
            return False, message
        
        return True, None

    def check_member_id(self, member_id):
        g.cur.execute("SELECT EXISTS(SELECT 1 FROM member where id = %s)",(int(member_id),))
        result = g.fetchone()[0]
        if not result:
            return False, "Invalid id"
        
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