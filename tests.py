import unittest
import yaml
import sys
from src import ConfigLoader, Runtime, RunPy, Interpreter
from src.ply import Lexer, Parser
from schema import SchemaError

goodconf = ConfigLoader()
goodconf.load('./src/data/default_config.yaml')


class ConfigLoaderTest(unittest.TestCase):
    '''
    测试ConfigLoader是否能够正确加载配置并校验配置是否合法
    '''
    def test_parse_job2(self):
        conf = ConfigLoader()
        conf.load('./config.yaml')
        lexer = Lexer(conf)
        lexer.load('./jobs/example.job')
        parser = Parser(conf, lexer)
        with open('./jobs/example.job', 'r') as f:
            p = parser.parseStr(f.read())
            p.print()

    def test_missing_key(self):
        conf = ConfigLoader()
        self.assertRaises(SchemaError, conf.load, 'tests/missing_key.yaml')

    def test_wrong_value_type(self):
        conf = ConfigLoader()
        self.assertRaises(SchemaError, conf.load,
                          'tests/wrong_value_type.yaml')

    def test_good_value(self):
        conf = ConfigLoader()
        path = 'tests/good_value.yaml'
        conf.load(path)
        with open(path, 'r', encoding='utf8') as f:
            right = yaml.load(f, yaml.CLoader)
        right.update({'pwd': '.'})
        self.assertEqual(conf.getConfig(), right, 'Config Loaded Incorrectly.')
        self.assertEqual(conf.getConfig().get('pwd'), '.',
                         'Failed to extract default value.')


class LexerTest(unittest.TestCase):
    '''
    测试词法分析模块能否正确获取token并识别出错误token
    '''
    def get_token(self, str):
        conf = ConfigLoader()
        conf.load('tests/good_value.yaml')
        lexer = Lexer(conf)
        lexer.load_str(str)
        return lexer.token()

    def test_lexer_string1(self):
        str = r'"asdsad\"dasds"'
        token = self.get_token(str)
        self.assertEqual(str, f'"{ token.value }"')

    def test_lexer_string2(self):
        str = r"'asdsad\'\'\'dasds'"
        token = self.get_token(str)
        self.assertEqual(str, f"'{ token.value }'")

    def test_lexer_string3(self):
        str = r"'asddsad'"
        token = self.get_token(str)
        self.assertEqual(str, f"'{ token.value }'")

    def test_lexer_string4(self):
        str = "'asd\ndsad'"
        self.assertRaises(RuntimeError, self.get_token, str)

    def test_lexer_keyword(self):
        for key in Lexer.reserved.keys():
            t = self.get_token(key)
            self.assertEqual(key, t.value)

    def test_lexer_file(self):
        conf = ConfigLoader()
        conf.load('tests/good_value.yaml')
        lexer = Lexer(conf)
        lexer.load('tests/Example.job')
        t = lexer.token()
        while t:
            t = lexer.token()

class ParserTest(unittest.TestCase):
    '''
    测试语法分析程序能否正确解析脚本文件
    '''
    def test_parse_job(self):
        conf = ConfigLoader()
        conf.load('./config.yaml')
        lexer = Lexer(conf)
        lexer.load('./jobs/example.job')
        parser = Parser(conf, lexer)
        with open('./jobs/example.job', 'r') as f:
            p = parser.parseStr(f.read())
            p.print()

    def test_parse_job2(self):
        conf = ConfigLoader()
        conf.load('./config.yaml')
        lexer = Lexer(conf)
        lexer.load('./jobs/example_echo.job')
        parser = Parser(conf, lexer)
        with open('./jobs/example_echo.job', 'r') as f:
            p = parser.parseStr(f.read())
            p.print()


    def test_parse_job3(self):
        conf = ConfigLoader()
        conf.load('./config.yaml')
        lexer = Lexer(conf)
        lexer.load('./jobs/example_weather.job')
        parser = Parser(conf, lexer)
        with open('./jobs/example_weather.job', 'r') as f:
            p = parser.parseStr(f.read())
            p.print()

class RuntimeTest(unittest.TestCase):
    '''
    测试Runtime的设置变量，提取关键词功能是否正常
    '''
    def test_runtime_setvar(self):
        rt = Runtime("123456", goodconf)
        rt.assign('asd', 123)
        rt.assign('_ret', None)
        self.assertEqual(rt.getvar('asd'), '123')
        self.assertEqual(rt.getvar('_ret'), 'None')

    def test_runtime_extract(self):
        rt = Runtime("123456", goodconf)
        rt._extractKeywords('爱动机哦三大赛充值啊所拆机就')
        self.assertEqual(rt.getvar('_input_keyword'), '充值')
        rt._extractNumbers('爱动机哦123123拆机就')
        self.assertEqual(rt.getvar('_input_number'), '123123')


class RunpyTest(unittest.TestCase):
    '''
    测试RunPy能否正常注册外部脚本并检测参数合法性
    '''
    runpy = RunPy.getInstance()
    runpy.init(goodconf)

    @runpy.register('test1')
    def _testFunc(self, arg1, arg2, arg3=1):
        return arg1+arg2+arg3

    def test_runpy_default_arg(self):
        ret = self.runpy.callFunc('test1', self, 1, 0)
        self.assertEqual(ret, 2)

    def test_runpy_minimum_args(self):
        self.assertRaises(RuntimeError, self.runpy.callFunc, 'test1', self,  1)

    def test_runpy_maximum_args(self):
        self.assertRaises(RuntimeError, self.runpy.callFunc,
                          'test1', self, 2, 3, 4, 5)

class MainTest(unittest.TestCase):
    '''
    测试脚本运行全过程
    '''

    def test_main_test(self):
        stdout = sys.stdout
        stdin = sys.stdin

        sys.stdout = open("./tests/out.txt", 'w+')
        sys.stdin = open('./tests/in.txt', 'r')
        interpreter = Interpreter(goodconf)
        runtime = Runtime('test', goodconf, enable_timeout=False)
        interpreter.accept(runtime)

        sys.stdout = stdout
        with open('./tests/out.txt') as f:
            out = f.read()
        with open('./tests/example_output.txt') as f:
            example_out = f.read()

        self.assertEqual(out, example_out)

    def test_main_test2(self):
        stdout = sys.stdout
        stdin = sys.stdin

        sys.stdout = open("./tests/out.txt", 'w+')
        sys.stdin = open('./tests/in2.txt', 'r')
        interpreter = Interpreter(goodconf)
        runtime = Runtime('test', goodconf, enable_timeout=False)
        interpreter.accept(runtime)

        sys.stdout = stdout
        with open('./tests/out.txt') as f:
            out = f.read()
        with open('./tests/example_output2.txt') as f:
            example_out = f.read()

        self.assertEqual(out, example_out)

if __name__ == "__main__":
    unittest.main()
