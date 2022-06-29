import flask
a = flask.Flask(__name__)
@a.route('/')
def b(): return '维护中'
