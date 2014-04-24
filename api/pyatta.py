#!/usr/bin/env python

import sys
import os
topdir = os.path.dirname(os.path.realpath(__file__)) + "../.."
topdir = os.path.realpath(topdir)
sys.path.insert(0, topdir)
#from dns_handler import dns_handler, dns_option_handler
from base_setup import auth, app, token_gen, db
#from session_handler import session_handler
from user_handler import UserListAPI, UserAPI
from vyos_session import utils
from flask.views import MethodView
from flask.ext.restful import Api

#initialization
DEBUG = bool(utils.get_config_params('api','debug'))
app.config['SECRET_KEY'] = utils.get_config_params('api_auth','secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = utils.get_config_params('sql','db_uri')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = bool(utils.get_config_params('sql','commit_on_teardown'))
logger = utils.logger

def check_db():
    pass 

#extensions
api = Api(app)

#add resources
#api.add_resource(session_handler,'/v1.0/session/<action>')
#api.add_resource(dns_handler, '/v1.0/service/dns/forwarding')
#api.add_resource(dns_option_handler,'/v1.0/service/dns/forwarding/<option>')
api.add_resource(token_gen,'/v1.0/token')
api.add_resource(UserListAPI, '/v1.0/users')
api.add_resource(UserAPI, '/v1.0/users/<int:id>', endpoint = 'user')

if __name__ == '__main__':
    if not check_db() :
        logger.error('No database detected. Please check the configuration file !') 
        sys.exit(1)

    db.create_all()
    app.run(debug = DEBUG)