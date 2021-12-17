import unittest
import yaml
from src import ConfigLoader, Runtime, RunPy
from src.ply import Lexer, Parser
from schema import SchemaError

goodconf = ConfigLoader()
goodconf.load('./src/data/default_config.yaml')


class ConfigLoaderTest(unittest.TestCase):
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
    def test_parse_job(self):
        conf = ConfigLoader()
        conf.load('./config.yaml')
        lexer = Lexer(conf)
        lexer.load('./example.job')
        parser = Parser(conf, lexer)
        with open('./example.job', 'r') as f:
            p = parser.parseStr(f.read())
            p.print()


class RuntimeTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
