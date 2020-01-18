#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import mistune
import tornado.web

from urllib.parse import unquote, quote

from .models import *
from .markdown import *
from tornado.escape import to_unicode, xhtml_escape

class BaseHandler(tornado.web.RequestHandler):
    def get_pure_title(self, title):
        return re.sub('''<("[^"]*"|'[^']*'|[^'">])*>''', "", title).strip()

    def escape_string(self, s):
        return xhtml_escape(s)
        
    def description(self, text):
        if len(text) <= 200:
            return re.sub('(<.*?>)', '', text).replace('\n', ' ')[:int(len(text)/2-4)] + '...'
        elif len(text) > 200:
            return re.sub('(<.*?>)', '', text).replace('\n', ' ')[:195] + '...'

    def md_to_html(self, text):
        text = to_unicode(text)
        renderer = MyRenderer()
        md = mistune.create_markdown(renderer=renderer)
        return md(text)

    def urlencode(self, text):
        return quote(text.encode('utf8'))

    def urldecode(self, text):
        return unquote(text.encode('utf8'))

    def get_custom_page(self):
        return get_all_pages()

    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username

    def get_error_html(self, status_code, **kwargs):
        if status_code == 404:
            self.render("404.html",
                title = "404 Page Not Found",
                )
        else:
            try:
                exception = "%s\n\n%s" % (kwargs["exception"],
                    traceback.format_exc())
                if self.settings.get("debug"):
                    self.set_header('Content-Type', 'text/plain')
                    for line in exception:
                        self.write(line)
                else:
                    self.write("oOps...! I made ​​a mistake... ")
            except Exception:
                return super(BaseHandler, self).get_error_html(status_code,
                    **kwargs)