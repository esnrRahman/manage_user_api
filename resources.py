#!/usr/bin/env python

from models import User, Group, association_table
from db import session
from flask import jsonify

import json

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


def createJSON(inputList):
    resultList = []
    for i in inputList:
        dict = {}
        dict[str(i[0])] = i[1]
        resultList.append(json.dumps(dict))
    return resultList



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
        users = session.query(User).order_by(User.name).all()
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
        groups = session.query(Group).order_by(Group.name).all()
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


class UserToGroupResource(Resource):
    def post(self, user_id, group_id):
        user = session.query(User).filter(User.id == user_id).first()
        group = session.query(Group).filter(Group.id == group_id).first()
        group.users.append(user)
        session.commit()
        return 201

    @marshal_with(user_fields)
    def delete(self, user_id, group_id):
        user = session.query(User).filter(User.id == user_id).first()
        group = session.query(Group).filter(Group.id == group_id).first()
        import pdb; pdb.set_trace()
        group.users.remove(user)
        session.commit()
        return user, 201


class GetUsersFromGroupResource(Resource):
    @marshal_with(user_fields)
    def get(self, group_id):
        users = Group.query.filter(Group.id == group_id).first().users
        return users, 201


class GetGroupsFromUserResource(Resource):
    @marshal_with(group_fields)
    def get(self, user_id):
        groups = session.query(Group).join(Group.users).filter(User.id == user_id).all()
        return groups, 201


class ListUsersWithGroupCountResource(Resource):
    def get(self):
        allUsers = session.query(User.name, func.count(association_table.c.group_id).label('group_count')). \
            join(association_table).group_by(User).order_by('group_count ASC').all()
        resultList = createJSON(allUsers)
        return resultList, 201


class ListGroupsWithUserCountResource(Resource):
    def get(self):
        allGroups = session.query(Group.name, func.count(association_table.c.user_id).label('user_count')).\
            join(association_table).group_by(Group).order_by('user_count ASC').all()
        resultList = createJSON(allGroups)
        return resultList, 201
