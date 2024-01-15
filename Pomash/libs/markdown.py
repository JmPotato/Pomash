#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mistune

from pygments import highlight
from pygments.styles import get_style_by_name
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from .utils import trim
from .. import dark_mode, pygments_style_light, pygments_style_dark


class MarkdownRender(mistune.HTMLRenderer):
    def emphasis(self, text):
        return "%s" % text

    def block_code(self, code, info=None):
        if info is None:
            return "<pre><code>%s</code></pre>" % code.strip()
        lexer = get_lexer_by_name(info, stripall=True)

        try:
            get_style_by_name(trim(pygments_style_light))
            light_style = trim(pygments_style_light)
        except:
            light_style = "pastie"

        try:
            get_style_by_name(trim(pygments_style_dark))
            dark_style = trim(pygments_style_dark)
        except:
            dark_style = "monokai"

        formatter = HtmlFormatter(
            style=dark_style if dark_mode else light_style,
            noclasses=True,
            linenos=False,
        )

        return '<div class="highlight-pre">%s</div>' % highlight(code, lexer, formatter)

    def autolink(self, link, is_email):
        if is_email:
            mailto = "".join(["&#%d;" % ord(letter) for letter in "mailto:"])
            email = "".join(["&#%d;" % ord(letter) for letter in link])
            url = mailto + email
            return '<a href="%(url)s">%(link)s</a>' % {"url": url, "link": email}

        title = link.replace("http://", "").replace("https://", "")
        if len(title) > 30:
            title = title[:24] + "..."
        return '<a href="%s">%s</a>' % (link, title)
