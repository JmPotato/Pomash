#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tomllib
import os.path
import tornado.web

from .config import config
from .pomash import handlers as handler

THEME_PATH = os.path.join(os.path.dirname(__file__), "theme/" + config["theme"]["name"])


class Application(tornado.web.Application):
    def __init__(self):
        handlers = handler
        settings = dict(
            # Assets-related
            static_path=os.path.join(THEME_PATH, "static"),
            template_path=os.path.join(THEME_PATH, "templates"),
            autoescape=None,
            # Blog-related
            blog_name=config["name"],
            blog_url=config["url"].strip().lstrip().rstrip("/"),
            blog_author=config["author"],
            theme=config["theme"],
            analytics=config["google_analytics"]["id"].strip().lstrip(),
            cookie_secret=config["admin"]["cookie_secret"],
            debug=config["development"]["debug"],
        )
        tornado.web.Application.__init__(self, handlers, **settings)
