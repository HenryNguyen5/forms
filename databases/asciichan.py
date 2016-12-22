import os

import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def rot13(text):
    returnStr = ''
    alphabetStr = 'abcdefghijklmnopqrstuvwxyz'
    capAlphabetStr = alphabetStr + alphabetStr.upper()
    alphabetList = list(capAlphabetStr)

    for character in text:
        if(character in alphabetList):
            currIdx = alphabetList.index(character)
            nxtIdx = currIdx + 13
            if (currIdx <= 25 and nxtIdx >= 26) or (currIdx > 25 and nxtIdx >= 52):
                returnStr += alphabetList[nxtIdx - 26]
            else:
                returnStr += alphabetList[nxtIdx]
        else:
            returnStr += character
    return returnStr


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):

    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("Select * FROM Art ORDER BY created DESC")
        self.render("front.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = Art(title=title, art=art)
            a.put()
            # get rid of redirect msg
            self.redirect("/")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(art=art,
                              title=title, error=error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
],
    debug=True)
