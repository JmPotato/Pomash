import string
import os.path
import tornado.web

from settings import *
from libs.utils import *
from libs.models import *

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/", HomeHandler),
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            xsrf_cookies = True,
            cookie_secret = cookie_secret,
            login_url = "/login",
            debug = DeBug
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        token = self.get_secure_cookie("token")
        if not token:
            return None
        username = token.split("^")[0]
        if not username:
            return None
        return username

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html", title = blog_name, blog_url = blog_url, blog_name = blog_name, articlesList = get_articles(4))