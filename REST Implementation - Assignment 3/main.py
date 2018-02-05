# Assignment: REST Planning and Implementation
# Class: CS 496
# Name: Peter Moldenhauer
# Date: 1/21/2018

from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	type = ndb.StringProperty(required=True)
	length = ndb.IntegerProperty(required=True)
	at_sea = ndb.BooleanProperty()

class BoatHandler(webapp2.RequestHandler):
	# Create a new boat - starts off "At sea"
	def post(self):
		boat_data = json.loads(self.request.body)
		input_name = False
		input_type = False
		input_length = False
		for item in boat_data:
			if item == "name":
				input_name = True
			elif item == "type":
				input_type = True
			elif item == "length":
				input_length = True
		if input_name and input_type and input_length:
			new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'])
			new_boat.at_sea = True
			new_boat.put()
			new_boat.id = str(new_boat.key.urlsafe())
			new_boat.put()
			new_boat_dict = new_boat.to_dict()
			new_boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()
			self.response.write(json.dumps(new_boat_dict))
		else:
			self.response.status = 400
			error_string = "400 ERROR!\nPOST must be in the format of: {\"name\": \"str\", \"length\": int, \"type\": \"str\"}"
			self.response.write(error_string.replace("\n", "<br />"))
	
	# View boat(s) - either a single boat or list of all boats
	def get(self, id=None):
		# View single boat
		if id:
			boat_exists = False
			for boat in Boat.query():
				if boat.id == id:
					boat_exists = True
			if boat_exists:
				get_boat = ndb.Key(urlsafe=id).get()
				get_boat_dict = get_boat.to_dict()
				get_boat_dict['self'] = "/boats/" + id
				self.response.write(json.dumps(get_boat_dict))
			else:
				self.response.status = 400
				error_string = "400 ERROR!\nThe given boat does not exist!"
				self.response.write(error_string.replace("\n", "<br />"))
		# View list of all boats
		else:
			get_boat_list = [get_boats.to_dict() for get_boats in Boat.query()]
			for boat in get_boat_list:
				boat['self'] = "/boats/" + str(boat['id'])
			self.response.write(json.dumps(get_boat_list))
	
	# Modify boat with PATCH (this is a "partial update")
	def patch(self, id=None):
		if id:
			boat_exists = False
			patch_boat_data = json.loads(self.request.body)
			for boat in Boat.query():
				if boat.id == id:
					boat_exists = True
			if boat_exists:
				patch_boat = ndb.Key(urlsafe=id).get()
				# Make sure only 1 field is being updated
				if len(patch_boat_data) > 1:
					self.response.status = 400
					error_string = "400 ERROR!\nData in body of PATCH should relate to only 1 field!\nSuch as: {name: str}"
					self.response.write(error_string.replace("\n", "<br />"))
				else:
					for key in patch_boat_data:
						if key == "name":
							patch_boat.name = patch_boat_data['name']
							patch_boat.put()
							self.response.write("Boat name was successfully modified")
						elif key == "type":
							patch_boat.type = patch_boat_data['type']
							patch_boat.put()
							self.response.write("Boat type was successfully modified")
						elif key == "length":
							patch_boat.length = patch_boat_data['length']
							patch_boat.put()
							self.response.write("Boat length was successfully modified")
						else:
							self.response.status = 400
							error_string = "400 ERROR!\nIncorrect format of data in body of PATCH"
							self.response.write(error_string.replace("\n", "<br />"))
			else:
				self.response.status = 400
				error_string = "400 ERROR!\nBoat does not exist"
				self.response.write(error_string.replace("\n", "<br />"))

	# Modify boat with PUT (this is a "total update")
	def put(self, id=None):
		if id:
			put_boat_data = json.loads(self.request.body)
			boat_exists = False
			for boat in Boat.query():
				if boat.id == id:
					boat_exists = True
			if boat_exists:
				put_boat = ndb.Key(urlsafe=id).get()
				input_name = False
				input_type = False
				input_length = False
				for item in put_boat_data:
					if item == "name":
						input_name = True
					elif item == "type":
						input_type = True
					elif item == "length":
						input_length = True
				if input_name and input_type and input_length:
					put_boat.name = put_boat_data['name']
					put_boat.type = put_boat_data['type']
					put_boat.length = put_boat_data['length']
					put_boat.put()
					self.response.write("Boat name, type and length successfully modified")
				else:
					self.response.status = 400
					error_string = "400 ERROR!\nIncorrect format of data in body of PUT\nUse the format of: {\"name\": \"str\", \"length\": int, \"type\": \"str\"}"
					self.response.write(error_string.replace("\n", "<br />"))
			else:
				self.response.status = 400
				error_string = "400 ERROR!\nBoat does not exist"
				self.response.write(error_string.replace("\n", "<br />"))
	
	# Delete a boat
	def delete(self, id=None):
		if id:
			boat_exists = False
			for boat in Boat.query():
				if boat.id == id:
					boat_exists = True
			if boat_exists:
				clear_slip = False
				for slip in Slip.query(Slip.current_boat == id):
					if slip.current_boat and slip.arrival_date:
						slip.current_boat = ""
						slip.arrival_date = ""
						slip.put()
						clear_slip = True
				if clear_slip:
					ndb.Key(urlsafe=id).delete()
					self.response.write("Boat was successfully deleted and the slip was emptied")
				else:
					ndb.Key(urlsafe=id).delete()
					self.response.write("Boat was successfully deleted")
			else:
				self.response.status = 400
				self.response.write("400 ERROR! Cannot delete boat, boat does not exist")
	
	
