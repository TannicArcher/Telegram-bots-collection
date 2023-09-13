# -*- coding: utf-8 -*-
import requests


class Sms:
	def __init__(self, api_key):
		self.key = api_key
		self.url = 'https://smshub.org/stubs/handler_api.php'
		self.url2 = 'https://smshub.org/api.php'

	def request(self, action):
		try:
			params = {**{'api_key': self.key}, **action.data}
			response = requests.get(self.url, params)
			return response.text
		except (ConnectionError, TimeoutError):
			return 'NO_CONNECTION'

	def request2(self, action):
		try:
			data = {
				'cat': 'scripts',
				'act': 'manageActivations',
				**action.data,
				'apikey': self.key
			}
			response = requests.post(self.url2, data=data)
			return response.text
		except (ConnectionError, TimeoutError):
			return 'NO_CONNECTION'

