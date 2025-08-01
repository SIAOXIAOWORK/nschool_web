from flask_restful import Resource, reqparse, request
import datetime
from utils.util import verify_token
from service.booking_service import Booking
from service.offering_service import OfferingService
from app import g


class GetBookingDataByMember(Resource):
    def __init__(self):
        pass

    # for the member source
    @verify_token
    def get(self, payload):
        booking = Booking()
        result, message, payload = booking.get_booking_items(member_id = payload['id'])
        data =[]

        for i in payload:
            g.cur.execute("SELECT * FROM offering_times WHERE id = %s", (i["offering_time_id"],))
            offering_time_data = g.cur.fetchall()

            g.cur.execute("SELECT * FROM offering_items WHERE id =%s", (offering_time_data[0]["offering_item_id"],))
            offering_item_data = g.cur.fetchall()

            new_data =  {
                    "id" : i["id"],
                    "create_at": i["create_at"].isoformat(),
                    "offering_time": offering_time_data,
                    "offering_item": offering_item_data
                }

            data.append(new_data)

        def convert_datetime(obj):
            if isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: convert_datetime(v) for k, v in obj.items()}
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            else:
                return obj
        
        payload = convert_datetime(data)
        return {'result': result, 'message': message, 'payload':payload}
    

class ModifyBookingDataByMember(Resource):
    
    @verify_token
    def delete(self, payload, booking_id):
        booking = Booking()

        result, message, payload = booking.cancel_booking_item_by_id(payload, booking_id)

        return {'result': result, 'message': message, "payload": payload}
        

class GetBookingDataByVendor(Resource):

    @verify_token
    def get(self, payload):
        booking = Booking()
        result, message, payload = booking.get_booking_items(vendor_id = payload["vendor_id"])

        data = []

        for i in payload:
            g.cur.execute("SELECT * FROM offering_times WHERE id = %s", (i["offering_time_id"],))
            offering_time_data = g.cur.fetchall()

            g.cur.execute("SELECT * FROM offering_items WHERE id =%s", (offering_time_data[0]["offering_item_id"],))
            offering_item_data = g.cur.fetchall()

            new_data =  {
                    "id" : i["id"],
                    "create_at": i["create_at"].isoformat(),
                    "offering_time": offering_time_data,
                    "offering_item": offering_item_data
                }

            data.append(new_data)

        def convert_datetime(obj):
            if isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: convert_datetime(v) for k, v in obj.items()}
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            else:
                return obj
        
        payload = convert_datetime(data)
        return {'result': result, 'message': message, 'payload':payload}


        


class BookingOffering(Resource):
    @verify_token
    def post(self, payload, offering_time_id):
        
        member_id = payload["id"]
        booking = Booking()

        result, message, payload =  booking.create_booking_service(member_id, offering_time_id)
        return {'result': result, 'message': message, 'payload':payload}
    


def booking_routes(api):
    api.add_resource(GetBookingDataByMember, "/api/member/booking_list")
    api.add_resource(GetBookingDataByVendor, "/api/vendor/booking_list")
    api.add_resource(ModifyBookingDataByMember, "/api/member/booking_list/<int:booking_id>")
    api.add_resource(BookingOffering, "/api/booking/<int:offering_time_id>")