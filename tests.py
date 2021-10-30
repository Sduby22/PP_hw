import unittest
import yaml
from src.ConfigLoader import ConfigLoader
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
            self.assertEqual(conf.getConfig(), yaml.load(f, yaml.CLoader), 'Config Loaded Incorrectly.')


if __name__ == "__main__":
    unittest.main()
