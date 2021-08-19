from utils import input_option

class Wealth:

	def __init__(self, auth_system):
		self.auth_system = auth_system
	
	def run(self):
		while True:
			index = input_option(
				"What do you want to do ?",
				[
					"Add a connection",
					"See my patrimony accounts",
					"See my investments / history",
					"Back",
				],
			)
			if index == 3:
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

