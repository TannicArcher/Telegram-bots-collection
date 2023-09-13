# -*- coding: utf-8 -*-
from .models import ServiceModel
from .helper import object_factory


class ServiceStorage:
	# names = {
	# 	'Vkontakte': 'vk_0', 'Odnoklassniki': 'ok_0', 'Whatsapp': 'wa_0', 'Viber': 'vi_0', 'Telegram': 'tg_0',
	# 	'WeChat': 'wb_0', 'Google': 'go_0', 'Avito': 'av_0', 'AvitoSmsForwarding': 'av_1', 'Facebook': 'fb_0',
	# 	'Twitter': 'tw_0', 'AnyOther': 'ot_0', 'AnyOtherSmsForwarding': 'ot_1', 'Uber': 'ub_0', 'Qiwi': 'qw_0',
	# 	'GettTaxi': 'gt_0', 'OlX': 'sn_0', 'Instagram': 'ig_0', 'Lukoil': 'ss_0', 'Youla': 'ym_0',
	# 	'YoulaSmsForwarding': 'ym_1', 'MailRu': 'ma_0', 'Microsoft': 'mm_0', 'AirBnb': 'uk_0',
	# 	'LineMessenger': 'me_0', 'Yahoo': 'mb_0', 'DrugVokrug': 'we_0', 'Pyaterochka': 'bd_0', 'HQTrivia': 'kp_0',
	# 	'DeliveryClub': 'dt_0', 'Yandex': 'ya_0', 'YandexSmsForwarding': 'ya_1', 'Steam': 'mt_0', 'Tinder': 'oi_0',
	# 	'MeetMe': 'fd_0', 'Mamba': 'fd_0', 'Dent': 'zz_0', 'KakaoTalk': 'kt_0', 'AOL': 'pm_0', 'LinkedIN': 'tn_0'}
	names = {
		'Vkontakte': 'vk_0', 'Odnoklassniki': 'ok_0', 'Whatsapp': 'wa_0', 'Viber': 'vi_0', 'Telegram': 'tg_0',
		'WeChat': 'wb_0', 'Google': 'go_0', 'Avito': 'av_0', 'Facebook': 'fb_0', 'Twitter': 'tw_0', 'AnyOther': 'ot_0',
		'Uber': 'ub_0', 'Qiwi': 'qw_0', 'GettTaxi': 'gt_0', 'OlX': 'sn_0', 'Instagram': 'ig_0', 'Lukoil': 'ss_0',
		'Youla': 'ym_0', 'MailRu': 'ma_0', 'Microsoft': 'mm_0', 'AirBnb': 'uk_0', 'LineMessenger': 'me_0',
		'Yahoo': 'mb_0', 'DrugVokrug': 'we_0', 'Pyaterochka': 'bd_0', 'HQTrivia': 'kp_0', 'DeliveryClub': 'dt_0',
		'Yandex': 'ya_0', 'Steam': 'mt_0', 'Tinder': 'oi_0', 'Mamba': 'fd_0', 'Dent': 'zz_0', 'KakaoTalk': 'kt_0',
		'AOL': 'pm_0', 'LinkedIN': 'tn_0', 'Wildberries': 'uu_0', 'BlaBlaCar': 'ua_0', 'Ozon': 'ua_0',
		'PayPal': 'ts_0','Amazon': 'am_0','DROM': 'hz_0','mvideo': 'tk_0','kufar': 'kb_0',}


class SmsService:
	def __init__(self):
		for name, short_name in ServiceStorage.names.items():
			object = object_factory(
				name,
				base_class=ServiceModel,
				argnames=['__service_short_name', '__count_slot', '__service_price_map', '__service_prices',
				          '__service_quantities', '__service_min_price', '__service_max_price', '__service_is_work']
			)(__service_short_name=short_name, __count_slot=0, __service_price_map=None, __service_prices=None,
			  __service_quantities=None, __service_min_price=0, __service_max_price=0, __service_is_work=False)
			setattr(self, '_' + name, object)

	@property
	def kufar(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self.kufar

	@property
	def mvideo(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self.mvideo

	@property
	def DROM(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self.DROM

	@property
	def Amazon(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self.Amazon

	@property
	def PayPal(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self.PayPal


	@property
	def Ozon(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self.ozon

	@property
	def BlaBlaCar(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self.BlaBlaCar

	@property
	def Wildberries(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Wildberries

	@property
	def Vkontakte(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Vkontakte

	@property
	def Odnoklassniki(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Odnoklassniki

	@property
	def Whatsapp(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Whatsapp

	@property
	def Viber(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Viber

	@property
	def Telegram(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Telegram

	@property
	def WeChat(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._WeChat

	@property
	def Google(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Google

	@property
	def Avito(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Avito
	#
	# @property
	# def AvitoSmsForwarding(self):
	# 	"""
	# 	:rtype: smshuborg.models.ServiceModel
	# 	"""
	# 	return self._AvitoSmsForwarding

	@property
	def Facebook(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Facebook

	@property
	def Twitter(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Twitter

	@property
	def AnyOther(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._AnyOther
	#
	# @property
	# def AnyOtherSmsForwarding(self):
	# 	"""
	# 	:rtype: smshuborg.models.ServiceModel
	# 	"""
	# 	return self._AnyOtherSmsForwarding

	@property
	def Uber(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Uber

	@property
	def Qiwi(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Qiwi

	@property
	def GettTaxi(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._GettTaxi

	@property
	def OlX(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._OlX

	@property
	def Instagram(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Instagram

	@property
	def Lukoil(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Lukoil

	@property
	def Youla(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Youla
	#
	# @property
	# def YoulaSmsForwarding(self):
	# 	"""
	# 	:rtype: smshuborg.models.ServiceModel
	# 	"""
	# 	return self._YoulaSmsForwarding

	@property
	def MailRu(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._MailRu

	@property
	def Microsoft(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Microsoft

	@property
	def AirBnb(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._AirBnb

	@property
	def LineMessenger(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._LineMessenger

	@property
	def Yahoo(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Yahoo

	@property
	def DrugVokrug(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._DrugVokrug

	@property
	def Pyaterochka(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Pyaterochka

	@property
	def HQTrivia(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._HQTrivia

	@property
	def DeliveryClub(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._DeliveryClub

	@property
	def Yandex(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Yandex
	#
	# @property
	# def YandexSmsForwarding(self):
	# 	"""
	# 	:rtype: smshuborg.models.ServiceModel
	# 	"""
	# 	return self._YandexSmsForwarding

	@property
	def Steam(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Steam

	@property
	def Tinder(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Tinder
	#
	# @property
	# def MeetMe(self):
	# 	"""
	# 	:rtype: smshuborg.models.ServiceModel
	# 	"""
	# 	return self._MeetMe

	@property
	def Mamba(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Mamba

	@property
	def Dent(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._Dent

	@property
	def KakaoTalk(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._KakaoTalk

	@property
	def AOL(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._AOL

	@property
	def LinkedIN(self):
		"""
		:rtype: smshuborg.models.ServiceModel
		"""
		return self._LinkedIN
