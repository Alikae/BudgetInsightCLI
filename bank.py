from utils import input_option, get_connectors_with_capability, get_connector_fields, fill_fields
from rich import print

class Bank:

	def __init__(self, auth_system):
		self.auth_system = auth_system

	def run(self):
		while True:
			index = input_option(
				"What do you want to do ?",
				[
					"Add an account",
					"Add a transaction",
					"See my accounts",
					"See my transactions",
					"Back",
				],
			)
			if index == 0:
				self.add_account()
			elif index == 1:
				pass
			elif index == 2:
				pass
			elif index == 3:
				pass
			elif index == 4:
				return

	def add_account(self):
		connectors = get_connectors_with_capability("bank")
		connectors_names = list(connectors.keys())
		index = input_option(
			"Choose a connector:",
			connectors_names
		)
		connector = connectors[connectors_names[index]]
		fields = get_connector_fields(connector["id"])
		print(fields)
		filled_fields = fill_fields(fields)
		print(filled_fields)

		# handle connection state errors
