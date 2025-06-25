from flask_restful import Resource, reqparse
from service.auth_service import LoginServer, RegisterServer
from utils.token_util import verify_token
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
            return jsonify({
                "result": "success",
                "token": token
            })
        
        return jsonify({
            "result":"faild",
            "token": None
        })
    

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
        register = RegisterServer()
        
        result, message = register.register_member(account, password, user_name, email, phone)
        
        if result:
            return "success"
        
        return jsonify({
            "result": result,
            "message": message
        })
    
class Register_vendor(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("store_name", type=str, required=True, help="store_name can't be empty.")
        self.parser.add_argument("store_address", type=str, required=True, help="store_address can't be empty.")
        self.parser.add_argument("store_phone", type=str, required=True, help="store_phone can't be empty.")
        self.parser.add_argument("store_reg_no", type=str, required=True, help="store_reg_no can't be empty.")

    def post(self):
        
        is_valid, payload = verify_token()
        if not is_valid:
            return {"success":False, "message":payload},401
        
        member_id = payload["id"]     
        args = self.parser.parse_args()
        store_name = args["store_name"]
        store_address = args["store_address"]
        store_phone = args["store_phone"]
        store_reg_no = args["store_reg_no"]
        register = RegisterServer()
        result, message = register.register_vendor(member_id, store_name, store_address, store_phone, store_reg_no)

        if not result:
            return {"success":False, "message":message},400

        return {"success":True}

def register_routes(api):
    api.add_resource(Register_member, "/register_member")
    api.add_resource(Register_vendor, "/register_vendor")