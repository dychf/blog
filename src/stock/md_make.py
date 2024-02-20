
import datetime
import os 
from core import valuation

dirs = 'docs/公司估值/'  

if not os.path.exists(dirs):
    os.makedirs(dirs)

# 获取当前日期
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

# 创建Markdown文件的名称（例如：2023-04-01.md）
filename = f"{dirs}{current_time}.md"

# Markdown表格的标题和头部
table_header = f"""
# Report {current_time}
Date: {current_time}


"""


df= valuation("000333", 17)
table_rows=df.to_markdown()

# 合并表格头部和行内容
table_content = table_header + table_rows

# 创建并写入Markdown文件
with open(filename, 'w', encoding='utf-8') as md_file:
    md_file.write(table_content)

print(f"Markdown file '{filename}' has been created with a table inside.")
