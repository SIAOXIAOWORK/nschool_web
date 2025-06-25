from app import g


class Offering:
    def __init__(self,vendor_id, offering_name, price, duration_min, description=None, need_deposit=False, deposit_percent=None):
        self.vendor_id = vendor_id
        self.offering_name = offering_name
        self.price = price
        self.duration_min = duration_min
        self.description = description
        self.need_deposit = bool(need_deposit)
        self.deposit_percent = deposit_percent
        

    def generate_offering_item(self):
        try:    
            g.cur.execute("INSERT INTO offering_items(vendor_id, offering_name, price, duration_min, description, need_deposit, deposit_percent) VALUES(%s, %s, %s, %s, %s, %s, %s)",(self.vendor_id, self.offering_name, self.price, self.duration_min, self.description, bool(self.need_deposit), self.deposit_percent))
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
            need_deposit = %s,
            deposit_percent = %s
            WHERE id = %s
        """

        g.cur.execute(sql,(self.offering_name, self.price, self.duration_min, self.description, bool(self.need_deposit), self.deposit_percent,offering_data["id"]))
        g.conn.commit()
        return True, None
        
        

        
        
        
        
class OfferingLogic:

    def get_offering_items_by_all(self):
        g.cur.execute("SELECT * FROM offering_items")
        return g.cur.fetchall()
    
    def get_offering_items_by_vendor(self, vendor_id):
        g.cur.execute("SELECT * FROM offering_items where vendor_id = %s",(vendor_id,))
        return g.cur.fetchall()
    
    def get_offering_items_by_id(self, offering_id):
        g.cur.execute("SELECT * FROM offering_items where id = %s", (offering_id,))
        return g.cur.fetchall()
    


