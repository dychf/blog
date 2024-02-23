import datetime
import os
from .stock import Stock
from .util import encoded_url

header_temp = """
更新时间: {}
### {}
* 代码：{}
* 简介：{}
"""

chart_url_temp = 'https://quickchart.io/chart?c={{"type": "line", "data": {{"labels": {labels}, "datasets": [{{"label": "归母净利润", "data": {data}}}]}}}}'
netprofit_line_temp = """
### 利润曲线

<img src="{}" style="width: 400px; height: auto;">
"""


table_head_temp = """
### 估值

|    日期    |    价格    |    买入    |    卖出    |    
|:------------:|:------------:|:------------:|:------------:|"""

table_row_temp = """
|{}|{}|{}|{}|
"""


def create_md(stock_code):
    dirs = "../docs/公司估值/"
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stock_info = Stock(stock_code).valuation(17)

    filename = "{}{}.md".format(dirs, stock_info.name)
    header = header_temp.format(current_time, stock_info.name, stock_info.code, stock_info.name)
    chart_url = chart_url_temp.format(
        labels=["21", "22", "23"], data=stock_info.netprofits
    )
    netprofit_line = netprofit_line_temp.format(encoded_url(chart_url))
    table_row = table_row_temp.format(
        current_date,
        stock_info.market_price,
        stock_info.ideal_buy,
        stock_info.ideal_sell,
    )

    with open(filename, "w", encoding="utf-8") as md_file:
        md_file.write(header)
        md_file.write(netprofit_line)
        md_file.write(table_head_temp)
        md_file.write(table_row)
