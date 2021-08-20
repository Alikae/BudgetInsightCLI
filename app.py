from auth_system import AuthSystem
from utils import input_option, get_connectors_with_capability, get_connector_fields, fill_fields
from bank import Bank
from wealth import Wealth
from request_system import Request

class App:

	def __init__(self):
		self.auth_system = AuthSystem()
		self.api = None

	def run(self):
		while True:
			# Choose an api to interact with
			choices = ["Add a connection", "bank", "wealth", "bill", "Quit"]
			index = input_option(
				"What do you want to do?",
				choices,
			)
			if index == 0:
				self.add_connection()
				continue
			elif index == 4:
				return
			self.api = choices[index]
			print("API " + self.api + " :")
			getattr(self, self.api)()

	def add_connection(self):
		""" Add a connection between the users and a bank account
		"""
		connectors = get_connectors_with_capability("bank")
		connectors_names = list(connectors.keys())
		index = input_option(
			"Choose a connector:",
			connectors_names
		)
		connector = connectors[connectors_names[index]]
		fields = get_connector_fields(connector["id"])
		while True:
			filled_fields = fill_fields(fields)
			json = filled_fields.copy()
			json["id_connector"] = connector["id"]
			connection = Request(
				"post",
				f"/users/{self.auth_system.user['id']}/connections",
				self.auth_system.init_request_header(),
				json,
			).call()
			if handle_connection_state_errors(connection):
				break
		print("Connection created!")
		self.activate_accounts(connection["id"])
	
	def activate_accounts(self, connection_id):
		res = Request(
			"get",
			f"/users/{self.auth_system.user['id']}/connections/{connection_id}/accounts?all",
			self.auth_system.init_request_header(),
		).call()
		to_activate = []
		for account in res["accounts"]:
			activate = input_option(
				"Activate " + account["name"] + "?",
				["No", "Yes"],
			)
			if activate:
				to_activate.append(str(account["id"]))
		if len(to_activate):
			Request(
				"put",
				f"/users/me/connections/{connection_id}/accounts/" + ",".join(to_activate) + "?all",
				self.auth_system.init_request_header(),
				{
					"disabled": False,
				},
			).call()

	def bank(self):
		Bank(self.auth_system).run()

	def wealth(self):
		Wealth(self.auth_system).run()

	def bill(self):
		pass

def handle_connection_state_errors(res):
	# TODO ?
	if "code" in res:
		if res["code"] == "wrongpass":
			print("Incorrect Password")
			return False
		if res["code"] == "config":
			print(res["description"])
			return False
	if res["state"]:
		print("Unhandled Error.")
		sys.exit()
	return True


if __name__ == "__main__":
	try:
		App().run()
	except KeyboardInterrupt:
		print("Marvellous day to you. Ciao!")

