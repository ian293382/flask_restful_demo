from flask import Flask, jsonify, g
# from flask import render_template, request
from Performance import Performance
from v1 import v1_bp
import uuid, time

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

performance = Performance("performance.csv ")

@app.before_request
def preprocess():
  g.uuid = uuid.uuid4()
  g.conn = {"is_connected": True}
  g.start = time.time()

@app.after_request
def postprocess(response):
  g.conn["is_connected"] = False
  g.end = time.time()
  g.status_code = response.status_code
  performance.log(g)
  app.logger.info(f"response time: {g.end-g.start}")
  return response

@app.teardown_request
def teardown_process(error):

  g.conn["is_connected"] = False
  app.logger.error(f"This user-{g.uuid} is experiencing the error:{error}")

app.register_blueprint(v1_bp, url_prefix="/v1")

if __name__ =="__main__":
  print(app.url_map)
  app.run(port=8081)