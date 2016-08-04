#!/usr/bin/env python

from models import User
from db import session

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
parser.add_argument('name', type=str)
parser.add_argument('email', type=str)


class AddUserResource(Resource):
    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser.parse_args()
        user = User(name=parsed_args['name'], email=parsed_args['email'])
        session.add(user)
        session.commit()
        return user, 201


class GetUsersResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = session.query(User).all()
        return users


