from utils import input_option
from request_system import Request
from rich import print

class Bill:

	def __init__(self, auth_system):
		self.auth_system = auth_system
	
	def run(self):
		while True:
			index = input_option(
				"What do you want to do ?",
				[
					"See my subscriptions",
					"See my documents",
					"Back",
				],
			)
			if index == 0:
				self.get_subscriptions()
			elif index == 1:
				self.get_documents()
			elif index == 2:
				return

	def get_subscriptions(self):
		res = Request(
			"get",
			f"/users/{self.auth_system.user['id']}/subscriptions?all",
			self.auth_system.init_request_header(),
		).call()
		# auto enable each subscription, not good for a real application
		for subscription in res["subscriptions"]:
			res = Request(
				"put",
				f"/users/{self.auth_system.user['id']}/subscriptions/{subscription['id']}?all",
				self.auth_system.init_request_header(),
				{"disabled": False},
			).call()
			print(subscription["label"], "(", subscription["subscriber"], ")")

	def get_documents(self):
		res = Request(
			"get",
			f"/users/{self.auth_system.user['id']}/documents?all",
			self.auth_system.init_request_header(),
		).call()
		for document in res["documents"]:
			print(document["name"], "(", document["url"], ")")

