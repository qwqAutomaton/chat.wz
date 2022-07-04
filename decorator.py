import flask
def adminOnly(f):
    def _wrapper(*args, **kwargs):
        if flask.request.remote_addr != '127.0.0.1' or flask.request.remote_addr != '192.168.199.149':
            flask.abort(403)
        else:
            f(*args, **kwargs)
    return _wrapper