#!/usr/bin/python2.7
# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']


form = """
<form method="post">
    What is your birthday?
    <br>

    <label>
      Month
      <input type="text" name="month" value="%(month)s">
    </label>

    <label>
      Day
      <input type="text" name="day" value="%(day)s">
    </label>

    <label>
      Year
      <input type="text" name="year" value="%(year)s">
    </label>

    <div style="color: red">%(error)s</div>

    <br>
    <br>
    <input type="submit">
</form>
"""


month_abbvs = dict((m[:3].lower(), m) for m in months)


def valid_month(month):
    if month:
        month = month[:3].lower()
        print month
        return month_abbvs.get(month)


def valid_day(day):
    if day.isdigit() and int(day) > 0 and int(day) <= 31:
        return int(day)


def valid_year(year):
    if year.isdigit() and int(year) >= 1950 and int(year) <= 2020:
        return int(year)


class MainPage(webapp2.RequestHandler):

    def write_fourm(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": month,
                                        "day": day,
                                        "year": year})

    def get(self):
        self.write_fourm()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            # re-render form
            self.write_fourm("That doesn't look right to me, friend.",
                             user_month, user_day, user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write(
            "Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', ThanksHandler)],
    debug=True)
