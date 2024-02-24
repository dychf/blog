from urllib.parse import quote
from .config import cookies, url, headers
import requests
import json


def round_float_attributes(cls):
    """
    装饰器，保留两位小数
    """
    init_method = cls.__init__

    def new_init(self, *args, **kwargs):
        init_method(self, *args, **kwargs)
        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, float):
                setattr(self, attr_name, round(attr_value, 2))

    cls.__init__ = new_init

    return cls


def price(market, equity):
    """
    计算股票价格, 股票价格=总市值/总股本
    market: 市值
    equity: 总股本
    """
    return round(market / equity, 2)


def encoded_url(url):
    """
    对url进行编码
    """
    return quote(url, safe=":/?=&")


def request_data(params):
    """
    请求数据
    """
    response = requests.get(url, params=params, cookies=cookies, headers=headers).text
    return json.loads(response)
