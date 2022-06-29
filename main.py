import flask
import sqlite3
import base64

app = flask.Flask(__name__)
database = 'data.sql'


def init():
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute('create table if not exists data(id INTEGER PRIMARY KEY AUTOINCREMENT, addr TEXT NOT NULL, nick TEXT NOT NULL, time INT NOT NULL, content TEXT NOT NULL);')
    db.commit()


def insert(addr, nick, time, content):
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute("insert into data(addr, nick, time, content) values('%s', '%s', %d, '%s');" %
                (addr, nick, time, content))
    db.commit()


def query(time, count):
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute('select * from data where time <= %d order by id desc' % time)
    return cur.fetchmany(count)


@app.route('/info')
def info(): return flask.render_template('info.html')


@app.route('/joinme')
def joinme(): return flask.render_template('joinme.html')


@app.route('/')
def index(): return flask.render_template('index.html')


@app.route('/favicon.ico')
def favicon(): return app.send_static_file('icon.ico')


@app.route('/api', methods=['GET', 'POST'])
def api():
    if flask.request.method == 'GET':
        args = flask.request.args
        try:
            timestamp = int(args.get('t'))
            count = int(args.get('c'))
        except ValueError as e:
            return flask.jsonify(code=1, status=e.__str__(), content=[])
        except TypeError as e:
            return flask.jsonify(code=2, status=e.__str__(), content=[])
        if count > 10:
            return flask.jsonify(code=3, status='cnt = ' + str(count) + ' > 10', content=[])
        result = query(timestamp, count)
        result = list(map(lambda x: [x[0], x[1], base64.b64decode(x[2].encode()).decode(
            'utf-8'), x[3], base64.b64decode(x[4].encode()).decode('utf-8')], result))
        return flask.jsonify(code=0, status='OK', content=result, tail=True if len(result) == 0 else result[-1][0] == 1)
    elif flask.request.method == 'POST':
        data = flask.request.json
        try:
            nickname = base64.b64encode(data['n'].encode('utf-8')).decode()
            timestamp = int(data['t'])
            content = base64.b64encode(data['c'].encode('utf-8')).decode()
            address = flask.request.remote_addr
            insert(address, nickname, timestamp, content)
            return flask.jsonify(code=0, status='OK')
        except Exception as e:
            return flask.jsonify(code=-1, status='no OK')


# @app.route('/token', methods=['POST'])
# def token():
#     '''
#     post {
#         act: 'query', val: 'xxxx'
#     }
#     resp {
#         code: 0 / 1, val: 'xxx'
#     } // 0: no msg; 1: yes msg

#     post {
#         act: 'require', val: 'yyy'
#     }
#     resp {
#         code: 0 / 1, val: 'xxxx'
#     } // 0: ok, 1: err
#     '''
#     data = flask.request.json
#     try:
#         act = data['act']
#         val = data['val']
#         if act == 'require':
#             pass # TODO here
#     except Exception as e:
#         return flask.jsonify(code=1, val='')


init()
