#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mistune
import tornado.web

from models import *
from markdown import *
from tornado.escape import to_unicode

class BaseHandler(tornado.web.RequestHandler):
    def md_to_html(self, text):
        text = to_unicode(text)
        renderer = MyRenderer()
        md = mistune.Markdown(renderer=renderer)
        return md.render(text)

    def get_custom_page(self):
        return get_all_pages()

    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username

    def render_string(self, template_name, **kwargs):
        base_value = dict(
            blog_url = self.application.settings["blog_url"],
            blog_name = self.application.settings["blog_name"],
            )
        template_path = self.get_template_path()
        if not template_path:
            frame = sys._getframe(0)
            web_file = frame.f_code.co_filename
            while frame.f_code.co_filename == web_file:
                frame = frame.f_back
            template_path = os.path.dirname(frame.f_code.co_filename)
        with tornado.web.RequestHandler._template_loader_lock:
            if template_path not in tornado.web.RequestHandler._template_loaders:
                loader = self.create_template_loader(template_path)
                tornado.web.RequestHandler._template_loaders[template_path] = loader
            else:
                loader = tornado.web.RequestHandler._template_loaders[template_path]
        t = loader.load(template_name)
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        namespace.update(base_value)
        return t.generate(**namespace)

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