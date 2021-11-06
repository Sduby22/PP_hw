from logging import getLogger
from src.RunPy import getInstance
from src.ConfigLoader import *

logger = getLogger('Runtime')

class Runtime:
    def __init__(self, config='./config.yaml'):
        logger.info("Initializing runtime")
        self._configLoader = ConfigLoader()
        self._configLoader.load(config)
        logger.debug(f"[Runtime] config is {self.getConfig()}")
        self._runpy = getInstance()
        self._runpy.init(self._configLoader)
        pass

    def handleCall(self, number):
        logger.info(f'Incoming call {number}')
        pass    

    def getConfig(self):
        return self._configLoader.getRuntimeConfig()
