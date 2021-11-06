from logging import getLogger

logger = getLogger('Runtime')

class Runtime:
    def __init__(self,configLoader):
        self._configLoader = configLoader
        logger.info("[Runtime] Initializing runtime")
        logger.debug(f"[Runtime] config is {self.getConfig()}")
        pass

    def start(self, number):
        logger.info(f'[Runtime] Incoming call {number}')
        pass    

    def getConfig(self):
        return self._configLoader.getRuntimeConfig()

