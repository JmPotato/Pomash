import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options
from Pomash import Application

define("port", default=8888, help="run on the given port for develop", type=int)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()