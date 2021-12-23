from logging import getLogger
from ply.yacc import yacc
from functools import reduce

from src.ConfigLoader import ConfigLoader
from src.ply.Lexer import Lexer
from . import ASTNode

logger = getLogger('Interpreter')


class Parser:
    def __init__(self, configLoader: ConfigLoader, lexer: Lexer):
        self._lexer = lexer
        self.tokens = lexer.tokens
        self._yacc = yacc(module=self, debug=True)
        self._configLoader = configLoader

    def parseStr(self, str):
        """
        解析一个字符串，生成语法树

        :param str str: 要解析的字符串
        """
        return self._yacc.parse(str, self._lexer.getLexer())

    def p_job(self, p):
        '''job : newlines 
               | newlines stepdecl job'''
        if len(p) == 2:
            p[0] = ASTNode(('root'))
        else:
            p[0] = ASTNode(('root'), p[2], *p[3].childs)

    def p_stepdecl(self, p):
        '''
        stepdecl : STEP ID expressions ENDSTEP
        '''
        p[0] = ASTNode(('stepdecl', p[2]), *p[3])

    def p_expressions(self, p):
        '''
        expressions : newlines
                    | NEWLINE expression expressions
        '''
        if len(p) == 2:
            p[0] = []
        else:
            p[0] = [p[2]] + p[3]

    def p_expression(self, p):
        '''
        expression : oneline
                   | switch
        '''
        p[0] = p[1]

    def p_id(self, p):
        '''
        id : ID
        '''
        p[0] = ASTNode(('id', p[1]))

    def p_oneline(self, p):
        '''
        oneline : VAR '=' terms
                | SPEAK terms
                | CALLPY id va_args
                | BEEP
                | WAIT terms
                | CALL id va_args
                | HANGUP
        '''
        if len(p) == 4 and p[2] == '=':
            p[0] = ASTNode(('expression', 'assign', p[1]), p[3])
        else:
            p[0] = ASTNode(('expression', p[1]), *p[2:])

    def p_switch(self, p):
        '''
        switch : SWITCH VAR  switch_body ENDSWITCH
        '''
        p[0] = ASTNode(('expression', 'switch', p[2]), *p[3])
        pass

    def p_switch_body(self, p):
        '''
        switch_body : cases
                    | cases default
        '''
        p[0] = reduce(lambda x, y: x+y, p[1:])

    def p_cases(self, p):
        '''
        cases   : newlines
                | NEWLINE case cases
        '''
        if len(p) == 4:
            p[0] = p[3]
            p[0] = [p[2]] + p[3]
        else:
            p[0] = []

    def p_default(self, p):
        '''
        default : DEFAULT oneline NEWLINE
        '''
        p[0] = [ASTNode(('default',), p[2])]

    def p_case(self, p):
        '''
        case    : CASE STR oneline
        '''
        p[0] = ASTNode(('case', p[2]), p[3])

    def p_terms(self, p):
        '''
        terms : term 
              | term '+' terms
        '''
        if len(p) == 2:
            p[0] = ASTNode(('terms',), p[1])
        else:
            p[0] = p[3]
            p[0].childs = [p[1]] + p[0].childs

    def p_term_var(self, p):
        '''
        term    : VAR 
        '''
        p[0] = ASTNode(("var", p[1]))

    def p_term_str(self, p):
        '''
        term    : STR
        '''
        p[0] = ASTNode(("str", p[1]))

    def p_va_args(self, p):
        '''
        va_args : empty 
                | term va_args
        '''
        if len(p) == 3:
            p[0] = p[2]
            p[0].childs = [p[1]] + p[0].childs
        else:
            p[0] = ASTNode(('va_args',))

    def p_empty(self, _):
        '''
        empty :
        '''
        pass

    def p_newlines(self, _):
        '''
        newlines    : NEWLINE
                    | empty
        '''
        pass

    def p_error(self, p):
        if self._configLoader.getJobConfig()['halt-onerror']:
            raise RuntimeError("SyntaxError at line {}, Unexpected {}".format(
                self._lexer.getLexer().lineno, p))
        logger.error('SyntaxError at line {}, Unexpected {}'.format(
            self._lexer.getLexer().lineno, p))
