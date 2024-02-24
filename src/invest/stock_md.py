import datetime
import os
from .stock import Stock
from .util import encoded_url
import re

file_dir = "../docs/公司估值/"

init_md = """
# name

`更新时间：time`

### 基本信息

* 代码：code
* 所属行业：industry
* 主营业务：main_business

### 利润趋势

<img src="netprofits_url" style="width: 400px; height: auto;">

### 机构预测

* 当前价：current_price
* 目标均价：avg_price
* 最高目标价：max_price
* 最低目标价：min_price

### 估值

|    日期    |    价格    |    买入    |    卖出    |    行业平均PE    |    年报期    |    
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
"""


chart_url_temp = 'https://quickchart.io/chart?c={{"type": "line", "data": {{"labels": {labels}, "datasets": [{{"label": "归母净利润", "data": {data}}}]}}}}'

table_split = (
    "|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|"
)
table_row_temp = "|{}|{}|{}|{}|{}|{}|"


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
            stock.industry_mean_pe,
            stock.period[0] + "—" + stock.period[-1],
        )
    )
    return md.replace(table_split, row)


def create_md(stock_code):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock_info = Stock(stock_code).valuation()

    file_path = "{}{}.md".format(file_dir, stock_info.name)

    chart_url = chart_url_temp.format(
        labels=stock_info.period, data=stock_info.netprofits
    )
    chart_url = encoded_url(chart_url)
    if not os.path.exists(file_path):
        md = init_md.replace("name", stock_info.name)
        md = md.replace("time", current_time)
        md = md.replace("code", stock_info.code)
        md = md.replace("industry", stock_info.industry)
        md = md.replace("main_business", stock_info.main_business)
        md = md.replace("netprofits_url", chart_url)
        md = md.replace("current_price", str(stock_info.market_price))
        md = md.replace("avg_price", str(stock_info.avg_price))
        md = md.replace("max_price", str(stock_info.max_price))
        md = md.replace("min_price", str(stock_info.min_price))
    else:
        with open(file_path, "r", encoding="utf-8") as md_file:
            md = md_file.read()

        # 替换更新时间
        update_time_pattern = r"\s*(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})"
        md = re.sub(update_time_pattern, current_time, md)

        # 替换利润趋势url
        md = re.sub(r'src="[^"]+"', 'src="{}"'.format(chart_url), md)

        # 替换机构预测
        md = re.sub(
            r"当前价：\d+\.\d+", r"当前价：{}".format(stock_info.market_price), md
        )
        md = re.sub(
            r"目标均价：\d+\.\d+", r"目标均价：{}".format(stock_info.avg_price), md
        )
        md = re.sub(
            r"最高目标价：\d+\.\d+", r"最高目标价：{}".format(stock_info.max_price), md
        )
        md = re.sub(
            r"最低目标价：\d+\.\d+", r"最低目标价：{}".format(stock_info.min_price), md
        )

    md = add_row(current_date, md, stock_info)
    with open(file_path, "w", encoding="utf-8") as md_file:
        md_file.write(md)
