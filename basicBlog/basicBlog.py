import os

import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blogs(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Main(Handler):
    def get(self):
        blogs = db.GqlQuery("Select * FROM Blogs ORDER BY created DESC")
        self.render("main.html", blogs=blogs)


class Blog(Handler):

    def renderBlog(self):
        currUrl = self.request.path
        blogId = currUrl.split('/')[-1]
        blog = Blogs.get_by_id(int(blogId))
        self.render("blog.html", blog=blog)

    def get(self):
        self.renderBlog()


class NewPost(Handler):

    def renderNewPost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.renderNewPost()

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            b = Blogs(subject=subject, content=content)
            b.put()
            # get rid of redirect msg
            self.redirect("/blog/" + str(b.key().id()))
        else:
            error = "we need both a subject and some content!"
            self.renderNewPost(content=content,
                               subject=subject, error=error)

app = webapp2.WSGIApplication([
    (r'/blog.*', Blog),
    ('/newpost', NewPost),
    ('/', Main),
],
    debug=True)
