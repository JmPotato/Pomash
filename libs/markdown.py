import re
import misaka

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from tornado.escape import xhtml_escape

class MyRender(misaka.HtmlRenderer, misaka.SmartyPants):
    def block_code(self, code, language):
        if language:
            lexer = get_lexer_by_name(language, stripall=True)
        else:
            return "<pre><code>%s</code></pre>" % xhtml_escape(code.strip())

        formatter = HtmlFormatter(noclasses=False, linenos=False)

        return '<div class="highlight-pre">%s</div>' % highlight(code, lexer, formatter)

    def autolink(self, link, is_email):
        if is_email:
            mailto = "".join(['&#%d;' % ord(letter) for letter in "mailto:"])
            email = "".join(['&#%d;' % ord(letter) for letter in link])
            url = mailto + email
            return '<a href="%(url)s">%(link)s</a>' % {'url': url, 'link': email}

        title = link.replace('http://', '').replace('https://', '')
        if len(title) > 30:
            title = title[:24] + "..."
        return '<a href="%s">%s</a>' % (link, title)