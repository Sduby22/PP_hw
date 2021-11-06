from yaml import  load, CLoader
from schema import Schema, Optional

class ConfigLoader:
    def __init__(self, path=''):
        if path:
            self.load(path)
        pass

    def getConfig(self):
        return self._config

    def _updateDefault(self):
        with open('./src/data/default_config.yaml', 'r', encoding='utf-8') as f:
            default = load(f, CLoader)
        default.update(self._config)
        self._config = default

    def load(self, path='./config.yaml', encoding='utf8'):
        with open(path, 'r', encoding=encoding) as f:
            config = load(f, CLoader)
        if self._validate(config):
            self._config = config
        else:
            self._config = None
        self._updateDefault()

    def _validate(self, config):
        schema = Schema({
            Optional('pwd', default='.'): str,
            'runtime': {
                'user-db': str,
                'wait-forever': bool,
            },
            'job': {
                'path': str,
                'halt-onerror': bool,
            },
            'scripts': {
                'halt-onerror': bool,
                'dirs': [str]
            }
        })
        return schema.validate(config)

    def getRuntimeConfig(self):
        return self._config.get('runtime')

    def getJobConfig(self):
        return self._config.get('job')

    def getScriptsConfig(self):
        return self._config.get('scripts')
