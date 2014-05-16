#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.web

from settings import *
from .Pomash import handlers as handler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = handler
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            autoescape=None,
            blog_name = blog_name,
            blog_url = blog_url,
            cookie_secret = cookie_secret,
            login_url = "/login",
            debug = DeBug
        )
        tornado.web.Application.__init__(self, handlers, **settings)
