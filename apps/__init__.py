# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import argparse
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
import logging, doctest

global memcache
memcache={}
global memcache_config
memcache_config = {
    "memcache_policy": "LRU",
    "memcache_capacity": 1000000,
    "memcache_size": 0
}
logging.info("Memcache Initialized: ", memcache)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
db = SQLAlchemy()
# parser = argparse.ArgumentParser()
# parser.add_argument("--start", help="Add the start index of the key", type=int)
# parser.add_argument("--end", help="Add the end index of the key", type=int)
# args = parser.parse_args()
# print(args.start, args.end)
# RANGE_START=args.start or os.getenv('RANGE_START')
# RANGE_END=args.end or os.getenv('RANGE_END')
# print(RANGE_START, RANGE_END)
ETCD_HOST=os.getenv('ETCD_HOST').split(',')
ETCD_PORT=os.getenv('ETCD_PORT')
FILE_LOCATION=os.getenv('FILE_LOCATION')
# login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    # login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('home', 'msg_queue', 'etcd_cluster_mgnt'):
        module = import_module('apps.services.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove() 


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    logger.info(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
