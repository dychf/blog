import datetime
import os
from .stock import Stock
from .util import encoded_url
import re

file_dir = "../docs/公司估值/"

init_md = """
# name

`更新时间：time`

* 代码：code
* 简介：introduction

### 利润

<img src="netprofits_url" style="width: 400px; height: auto;">

### 估值

|    日期    |    价格    |    买入    |    卖出    |    年报期    |    
|:---------:|:---------:|:---------:|:---------:|:---------:|
"""


chart_url_temp = 'https://quickchart.io/chart?c={{"type": "line", "data": {{"labels": {labels}, "datasets": [{{"label": "归母净利润", "data": {data}}}]}}}}'

table_split = "|:---------:|:---------:|:---------:|:---------:|:---------:|"
table_row_temp = "|{}|{}|{}|{}|{}|"


def add_row(date, md, stock):
    if md.count(date) > 1:
        return md
    row = (
        table_split
        + " \n "
        + table_row_temp.format(
            date,
            stock.market_price,
            stock.ideal_buy,
            stock.ideal_sell,
            stock.period[0] + "--" + stock.period[-1],
        )
    )
    return md.replace(table_split, row)


def create_md(stock_code):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock_info = Stock(stock_code).valuation(17)

    file_path = "{}{}.md".format(file_dir, stock_info.name)

    chart_url = chart_url_temp.format(
        labels=stock_info.period, data=stock_info.netprofits
    )
    chart_url = encoded_url(chart_url)
    if not os.path.exists(file_path):
        md = init_md.replace("name", stock_info.name)
        md = md.replace("time", current_time)
        md = md.replace("code", stock_info.code)
        md = md.replace("introduction", stock_info.name)
        md = md.replace("netprofits_url", chart_url)
    else:
        with open(file_path, "r", encoding="utf-8") as md_file:
            md = md_file.read()
        update_time_pattern = r"更新时间：\s*(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})"
        md = re.sub(update_time_pattern, "更新时间：{}".format(current_time), md)

        md = re.sub(r'src="[^"]+"', 'src="{}"'.format(chart_url), md)

    md = add_row(current_date, md, stock_info)
    with open(file_path, "w", encoding="utf-8") as md_file:
        md_file.write(md)
