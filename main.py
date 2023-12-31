from flask import Flask
from flask import render_template, request
from Users import UserModel

app = Flask(__name__, template_folder="./templement/")
app.config.from_object("config.DevelopmentConfig")
userModel = UserModel("users.csv")

@app.route("/")
def login():
  return render_template("_name_form.html")

@app.route("/index_v1", methods=["POST"])
def index():
  return render_template("index.html", username=request.form["username"])

@app.route("/users")
def users():
  return render_template("users.html", users=userModel.get_users())

if __name__ =="__main__":
  app.run(port=8081)