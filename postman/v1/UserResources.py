from flask_restful import Resource, reqparse, fields, marshal_with
from flask import request
from .Users import UserModel
from flask import current_app as app
from flask import g
import pathlib, os
userModel = UserModel(os.path.join(pathlib.Path(__file__).parent,"users.csv"))

class UserResources(Resource):
  user_fields = {
    "user_id": fields.Integer,
    "username": fields.String,
    "age": fields.Integer,
    "nickname": fields.String(default="Any thing")
  }

  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument("username", type=str, help="username must be string")
    self.parser.add_argument("age", type=int, help="age must be number")

  @marshal_with(user_fields)
  def get(self, user_id=None):
      parser = self.parser
      parser.add_argument("items", type=int, help="it's an integet representing the number of users")
      parser.add_argument("offset", type=int, help="the beginning index of users")
      parser.add_argument("filter_by", type=str, help="a string repesenting the search cirteria")
      parser.add_argument("sort_by", type=str, help="a string representing the sorting cirteria")
      args = parser.parse_args()

      app.logger.info(f"uuid: {g.uuid}, is_connected: {g.conn['is_connected']}")

      return userModel.get_users(
        user_id,
        items=args.get("items"),
        offset=args.get("offset"),
        filter_by=args.get("filter_by"),
        sort_by=args.get("sort_by")
      )

  def post(self):
    parser = self.parser
    parser.add_argument("username", type=str, help="username must be string and required", required=True)
    parser.add_argument("age", type=int, help="age must be number and required", required=True)
    args = parser.parse_args()
    user = userModel.new_user(username=args["username"], age=args["age"])
    return user, 201,{"location": f"/users/{user['user_id']}"}

  def delete(self, user_id):
    user = userModel.delete_user(user_id)
    return user

  def put(self, user_id):
    return self.update_user(user_id)

  def patch(self, user_id):
    return self.update_user(user_id)


  def update_user(self, user_id):
    args = self.parser.parse_args()
    user = userModel.update_user(user_id, username=args.get("username"), age=args.get("age"))
    return user