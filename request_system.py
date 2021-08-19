from config import BASE_URL
import requests
import os
from rich import print

class Request:

	if "DEBUG" in os.environ:
		debug = True
	else:
		debug = False

	def __init__(self, method, url, headers = {}, json = {}):
		self.method = method
		self.url = BASE_URL + url
		self.headers = headers
		self.json = json
	
	def call(self):
		if Request.debug:
			self.print()
		res = getattr(requests, self.method)(self.url, headers=self.headers, json=self.json)
		json = res.json()
		if Request.debug:
			print("Result:")
			print(json)
		return json

	def print(self):
		print(self.method.upper() + " " + self.url)
		print("Headers")
		print(self.headers)
		print("JSON")
		print(self.json)

