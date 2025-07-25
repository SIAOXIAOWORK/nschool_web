from app import g
from datetime import timedelta


class Offering:
    def __init__(self,vendor_id, offering_name, price, duration_min, description=None, deposit_percent=0):
        self.vendor_id = vendor_id
        self.offering_name = offering_name
        self.price = price
        self.duration_min = duration_min
        self.description = description
        self.deposit_percent = deposit_percent
        

    def generate_offering_item(self):
        try:    
            g.cur.execute("INSERT INTO offering_items(vendor_id, offering_name, price, duration_min, description, deposit_percent) VALUES(%s, %s, %s, %s, %s, %s)",(self.vendor_id, self.offering_name, self.price, self.duration_min, self.description, self.deposit_percent))
        except:
            return False
        g.conn.commit()
        return True
    

    def Modify_offering_item(self, offering_id):
        g.cur.execute("SELECT id, vendor_id FROM offering_items where id = %s", (offering_id,))
        offering_data = g.cur.fetchall()[0]
        print(offering_data)
        if not self.vendor_id == offering_data["vendor_id"] :
            return False, "You don't have permission to modify this offering_item."
        sql = """
        UPDATE offering_items 
        SET 
            offering_name = %s,
            price = %s,
            duration_min = %s,
            description = %s,
            deposit_percent = %s
            WHERE id = %s
        """

        g.cur.execute(sql,(self.offering_name, self.price, self.duration_min, self.description, self.deposit_percent,offering_data["id"]))
        g.conn.commit()
        return True, None
        
        

        
        
        
        
class OfferingService:

    def get_offering_items_by_all(self):
        g.cur.execute("SELECT * FROM offering_items")
        return g.cur.fetchall()
    
    def get_offering_items_by_vendor(self, vendor_id):
        g.cur.execute("SELECT * FROM offering_items where vendor_id = %s",(vendor_id,))
        return g.cur.fetchall()
    
    def get_offering_items_by_id(self, offering_id):
        g.cur.execute("SELECT * FROM offering_items where id = %s", (offering_id,))
        return g.cur.fetchall()
    
    def delete_offering_items(self, vendor_id, offering_id):
        g.cur.execute("SELECT vendor_id FROM offering_items where id = %s",(offering_id,))
        if not vendor_id == g.cur.fetchone()['vendor_id']:
            return False, "You don't have permission to delete this offering_item."
        
        g.cur.execute("SELECT * FROM offering_items where id = %s",(offering_id,))
        offering_data = g.cur.fetchall()
        g.cur.execute("DELETE FROM offering_items where id = %s",(offering_id,))
        g.conn.commit()

        return True, offering_data
    

    def get_offering_time_by_offering_id(self, offering_item_id):
        g.cur.execute("SELECT * FROM offering_times where offering_item_id = %s",(offering_item_id,))
        sql_data = g.cur.fetchall()
        if not sql_data:
            message = "This offering_item_id is not existed"
            return False, message,None
        
        for i in sql_data:
            i['start_time'] = i['start_time'].isoformat()
            i['end_time'] = i['end_time'].isoformat()

        
        return True, None, sql_data        
    
    def get_offering_time_by_id(self, offering_time_id):
        g.cur.execute("SELECT * FROM offering_times where id = %s",(offering_time_id,))
        sql_data = g.cur.fetchone()
        if not sql_data:
            message = "This offering_time_id is not existed"
            return False, message, None
        
        sql_data['start_time'] = sql_data['start_time'].isoformat()
        sql_data['end_time'] = sql_data['end_time'].isoformat()

        return True, None, sql_data
        
            
    
    def set_offering_time(self, vendor_id, offering_id, start_time):
        g.cur.execute("SELECT vendor_id, duration_min FROM offering_items where id =%s",(offering_id,))
        sql_data = g.cur.fetchone()
        print(start_time)
        if not sql_data:
            message = "This offering_item not existed."
            return False, message, None
        
        sql_vendor_id = sql_data['vendor_id']

        if not vendor_id == sql_vendor_id:
            message = "You don't have permission to set the offering_time."
            return False, message, None
        
        end_time = start_time + timedelta(minutes=sql_data["duration_min"])

        insert_sql = """
            INSERT INTO offering_times (
                offering_item_id,
                vendor_id,
                start_time,
                end_time
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id, offering_item_id, vendor_id, start_time, end_time
        """
        g.cur.execute(insert_sql, (offering_id, vendor_id, start_time, end_time))
        row = g.cur.fetchone()
        print(row)
        payload = {
            "id": row['id'],
            "offering_item_id": row['offering_item_id'],
            "vendor_id": row['vendor_id'],
            "start_time": row['start_time'].isoformat(),
            "end_time": row['end_time'].isoformat()
        }
        g.conn.commit()
        message = "Set offering_time success"
        return True, message, payload

    def modify_offering_time(self, vendor_id, offering_time_id, start_time):
        g.cur.execute("SELECT * FROM offering_times where id = %s",(offering_time_id,))
        offering_time_sql_data = g.cur.fetchone()
        
        if not offering_time_sql_data:
            message = "This offering_time_id is not existed."
            return False, message, None
        
        if not vendor_id == offering_time_sql_data['vendor_id']:
            message = "You don't have permission to modify the offering_time."
            return False, message, None
        
        g.cur.execute("SELECT duration_min FROM offering_items where id = %s",(offering_time_sql_data['offering_item_id'],))
        offering_item_sql_data = g.cur.fetchone()
        end_time = start_time + timedelta(minutes=offering_item_sql_data["duration_min"])

        update_sql ="""
        UPDATE offering_times
        SET
            start_time = %s,
            end_time = %s
            WHERE id = %s
        RETURNING id, offering_item_id, vendor_id, start_time, end_time
        """

        g.cur.execute(update_sql,(start_time, end_time, offering_time_id))
        row = g.cur.fetchone()
        payload = {
            "id": row['id'],
            "offering_item_id": row['offering_item_id'],
            "vendor_id": row['vendor_id'],
            "start_time": row['start_time'].isoformat(),
            "end_time": row['end_time'].isoformat()
        }
        
        g.conn.commit()

        return True, None, payload

    def delete_offering_time(self, vendor_id, offering_time_id):
        g.cur.execute("SELECT vendor_id FROM offering_times where id = %s",(offering_time_id,))
        offering_sql_data = g.cur.fetchone()
        if not offering_sql_data:
            message =  "This offering_time_id is not existed."
            return False, message, None
        
        if not vendor_id == offering_sql_data['vendor_id']:
            message = "You don't have permission to delete the offering_time."
            return False, message, None
        
        g.cur.execute("DELETE FROM offering_times where id = %s RETURNING id, offering_item_id, vendor_id, start_time, end_time",(offering_time_id,))
        payload = g.cur.fetchone()
        payload['start_time'] = payload['start_time'].isoformat()
        payload['end_time'] = payload['end_time'].isoformat()
        g.conn.commit()

        return True, None, payload

