from ply.yacc import yacc
from src.ply.Lexer import tokens

class Parser:
    def __init__(self, configLoader):
        global yac
        self._yacc = yac
        self._configLoader = configLoader

yac = yacc()
