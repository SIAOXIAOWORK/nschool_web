from flask_restful import Resource, reqparse
from service.auth_service import LoginServer, MemberService, Member, CheckData
from utils.token_util import verify_token, get_jwt_token
from flask import jsonify


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors = True)
        self.parser.add_argument("account", type = str, required=True, help = "Account must be string.")
        self.parser.add_argument("password", type = str, required=True, help = "Password must be string.")

    def post(self):
        args = self.parser.parse_args()

        account = args["account"]
        password = args["password"]

        loginserver = LoginServer()
        result, token = loginserver.check_login_args(account,password)

        if result:
            return {
                "result": "success",
                "token": token
            }
        
        return {
            "result":"faild",
            "token": None
        }
    

def login_routes(api):
    api.add_resource(Login, "/login")


class Register_member(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("account", type=str , required=True, help="Account must be string.")
        self.parser.add_argument("password", type=str , required=True, help="Password must be string.")
        self.parser.add_argument("user_name", type=str , required=True, help="User_name must be string.")
        self.parser.add_argument("email", type=str , required=True, help="Email must be string.")
        self.parser.add_argument("phone", type=str , required=True, help="Phone must be string.")

    def post(self):
        args = self.parser.parse_args()
        account = args["account"]
        password = args["password"]
        user_name = args["user_name"]
        email = args["email"]
        phone = args["phone"]
        memberservice = MemberService()
        
        result, message = memberservice.register_member(account, password, user_name, email, phone)
        
        if result:
            return "success"
        
        return {
            "result": result,
            "message": message
        }
    
class MemberDetial(Resource):
    #查看個人資料
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("user_name", type=str , required=False, help="Account must be string.")
        self.parser.add_argument("phone", type=str,  required = False, help="Phone must be string.")
        self.parser.add_argument("email", type=str, required=False, help="Email must be string.")
   
    @verify_token
    def get(self, payload, member_id):
        memberservice = MemberService()
        result, message, member_data = memberservice.get_member_data(payload, member_id)
        if not result :
            return {'success':result, 'message':message}
        
        return {'success':result, 'message':message, 'member_data':member_data}
    
    @verify_token
    def put(self, payload, member_id):
        memberservice = MemberService()
        result, message, member_data = memberservice.get_member_data(payload, member_id)
        if not result :
            return {'success':result, 'message':message}
        args = self.parser.parse_args()

        result, message , payload = memberservice.modify_member_data(member_id, **args)
        return {'success': result, 'message':message, 'payload': payload}
    
class MemberPassword(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("password", type=str, required = True)
    
    @verify_token
    def put(self, payload, member_id):
        if not member_id == payload['id']:
            message = "You don't have permission to change password."
            return {'success':False, 'message':message, 'payload':None}
        
        args = self.parser.parse_args()
        password = args['password']
        memberservice = MemberService()
        result, message, payload = memberservice.change_password(member_id, password)

        return {'success':result, 'message':message, 'payload':payload}
        


        
            
        

    



    
class Register_vendor(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("store_name", type=str, required=True, help="store_name can't be empty.")
        self.parser.add_argument("store_address", type=str, required=True, help="store_address can't be empty.")
        self.parser.add_argument("store_phone", type=str, required=True, help="store_phone can't be empty.")
        self.parser.add_argument("store_reg_no", type=str, required=True, help="store_reg_no can't be empty.")

    @verify_token
    def post(self,payload):
                      
        member_id = payload["id"]     
        args = self.parser.parse_args()
        store_name = args["store_name"]
        store_address = args["store_address"]
        store_phone = args["store_phone"]
        store_reg_no = args["store_reg_no"]
        memberservice = MemberService()
        result, message, token = memberservice.register_vendor(member_id, store_name, store_address, store_phone, store_reg_no)

        if not result:
            return {"success":False, "message":message},400

        return {"success":True, "message":message, "token":token}

def auth_routes(api):
    api.add_resource(MemberDetial, "/member/<int:member_id>")
    api.add_resource(Register_member, "/member/create")
    api.add_resource(Register_vendor, "/member/vendor_create")
    api.add_resource(MemberPassword, "/member/<int:member_id>/change_password")