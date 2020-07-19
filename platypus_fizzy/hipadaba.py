import asyncio
import xml.etree.ElementTree as ET
from platypus_fizzy.config import sics_config


class Hipadaba(object):

    def __init__(self):
        # StreamReader/Writer
        self.reader = None
        self.writer = None

        self.ip = sics_config["ip"]
        self.port = sics_config["port"]

    def obtain_tree(self):
        # download the entire hipadaba tree
        pass

    def communicate(self):
        pass
