import yaml
import os
from datetime import date

# 读取配置
config_path = os.getenv("CONFIG_PATH", "config.yaml")
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

print(str(config["reservation"]["data"]))




