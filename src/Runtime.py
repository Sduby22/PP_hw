from logging import getLogger
from termcolor import cprint
from inputimeout import inputimeout, TimeoutOccurred
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

    def __init__(self, number, config: ConfigLoader, enable_timeout = True):
        logger.info("Initializing runtime")
        self._conf = config
        self._enable_timeout = enable_timeout
        self._variables = {
            '_input': '',
            '_input_keyword': '',
            '_number': number,
            '_ret': '',
        }
        pass

    def speak(self, str):
        """
        实现脚本中的speak命令

        :param str str: speak的内容
        """
        cprint(f'Robot >>> {str}', 'yellow')

    def wait(self, timeStr):
        """
        等待用户输入, 如果时间超过timeStr，则超时

        :param timeStr str: 要等待的时间字符串
        """
        self.speak(f'Waiting user input for {timeStr} seconds')
        if self._enable_timeout:
            try:
                str = inputimeout(prompt='Input <<< ', timeout=int(timeStr))
            except TimeoutOccurred:
                str = 'timeout'
                logger.info("User input timed out.")
        else:
            str = input()
        self.assign('_input', str)
        self._extractKeywords(str)
        self._extractNumbers(str)

    def hangup(self):
        """
        挂断连接，终止脚本

        """
        logger.info(f"user {self._variables.get('_number')} hung up")

    def assign(self, var, val):
        """
        为变量赋值

        :param var str: 变量名
        :param val Any: 要赋的值（会被转换为字符串）
        """
        self._variables[var] = str(val)
        pass

    def beep(self):
        """
        实现发送滴声的方法（为电话客服设计）

        """
        print('beep')
        pass

    def getvar(self, varname):
        """
        获取变量的值    

       :param varname str: 变量名
        """
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
            
    def _getConfig(self):
        return self._conf.getRuntimeConfig()

