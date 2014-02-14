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
            ("/login", LoginHandler),
            ("/admin", AdminHandler),
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            cookie_secret = cookie_secret,
            login_url = "/login",
            debug = DeBug
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if not username:
            return Nones
        return username

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html",
            title = blog_name,
            blog_url = blog_url,
            blog_name = blog_name,
            articlesList = get_articles(5)
            )

class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            if verify_token(self.get_current_user(), self.get_secure_cookie("token")):
                self.redirect("/admin")
                return
            else:
                self.render("login.html",
                    title = blog_name,
                    blog_url = blog_url,
                    blog_name = blog_name,
                    not_login = True
                    )
        else:
            self.render("login.html",
                title = blog_name,
                blog_url = blog_url,
                blog_name = blog_name,
                not_login = False
                )

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if verify_user(username, to_md5(password)):
            token = make_token(username)
            updata_token(username, token)
            self.set_secure_cookie("token", token)
            self.set_secure_cookie("username", username)
            self.redirect("/admin")
            return
        else:
            self.render("login.html",
                title = blog_name,
                blog_url = blog_url,
                blog_name = blog_name,
                not_login = True
                )

class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("admin.html",
            title = blog_name,
            blog_url = blog_url,
            blog_name = blog_name,
            blog_author = blog_author,
            articlesList = get_all_articles()
            )
        