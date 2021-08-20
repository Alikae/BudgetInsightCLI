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
					"See my accounts",
					"See my transactions",
					"Back",
				],
			)
			if index == 0:
				self.get_accounts()
			elif index == 1:
				self.get_transactions()
			elif index == 2:
				return
	
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
		""" Retrieve transactions from all accounts
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
		if not len(res["accounts"]):
			print("No accounts linked yet! Add a connection first.")

