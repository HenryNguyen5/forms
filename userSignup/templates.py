import os
import re
import webapp2
import jinja2
import hmac

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return (EMAIL_RE.match(email) or email == '')


def valid_verifyPass(password, verify):
    return password == verify


def noErrors(errDictionary):
    for key in errDictionary:
        if errDictionary[key] != '':
            return False
    return True


class HashCookie():
    __secret = 'superSekreitcookies'

    def hash(self, val):
        h = hmac.new(self.__secret, val).hexdigest()
        return '%s|%s' % (val, h)

    def check(self, hCookie):
        plainVal = hCookie.split('|')[0]
        if(self.hash(plainVal) == hCookie):
            return plainVal


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler, HashCookie):

    def get(self):
        self.render("signup.html", errDictHTML='')

    def post(self):
        errDict = {'usrErr': '', 'passErr': '',
                   'verifyErr': '', 'emailErr': ''}
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        if(not valid_username(username)):
            errDict['usrErr'] = "Thats not a valid username"
            print "user not valid"
        if(not valid_password(password)):
            errDict['passErr'] = "Thats not a valid password"
        if(not valid_verifyPass(password, verify)):
            errDict['verifyErr'] = "Your passwords dont match"
        if(not valid_email(email)):
            errDict['emailErr'] = "Thats not a valid email"

        if(noErrors(errDict)):
            hCookie = self.hash(username)
            self.response.headers.add_header(
                'Set-Cookie', str("username=%s; Path=/" % hCookie))
            self.redirect('/welcome')
        self.render("signup.html", errDictHTML=errDict)


class Welcome(Handler, HashCookie):

    def get(self):
        cookie = self.request.cookies.get('username', '')
        chkdCookie = self.check(cookie)
        if (chkdCookie):
            self.render("welcome.html", user=chkdCookie)
        else:
            self.redirect('/signup')

class LogOut(Handler):
    def get(self):
        cookieToDel = self.request.cookies.get('username', '')
        self.response.headers.add_header('Set-Cookie', "username=; Path=/")
        self.redirect('/signup')

app = webapp2.WSGIApplication([
    ('/signup', MainPage),
    ('/welcome', Welcome),
    ('/logout', LogOut),
],
    debug=True)
