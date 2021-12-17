from yaml import load, CLoader
from schema import Schema, Optional


class ConfigLoader:
    def __init__(self, path=''):
        if path:
            self.load(path)
        pass

    def getConfig(self):
        """
        获取配置文件解析出的对象

        """
        return self._config

    def load(self, path='./config.yaml', encoding='utf8'):
        """
        加载配置文件，进行完整性检查，并处理缺省值

        :param path str: 配置文件路径
        :param encoding str: 编码方式
        """
        with open(path, 'r', encoding=encoding) as f:
            config = load(f, CLoader)
        if self._validate(config):
            self._config = config
        else:
            self._config = {}
        self._updateDefault()

    def getRuntimeConfig(self):
        """
        获取运行时的配置

        """
        return self._config.get('runtime')

    def getJobConfig(self):
        """
        获取脚本解析部分的配置

        """
        return self._config.get('job')

    def getScriptsConfig(self):
        """
        获取RunPy模块的配置

        """
        return self._config.get('scripts')

    def _updateDefault(self):
        with open('./src/data/default_config.yaml', 'r', encoding='utf-8') as f:
            default = load(f, CLoader)
        default.update(self._config)
        self._config = default

    def _validate(self, config):
        schema = Schema({
            Optional('pwd', default='.'): str,
            'runtime': {
                'user-db': str,
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
