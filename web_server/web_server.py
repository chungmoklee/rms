from gevent import monkey; monkey.patch_all()
import os

from socketio import socketio_manage
from socketio.server import SocketIOServer


webroot = os.path.abspath(os.path.dirname(__file__))
webroot = os.path.join(webroot, "web")


class Application(object):
    def __init__(self, namespaces):
        self.buffer = []
        self.namespaces = namespaces

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'

#        if path.startswith('static/') or path == 'index.html':
        if path.startswith("socket.io"):
            socketio_manage(environ, self.namespaces)
        else:
            try:
                data = open(os.path.join(webroot, path)).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

#        else:
#            return not_found(start_response)


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


def make_server(namespaces):
    return SocketIOServer(
        ('0.0.0.0', 51324),
        Application(namespaces),
        resource="socket.io")
