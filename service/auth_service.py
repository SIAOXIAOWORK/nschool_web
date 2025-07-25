from app import g
import hashlib
from utils.util import generate_jwt, CheckData
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
                vendor_id = vendor_data["id"]


            token_args = {"id":member_id, "user_name":user_name, "vendor_id":vendor_id, "exp":int(time.time())+3600}
            token = generate_jwt(token_args)
            return True, token
        return False, None
    

class Member:
    def __init__(self, id, user_name, phone, email):
        self.id = id
        self.user_name = user_name
        self.phone = phone
        self.email = email

    
    




class MemberService:


    def get_member_data(self, payload, member_id):
        result = False
        message = None
        if not member_id == payload['id']:
            message = "You don't have permission to get member data."
            return result, message, None
        
        g.cur.execute("SELECT account, user_name, phone, email FROM member where id = %s",(member_id,))
        member_data = g.cur.fetchone()
        result = True
        return result, message, member_data
    
    def modify_member_data(self, member_id, **kwargs):
        check_data = CheckData()
        user_name = kwargs.get("user_name")
        phone = kwargs.get("phone")
        email = kwargs.get("email")
        g.cur.execute("SELECT id, user_name, phone, email FROM member where id = %s",(member_id,))
        member_data = g.cur.fetchone()
        member = Member(**member_data)
        
        
        if user_name:
            result , message = check_data.check_user_name(user_name)
            if not result:
                return result, message, None
            member.user_name = user_name

        if phone:
            result, message = check_data.check_phone(phone)
            if not result:
                return result, message, None
            member.phone = phone
            
        if email:
            result, message = check_data.check_email(email)
            if not result:
                return result, message, None
            member.email = email
            
        sql = """
            UPDATE member 
            SET
                user_name = %s,
                phone = %s,
                email = %s
            WHERE id = %s
            """
        g.cur.execute(sql, (member.user_name, member.phone, member.email, member_id))
        g.conn.commit()
        payload = member.__dict__
        return True, None, payload
    
    def change_password(self, member_id, password):
        checkdata = CheckData()
        result, message = checkdata.check_password(password)
        
        if not result:
            return False, message, None

        hash_password = hashlib.md5(password.encode()).hexdigest()
        sql = """
        UPDATE member
        SET
            password = %s
        WHERE id = %s
        """
        g.cur.execute(sql,(hash_password, member_id))
        g.conn.commit()

        message = "Change password success."

        return True, message, None
    
        
        



    
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

        message = None
        token = None
        result = None

        checkdata = CheckData()

        result, message = checkdata.check_register_verdor_args(store_phone, store_reg_no)
        if not result:
            return result, message, token
        
        g.cur.execute("INSERT INTO vendor(member_id, store_name, store_address, store_phone, store_reg_no) VALUES (%s, %s, %s, %s, %s)",(member_id, store_name, store_address, store_phone, store_reg_no))
        g.conn.commit()

        g.cur.execute("SELECT user_name From member where id = %s",(member_id,))
        user_data = g.cur.fetchone()
        if user_data:
            user_name = user_data["user_name"]

        g.cur.execute("SELECT id FROM vendor where member_id = %s", (member_id,))
        vendor_data = g.cur.fetchone()
        if vendor_data:
            vendor_id = vendor_data["id"]

        token_args = {"id":member_id, "user_name":user_name, "vendor_id":vendor_id, "exp":int(time.time())+3600}
        token = generate_jwt(token_args)



        return result, message, token
        

            

    

