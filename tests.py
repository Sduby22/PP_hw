import unittest
import yaml
from src.ConfigLoader import ConfigLoader
from src.ply.Lexer import Lexer, KEYWORD
from schema import SchemaError

class ConfigLoaderTest(unittest.TestCase):
    def test_missing_key(self):
        conf = ConfigLoader()
        self.assertRaises(SchemaError, conf.load, 'tests/missing_key.yaml')

    def test_wrong_value_type(self):
        conf = ConfigLoader()
        self.assertRaises(SchemaError, conf.load, 'tests/wrong_value_type.yaml')

    def test_good_value(self):
        conf = ConfigLoader()
        path = 'tests/good_value.yaml'
        conf.load(path)
        with open(path, 'r' ,encoding='utf8') as f:
            right = yaml.load(f, yaml.CLoader)
        right.update({'pwd': '.'})
        self.assertEqual(conf.getConfig(), right, 'Config Loaded Incorrectly.')
        self.assertEqual(conf.getConfig().get('pwd'), '.', 'Failed to extract default value.')

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
        self.assertEqual(str, token.value)


    def test_lexer_string2(self):
        str = r"'asdsad\'\'\'dasds'"
        token = self.get_token(str)
        self.assertEqual(str, token.value)

    def test_lexer_string3(self):
        str = r"'asd'dsad'"
        token = self.get_token(str)
        self.assertNotEqual(str, token.value)

    def test_lexer_string4(self):
        str = "'asd\ndsad'"
        self.assertRaises(RuntimeError, self.get_token, str)

    def test_lexer_keyword(self):
        for key in KEYWORD:
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

if __name__ == "__main__":
    unittest.main()
