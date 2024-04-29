from invest.stock_md import create_md
import os
import sys
import yaml

os.chdir(sys.path[0])

with open("config.yaml", "r", encoding='utf-8') as file:
    config = yaml.safe_load(file)


if __name__ == "__main__":

    for s_info in config["stock_codes"]:
        try:
            create_md(s_info["code"])
        except:
            continue
