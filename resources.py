#!/usr/bin/env python

from models import User, Group, association_table
from db import session

import json
import re

from sqlalchemy import func
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


def createJSON(input_list):
    result_list = []
    for i in input_list:
        dictionary = {}
        dictionary[str(i[0])] = i[1]
        result_list.append(json.dumps(dictionary))
    return result_list


def check_email_syntax(input_email):
    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, input_email):
        return True
    else:
        return False


class UserResource(Resource):
    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser.parse_args()

        input_email = parsed_args['email']
        if not check_email_syntax(input_email):
            abort(400, message="Email - {} syntax is invalid".format(input_email))

        user = User(name=parsed_args['name'], email=input_email)
        session.add(user)
        session.commit()
        return user, 201

    @marshal_with(user_fields)
    def get(self):
        users = session.query(User).order_by(User.name).all()
        return users, 200


class EditUserResource(Resource):
    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))

        input_email = parsed_args['email']
        if not check_email_syntax(input_email):
            abort(400, message="Email - {} syntax is invalid".format(input_email))

        user.name = parsed_args['name']
        user.email = parsed_args['email']
        session.add(user)
        session.commit()
        return user, 200

    @marshal_with(user_fields)
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))

        session.delete(user)
        session.commit()
        return user, 200


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
        groups = session.query(Group).order_by(Group.name).all()
        return groups, 200


class EditGroupResource(Resource):
    @marshal_with(group_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        group = session.query(Group).filter(Group.id == id).first()
        if not group:
            abort(404, message="Group {} doesn't exist".format(id))

        group.name = parsed_args['name']
        today = datetime.now()
        group.date_created = datetime(today.year, today.month, today.day, today.hour, today.minute, today.second)
        session.add(group)
        session.commit()
        return group, 200

    @marshal_with(group_fields)
    def delete(self, id):
        group = session.query(Group).filter(Group.id == id).first()
        if not group:
            abort(404, message="Group {} doesn't exist".format(id))

        session.delete(group)
        session.commit()
        return group, 200


class UserToGroupResource(Resource):
    @marshal_with(user_fields)
    def post(self, user_id, group_id):
        user = session.query(User).filter(User.id == user_id).first()
        group = session.query(Group).filter(Group.id == group_id).first()
        if not (user or group):
            abort(404, message="user or group doesn't exist")

        group.users.append(user)
        session.commit()
        return user, 201

    @marshal_with(user_fields)
    def delete(self, user_id, group_id):
        user = session.query(User).filter(User.id == user_id).first()
        group = session.query(Group).filter(Group.id == group_id).first()
        if not (user or group):
            abort(404, message="user or group doesn't exist")

        group.users.remove(user)
        session.commit()
        return user, 200


class GetUsersFromGroupResource(Resource):
    @marshal_with(user_fields)
    def get(self, group_id):
        users = Group.query.filter(Group.id == group_id).first().users
        return users, 200


class GetGroupsFromUserResource(Resource):
    @marshal_with(group_fields)
    def get(self, user_id):
        groups = session.query(Group).join(Group.users).filter(User.id == user_id).all()
        return groups, 200


class ListUsersWithGroupCountResource(Resource):
    def get(self):
        all_users = session.query(User.name, func.count(association_table.c.group_id).label('group_count')). \
            join(association_table).group_by(User).order_by('group_count ASC').all()
        result_list = createJSON(all_users)
        return result_list, 200


class ListGroupsWithUserCountResource(Resource):
    def get(self):
        all_groups = session.query(Group.name, func.count(association_table.c.user_id).label('user_count')).\
            join(association_table).group_by(Group).order_by('user_count DESC').all()
        result_list = createJSON(all_groups)
        return result_list, 200
