from request_system import Request
from getpass import getpass
import sys
import re

def input_option(prompt, options):
	print("\n" + prompt)
	option = ""
	i = 0
	for option in options:
		print(i, ")", option)
		i += 1
	while True:
		try:
			res = input()
			if res == "":
				res = 0
			option = int(res)
			if option < len(options):
				return option
		except ValueError:
			pass
		print("Choose a valid option")

def get_connectors_with_capability(capability):
	print("Loading connectors...")
	res = Request(
		"get",
		"/connectors",
	).call()
	connectors = {}
	for connector in res["connectors"]:
		print("\t\t", connector["name"])
		print(connector["capabilities"])
		if capability in connector["capabilities"]:
			connectors[connector["name"]] = connector
	return connectors

def get_connector_fields(connector_id):
	res = Request(
		"get",
		f"/connectors/{connector_id}/fields",
	).call()
	return res["fields"]

def fill_fields(fields):
	filled_fields = {}
	for field in fields:
		while True:
			label = field["label"] + ": "
			if field["type"] == "text":
				res = input(label)
			elif field["type"] == "password":
				res = getpass(label)
			elif field["type"] == "list":
				choices = [v["label"] for v in field["values"]]
				if not field["required"]:
					choices.append("Nothing")
				index = input_option(label, choices)
				if index == len(field["values"]):
					res = ""
				else:
					res = field["values"][index]["value"]
			else:
				print("Unsupported field type:", field["type"])
				sys.exit()
			if (field == "" and not field["required"]) or not field["regex"] or re.match(field["regex"], res):
				filled_fields[field["name"]] = res
				break
			print("Please enter a valid", field["label"])
	return filled_fields

