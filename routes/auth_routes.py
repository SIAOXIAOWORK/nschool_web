from flask_restful import Resource, reqparse
from service.auth_service import LoginServer, MemberService, Member, CheckData
from utils.util import verify_token, get_jwt_token
from flask import jsonify, request


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
                "success": True,
                "token": token
            }
        
        return {
            "success": False,
            "message": "帳號或密碼錯誤"
        }
    

def login_routes(api):
    api.add_resource(Login, "/api/login")


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
    @verify_token
    def post(self, payload):
        member_id = payload["id"]
        data = request.get_json()
        store_name = data.get("store_name")
        store_address = data.get("store_address")
        store_phone = data.get("store_phone")
        store_reg_no = data.get("store_reg_no")

        # 資料檢查
        if not all([store_name, store_address, store_phone, store_reg_no]):
            return {"success": False, "message": "所有欄位皆為必填"}, 400

        memberservice = MemberService()
        result, message, token = memberservice.register_vendor(member_id, store_name, store_address, store_phone, store_reg_no)

        if not result:
            return {"success":False, "message":message}, 400

        return {"success": True, "message": message, "token": token}

def auth_routes(api):
    api.add_resource(MemberDetial, "/api/member/<int:member_id>")
    api.add_resource(Register_member, "/member/create")
    api.add_resource(Register_vendor, "/api/member/register_vendor")
    api.add_resource(MemberPassword, "/member/<int:member_id>/change_password")