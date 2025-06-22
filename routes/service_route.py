from flask_restful import Resource, reqparse
from utils.token_util import verify_token
from service.vendor_service import ServiceItem

class StoreService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("service_name", type=str, required=True, help="Service name is required.")
        self.parser.add_argument("price", type=int, required=True, help="Price is required")
        self.parser.add_argument("duration_min", type=int, required=True, help="Duration (in minutes) is required.")
        self.parser.add_argument("description", type=str, required=False)
        self.parser.add_argument("need_deposit", type=bool, required=False)
        self.parser.add_argument("deposit_percent", type=int, required=False)


    def post(self):
        args = self.parser.parse_args()
        
        is_valid, payload = verify_token()
        if not is_valid:
            return {"success":False, "message":payload},401
        
        if not payload["vendor_id"]:
            return {"success":False, "message":"Vendor_id is null."},401
        
        vendor_id = payload["vendor_id"]

        service_item = ServiceItem(vendor_id, **args)

        result = service_item.generate_service_item()

        if result:
            return {"success":True, "message":"Service_item created"}
        
        else:
            return {"success":False, "message":"Service_item created failed"},401
        

def service_routes(api):
    api.add_resource(StoreService, "/serviceitems")


