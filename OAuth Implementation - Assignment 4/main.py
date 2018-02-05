from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import webapp2
import urllib
import random
import string
import json
import os

CLIENT_ID = '128374776299-hdm3lu6j28upp2a5luima2b7jf9qic4a.apps.googleusercontent.com'
CLIENT_SECRET = 'hsL4AxZHtx_ObsFj8G65Yg1H'
REDIRECT_URI = 'https://oauth20assignment.appspot.com/oauth'

class OauthHandler(webapp2.RequestHandler):
	def get(self):
		#logging.debug('The contents of GET: ' + repr(self.request.GET))
		auth_code = self.request.GET['code']
		state = self.request.GET['state']
		post_body = {'code': auth_code, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'redirect_uri': REDIRECT_URI, 'grant_type': 'authorization_code'}
		payload = urllib.urlencode(post_body)
		headers = {'Content-Type':'application/x-www-form-urlencoded'}
		
		# Get the access token
		result = urlfetch.fetch(url="https://www.googleapis.com/oauth2/v4/token", payload = payload, method = urlfetch.POST, headers = headers)
		json_result = json.loads(result.content)
		
		# Access the Google+ info with the access token
		headers = {'Authorization': 'Bearer ' + json_result['access_token']}
		result = urlfetch.fetch(url="https://www.googleapis.com/plus/v1/people/me", method = urlfetch.GET, headers = headers)
		json_result = json.loads(result.content)
		fname_exists = False
		lname_exists = False
		gplink_exists = False
		for item in json_result:
			if item == 'name':
				if item[0]:
					fname_exists = True
					lname_exists = True
			if item == 'url':
				gplink_exists = True
		
		if fname_exists and lname_exists and gplink_exists:
			fname = json_result['name']['givenName']
			lname = json_result['name']['familyName']
			gplink = str(json_result['url'])
			template_values = {'fname': fname, 'lname': lname, 'gplink': gplink, 'gplink_name': "View Profile", 'state': state}
		else:
			template_values = {'noAccount': "ERROR: No Google+ account found", 'state': state}
		
		path = os.path.join(os.path.dirname(__file__), 'templates/oauth.html')
		self.response.out.write(template.render(path, template_values))

class MainPage(webapp2.RequestHandler):
    def get(self):
		random_secret = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
		url = "https://accounts.google.com/o/oauth2/v2/auth?"
		url += "response_type=code"
		url += "&client_id="
		url += CLIENT_ID
		url += "&redirect_uri="
		url += REDIRECT_URI
		url += "&scope=email"
		url += "&state="
		url += random_secret
		template_values = {'url': url}
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/oauth', OauthHandler)
], debug=True)
