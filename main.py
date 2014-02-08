import os.path
import tornado.web

from .libs.utils import *
from .libs.models import *
from settings import cookie_secret, DeBug

from jinja2 import Environment, FileSystemLoader

templates_path = os.path.join(os.path.dirname(__file__), "templates")

env = Environment(
    loader=FileSystemLoader(templates_path),
    autoescape=False
    )

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/", HomeHandler),
            ("/auth/login", LoginHandler),
            ("/auth/logout", LogoutHandler),
            ("/admin", AdminHandler),
            ("/article/([\d]+)", ArticleHandler),
            ("/article/new/([\d]+)", NewArticleHandler),
            ("/article/edit/([\d]+)", EditArticleHandler),
            ("/article/delete/([\d]+)", DelArticleHandler),
            ("/category/([\d]+)", CategoryHandler),
            (r'.*', NotFound)
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = True,
            cookie_secret = cookie_secret,
            login_url = "/auth/login",
            debug = DeBug
        )
        tornado.web.Application.__init__(self, handlers, **settings)