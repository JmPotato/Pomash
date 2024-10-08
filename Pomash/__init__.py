#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

import tornado.web

from Pomash.config import config
from Pomash.Pomash import handlers as handler

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
            blog_name=config["name"].strip(),
            blog_url=config["url"].strip().rstrip("/"),
            blog_author=config["author"].strip(),
            theme=config["theme"],
            analytics=config["google_analytics"]["id"].strip(),
            cookie_secret=config["admin"]["cookie_secret"],
            debug=config["development"]["debug"],
        )
        tornado.web.Application.__init__(self, handlers, **settings)
