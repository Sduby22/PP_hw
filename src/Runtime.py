from logging import getLogger

logger = getLogger('Runtime')

class Runtime:
    def __init__(self,config_loader):
        self.configLoader = config_loader
        logger.info("[Runtime] Initializing runtime")
        logger.debug(f"[Runtime] config is {self.getConfig()}")
        pass

    def start(self, number):
        logger.info(f'[Runtime] Incoming call {number}')
        pass    

    def getConfig(self):
        return self.configLoader.getRuntimeConfig()
