#!flask/bin/python

from models import User
from db import session
from app import app

from flask import Flask
from flask.ext.restful import Api

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'uri': fields.Url('user', absolute=True),
}

group_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date': fields.DateTime(dt_format='rfc822'),
    'uri': fields.Url('group', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('user', type=str)


class User(Resource):
    @marshal_with(user_fields)
    @app.route('/user/api/v1.0/users/<int:user_id>', methods=['POST'])
    def add_user(self):
        parsed_args = parser.parse_args()
        user = User(name=parsed_args['name'], email=parsed_args['email'])
        session.add(user)
        session.commit()
        return user, 201

    @marshal_with(user_fields)
    @app.route('/user/api/v1.0/users', methods=['GET'])
    def get_users(self):
        users = session.query(User).all()
        return users

