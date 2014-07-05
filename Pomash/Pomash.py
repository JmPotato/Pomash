#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import string
import os.path
import tornado.web
import tornado.template

from settings import *
from libs.utils import *
from libs.models import *
from libs.handler import *

from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient

app_key = 'fugru0h79njb20s'
app_secret = 'l2aigyu0eldnmzn'

flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html",
            title = blog_name,
            articlesList = get_articles(1, post_per_page),
            post_per_page = post_per_page,
            page_number = 1,
            count = get_article_count(),
            )

class PageHandler(BaseHandler):
    def get(self, page):
        self.render("home.html",
            title = blog_name,
            articlesList = get_articles(int(page), post_per_page),
            post_per_page = post_per_page,
            page_number = int(page),
            count = get_article_count(),
            )

class CuPageHandler(BaseHandler):
    def get(self, page_id):
        page = gat_page(page_id)
        self.render("page.html",
            title = blog_name + " | %s" % page.title,
            page = page,
            )
        
class ArticleHandler(BaseHandler):
    def get(self, article_id):
        article = get_article(article_id)
        tags = [tag.strip() for tag in article.tag.split(",")]
        self.render("article.html",
            title = blog_name + " | %s" % article.title,
            article = article,
            tags = tags,
            comment = enable_comment,
            disqus_name = disqus_name,
            twitter_card = twitter_card,
            twitter_username = twitter_username,
            )

class ArticlesHandler(BaseHandler):
    def get(self):
        all_articles = get_all_articles()
        year_list = {}
        articlesList = []
        for article in all_articles:
            year = article["datetime"].split("-")[0]
            if year in year_list:
                year_list[year].append(article)
            else:
                year_list[year] = []
                year_list[year].append(article)
        articlesList.append(year_list)
        self.render("articles.html",
            title = blog_name + " | Articles",
            articlesList = articlesList,
            )

class TagHandler(BaseHandler):
    def get(self, tag_name):
        self.render("tag.html",
            title = blog_name + " | %s" % tag_name,
            tag_name = tag_name,
            articlesList = get_tag_articles(tag_name),
            )

class TagsHandler(BaseHandler):
    def get(self):
        self.render("tags.html",
            title = blog_name + " | All Tags",
            tags = get_all_tags(),
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
                    )
        else:
            self.render("login.html",
                title = blog_name,
                )

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if login_username == username:
            if verify_user(username, to_md5(password)):
                token = make_token(username)
                update_token(username, token)
                self.set_secure_cookie("token", token)
                self.set_secure_cookie("username", username)
                self.redirect("/admin")
                return
            else:
                self.redirect("/login")
        else:
            self.redirect("/login")

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
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
            )

class DropboxHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        message = self.get_argument('message', 'Please backup your datebase and settings if you first use Pomash')
        if self.get_secure_cookie("access_token"):
            authorized = True
        else:
            authorized = False
        self.render("dropbox.html",
            title = blog_name + " | Dropbox",
            authorized = authorized,
            authorize_url = flow.start(),
            message = message,
            )

    def post(self):
        code = self.get_argument("code", None).strip()
        access_token, user_id = flow.finish(code)
        self.set_secure_cookie("access_token", access_token)
        self.set_secure_cookie("user_id", user_id)
        self.redirect("/admin/dropbox")

class DropboxBUHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        client = DropboxClient(self.get_secure_cookie("access_token"))
        try:
            client.file_delete('/blog.db')
            client.file_delete('/settings.py')
        except:
            print("Can't find any backup")
        finally:
            with open(os.path.join(os.path.abspath(os.path.dirname("__file__")), 'blog.db'), 'rb') as f:
                response = client.put_file('/blog.db', f)
            with open(os.path.join(os.path.abspath(os.path.dirname("__file__")), 'settings.py'), 'rb') as f:
                response = client.put_file('/settings.py', f)
            self.redirect("/admin/dropbox?message=Backup successfully")

class DropboxLDHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        client = DropboxClient(self.get_secure_cookie("access_token"))
        try:
            with client.get_file('/blog.db') as f:
                out = open('blog.db', 'wb')
                out.write(f.read())
                out.close()
            with client.get_file('/settings.py') as f:
                out = open('settings.py', 'wb')
                out.write(f.read())
                out.close()
        except:
            print("Can't find any backup")
            self.redirect('/admin/dropbox?message=Failed to load backup. Please make sure you have a backup on Dropbox')
        finally:
            self.redirect('/admin/dropbox?message=Load backup successfully')

class NewPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("editor.html",
            is_page = True,
            title = blog_name + " | New Page",
            new = True,
            )

    def post(self):
        title = self.get_argument("title", None)
        content = self.get_argument("content", None)
        if creat_page(title = title, content = content):
            self.redirect("/")
        else:
            self.redirect("/admin")

class EditPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page_id):
        self.render("editor.html",
            is_page = True,
            title = blog_name + " | Edit Page",
            new = False,
            page = gat_page(page_id),
            )
    
    def post(self, page_id):
        title = self.get_argument("title", None)
        content = self.get_argument("content", None)
        if update_page(int(page_id), title = title, content = content):
            self.redirect("/admin")

class DelPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page_id):
        if delete_page(page_id):
            self.redirect("/admin")

class NewArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("editor.html",
            is_page = False,
            title = blog_name + " | New Article",
            new = True,
            )

    def post(self):
        title = self.get_argument("title", None)
        tags = self.get_argument("tag", None)
        content = self.get_argument("content", None)
        creat_article(title = title, content = content, tags = tags)
        self.redirect("/")

class EditArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        self.render("editor.html",
            is_page = False,
            title = blog_name + " | Edit Article",
            new = False,
            article = get_article(article_id),
            )
    
    def post(self, article_id):
        title = self.get_argument("title", None)
        tags = self.get_argument("tag", None)
        content = self.get_argument("content", None)
        if update_article(int(article_id), title = title, content = content, tags = tags):
            self.redirect("/admin")

class DelArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        if delete_article(article_id):
            self.redirect("/admin")

class FeedHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "text/xml; charset=utf-8")
        self.render("feed.xml",
            articlesList = get_all_articles(),
            blog_author = blog_author,
            )

class PageNotFound(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(404)

handlers = [
    ("/", HomeHandler),
    ("/tag/([^/]+)/*", TagHandler),
    ("/tags", TagsHandler),
    ("/feed", FeedHandler),
    ("/articles", ArticlesHandler),
    ("/article/([\d]+)", ArticleHandler),
    ("/page/([\d]+)", PageHandler),
    ("/page/custom/([\d]+)", CuPageHandler),
    ("/admin", AdminHandler),
    ("/login", LoginHandler),
    ("/logout", LogoutHandler),
    ("/admin/dropbox", DropboxHandler),
    ("/admin/dropbox/start", DropboxBUHandler),
    ("/admin/dropbox/load", DropboxLDHandler),
    ("/admin/edit/new/article", NewArticleHandler),
    ("/admin/edit/article/([\d]+)", EditArticleHandler),
    ("/admin/edit/delete/article/([\d]+)", DelArticleHandler),
    ("/admin/edit/new/page", NewPageHandler),
    ("/admin/edit/page/([\d]+)", EditPageHandler),
    ("/admin/edit/delete/page/([\d]+)", DelPageHandler),
    (r'.*', PageNotFound),
]