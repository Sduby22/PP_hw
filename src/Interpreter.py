from functools import reduce
from src import ConfigLoader
from src import Runtime
from src.ply.AST import ASTNode
from .ply import Lexer
from .ply import Parser
from src import RunPy
from logging import getLogger

logger = getLogger('Interpreter')


class Interpreter:
    def __init__(self, configLoader: ConfigLoader):
        self._lexer = Lexer(configLoader)
        self._parser = Parser(configLoader, self._lexer)
        self._config = configLoader
        self.job = ''
        self.ast = None
        self.steps = {}
        self._stop = False

        self._load_job()
        self._parse()

    def _load_job(self):
        with open(self._config.getJobConfig().get('path'), 'r') as f:
            self.job = f.read()
        self._lexer.load_str(self.job)

    def _parse(self):
        logger.info("Begin parsing job file...")
        if self.job == '':
            raise RuntimeError('job is empty')
        self.ast = self._parser.parseStr(self.job)
        for stepdecl in self.ast.childs:
            self.steps[stepdecl.type[1]] = stepdecl

    def setRuntime(self, runtime: Runtime):
        self.runtime = runtime

    def run(self):
        if not self.runtime or not self.ast:
            raise RuntimeError("Must call setRuntime and load_job before Run")
        logger.info("Begin running...")
        if 'Main' not in self.steps:
            raise RuntimeError("Entry step Main not defined")
        self._runStep(self.steps['Main'])

    def stop(self):
        logger.debug("Requesting to stop...")
        self._stop = True

    def _getStep(self, stepname):
        step = self.steps.get(stepname, None)
        if not step:
            raise RuntimeError(f"Undefined step {stepname}")
        return step

    def _runStep(self, step: ASTNode, *args):
        self._setargs(self, *args)
        for expression in step.childs:
            self._exec(expression)

    def _exec(self, expr: ASTNode):
        if self._stop:
            return 
        if expr.type[0] != 'expression':
            logger.error('Not an expression')
        match expr.type[1]:
            case 'call':
                self._runStep(self._getStep(expr.childs[0].type[1]), *self._eval(expr.childs[1]))
            case 'assign':
                self.runtime.assign(expr.type[2], self._eval(expr.childs[0]))
            case 'speak':
                self.runtime.speak(self._eval(expr.childs[0]))
            case 'callpy':
                self.runtime.callpy(expr.childs[0].type[1], *self._eval(expr.childs[1]))
            case 'beep':
                self.runtime.beep()
            case 'wait':
                self.runtime.wait(self._eval(expr.childs[0]))
            case 'hangup':
                self.stop()
                self.runtime.hangup()
            case 'switch':
                self._exec_switch(expr)

    def _exec_switch(self, expr: ASTNode):
        condition = self.runtime.getvar(expr.type[2])
        cases = [child.type[1] for child in expr.childs if child.type[0] == 'case']
        default = expr.childs[-1] if expr.childs[-1].type[0] == 'default' else None
        match = -1
        for i in range(len(cases)):
            if condition == cases[i]:
                match = i
                break
        if match == -1 and default:
            return self._exec(default.childs[0])
        elif match != -1:
            return self._exec(expr.childs[match].childs[0])

    def _eval(self, term: ASTNode):
        match term.type[0]:
            case 'var':
                return self.runtime.getvar(term.type[1])
            case 'str':
                return term.type[1]
            case 'terms':
                return reduce(lambda x, y: x+self._eval(y), term.childs, '')
            case 'va_args':
                return [self._eval(x) for x in term.childs]
            case _:
                raise RuntimeError("eval an unknown ASTNode")
            
    def _setargs(self, *args):
        for i in range(len(args)):
            self.runtime.assign(str(i), args[i])

