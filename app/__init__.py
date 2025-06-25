from configparser import ConfigParser
import psycopg
from flask import Flask, g
from flask_restful import Api
from routes.auth_routes import login_routes, register_routes
from routes.offering_route import offering_routes
from psycopg.rows import dict_row

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
        g.cur = g.conn.cursor(row_factory=dict_row)

    @app.teardown_request
    def close_db(exception):
        if hasattr(g, 'cur'):
            g.cur.close()
        if hasattr(g, 'conn'):
            g.conn.close()

    #登入
    login_routes(api)

    #註冊
    register_routes(api)


    offering_routes(api)
    return app


