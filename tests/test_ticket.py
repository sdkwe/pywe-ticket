# -*- coding: utf-8 -*-

import redis_extensions as redis
from pywe_storage import RedisStorage
from pywe_ticket import ticket as com_ticket
from pywe_ticket import Ticket, api_ticket, jsapi_ticket

from local_wecfg_example import WECHAT


class TestTicketCommands(object):

    def test_ticket_mem(self):
        appid = WECHAT.get('JSAPI', {}).get('appID')
        appsecret = WECHAT.get('JSAPI', {}).get('appsecret')

        ticket = Ticket(appid=appid, secret=appsecret)
        ticket1 = ticket.ticket()
        assert isinstance(ticket1, basestring)

        ticket2 = ticket.api_ticket()
        assert isinstance(ticket2, basestring)

        ticket3 = ticket.jsapi_ticket()
        assert isinstance(ticket3, basestring)

        assert ticket1 == ticket3 != ticket2

        ticket4 = com_ticket(appid=appid, secret=appsecret)
        assert isinstance(ticket4, basestring)

        ticket5 = api_ticket(appid=appid, secret=appsecret)
        assert isinstance(ticket5, basestring)

        ticket6 = jsapi_ticket(appid=appid, secret=appsecret)
        assert isinstance(ticket6, basestring)

        assert ticket4 == ticket6 != ticket5

    def test_ticket_redis(self):
        appid = WECHAT.get('JSAPI', {}).get('appID')
        appsecret = WECHAT.get('JSAPI', {}).get('appsecret')

        r = redis.StrictRedisExtensions(host='localhost', port=6379, db=0)
        storage = RedisStorage(r)

        ticket = Ticket(appid=appid, secret=appsecret, storage=storage)
        ticket1 = ticket.ticket()
        assert isinstance(ticket1, basestring)

        ticket2 = ticket.api_ticket()
        assert isinstance(ticket2, basestring)

        ticket3 = ticket.jsapi_ticket()
        assert isinstance(ticket3, basestring)

        assert ticket1 == ticket3 != ticket2

        ticket4 = com_ticket(appid=appid, secret=appsecret)
        assert isinstance(ticket4, basestring)

        ticket5 = api_ticket(appid=appid, secret=appsecret)
        assert isinstance(ticket5, basestring)

        ticket6 = jsapi_ticket(appid=appid, secret=appsecret)
        assert isinstance(ticket6, basestring)

        assert ticket4 == ticket6 != ticket5
