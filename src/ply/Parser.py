from ply.yacc import yacc
from . import ASTNode, Lexer

class Parser:
    def __init__(self, configLoader):
        self._yacc = yacc(module=self)
        self._lexer = Lexer(configLoader)
        self._tokens = self._lexer.tokens
        self._configLoader = configLoader

    def p_job(self):
        '''job : stepdecl
               | stepdecl job'''
        if len(p) == 2:
            p[0] = ASTNode(('root'), p[1])
        else:
            p[0] = ASTNode(('root'), p[1], *p[2].childs)

    def p_stepblock(self):
        '''
        stepdecl : 'step' ID expressions 'endstep'
        '''
        p[0] = ASTNode(('stepdecl', p[2]), *p[3].childs)

    def p_expressions(self):
        '''
        expressions : empty
                    | expression expressions
        '''
        if len(p) == 3:
            p[0] = ASTNode(('expressions'), p[1], *p[2].childs)
        else:
            p[0] = ASTNode(('expressions'))

    def p_expression(self):
        '''
        expression : oneline | switch
        '''
        p[0] = p[1]

    def p_oneline(self):
        '''
        oneline : VAR '=' terms
                | 'speak' terms
                | 'callpy' ID va_args
                | 'beep'
                | 'wait' term
                | 'call' ID va_args
                | 'hangup'
        '''
        if len(p) == 4 and p[2] == '=':
            p[0] = ASTNode(('expression', 'assign'), p[1], p[3])
        else:
            p[0] = ASTNode(('expression', p[1]), *p[2:])

    def p_switch(self):
        pass

    def p_empty(self):
        '''
        empty :
        '''
        pass
