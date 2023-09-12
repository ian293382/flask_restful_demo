from flask_restful import Resource, fields, marshal_with
from .UserResources import userModel, UserResources

class ClassSizeField(fields.Raw):
  def format(self, users):
    return len(users)

class ClassRoomResources(Resource):
  class_fields = {
    "class_id": fields.Integer(default=-1),
    "class_name": fields.String(default=""),
    "class_size": ClassSizeField(attribute="users"),
    "users": fields.List(fields.Nested(UserResources.user_fields), default=[])
  }
  def __init__(self):
    self.rooms = {
      0:{
        "class_id": 0,
        "class_name": "calss_a",
        "users": [0, 1]
      },
      1: {
        "class_id": 1,
        "class_name": "class_b",
        "users":[1, 3, 4]
      }
    }

  @marshal_with(class_fields)
  def get(self, class_id=None):
    if class_id is None:
      return list(self.rooms.values())
     # 使用 in 关键字检查是否存在于字典中
    elif class_id in self.rooms:
      room = self.rooms[class_id].copy()
      room["users"] = list(map(self.update_user_info, room["users"]))
      return room
    else:
      return {}

  def update_user_info(self, user_id):
    return userModel.get_users(user_id)
