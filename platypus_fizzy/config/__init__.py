import configparser
import os


config = configparser.ConfigParser()
dae_config = {}
sics_config = {}

# read config file
config.read([".platypus.cfg", os.path.expanduser("~/.platypus.cfg")])


# setup DAE
dae_config["ip"] = config["DAE"]["ip"]
dae_config["port"] = config["DAE"]["port"]
dae_config["user"] = config["DAE"]["user"]
dae_config["password"] = config["DAE"]["password"]


# setup SICS
sics_config["ip"] = config["SICS"]["ip"]
sics_config["port"] = config["SICS"]["port"]
sics_config["user"] = config["SICS"]["user"]
sics_config["password"] = config["SICS"]["password"]
