import tornado.web

class BaseHandler(tornado.web.RequestHandler):
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
