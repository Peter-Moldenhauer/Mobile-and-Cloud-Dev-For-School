import datetime
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        message = '<p>Hello World!</p><p>The current date/time is: %s</p>' %datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        self.response.out.write(message)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
