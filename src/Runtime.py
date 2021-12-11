from logging import getLogger
from .RunPy import getInstance
from . import ConfigLoader

logger = getLogger('Runtime')

class Runtime:
    def __init__(self, config='./config.yaml'):
        logger.info("Initializing runtime")
        self._configLoader = ConfigLoader()
        self._configLoader.load(config)
        logger.debug(f"[Runtime] config is {self.getConfig()}")
        self._runpy = getInstance()
        self._runpy.init(self._configLoader)
        self._variables = {
                '_input': '',
                '_input_number': '',
                '_number': '',
                '_input': '',
                '_ret': '',
            }
        pass

    def handleCall(self, number):
        logger.info(f'Incoming call {number}')
        self._variables['number'] = number

    def speak(self, str):
        print(f'<<< {str}')

    def wait(self, time):
        print(f'Waiting {time} milliseconds for user input...')
        input('>>> ')

    def getConfig(self):
        return self._configLoader.getRuntimeConfig()

    def hangup(self):
        pass	
