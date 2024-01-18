#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import dropbox
import os.path
import tornado.web
import tornado.template

from .config import *
from .libs.utils import *
from .libs.models import *
from .libs.handler import *

post_per_page = config["theme"]["post_per_page"]
dropbox_app_token = config["backup"]["dropbox_app_token"]
if dropbox_app_token:
    dbx = dropbox.Dropbox(dropbox_app_token)


class HomeHandler(BaseHandler):
    def get(self):
        self.render(
            "home.html",
            all_articles=get_all_articles(),
            articlesList=get_articles(1, post_per_page),
            post_per_page=float(post_per_page),
            page_number=1,
            count=float(get_article_count()),
            max_page=math.ceil(float(get_article_count()) / float(post_per_page)),
        )


class PageHandler(BaseHandler):
    def get(self, page):
        self.render(
            "home.html",
            all_articles=get_all_articles(),
            articlesList=get_articles(int(page), post_per_page),
            post_per_page=float(post_per_page),
            page_number=int(page),
            count=float(get_article_count()),
            max_page=math.ceil(float(get_article_count()) / float(post_per_page)),
        )


class CuPageHandler(BaseHandler):
    def get(self, page_id):
        article = gat_page(page_id)
        if not article:
            self.redirect("/404")
        self.render("page.html", all_articles=get_all_articles(), article=article)


class ArticleHandler(BaseHandler):
    def get(self, article_id):
        article = get_article(article_id)
        if not article:
            self.redirect("/404")
        tags = [tag.strip() for tag in article.tag.split(",")]
        self.render(
            "article.html",
            article=article,
            tags=tags,
            twitter_card_enabled=config["twitter_card"]["enabled"],
            twitter_username=config["twitter_card"]["username"],
            all_articles=get_all_articles(),
            giscus=config["giscus"],
        )


class ArticlesHandler(BaseHandler):
    def get(self):
        all_articles = get_all_articles()
        year_list = {}
        for article in all_articles:
            year = article["datetime"].split("-")[0]
            if year in year_list:
                year_list[year].append(article)
            else:
                year_list[year] = []
                year_list[year].append(article)
        self.render(
            "articles.html",
            all_articles=get_all_articles(),
            articlesList=year_list,
        )


class TagHandler(BaseHandler):
    def get(self, tag_name):
        all_tag_articles = get_tag_articles(tag_name)
        year_list = {}
        for article in all_tag_articles:
            year = article["datetime"].split("-")[0]
            if year in year_list:
                year_list[year].append(article)
            else:
                year_list[year] = []
                year_list[year].append(article)
        self.render(
            "tag.html",
            all_articles=get_all_articles(),
            tag_name=tag_name,
            articlesList=year_list,
        )


class TagsHandler(BaseHandler):
    def get(self):
        self.render(
            "tags.html",
            all_articles=get_all_articles(),
            tags=get_all_tags(),
        )


class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            if verify_token(self.get_current_user(), self.get_secure_cookie("token")):
                self.redirect("/admin")
                return
            else:
                self.render("login.html")
        else:
            self.render("login.html")

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        if config["admin"]["username"] == username:
            if verify_user(username, to_md5(password)):
                token = make_token()
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
    def get(self):
        if not self.get_current_user():
            self.redirect("/")
        self.clear_all_cookies()
        self.redirect("/")


class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        dropbox_on = True
        if not dropbox_app_token:
            dropbox_on = False
        self.render(
            "admin.html",
            articlesList=get_all_articles(),
            dropbox_on=dropbox_on,
        )


class PasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        message = self.get_argument("message", None)
        self.render(
            "change_pw.html",
            message=message,
        )

    @tornado.web.authenticated
    def post(self):
        username = self.get_current_user().decode("utf-8")
        if verify_user(username, to_md5(self.get_argument("o_password", None))):
            if change_password(username, to_md5(self.get_argument("n_password", None))):
                self.clear_all_cookies()
                self.redirect("/")
        else:
            self.redirect(
                "/admin/change_password?message=Failed to change Password: Wrong Old Password"
            )


class DropboxHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not dropbox_app_token:
            authorized = False
            message = self.get_argument(
                "message",
                "Authenticated Failed: You have not filled the token in settings.py",
            )
        else:
            authorized = True
            message = self.get_argument(
                "message", "Please backup your database and settings regularly."
            )
        self.render(
            "dropbox.html",
            authorized=authorized,
            message=message,
        )


class DropboxBackupHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if backup(dbx, DB_FILE) and backup(dbx, CONFIG_FILE):
            self.redirect("/admin/dropbox?message=Backup successfully")
        else:
            self.redirect("/admin/dropbox?message=Backup failed")


class DropboxRestoreHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if restore(dbx, DB_FILE) and restore(dbx, CONFIG_FILE):
            self.redirect("/admin/dropbox?message=Restore successfully")
        else:
            self.redirect("/admin/dropbox?message=Restore failed")


class NewPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            "editor.html",
            is_page=True,
            new=True,
        )

    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title", None)
        content = self.get_argument("content", None)
        if create_page(title=title, content=content):
            self.redirect("/")
        else:
            self.redirect("/admin")


class EditPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page_id):
        self.render(
            "editor.html",
            is_page=True,
            new=False,
            content=gat_page(page_id),
        )

    @tornado.web.authenticated
    def post(self, page_id):
        title = self.get_argument("title", None)
        content = self.get_argument("content", None)
        if update_page(int(page_id), title=title, content=content):
            self.redirect("/admin")


class DelPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page_id):
        if delete_page(page_id):
            self.redirect("/admin")


class NewArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
            "editor.html",
            is_page=False,
            new=True,
        )

    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title", None)
        tags = self.get_argument("tag", None)
        content = self.get_argument("content", None)
        create_article(title=title, content=content, tags=tags)
        self.redirect("/")


class EditArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        self.render(
            "editor.html", is_page=False, new=False, content=get_article(article_id)
        )

    @tornado.web.authenticated
    def post(self, article_id):
        title = self.get_argument("title", None)
        tags = self.get_argument("tag", None)
        content = self.get_argument("content", None)
        if update_article(int(article_id), title=title, content=content, tags=tags):
            self.redirect("/article/" + article_id)


class DelArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        if delete_article(article_id):
            self.redirect("/admin")


class FeedHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "text/xml; charset=utf-8")
        self.render(
            "feed.xml",
            articlesList=get_all_articles(),
        )


class PageNotFound(BaseHandler):
    def get(self):
        self.render("404.html")


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
    ("/admin/dropbox/start", DropboxBackupHandler),
    ("/admin/dropbox/load", DropboxRestoreHandler),
    ("/admin/change_password", PasswordHandler),
    ("/admin/edit/new/article", NewArticleHandler),
    ("/admin/edit/article/([\d]+)", EditArticleHandler),
    ("/admin/edit/delete/article/([\d]+)", DelArticleHandler),
    ("/admin/edit/new/page", NewPageHandler),
    ("/admin/edit/page/([\d]+)", EditPageHandler),
    ("/admin/edit/delete/page/([\d]+)", DelPageHandler),
    (r".*", PageNotFound),
]
