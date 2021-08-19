from utils import input_option, get_connectors_with_capability, get_connector_fields, fill_fields
from rich import print
from request_system import Request

class Bank:

	def __init__(self, auth_system):
		self.auth_system = auth_system

	def run(self):
		while True:
			index = input_option(
				"What do you want to do ?",
				[
					"Add a connection",
					"See my accounts",
					"See my transactions",
					"Back",
				],
			)
			if index == 0:
				self.add_connection()
			elif index == 1:
				pass
			elif index == 2:
				pass
			elif index == 3:
				return
	
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
			print(filled_fields)
			json = filled_fields.copy()
			json["id_connector"] = connector["id"]
			res = Request(
				"post",
				f"/users/{self.auth_system.user['id']}/connections",
				self.auth_system.init_request_header(),
				json,
			).call()
			print(res)
			if handle_connection_state_errors(res):
				break
		print("Connection created!")

def handle_connection_state_errors(res):
	# TODO ?
	if "code" in res and res["code"] == "wrongpass":
		print("Incorrect Password")
		return False
	if res["state"]:
		print("Unhandled Error.")
		sys.exit()
	return True

