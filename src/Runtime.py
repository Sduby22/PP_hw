from logging import getLogger

from .RunPy import getInstance
from . import ConfigLoader

logger = getLogger('Runtime')


class Runtime:

    KEYWORDS = [
        '是',
        '否',
        '话费',
        '投诉',
        '客服',
        '充值',
    ]

    def __init__(self, number, config: ConfigLoader):
        logger.info("Initializing runtime")
        self._conf = config
        self._runpy = getInstance()
        self._runpy.init(self._conf)
        self._variables = {
            '_input': '',
            '_input_keyword': '',
            '_number': number,
            '_ret': '',
        }
        pass

    def getConfig(self):
        return self._conf.getRuntimeConfig()

    def speak(self, str):
        print(f'>>> {str}')

    def wait(self, timeStr):
        print(f'Waiting {timeStr} milliseconds for user input...')
        str = input('<<< ')
        self._variables['_input'] = str
        self._extractKeywords(str)

    def hangup(self):
        logger.info(f"user {self._variables.get('_number')} hung up")
        print('beep')

    def assign(self, var, val):
        self._variables[var] = val
        pass

    def callpy(self, name, *args):
        print('callpy', name, args)
        pass

    def beep(self):
        print('beep')
        pass

    def getvar(self, varname):
        if varname not in self._variables:
            self._variables[varname] = ''
        return self._variables[varname]

    def setarg(self, *args):
        for i in range(len(args)):
            self._variables[str(i)] = args[i]

    def _extractKeywords(self, str):
        for key in self.KEYWORDS:
            if key in str:
                self._variables['_input_keyword'] = key
                break
