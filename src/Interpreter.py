from src.ply.Lexer import Lexer
from src.ply.Parser import Parser
from logging import getLogger

logger = getLogger('Interpreter')

class Interpreter:
    def __init__(self, configLoader):
        self._lexer = Lexer(configLoader)
        self._parser = Parser(configLoader)
