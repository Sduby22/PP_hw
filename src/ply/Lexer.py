from ply.lex import lex
from logging import getLogger
from .. import ConfigLoader

logger = getLogger('Interpreter')


class Lexer:

    reserved = {
        'switch':    'SWITCH',
        'case':      'CASE',
        'default':   'DEFAULT',
        'endswitch': 'ENDSWITCH',
        'step':      'STEP',
        'endstep':   'ENDSTEP',
        'call':      'CALL',
        'callpy':    'CALLPY',
        'wait':      'WAIT',
        'beep':      'BEEP',
        'speak':     'SPEAK',
        'hangup':    'HANGUP',
    }

    tokens = [
        'NEWLINE',
        'VAR',
        'ID',
        'STR',
    ] + list(reserved.values())

    literals = ['+', '=']
    t_ignore_COMMENT = r'\#.*'
    t_ignore = ' \t'

    def __init__(self, configLoader):
        self._lexer = lex(module=self)
        self._f = None
        self._configLoader = configLoader

    def getLexer(self):
        """
        获取类内的ply.lexer对象

        """
        return self._lexer

    def load(self, path):
        """
        载入脚本文件

        :param path str: 脚本文件路径
        """
        self._f = None
        with open(path, 'r', encoding='utf8') as f:
            self._f = f.read()
        if not self._f:
            logger.error(f'Failed to load file {path}')
            return
        self._lexer.input(self._f)
        self._lexer.lineno = 1

    def load_str(self, str):
        """
        载入一段字符串

        :param str str:
        """
        self._f = str
        self._lexer.input(str)
        self._lexer.lineno = 1

    def token(self):
        """
        获取下一个词法符号

        :raises RuntimeError: 未载入脚本文件
        """
        if not self._f:
            raise RuntimeError('reading token before load.')
        return self._lexer.token()

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')    # Check for reserved words
        return t

    def t_VAR(self, t):
        r'\$[a-zA-Z_0-9]*'
        t.value = t.value[1:]
        return t

    def t_STR(self, t):
        r'''("((\\\")|[^\n\"])*")|('((\\\')|[^\n\'])*')'''
        t.value = t.value[1:-1]
        return t

    def t_error(self, t):
        msg = f'line {t.lexer.lineno}: Unexpected symbol {t.value}'
        if self._configLoader.getJobConfig().get('halt-onerror'):
            raise RuntimeError(msg)
        logger.error(msg)
        t.lexer.skip(1)


if __name__ == '__main__':
    c = ConfigLoader('src/data/default_config.yaml')
    l = Lexer(c)
    l.load_str('''step name endstep''')
    token = l.token()
    while token:
        print(token)
        token = l.token()