class Slip(ndb.Model):
	id = ndb.StringProperty()
	number = ndb.IntegerProperty(required=True)
	current_boat = ndb.StringProperty()
	arrival_date = ndb.StringProperty()
	
class SlipHandler(webapp2.RequestHandler):
	# Create a new slip - starts off empty
	def post(self):
		post_slip_data = json.loads(self.request.body)
		post_slip_list = [post_slip_query.to_dict() for post_slip_query in Slip.query()]
		input_number = False
		for i in post_slip_data:
			if i == "number":
				input_number = True
		if input_number:
			in_use = False
			for slip in post_slip_list:
				if slip['number'] == post_slip_data['number']:
					in_use = True
					self.response.status = 403
					self.response.write("403 ERROR! Slip number is already used")
			if not in_use:
				post_slip = Slip(number=post_slip_data['number'])
				post_slip.current_boat = ""
				post_slip.arrival_date = ""
				post_slip.put()
				post_slip.id = str(post_slip.key.urlsafe())
				post_slip.put()
				post_slip_dict = post_slip.to_dict()
				post_slip_dict['self'] = '/slips/' + post_slip.key.urlsafe()
				self.response.write(json.dumps(post_slip_dict))
		else:
			self.response.status = 400
			error_string = "400 ERROR!\nNo slip number provided\nExpected format: {\"number\": int}"
			self.response.write(error_string.replace("\n", "<br />"))
	
	# View a slip(s) - either a single slip or a list of all slips
	def get(self, id=None):
		# View single slip
		if id:
			slip_exists = False
			for slip in Slip.query():
				if slip.id == id:
					slip_exists = True
			if slip_exists:
				get_slip = ndb.Key(urlsafe=id).get()
				get_slip_dict = get_slip.to_dict()
				get_slip_dict['self'] = "/slips/" + id
				self.response.write(json.dumps(get_slip_dict))
			else:
				self.response.status = 400
				self.response.write("400 ERROR! Slip does not exist")
		# View list of all slips
		else:
			get_slip_list = [get_slip_query.to_dict() for get_slip_query in Slip.query()]
			for slip in get_slip_list:
				slip['self'] = "/slips/" + str(slip['id'])
			self.response.write(json.dumps(get_slip_list))
	
	# Modify slip with PATCH (this is a "partial update")
	def patch(self, id=None):
		if id:
			patch_slip_data = json.loads(self.request.body)
			slip_exists = False
			for slip in Slip.query():
				if slip.id == id:
					slip_exists = True
			if slip_exists:
				patch_slip = ndb.Key(urlsafe=id).get()
				if len(patch_slip_data) > 1:
					self.response.status = 400
					error_string = "400 ERROR!\nData in body of PATCH should relate to only 1 field!\nSuch as: {\"number\": int}"
					self.response.write(error_string.replace("\n", "<br />"))
				else:
					for key in patch_slip_data:
						if key == "number":
							patch_slip_list = [patch_slip_query.to_dict() for patch_slip_query in Slip.query()]
							in_list = False
							for slip in patch_slip_list:
								if slip['number'] == patch_slip_data['number']:
									in_list = True
									self.response.status = 403
									self.response.write("403 ERROR! Slip number is already in use")
							if not in_list:
								patch_slip.number = patch_slip_data['number']
								patch_slip.put()
								self.response.write("Slip number successfully modified")
						else:
							self.response.status = 400
							error_string = "400 ERROR!\nIncorrect format in body of PATCH\nExpected format: {\"number\": int}"
							self.response.write(error_string.replace("\n", "<br />"))
			else:
				self.response.status = 400
				self.response.write("400 ERROR! Slip does not exist")
				
	# Delete slip
	def delete(self, id=None):
		if id:
			slip_exists = False
			for slip in Slip.query():
				if slip.id == id:
					slip_exists = True
			if slip_exists:
				delete_slip = ndb.Key(urlsafe=id).get()
				if delete_slip.current_boat:
					boat_in_slip = ndb.Key(urlsafe=delete_slip.current_boat).get()
					boat_in_slip.at_sea = True;
					boat_in_slip.put()
					delete_slip.key.delete()
					self.response.write("Slip was successfully deleted and boat was sent out to sea")
				else:
					delete_slip.key.delete()
					self.response.write("Slip was successfully deleted")
			else:
				self.response.status = 400
				self.response.write("400 ERROR! Cannot deleted slip, slip does not exist")


