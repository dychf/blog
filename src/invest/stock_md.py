import datetime
import os
from .stock import Stock


tempalte = """
### {}
* 代码：{}
* PE：{}
* 价格：{}
* 买入点：{}
* 卖出点：{}
"""

def create_md(stock_codes):
    dirs = "../docs/公司估值/"
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = f"{dirs}{current_date}.md"

    header = f"# {current_date} \n 更新时间：{current_time} \n"

    content = ""
    for code in stock_codes:
        stock_info = Stock(code).valuation(17)
        content += tempalte.format(
            stock_info.name,
            stock_info.code,
            stock_info.PE,
            stock_info.market_price,
            stock_info.valuation_price,
            stock_info.ideal_sell,
        )

    with open(filename, "w", encoding="utf-8") as md_file:
        md_file.write(header + content)
