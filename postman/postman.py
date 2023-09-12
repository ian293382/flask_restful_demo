from flask import Flask, request, jsonify
# from flask import render_template, request
from Users import UserModel

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
userModel = UserModel("users.csv")

# 1st by user_id
@app.route("/users/<int:user_id>")
@app.route("/users")
def get_users(user_id=None):
  users = userModel.get_users(user_id)
  return jsonify(users)

@app.route("/users", methods=["POST"])
def new_user():
  user = userModel.new_user(username=request.json["username"], age=request.json["age"])
  response = jsonify(user)
  response.headers["location"] = f"/users/{user['user_id']}"
  return response

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
  user = userModel.delete_user(user_id)
  return jsonify(user)

@app.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
  username = request.json["username"] if "username" in request.json else None
  age = request.json["age"] if "age" in request.json else None
  user = userModel.update_user(user_id, username=username, age=age)
  return jsonify(user)

if __name__ =="__main__":
  app.run(port=8081)