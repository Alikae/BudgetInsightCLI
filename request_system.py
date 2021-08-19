from config import BASE_URL
import requests

class Request:

	def __init__(self, method, url, headers = {}, json = {}):
		self.method = method
		self.url = BASE_URL + url
		self.headers = headers
		self.json = json
	
	def call(self):
		res = getattr(requests, self.method)(self.url, headers=self.headers, json=self.json)
		return res.json()
