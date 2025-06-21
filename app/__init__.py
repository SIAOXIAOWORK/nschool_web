from configparser import ConfigParser
import psycopg
from flask import Flask, g
from flask_restful import Api
from routes.auth_routes import register_auth_routes, login_auth_routes

def create_app():

    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    api = Api(app)

    @app.before_request
    def connect_db():
        config = ConfigParser()
        config.read('./db.ini')
        db_setting = config['postgres']
        g.conn = psycopg.connect(**db_setting)
        g.cur = g.conn.cursor()

    @app.teardown_request
    def close_db(exception):
        if hasattr(g, 'cur'):
            g.cur.close()
        if hasattr(g, 'conn'):
            g.conn.close()

    #登入
    login_auth_routes(api)

    #註冊
    register_auth_routes(api)

    return app


