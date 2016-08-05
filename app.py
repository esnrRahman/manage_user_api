#!/usr/bin/env python

from flask import Flask
from flask.ext.restful import Api

from resources import UserResource
from resources import EditUserResource
from resources import GroupResource
from resources import EditGroupResource
from resources import AddUserToGroupResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserResource, '/manage/api/v1.0/users', endpoint='users')
api.add_resource(EditUserResource, '/manage/api/v1.0/users/<string:id>', endpoint='user')
api.add_resource(GroupResource, '/manage/api/v1.0/groups', endpoint='groups')
api.add_resource(EditGroupResource, '/manage/api/v1.0/groups/<string:id>', endpoint='group')
api.add_resource(AddUserToGroupResource, '/manage/api/v1.0/groups/<string:user_id>/<string:group_id>', endpoint='group_user')


if __name__ == '__main__':
    app.run(debug=True)
