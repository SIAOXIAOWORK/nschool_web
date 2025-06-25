from flask_restful import Resource, reqparse, request
from utils.token_util import verify_token
from service.offering_service import Offering,OfferingLogic

class OfferingService(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("offering_name", type=str, required=True, help="Service name is required.")
        self.parser.add_argument("price", type=int, required=True, help="Price is required")
        self.parser.add_argument("duration_min", type=int, required=True, help="Duration (in minutes) is required.")
        self.parser.add_argument("description", type=str, required=False)
        self.parser.add_argument("need_deposit", type=bool, required=False)
        self.parser.add_argument("deposit_percent", type=int, required=False)

    
        

class OfferingItemsList(Resource):

    def get(self):
        vendor_id = request.args.get("vendor_id",type=int)
        offeringlogic= OfferingLogic()
                
        if vendor_id:
           return offeringlogic.get_offering_items_by_vendor(vendor_id)

        return offeringlogic.get_offering_items_by_all()
    

class OfferingItemsDetail(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("offering_name", type=str, required=True, help="Service name is required.")
        self.parser.add_argument("price", type=int, required=True, help="Price is required")
        self.parser.add_argument("duration_min", type=int, required=True, help="Duration (in minutes) is required.")
        self.parser.add_argument("description", type=str, required=False)
        self.parser.add_argument("need_deposit", type=bool, required=False)
        self.parser.add_argument("deposit_percent", type=int, required=False)



    def get(self):
        offering_id = request.args.get("offering_id",type=int)
        offeringlogic = OfferingLogic()

        if offering_id:
            return offeringlogic.get_offering_items_by_id(offering_id)
        
        return {"success":False, "message":"Not found this offering_item"}
    
    def post(self):
        args = self.parser.parse_args()
        
        is_valid, payload = verify_token()
        if not is_valid:
            return {"success":False, "message":payload},401
        
        if 'vendor_id' not in payload or not payload["vendor_id"] :
            return {"success":False, "message":"Vendor_id is null."}
        
        if args["need_deposit"] == True and not args["deposit_percent"]:
            return {"success":False, "message":"Deposit_percent can't be empty."}
        
        vendor_id = payload["vendor_id"]
        offering_item = Offering(vendor_id, **args)
        result = offering_item.generate_offering_item()

        if result:
            return {"success":True, "message":"Offering_item created"}
        
        else:
            return {"success":False, "message":"Offering_item created failed"}




        
    def put(self):
        args = self.parser.parse_args()
        offering_id = request.args.get("offering_id",type=int)
        
        is_valid, payload = verify_token()
        if not is_valid:
            return {"success":False, "message":payload},401
        
        if 'vendor_id' not in payload or not payload["vendor_id"] :
            return {"success":False, "message":"Vendor_id is null."}
        
        if args["need_deposit"] == True and not args["deposit_percent"]:
            return {"success":False, "message":"Deposit_percent can't be empty."}
        
        offering = Offering(payload["vendor_id"] ,**args)
        result, message = offering.Modify_offering_item(offering_id)

        if result:
            return {"success":True, "message":f"Update success{offering.__dict__}"}
        
        return {"success":False, "message": message}
    
    def delete(self):
        
        offering_id = request.args.get("offering_id",type=int)
        
        is_valid, payload = verify_token()
        if not is_valid:
            return {"success":False, "message":payload},401
        
        if 'vendor_id' not in payload or not payload["vendor_id"] :
            return {"success":False, "message":"Vendor_id is null."}
        
        offeringlogic = OfferingLogic()
        result, message = offeringlogic.delete_offering_items(payload["vendor_id"], offering_id)

        if not result:
            return {"success": result, 'message':message}
        
        return {"success": result, 'message':message}

        

        


        

def offering_routes(api):
    api.add_resource(OfferingService, "/offeringitems/create")
    api.add_resource(OfferingItemsList,"/offeringitems")
    api.add_resource(OfferingItemsDetail, "/offeringitems")


