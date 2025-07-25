from app import g


class Booking:

    def get_booking_items(self, **kwgs):
        ALLOWED_FIELDS = {"id", "member_id", "vendor_id", "offering_time_id"}
        
        sql = "SELECT id, member_id, vendor_id, offering_time_id, create_at FROM booking_items WHERE TRUE"
        parama = []
        for i in kwgs:
            if i not in ALLOWED_FIELDS:
                continue
            sql += f" AND {i} = %s"
            parama.append(kwgs[i])

        g.cur.execute(sql, parama)
        sql_data = g.cur.fetchall()
        if not sql_data:
            message = "Data not found."
            return False, message, None
        
        return True, None, sql_data

    def cancel_booking_item_by_id(self, payload, booking_id):

        g.cur.execute("SELECT member_id FROM booking_items where id = %s", (booking_id,))
        member_id = g.cur.fetchone()
        if not member_id:
            return False, "Data not found", None
        if member_id != payload['id']:
            return False, "Insufficient permissions", None

        g.cur.execute("SELECT offering_time_id FROM booking_items where id = %s", (booking_id,))
        offering_time_id = g.cur.fetchone()
        if not offering_time_id:
            return False, "Booking_items not found.", None
        
        g.cur.execute("SELECT status FROM offering_times where id = %s", (offering_time_id,))
        offering_time_status = g.cur.fetchone()
        if not offering_time_status:
            return False, "Offering_times not found.", None
        
        if offering_time_status['status'] != "booked":
            return False, "Status error", None
        
        g.cur.execute("""UPDATE offering_times 
                      SET status = 'cancel'
                      WHERE id = %s""", (offering_time_id,))
        
        return True, "Booking canceled.", None
        

    def create_booking_service(self, member_id, offering_time_id):
        g.cur.execute("SELECT id, vendor_id, status FROM offering_times WHERE id = %s",(offering_time_id,))
        offering_data = g.cur.fetchone()
        
        if not offering_data:
            message = "This offering_id not exist."

            return False, message, None

        vendor_id = offering_data["vendor_id"]

        if offering_data["status"] == 'available':
            g.cur.execute("UPDATE offering_times SET status = 'booked' where id = %s",(offering_time_id,))
            g.cur.execute("INSERT INTO booking_items(member_id, offering_time_id, vendor_id) VALUES(%s,%s,%s) RETURNING id, member_id, offering_time_id, vendor_id", (member_id, offering_time_id, vendor_id))
            payload = g.cur.fetchone()
            g.conn.commit()
            message = "Booking success."
            return True, message, payload
        
        else:
            message = "This offering_time can't be booking"
            return False, message, None