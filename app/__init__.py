from configparser import ConfigParser
import psycopg
from flask import Flask, g, render_template, request, redirect, url_for, flash
from flask_restful import Api
from routes.auth_routes import login_routes, auth_routes
from routes.offering_route import offering_routes
from routes.booking_route import booking_routes
from psycopg.rows import dict_row
import os

def create_app():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(BASE_DIR, "..", "templates")
    app = Flask(__name__, template_folder=template_path)
    app.config.from_object('config.DevelopmentConfig')
    api = Api(app)

    @app.before_request
    def connect_db():
        config = ConfigParser()
        config.read('./db.ini')
        db_setting = config['postgres']
        g.conn = psycopg.connect(**db_setting)
        g.cur = g.conn.cursor(row_factory=dict_row)

    @app.teardown_request
    def close_db(exception):
        if hasattr(g, 'cur'):
            g.cur.close()
        if hasattr(g, 'conn'):
            g.conn.close()

    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            account = request.form['account']
            password = request.form['password']

            from service.auth_service import LoginServer
            service = LoginServer()
            result, message = service.check_login_args(account, password)

            if result:
                return render_template('login.html', success="登入成功!")
            
            else:
                return render_template('login.html', error="帳號或密碼錯誤，請重新登入")

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register_page():
        if request.method == 'POST':
            account = request.form['account']
            password = request.form['password']
            user_name = request.form['user_name']
            email = request.form['email']
            phone = request.form['phone']

            from service.auth_service import MemberService
            service = MemberService()
            resutl, message = service.register_member(account, password, user_name, email, phone)

            if resutl:
                return render_template("register.html", success = "註冊成功，請前往登入")
            
            else:
                return render_template('register.html', error=message)
            
        else:
            return render_template('register.html')


    @app.route('/member', methods=['GET', 'POST'])
    def member_page():
        from service.auth_service import MemberService
        payload= {"id": 3}
        service = MemberService()

        if request.method == 'POST':
            user_name = request.form['user_name']
            email = request.form['email']
            phone = request.form['phone']
            result, message, payload = service.modify_member_data(payload['id'], **request.form)
            _, _, member_data = service.get_member_data(payload, payload['id'])
            return render_template("member.html" , member=member_data, message="資料已成功更新")
        else:
            result, message, member_data = service.get_member_data(payload, payload['id'])
            return render_template('member.html', member=member_data)

    @app.route('/offering_list')
    def offering_list():
        from service.offering_service import OfferingService
        service = OfferingService()
        offerings = service.get_offering_items_by_all()
        return render_template('offering_list.html', offerings=offerings)
    
    @app.route('/manage_offering', methods=['GET'])
    def manage_offering_page():
        return render_template('manage_offering.html')
    
    @app.route('/member/register_vendor' , methods=['GET'])
    def create_vendor():
        return render_template('register_vendor.html')

    @app.route('/member/booking/booking_items')
    def member_booking_list():
        return render_template('member_booking_list.html')
    
    @app.route('/vendor/booking/booking_items')
    def vendor_booking_list():
        return render_template('vendor_booking_list.html')
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    #登入
    login_routes(api)

    #註冊
    auth_routes(api)

    #服務資料
    offering_routes(api)

    booking_routes(api)

    return app


