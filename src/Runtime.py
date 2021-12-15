from logging import getLogger
import asyncio
import aioconsole
import re

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
        # async def ainput():
        #     str = ''
        #     try:
        #         str = await asyncio.wait_for(aioconsole.ainput("<<<"), int(timeStr))
        #     except asyncio.TimeoutError as e:
        #         str = ''
        #     self.assign('_input', str)
        #     self._extractKeywords(str)
        #     self._extractNumbers(str)
        # asyncio.run(ainput())
        self.speak(f'Waiting user input for {timeStr} seconds')
        str = input('<<< ')
        self.assign('_input', str)
        self._extractKeywords(str)
        self._extractNumbers(str)

    def hangup(self):
        logger.info(f"user {self._variables.get('_number')} hung up")

    def assign(self, var, val):
        self._variables[var] = str(val)
        pass

    def beep(self):
        print('beep')
        pass

    def getvar(self, varname):
        if varname not in self._variables:
            self._variables[varname] = ''
        return self._variables[varname]

    def _extractKeywords(self, str):
        for key in self.KEYWORDS:
            if key in str:
                self._variables['_input_keyword'] = key
                break

    def _extractNumbers(self, str):
        match = re.findall(r'\d+', str)
        if match:
            self.assign('_input_number', match[0])
