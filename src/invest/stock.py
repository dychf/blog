import json
import jsonpath
import requests
import numpy as np
from .config import cookies, url, headers
from .util import price, round_float_attributes
import attr


@round_float_attributes
@attr.s
class StockInfo:
    name: str = attr.ib("")
    code: str = attr.ib("")
    total_share_capital: float = attr.ib(0)
    netprofits: list[float] = attr.ib(factory=list)
    netprofit_1: float = attr.ib(0)
    netprofit_3: float = attr.ib(0)
    growthrates: list[float] = attr.ib(factory=list)
    growthrate_1: float = attr.ib(0)
    PE: float = attr.ib(0)
    capitalization: float = attr.ib(0)
    market_price: float = attr.ib(0)
    valuation: float = attr.ib(0)
    valuation_price: float = attr.ib(0)
    ideal_buy_v: float = attr.ib(0)
    ideal_sell_v: float = attr.ib(0)
    ideal_buy: float = attr.ib(0)
    ideal_sell: float = attr.ib(0)


class Stock:

    def __init__(self, code):
        self.code = code
        self._get_data()

    def _get_data(self):
        params = {
            "openapi": "1",
            "dspName": "iphone",
            "tn": "tangram",
            "client": "app",
            "query": self.code,
            "code": self.code,
            "word": self.code,
            "resource_id": "5429",
            "ma_ver": "4",
            "finClientType": "pc",
        }
        response = requests.get(
            url, params=params, cookies=cookies, headers=headers
        ).text
        # with open("data.json", "w", encoding="utf-8") as f:
        #     f.write(bytes(response, 'utf-8').decode('unicode_escape'))

        jsonobj = json.loads(response)

        # 名称
        name = jsonpath.jsonpath(
            jsonobj, "$.Result[1].DisplayData.resultData.tplData.result.name"
        )
        # 当前价格
        currentPrice = jsonpath.jsonpath(
            jsonobj,
            "$.Result[1].DisplayData.resultData.tplData.result.minute_data.pankouinfos.origin_pankou.currentPrice",
        )
        # 总股本
        totalShareCapital = jsonpath.jsonpath(
            jsonobj,
            "$..Result[1].DisplayData.resultData.tplData.result.minute_data.pankouinfos.origin_pankou.totalShareCapital",
        )
        # 当前市值
        capitalization = jsonpath.jsonpath(
            jsonobj,
            "$..Result[1].DisplayData.resultData.tplData.result.minute_data.pankouinfos.origin_pankou.capitalization",
        )
        # 年报数据
        FY = jsonpath.jsonpath(
            jsonobj,
            "$.Result[3].DisplayData.resultData.tplData.result.tabs[4].content.profitSheetV2.chartInfo[4].body",
        )
        FY = np.asarray(FY)

        self.name = name[0]  # 名称
        self.market_price = float(currentPrice[0])  # 当前价格
        self.total_share_capital = round(float(totalShareCapital[0]) / 1e8, 2)  # 总股本
        self.capitalization = round(float(capitalization[0]) / 1e8, 2)  # 当前市值
        self.netprofits = FY[0, -3:, 7]  # 近三年归母净利润
        self.growthrates = FY[0, -3:, 8]  # 近三年归母净利润增长率

    def valuation(self, PE):

        netprofit_1 = np.average(
            [float(p) for p in self.netprofits], weights=[0.2, 0.3, 0.5]
        )

        growthrate_1 = np.average(
            [float(rate) for rate in self.growthrates], weights=[0.2, 0.3, 0.5]
        )

        netprofit_3 = netprofit_1 * (1 + growthrate_1 * 0.01) ** 3  # 估算三年后利润
        valuation = netprofit_3 * PE  # 估值
        ideal_buy_v = valuation / 2  # 理想买点
        ideal_sell_v = min(valuation * 1.5, netprofit_1 * 50)  # 理想卖点

        return StockInfo(
            name=self.name,
            code=self.code,
            total_share_capital=self.total_share_capital,
            netprofits=self.netprofits,
            growthrates=self.growthrates,
            netprofit_1=netprofit_1,
            netprofit_3=netprofit_3,
            growthrate_1=growthrate_1,
            PE=PE,
            capitalization=self.capitalization,
            market_price=self.market_price,
            valuation=valuation,
            valuation_price=price(valuation, self.total_share_capital),
            ideal_buy_v=ideal_buy_v,
            ideal_sell_v=ideal_sell_v,
            ideal_buy=price(ideal_buy_v, self.total_share_capital),
            ideal_sell=price(ideal_sell_v, self.total_share_capital),
        )
