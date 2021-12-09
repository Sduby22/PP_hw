from ply.lex import lex
from logging import getLogger

logger = getLogger('Interpreter')

class Lexer:
    KEYWORD = (
            'switch', 'case', 'default',
            'step', 'endstep', 'call', 'callpy', 
            'wait', 'beep', 'speak', 'hangup'
            )

    tokens = (
            'KEYWORD',
            'NEWLINE',
            'VAR',
            'STEP',
            'STRING',
            'OPERATOR',
            'NUMBER',
            )

    t_ignore_COMMENT = r'\#.*'
    t_ignore = ' \t'

    def __init__(self, configLoader):
        self._lexer = lex(module=self)
        self._f = None
        self._configLoader = configLoader

    def t_OPERATOR(self, t):
        r'\+|(=|>|<|!)?=|>|<'
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t


    def t_KEYWORD(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value not in self.KEYWORD:
            t.type = 'STEP'
        return t

    def t_VAR(self, t):
        r'\$[a-zA-Z_0-9]*'
        t.value = t.value[1:]
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'''("((\\\")|[^\n\"])*")|('((\\\')|[^\n\'])*')'''
        return t

    def t_error(self, t):
        msg = f'line {t.lexer.lineno}: Unexpected symbol {t.value}'
        if self._configLoader.getJobConfig().get('halt-onerror'):
            raise RuntimeError(msg)
        logger.error(msg) 
        t.lexer.skip(1)

    def getLexer(self):
        return self._lexer

    def load(self, path):
        self._f = None
        with open(path, 'r', encoding='utf8') as f:
            self._f = f.read()
        if not self._f:
            logger.error(f'Failed to load file {path}')
            return
        self._lexer.input(self._f)
        self._lexer.lineno = 1
    
    def load_str(self, str):
        self._f = str
        self._lexer.input(str)
        self._lexer.lineno = 1

    def token(self):
        if not self._f:
            raise RuntimeError('reading token before load.')
        return self._lexer.token()


