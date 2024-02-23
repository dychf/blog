from invest.stock_md import create_md
import os
import sys
import yaml

os.chdir(sys.path[0])


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


if __name__ == "__main__":

    create_md(config["stock_codes"])
