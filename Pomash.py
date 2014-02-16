import time
import string
import os.path
import tornado.web

from settings import *
from libs.utils import *
from libs.models import *
from libs.handler import *

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/", HomeHandler),
            ("/login", LoginHandler),
            ("/logout", LogoutHandler),
            ("/admin", AdminHandler),
            ("/admin/edit/article/([\d]+)", EditArticleHandler),
            ("/admin/edit/new/article", NewArticleHandler),
            ("/admin/edit/delete/article/([\d]+)", DelArticleHandler),
            ("/admin/edit/new/category", NewCategoryHandler),
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            blog_name = blog_name,
            blog_url = blog_url,
            cookie_secret = cookie_secret,
            login_url = "/login",
            debug = DeBug
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html",
            title = blog_name,
            articlesList = get_articles(5),
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
                    not_login = True
                    )
        else:
            self.render("login.html",
                title = blog_name,
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
                not_login = True,
                )

class LogoutHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            self.redirect("/")
        self.clear_cookie("username")
        self.clear_cookie("token")
        self.redirect("/")

class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin.html",
            title = blog_name + " | Admin",
            blog_author = blog_author,
            articlesList = get_all_articles(),
            success = False,
            )

class NewArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("editor.html",
            title = blog_name + " | New",
            new = True,
            categories = get_all_categories(),
            )

    def post(self):
        title = self.get_argument("title", None)
        category = self.get_argument("category", None)
        content = self.get_argument("content", None)
        creat_article(title = title, category = category, content = content)

class EditArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        self.render("editor.html",
            title = blog_name + " | Edit",
            new = False,
            article = get_article(article_id),
            )
    
    def post(self, article_id):
        title = self.get_argument("title", None)
        category = self.get_argument("category", None)
        content = self.get_argument("content", None)
        if update_article(int(article_id), title = title, category = category, content = content):
            pass
        else:
            pass

class DelArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        delete_article(article_id)
        self.render("admin.html",
            title = blog_name,
            blog_author = blog_author,
            articlesList = get_all_articles(),
            success = True,
            message = "Successful to delete an article"
            )

class NewCategoryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass