import datetime
import os
from .stock import Stock
from .util import encoded_url
import re

file_dir = "../docs/公司估值/"

header_temp = """
`更新时间：{}`

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
|:------------:|:------------:|:------------:|:------------:|
"""

table_row_temp = "|{}|{}|{}|{}|"


def create_md(stock_code):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock_info = Stock(stock_code).valuation(17)

    file_path = "{}{}.md".format(file_dir, stock_info.name)

    chart_url = chart_url_temp.format(
        labels=["21", "22", "23"], data=stock_info.netprofits
    )
    chart_url = encoded_url(chart_url)
    if not os.path.exists(file_path):
        header = header_temp.format(current_time, stock_info.code, stock_info.name)

        netprofit_line = netprofit_line_temp.format(chart_url)
        table_row = table_row_temp.format(
            current_time,
            stock_info.market_price,
            stock_info.ideal_buy,
            stock_info.ideal_sell,
        )

        with open(file_path, "w", encoding="utf-8") as md_file:
            md_file.write(header)
            md_file.write(netprofit_line)
            md_file.write(table_head_temp)
            md_file.write(table_row)
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            original_text = file.read()
        update_time_pattern = r"更新时间：\s*(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})"
        modified_text = re.sub(
            update_time_pattern, "更新时间：{}".format(current_time), original_text
        )

        url = chart_url_temp.format(
            labels=["22", "23", "24"],
            data=stock_info.netprofits,
        )
        url = encoded_url(url)
        modified_text = re.sub(r'src="[^"]+"', 'src="{}"'.format(url), modified_text)

        new_row = table_row_temp.format(
            current_time,
            stock_info.market_price,
            stock_info.ideal_buy,
            stock_info.ideal_sell,
        )
        modified_text = original_text.replace(
            "|:------------:|:------------:|:------------:|:------------:|",
            "|:------------:|:------------:|:------------:|:------------:|\n" + new_row,
        )
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_text)
