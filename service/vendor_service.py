from app import g


class ServiceItem:
    def __init__(self,vendor_id, service_name, price, duration_min, description=None, need_deposit=False, deposit_percent=None):
        self.vendor_id = vendor_id
        self.service_name = service_name
        self.price = price
        self.duration_min = duration_min
        self.description = description
        self.need_deposit = need_deposit
        self.deposit_percent = deposit_percent

    def generate_service_item(self):
        
        try:    
            g.cur.execute("INSERT INTO service_items(vendor_id, service_name, price, duration_min, description, need_deposit, deposit_percent) VALUES(%s, %s, %s, %s, %s, %s, %s)",(self.vendor_id, self.service_name, self.price, self.duration_min, self.description, self.need_deposit, self.deposit_percent))
        except:
            return False
        g.conn.commit()
        return True
        


