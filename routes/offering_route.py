from flask_restful import Resource, reqparse, request
from utils.util import verify_token, get_jwt_token
from service.offering_service import Offering,OfferingService
from utils.util import CheckData
 
        

class OfferingItemsList(Resource):

    def get(self):
        vendor_id = request.args.get("vendor_id",type=int)
        offeringservice= OfferingService()
                
        if vendor_id:
           return offeringservice.get_offering_items_by_vendor(vendor_id)

        return offeringservice.get_offering_items_by_all()
    

class OfferingItemsByVendor(Resource):
    
    @verify_token
    def get(self, payload):
        offeringservice= OfferingService()
        vendor_id = payload["vendor_id"]

        return offeringservice.get_offering_items_by_vendor(vendor_id)

    

class OfferingItemsDetail(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("offering_name", type=str, required=True, help="Service name is required.")
        self.parser.add_argument("price", type=int, required=True, help="Price is required")
        self.parser.add_argument("duration_min", type=int, required=True, help="Duration (in minutes) is required.")
        self.parser.add_argument("description", type=str, required=False)
        self.parser.add_argument("deposit_percent", type=int, required=False)



    def get(self, offering_id):
        offeringservice = OfferingService()

        if offering_id:
            return offeringservice.get_offering_items_by_id(offering_id)
        
        return {"success":False, "message":"Not found this offering_item"}
    
    @verify_token
    def put(self, payload, offering_id):
        args = self.parser.parse_args()
            
        offering = Offering(payload["vendor_id"] ,**args)
        result, message = offering.Modify_offering_item(offering_id)

        if result:
            return {"success":True, "message":f"Update success{offering.__dict__}"}
        
        return {"success":False, "message": message}
    
    @verify_token
    def delete(self,payload, offering_id):
               
        offeringservice = OfferingService()
        result, message = offeringservice.delete_offering_items(payload["vendor_id"], offering_id)

        if not result:
            return {"success": result, 'message':message}
        
        return {"success": result, 'message':message}

class OfferingItems(Resource): 
    
    @verify_token
    def post(self, payload):
        vendor_id = payload["vendor_id"]
        data = request.get_json()
        offering_name = data.get("offering_name")
        price = data.get("price")
        duration_min = data.get("duration_min")
        description = data.get("description")
        deposit_percent = data.get("deposit_percent")
        
        # 必填欄位檢查
        if not all([offering_name, price, duration_min]):
            return {"success": False, "message": "offering_name, price, duration_min 為必填"}, 400

        offering_item = Offering(vendor_id, offering_name=offering_name, price=price, duration_min=duration_min, description=description, deposit_percent=deposit_percent)
        result = offering_item.generate_offering_item()

        if result:
            return {"success": True, "message": "Offering_item created"}
        else:
            return {"success": False, "message": "Offering_item created failed"}




class OfferingTimeList(Resource):
    
    def __init__(self):
        checkdata = CheckData()
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("offering_id", type=int, required=True)
        self.parser.add_argument("start_time", type=checkdata.check_datetime, required=True)
        

    def get(self, offering_item_id):
        offeringservice = OfferingService()
        result, message, payload = offeringservice.get_offering_time_by_offering_id(offering_item_id)
        return {'result':result, 'message':message, 'payload':payload}

    
    @verify_token
    def post(self, payload):
        args = self.parser.parse_args()
        offering_id =args['offering_id']
        start_time = args['start_time']
        offeringservice = OfferingService()
        vendor_id = payload['vendor_id']
        result, message, payload = offeringservice.set_offering_time(vendor_id, offering_id, start_time)
        return {'result': result, 'message':message, 'payload':payload}

class OfferingTimeDetil(Resource):
    def __init__(self):
        checkdata = CheckData()
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument("start_time", type=checkdata.check_datetime, required=True)
    
    def get(self, offering_time_id):
        offeringservice = OfferingService()
        result, message, payload = offeringservice.get_offering_time_by_id(offering_time_id)
        return {'result': result, 'message':message, 'payload':payload}
    
    @verify_token
    def put(self, payload, offering_time_id):
        args = self.parser.parse_args()
        start_time = args['start_time']
        offeringservice = OfferingService()
        vendor_id = payload['vendor_id']
        result, message, payload = offeringservice.modify_offering_time(vendor_id,offering_time_id, start_time)
        return {'result': result, 'message':message, 'payload':payload}
    
    @verify_token
    def delete(self, payload, offering_time_id):
        vendor_id = payload['vendor_id']
        offeringserice = OfferingService()
        result, message, payload = offeringserice.delete_offering_time(vendor_id, offering_time_id)
        return {'result': result, 'message': message, 'payload':payload}
        
        

        

        


        

def offering_routes(api):
    # api.add_resource(OfferingItemsList,"/api/offering_list")
    api.add_resource(OfferingItemsByVendor,"/api/offering_list")
    api.add_resource(OfferingItemsDetail, "/api/offering/<int:offering_id>")
    api.add_resource(OfferingItems, "/api/offering")
    api.add_resource(OfferingTimeList, "/api/offering_time")
    api.add_resource(OfferingTimeDetil, "/offeringtimes/<int:offering_time_id>")

