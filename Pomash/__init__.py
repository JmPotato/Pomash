#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.web

from settings import *
from .Pomash import handlers as handler

theme_path = os.path.join(os.path.dirname(__file__), "theme/" + theme)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = handler
        settings = dict(
            static_path = os.path.join(theme_path, "static"),
            template_path = os.path.join(theme_path, "templates"),
            autoescape = None,
            blog_name = blog_name,
            blog_url = blog_url.strip().lstrip().rstrip("/"),
            blog_author = blog_author,
            cookie_secret = cookie_secret,
            analytics = analytics.strip().lstrip(),
            login_url = "/login",
            dark_mode = dark_mode,
            debug = DeBug
        )
        tornado.web.Application.__init__(self, handlers, **settings)
