#!/usr/bin python3

from os import getenv
from os.path import exists
from sys import exit

location = getenv("URL_LOCATION", "")
runtime_conf_path = getenv("_NGINX_RUNTIME_CONF")

if runtime_conf_path is None or not exists(runtime_conf_path):
    exit(0)


with open(runtime_conf_path, 'r') as fp:
    config = fp.read()


config = config.replace("${URL_LOCATION}", location)

with open(runtime_conf_path, 'w') as fp:
    print(config, file=fp)