class BoatInSlipHandler(webapp2.RequestHandler):
	# View if a boat is in a given slip (use slip id # in the url)
	def get(self, id=None):
		if id:
			slip_exists = False
			for slip in Slip.query():
				if slip.id == id:
					slip_exists = True
			if slip_exists:
				get_slip = ndb.Key(urlsafe=id).get()
				if get_slip.current_boat == "":
					self.response.write("Slip is free to use, no boat is in the given slip")
				else:
					get_boat = ndb.Key(urlsafe=get_slip.current_boat).get()
					boat_dict = get_boat.to_dict()
					boat_dict['self'] = "/boats/" + get_slip.current_boat
					self.response.write(json.dumps(boat_dict))
			else:
				self.response.status = 400
				self.response.write("400 ERROR! Slip does not exist")
	
	# Assign a boat to the given slip with PUT 
	def put(self, id=None):
		if id:
			put_data = json.loads(self.request.body)
			slip_exists = False
			for slip in Slip.query():
				if slip.id == id:
					slip_exists = True
			if slip_exists:
				put_slip = ndb.Key(urlsafe=id).get()
				input_current_boat = False
				input_arrival_date = False
				for item in put_data:
					if item == "current_boat":
						input_current_boat = True
					elif item == "arrival_date":
						input_arrival_date = True
				if input_current_boat and input_arrival_date:
					boat_exists = False
					for boat in Boat.query():
						if boat.id == put_data['current_boat']:
							boat_exists = True
					if boat_exists:
						put_boat = ndb.Key(urlsafe=put_data['current_boat']).get()
						if put_boat.at_sea:
							if put_slip.current_boat == "":
								put_slip.current_boat = put_data['current_boat']
								put_slip.arrival_date = put_data['arrival_date']
								put_slip.put()
								put_boat.at_sea = False
								put_boat.put()
								self.response.write("Boat was successfully added to the slip in the marina")
							else:
								self.response.status = 403
								self.response.write("403 ERROR! Cannot add boat to the given slip. The slip is already in use")
						else:
							self.response.status = 403
							self.response.write("403 ERROR! Cannot add boat to the given slip. The boat is already in another slip")
					else:
						self.response.status = 400
						self.response.write("400 ERROR! Cannot add boat to the given slip. The boat does not exist")
				else:
					self.response.status = 400
					self.response.write("400 ERROR! Incorrect format in body of PUT. Use the expected format of: {\"current_boat\": \"boat_id\", \"arrival_date\": \"YYYY-MM-DD\"}")
			else:
				self.response.status = 400
				self.response.write("400 ERROR! Slip does not exist")
	
	# Remove a boat from the given slip with DELETE
	def delete(self, id=None):
		if id:
			slip_exists = False
			for slip in Slip.query():
				if slip.id == id:
					slip_exists = True
			if slip_exists:
				slip = ndb.Key(urlsafe=id).get()
				if slip.current_boat:
					boat_in_slip = ndb.Key(urlsafe=slip.current_boat).get()
					boat_in_slip.at_sea = True
					boat_in_slip.put()
					slip.current_boat = ""
					slip.arrival_date = ""
					slip.put()
					self.response.write("Boat was successfully removed from the given slip and sent out to sea")
				else:
					self.response.status = 403
					self.response.write("403 ERROR! Cannot remove boat from slip. There is no boat in this slip")
			else:
				self.response.status = 400
				self.response.write("400 ERROR! Slip does not exst")


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("REST Planning and Implementation - Marina")


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/boats',BoatHandler),
	('/boats/(.*)',BoatHandler),
	('/slips',SlipHandler),
	('/slips/(.*)',SlipHandler),
	('/marina/(.*)',BoatInSlipHandler)
], debug=True)
