
import datetime

# 获取当前日期
current_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 创建Markdown文件的名称（例如：2023-04-01.md）
filename = f"md/{current_date_time}.md"

# 任务列表数据，每个任务都是一个字典
tasks = [
    {"name": "Task 1", "description": "Task 1 Description", "status": "✅"},
    {"name": "Task 2", "description": "Task 2 Description", "status": "❌"},
    {"name": "Task 3", "description": "Task 3 Description", "status": "🔜"},
]

# Markdown表格的标题和头部
table_header = """# My Daily Report

Date: {date}

## Tasks Table

| Task | Description | Status |
|------|-------------|--------|
""".format(date=current_date_time)

# 使用for循环生成表格行
table_rows = ""
for task in tasks:
    table_rows += f"| {task['name']} | {task['description']} | {task['status']} |\n"

# 合并表格头部和行内容
table_content = table_header + table_rows

# 创建并写入Markdown文件
with open(filename, 'w') as md_file:
    md_file.write(table_content)

print(f"Markdown file '{filename}' has been created with a table inside.")
