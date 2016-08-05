#!/usr/bin/env python

from models import User, Group
from db import session

from flask import Flask
from flask.ext.restful import Api

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with

from datetime import datetime

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'uri': fields.Url('user', absolute=True),
}

group_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'uri': fields.Url('group', absolute=True),
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('email', type=str)

class UserResource(Resource):
    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser.parse_args()
        user = User(name=parsed_args['name'], email=parsed_args['email'])
        session.add(user)
        session.commit()
        return user, 201

    @marshal_with(user_fields)
    def get(self):
        users = session.query(User).all()
        users.sort(key=lambda user: user.name)
        return users


class EditUserResource(Resource):
    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        user.name = parsed_args['name']
        user.email = parsed_args['email']
        session.add(user)
        session.commit()
        return user, 201

    @marshal_with(user_fields)
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return user, 201


class GroupResource(Resource):
    @marshal_with(group_fields)
    def post(self):
        parsed_args = parser.parse_args()
        group = Group(name=parsed_args['name'])
        session.add(group)
        session.commit()
        return group, 201

    @marshal_with(group_fields)
    def get(self):
        groups = session.query(Group).all()
        groups.sort(key=lambda group: group.name)
        return groups


class EditGroupResource(Resource):
    @marshal_with(group_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        group = session.query(Group).filter(Group.id == id).first()
        if not group:
            abort(404, message="Group {} doesn't exist".format(id))
        group.name = parsed_args['name']
        today = datetime.now()
        group.date_created = datetime(today.year, today.month, today.day)
        session.add(group)
        session.commit()
        return group, 201

    @marshal_with(group_fields)
    def delete(self, id):
        group = session.query(Group).filter(Group.id == id).first()
        if not group:
            abort(404, message="Group {} doesn't exist".format(id))
        session.delete(group)
        session.commit()
        return group, 201


class AddUserToGroupResource(Resource):
    def post(self, user_id, group_id):
        user = session.query(User).filter(User.id == user_id).first()
        group = session.query(Group).filter(Group.id == group_id).first()
        user.groups.append(group)
        group.users.append(user)
        session.commit()
        return 201

    @marshal_with(user_fields)
    def get(self, user_id, group_id):
        user = Group.query.filter(Group.id == group_id).first().users
        return user, 201