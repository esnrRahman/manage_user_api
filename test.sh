#!/bin/bash
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"test","email":"abc@test.com"}' http://127.0.0.1:5000/manage/api/v1.0/users
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"abc","email":"abcd@test.com"}' http://127.0.0.1:5000/manage/api/v1.0/users
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"def","email":"abc@test.com"}' http://127.0.0.1:5000/manage/api/v1.0/users

curl -i -H "Content-Type: application/json" -X POST -d '{"name":"group_abc"}' http://127.0.0.1:5000/manage/api/v1.0/groups
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"group_def"}' http://127.0.0.1:5000/manage/api/v1.0/groups
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"group_ghi"}' http://127.0.0.1:5000/manage/api/v1.0/groups

curl -i -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/manage/api/v1.0/user_group/2/2
curl -i -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/manage/api/v1.0/user_group/3/2
curl -i -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/manage/api/v1.0/user_group/3/3

