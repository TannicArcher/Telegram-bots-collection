# -*- coding: utf-8 -*-
import inspect
import json

from .activations import SmsActivation
from .errors import error_handler
from .models import ActionsModel, ActionsModel2
from .services import SmsService, ServiceStorage


class GetBalance(ActionsModel):
	_name = 'getBalance'

	def __init__(self):
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response):
		return float(response.split(':')[1])

	def request(self, wrapper):
		"""
		:rtype: int
		"""
		response = wrapper.request(self)
		return self.__response_processing(response)


class GetFreeSlots(ActionsModel):
	_name = 'getNumbersStatus'

	def __init__(self, country=None, operator=None):
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response):
		service_list = json.loads(response)

		service_obj = SmsService()
		for name, short_name in ServiceStorage.names.items():
			getattr(service_obj, name).count = int(service_list[short_name])
			getattr(service_obj, name).count = int(service_list[short_name])
			getattr(service_obj, name).priceMap = None
			getattr(service_obj, name).prices = None
			getattr(service_obj, name).quantities = None
			getattr(service_obj, name).minPrice = (None, None)
			getattr(service_obj, name).maxPrice = (None, None)
			getattr(service_obj, name).work = None
		return service_obj

	def request(self, wrapper):
		"""
		:rtype: smshuborg.services.SmsService
		"""
		response = wrapper.request(self)
		return self.__response_processing(response)


class GetFreeSlotsAndPrices(ActionsModel):
	_name = 'getNumbersStatusAndCostHubFree'

	def __init__(self):
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response):
		service_list = json.loads(response)

		service_obj = SmsService()
		for name, short_name in ServiceStorage.names.items():
			short_name = short_name[:-2]
			prices_dict = service_list[short_name]['priceMap']
			getattr(service_obj, name).priceMap = prices_dict

			quantities = list(map(int, list(prices_dict.values())))
			getattr(service_obj, name).quantities = quantities

			prices = list(map(float, list(prices_dict.keys())))
			getattr(service_obj, name).prices = prices
			if len(prices) != 0:
				getattr(service_obj, name).minPrice = (prices[0], quantities[0])
				getattr(service_obj, name).maxPrice = (prices[-1], quantities[-1])
			else:
				getattr(service_obj, name).minPrice = 0
				getattr(service_obj, name).maxPrice = 0

			getattr(service_obj, name).count = int(service_list[short_name]['totalQuantity'])
			getattr(service_obj, name).work = int(service_list[short_name]['work'])
		return service_obj

	def request(self, wrapper):
		"""
		:rtype: smshuborg.services.SmsService
		"""
		response = wrapper.request(self)
		return self.__response_processing(response)


class GetNumber(ActionsModel):
	_name = 'getNumber'

	def __init__(self, service, country=None, operator=None, forward=False, ref=None):
		service = service
		forward = int(forward)
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response, wrapper):
		data = response.split(':')
		return SmsActivation(data[1], data[2], wrapper)

	def request(self, wrapper):
		"""
		:rtype: smshuborg.activations.SmsActivation
		"""
		response = wrapper.request(self)
		return self.__response_processing(response, wrapper=wrapper)


class GetStatus(ActionsModel):
	_name = 'getStatus'

	def __init__(self, id):
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response):
		data = {'status': response, 'code': None}
		if ':' in response:
			data['status'] = response.split(':', 1)[0]
			data['code'] = response.split(':', 1)[1]
		return data

	def request(self, wrapper):
		"""
		:rtype: dict
		"""
		response = wrapper.request(self)
		return self.__response_processing(response)


class SetStatus(ActionsModel):
	_name = 'setStatus'

	def __init__(self, id, status, forward=False):
		forward = int(forward)
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response):
		data = {'status': response}
		return data

	def request(self, wrapper):
		"""
		:rtype: dict
		"""
		response = wrapper.request(self)
		return self.__response_processing(response)


class ChangeCountry(ActionsModel2):
	_name = 'countryChange'

	def __init__(self, country):
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response):
		data = json.loads(response)
		return data

	def request(self, wrapper):
		"""
		:rtype: int
		"""
		response = wrapper.request2(self)
		return self.__response_processing(response)


class ChangeOperator(ActionsModel2):
	_name = 'operatorChange'

	def __init__(self, country, operator):
		super().__init__(inspect.currentframe())

	@error_handler
	def __response_processing(self, response):
		data = json.loads(response)
		return data

	def request(self, wrapper):
		"""
		:rtype: int
		"""
		response = wrapper.request2(self)
		return self.__response_processing(response)
