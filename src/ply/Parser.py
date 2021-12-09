from ply.yacc import yacc
from src.ply.Lexer import Lexer

class Parser:
    def __init__(self, configLoader):
        self._yacc = yacc(module=self)
        self._lexer = Lexer(configLoader)
        self._tokens = self._lexer.tokens
        self._configLoader = configLoader

    def p_job(self):
        '''job : steps'''

