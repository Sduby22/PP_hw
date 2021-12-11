from .ply import Lexer
from .ply import Parser
from logging import getLogger

logger = getLogger('Interpreter')

class Interpreter:
    def __init__(self, configLoader):
        self._lexer = Lexer(configLoader)
        self._parser = Parser(configLoader)
