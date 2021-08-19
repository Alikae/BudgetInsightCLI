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
				self.get_accounts()
			elif index == 2:
				self.get_transactions()
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
	
	def get_accounts(self):
		""" Retrieve user accounts from all connections
		"""
		res = Request(
			"get",
			f"/users/{self.auth_system.user['id']}/accounts",
			self.auth_system.init_request_header(),
		).call()
		for account in res["accounts"]:
			print(account["original_name"], account["number"])
			print("\t", "IBAN " + str(account["iban"]))
			print("\t", "BIC  " + str(account["bic"]))
			print("\t", str(account["balance"]) + str(account["currency"]["symbol"]))
		if not len(res["accounts"]):
			print("No accounts linked yet! Add a connection first.")
	
	def get_transactions(self):
		""" Retrieve transactions from one account
		"""
		res = Request(
			"get",
			f"/users/{self.auth_system.user['id']}/accounts",
			self.auth_system.init_request_header(),
		).call()
		print("This month:")
		for account in res["accounts"]:
			res = Request(
				"get",
				f"/users/{self.auth_system.user['id']}/accounts/{account['id']}/transactions",
				self.auth_system.init_request_header(),
			).call()
			print(account["original_name"])
			for transaction in res["transactions"]:
				print("\t", transaction["date"], ":", transaction["value"], transaction["type"])


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

