import flask

app = flask.Flask(__name__)

# Before request
@app.before_request
def before_request():
    flask.g.ip = flask.request.remote_addr