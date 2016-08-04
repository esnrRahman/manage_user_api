#!/usr/bin/env python

from flask import Flask
from flask.ext.restful import Api

from resources import AddUserResource
from resources import GetUsersResource

app = Flask(__name__)
api = Api(app)

api.add_resource(GetUsersResource, '/manage/api/v1.0/users', endpoint='get_users')
api.add_resource(AddUserResource, '/manage/api/v1.0/users/add', endpoint='user')

if __name__ == '__main__':
    app.run(debug=True)
