Demo RESTful HTTP API using Flask, Flask-Restful and SQLAlchemy
===================

1. Install requisite packages:

pip install -r requirements.txt

2. Create tables:

./models.py

3. Run service:

./app.py

4. API functionalities:

Adding new user ->

>> curl -i -H "Content-Type: application/json" -X POST -d '{"name":"test","email":"abc@test.com"}' http://127.0.0.1:5000/manage/api/v1.0/users

Editing existing user:

>> curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"testing","email":"abc@testing.com"}' http://127.0.0.1:5000/manage/api/v1.0/users/<user_id>

Deleting existing user ->

>> curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/manage/api/v1.0/users/<user_id>

Adding new group ->

>> curl -i -H "Content-Type: application/json" -X POST -d '{"name":"abc"}' http://127.0.0.1:5000/manage/api/v1.0/groups

Editing existing group ->

>> curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"testing"}' http://127.0.0.1:5000/manage/api/v1.0/groups/<group_id>

Deleting group ->

>> curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/manage/api/v1.0/groups/<group_id>

Adding existing user to existing group ->

>> curl -i -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/manage/api/v1.0/groups/<user_id>/<group_id>

Removing user from the group ->

>> curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/manage/api/v1.0/groups/<user_id>/<group_id>

Listing all users - sorted in an alphabetical order by name ->

>> curl -i http://127.0.0.1:5000/manage/api/v1.0/users

Listing all groups - sorted in an alphabetical order by name ->

>> curl -i http://127.0.0.1:5000/manage/api/v1.0/groups

Listing all groups of a particular user ->

>> curl -i http://127.0.0.1:5000/manage/api/v1.0/user/groups/<string:user_id>

Listing all users of a particular group ->

>> curl -i http://127.0.0.1:5000/manage/api/v1.0/group/users/<string:group_id>

List of users and a number of groups that users belong to - sorted by the number of groups in ascending order ->

>> curl -i http://127.0.0.1:5000/manage/api/v1.0/list/users

List of groups and a number of users belonging to each group - sorted by the number of users in descending order ->

>> curl -i http://127.0.0.1:5000/manage/api/v1.0/list/groups

===================================================================================================================
Notes -

1. Change IP address if necessary in all the URL queries

2. test.sh is given to put data in your database. Currently pushes three users and groups to the database. 
User #2 is in Group #2. User #3 is in Group #2 and Group #3

3. Make sure "Content-Type: application/json"
