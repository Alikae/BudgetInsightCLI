from utils import input_option
from request_system import Request
from rich import print

class Wealth:

	def __init__(self, auth_system):
		self.auth_system = auth_system
	
	def run(self):
		while True:
			index = input_option(
				"What do you want to do ?",
				[
					"See my investments",
					"See my history",
					"Back",
				],
			)
			if index == 0:
				self.get_investments()
			elif index == 1:
				self.get_history()
			elif index == 2:
				return

	def get_investments(self):
		res = Request(
			"get",
			f"/users/{self.auth_system.user['id']}/investments",
			self.auth_system.init_request_header(),
		).call()
		if not handle_connection_state_errors(res):
			return
		print("Total:", res["valuation"], "(", res["diff_percent"], "%)")
		for investment in res["investments"]:
			print("\t", investment["label"], "(", investment["id"], ")")
			print("\t\t", investment["valuation"], "(", investment["diff_percent"], "%)")

	def get_history(self):
		while True:
			res = input("Give an investment ID (0 to quit)")
			try:
				res = int(res)
				if res == 0:
					return
				investment_id = res
				break
			except ValueError:
				print("enter a number please")
		res = Request(
			"get",
			f"/users/{self.auth_system.user['id']}/investments/{investment_id}/history",
			self.auth_system.init_request_header(),
		).call()
		for history in res["investmentvalues"]:
			print(history["vdate"], "(", history["unitvalue"], ")")
		if len(res["investmentvalues"] == 0):
			print("No History")


def handle_connection_state_errors(res):
	if "code" in res:
		if res["code"] == "noAccount":
			print("Link an account first.")
			return False
	return True
