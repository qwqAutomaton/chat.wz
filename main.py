import flask
import sqlite3

from requests import request

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


@app.route('/')
def index(): return flask.render_template('index.html')


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
        return flask.jsonify(code=0, status='OK', content=result, tail=result[-1][0] == 1)
    elif flask.request.method == 'POST':
        data = flask.request.json
        nickname = data['n']
        timestamp = int(data['t'])
        content = data['c']
        address = flask.request.remote_addr
        insert(address, nickname, timestamp, content)
        return flask.jsonify(code=0, status='OK')


if __name__ == '__main__':
    init()
    app.run(host='192.168.199.149', port=9010, debug=False)
