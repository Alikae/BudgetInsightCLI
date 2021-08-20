from config import BASE_URL, CLIENT_ID, CLIENT_SECRET
from request_system import Request
import os.path

class AuthSystem:

	def __init__(self):
		self.user = None
		if os.path.isfile("USER"):
			self.load_user("USER")
		else:
			self.create_user()

	def create_user(self):
		res = Request(
			"post",
			"/auth/init",
			{},
			{
				"client_id":		CLIENT_ID,
				"client_secret":	CLIENT_SECRET,
			},
		).call()
		self.user = {
			"id":		res["id_user"],
			"token":	res["auth_token"],
		}
		self.save_user("USER")
	
	def save_user(self, file_name):
		f = open(file_name, 'w')
		f.write(str(self.user["id"]) + '\n' + self.user["token"])
		f.close()

	def load_user(self, file_name):
		f = open(file_name, 'r')
		self.user = {
			"id":		int(f.readline()),
			"token":	f.readline(),
		}
		f.close()
		if self.user["token"][-1] == "\n":
			self.user["token"] = self.user["token"][:-1]
	
	def init_request_header(self):
		return {
			"Content-Type":		"application/json",
			"Authorization":	"OAuth " + self.user["token"],
		}

