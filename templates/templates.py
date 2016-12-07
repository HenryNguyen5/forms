import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


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


class MainPage(Handler):

    def get(self):
        self.render("shopping_list.html", name=self.request.get("rot13"))


app = webapp2.WSGIApplication([
    ('/', MainPage), ],
    debug=True)
