import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


hidden_html = """
<input type="hidden" name="food" value="%s">
"""

item_html = """<li>%s</li>"""
shopping_list_html = """
<br>
<br>
<h2>Shopping List</h2>
<ul>
  %s
</ul>
"""


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):

    def get(self):
        self.render("shopping_list.html", name=self.request.get("name"))


app = webapp2.WSGIApplication([
    ('/', MainPage), ],
    debug=True)
