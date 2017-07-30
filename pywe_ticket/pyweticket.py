# -*- coding: utf-8 -*-

import time

from pywe_base import BaseWechat
from pywe_exception import WeChatException
from pywe_storage import MemoryStorage
from pywe_token import access_token


class Ticket(BaseWechat):
    def __init__(self, appid=None, secret=None, type='jsapi', storage=None):
        # 微信JS-SDK说明文档, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141115
        super(Ticket, self).__init__()
        self.WECHAT_TICKET = self.API_DOMAIN + '/cgi-bin/ticket/getticket?access_token={access_token}&type={type}'
        self.appid = appid
        self.secret = secret
        self.storage = storage or MemoryStorage()
        self.type = type
        self.tickets = {}
        self.expires_at = None

    @property
    def ticket_info_key(self):
        return '{0}:{1}:ticket:info'.format(self.appid, self.type)

    def __about_to_expires(self, expires_at):
        return expires_at and expires_at - int(time.time()) < 60

    def __fetch_ticket(self, appid=None, secret=None, token=None, type=None, storage=None):
        storage = storage or self.storage
        ticket_info = self.get(self.WECHAT_TICKET, access_token=token or access_token(appid or self.appid, secret or self.secret, storage=storage), type=type)
        if 'expires_in' not in ticket_info:
            raise WeChatException(ticket_info)
        self.tickets[type] = ticket_info.get('ticket')
        expires_in = ticket_info.get('expires_in')
        self.expires_at = int(time.time()) + expires_in
        if storage:
            ticket_info['expires_at'] = self.expires_at
            storage.set(self.ticket_info_key, ticket_info, expires_in)
        return self.tickets.get(type, '')

    def ticket(self, appid=None, secret=None, token=None, type='jsapi', storage=None):
        if self.tickets.get(type, '') and not self.__about_to_expires(self.expires_at):
            return self.tickets.get(type, '')
        # Init appid/secret/storage/type
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.storage = storage or self.storage
        self.type = type or self.type
        # Fetch ticket_info
        ticket_info = self.storage.get(self.ticket_info_key)
        if ticket_info:
            ticket = ticket_info.get('ticket')
            if ticket and not self.__about_to_expires(ticket_info.get('expires_at')):
                return ticket
        return self.__fetch_ticket(appid, secret, token, type, storage)

    def api_ticket(self, appid=None, secret=None, token=None, storage=None):
        """ 卡券 api_ticket """
        return self.ticket(appid, secret, token, 'wx_card', storage)

    def jsapi_ticket(self, appid=None, secret=None, token=None, storage=None):
        return self.ticket(appid, secret, token, 'jsapi', storage)

    def refresh_ticket(self, appid=None, secret=None, token=None, type='jsapi', storage=None):
        return self.__fetch_ticket(appid, secret, token, type, storage)


ticketcls = Ticket()
ticket = ticketcls.ticket
api_ticket = ticketcls.api_ticket
jsapi_ticket = ticketcls.jsapi_ticket
refresh_ticket = ticketcls.refresh_ticket
