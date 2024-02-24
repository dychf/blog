import json
import jsonpath

import numpy as np

from .util import price, round_float_attributes, request_data
import attr
from .config import params_common, params_pe


@round_float_attributes
@attr.s
class StockInfo:
    name: str = attr.ib("")
    code: str = attr.ib("")
    total_share_capital: float = attr.ib(0)
    period: list[str] = attr.ib(factory=list)
    netprofits: list[float] = attr.ib(factory=list)
    netprofit_1: float = attr.ib(0)
    netprofit_3: float = attr.ib(0)
    growthrates: list[float] = attr.ib(factory=list)
    growthrate_1: float = attr.ib(0)
    industry_mean_pe: float = attr.ib(0)
    industry: str = attr.ib("")
    main_business: str = attr.ib("")
    capitalization: float = attr.ib(0)
    market_price: float = attr.ib(0)
    valuation: float = attr.ib(0)
    valuation_price: float = attr.ib(0)
    ideal_buy_v: float = attr.ib(0)
    ideal_sell_v: float = attr.ib(0)
    ideal_buy: float = attr.ib(0)
    ideal_sell: float = attr.ib(0)
    avg_price: float = attr.ib(0)
    max_price: float = attr.ib(0)
    min_price: float = attr.ib(0)


class Stock:

    def __init__(self, code):
        self.code = code
        self._get_data()
        self._industry_mean_pe()

    def _get_data(self):
        # params = params_common.format(code=self.code)
        params = {
            key: value.format(code=self.code) for key, value in params_common.items()
        }
        jsonobj = request_data(params)

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
            "$.Result[1].DisplayData.resultData.tplData.result.minute_data.pankouinfos.origin_pankou.totalShareCapital",
        )
        # 当前市值
        capitalization = jsonpath.jsonpath(
            jsonobj,
            "$.Result[1].DisplayData.resultData.tplData.result.minute_data.pankouinfos.origin_pankou.capitalization",
        )

        # 机构预测
        avg_price = jsonpath.jsonpath(
            jsonobj,
            "$.Result[3].DisplayData.resultData.tplData.result.tabs[5].content.newCompany.organRating.avgPrice",
        )
        max_price = jsonpath.jsonpath(
            jsonobj,
            "$.Result[3].DisplayData.resultData.tplData.result.tabs[5].content.newCompany.organRating.maxPrice",
        )
        min_price = jsonpath.jsonpath(
            jsonobj,
            "$.Result[3].DisplayData.resultData.tplData.result.tabs[5].content.newCompany.organRating.minPrice",
        )

        # 年报数据
        FY = jsonpath.jsonpath(
            jsonobj,
            "$.Result[3].DisplayData.resultData.tplData.result.tabs[4].content.profitSheetV2.chartInfo[4].body",
        )
        FY = np.asarray(FY)

        # 所属行业
        industry = jsonpath.jsonpath(
            jsonobj,
            "$.Result[3].DisplayData.resultData.tplData.result.tabs[5].content.companyInfo.issuedBy.industry",
        )

        # 主营业务
        main_business = jsonpath.jsonpath(
            jsonobj,
            "$.Result[3].DisplayData.resultData.tplData.result.tabs[5].content.companyInfo.issuedBy.mainBusiness",
        )

        self.name = name[0]  # 名称
        self.market_price = float(currentPrice[0])  # 当前价格
        self.total_share_capital = float(totalShareCapital[0]) / 1e8  # 总股本
        self.capitalization = float(capitalization[0]) / 1e8  # 当前市值
        self.netprofits = [float(p) for p in FY[0, -3:, 7]]  # 近三年归母净利润
        self.growthrates = FY[0, -3:, 8]  # 近三年归母净利润增长率
        self.period = [str(p) for p in FY[0, -3:, 0]]
        self.avg_price = float(avg_price[0])
        self.max_price = float(max_price[0])
        self.min_price = float(min_price[0])
        self.industry = industry[0]
        self.main_business = main_business[0]

    def _industry_mean_pe(self):
        params = {key: value.format(code=self.code) for key, value in params_pe.items()}
        jsonobj = request_data(params)
        industry_mean_pe = jsonpath.jsonpath(
            jsonobj,
            "$.Result[0].DisplayData.resultData.tplData.result.industryComparison.list[0].industryMean",
        )
        self.industry_mean_pe = float(industry_mean_pe[0])

    def valuation(self):

        netprofit_1 = np.average(self.netprofits, weights=[0.2, 0.3, 0.5])

        growthrate_1 = np.average(
            [float(rate) for rate in self.growthrates], weights=[0.2, 0.3, 0.5]
        )

        netprofit_3 = netprofit_1 * (1 + growthrate_1 * 0.01) ** 3  # 估算三年后利润
        valuation = netprofit_3 * self.industry_mean_pe  # 估值
        ideal_buy_v = valuation / 2  # 理想买点
        ideal_sell_v = min(valuation * 1.5, ideal_buy_v * 1.2)  # 理想卖点

        return StockInfo(
            name=self.name,
            code=self.code,
            period=self.period,
            industry=self.industry,
            total_share_capital=self.total_share_capital,
            netprofits=self.netprofits,
            growthrates=self.growthrates,
            netprofit_1=netprofit_1,
            netprofit_3=netprofit_3,
            growthrate_1=growthrate_1,
            industry_mean_pe=self.industry_mean_pe,
            capitalization=self.capitalization,
            market_price=self.market_price,
            valuation=valuation,
            valuation_price=price(valuation, self.total_share_capital),
            ideal_buy_v=ideal_buy_v,
            ideal_sell_v=ideal_sell_v,
            ideal_buy=price(ideal_buy_v, self.total_share_capital),
            ideal_sell=price(ideal_sell_v, self.total_share_capital),
            avg_price=self.avg_price,
            max_price=self.max_price,
            min_price=self.min_price,
            main_business=self.main_business,
        )
