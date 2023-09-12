from flask import Blueprint
from flask_restful import Api
from .UserResources import UserResources
from .ClassRoomResources import ClassRoomResources
from .MessageResources import MessageResources
from .Users import UserModel

v1_bp = Blueprint("v1_blueprint", __name__)
api = Api(v1_bp)



api.add_resource(UserResources, "/users", "/users/<int:user_id>")
api.add_resource(ClassRoomResources, "/class_rooms", "/class_rooms/<int:class_id>")
api.add_resource(MessageResources, "/messages/<int:user_id>")