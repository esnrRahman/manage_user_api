#!/usr/bin/env python

from flask import Flask
from flask.ext.restful import Api

from resources import UserResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserResource, '/user', endpoint='users')

if __name__ == '__main__':
    app.run(debug=True)
