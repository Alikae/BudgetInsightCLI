from auth_system import AuthSystem
from utils import input_option
from bank import Bank
from wealth import Wealth

class App:

	def __init__(self):
		self.auth_system = AuthSystem()
		self.api = None

	def run(self):
		while True:
			# Choose an api to interact with
			apis = ["bank", "wealth", "bill", "Quit"]
			index = input_option(
				"Choose an api: ",
				apis,
			)
			if index == 3:
				return
			self.api = apis[index]
			print("API " + self.api + " :")
			getattr(self, self.api)()

	def bank(self):
		Bank(self.auth_system).run()

	def wealth(self):
		Wealth(self.auth_system).run()

	def bill(self):
		pass

if __name__ == "__main__":
	try:
		App().run()
	except KeyboardInterrupt:
		print("Marvellous day to you. Ciao!")

