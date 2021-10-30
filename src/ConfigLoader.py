from yaml import  load, CLoader
from schema import Schema, Optional

class ConfigLoader:
    def __init__(self, path=''):
        if path:
            self.load(path)
        pass

    def getConfig(self):
        return self._config

    def load(self, path='./config.yaml', encoding='utf8'):
        with open(path, 'r', encoding=encoding) as f:
            config = load(f, CLoader)
        if self._validate(config):
            self._config = config
        else:
            self._config = None

    def _validate(self, config):
        schema = Schema({
            Optional('pwd', default='.'): str,
            'config': {
                'user-db': str,
                'wait-forever': bool,
                'timeout': int,
            },
            'scripts': {
                'dirs': [str]
            }
        })
        return schema.validate(config)
