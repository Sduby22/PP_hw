from . import ConfigLoader
import os
import importlib.util
import inspect
import logging

logger = logging.getLogger('RunPy')

def getInstance():
    global runpy
    return runpy

class RunPy:
    def __init__(self):
        self._configLoader = None
        self._fileList = []
        self._nameFuncMap = {}
        pass

    @classmethod
    def getInstance(cls):
        """
        RunPy使用单例模式，所有模块间共享一个RunPy实例，通过此调用获取
        """
        return runpy

    def init(self, configLoader):
        """
        初始化全局RunPy实例

        :param configLoader ConfigLoader: 配置加载器
        """
        if self._configLoader:
            return 
        self._configLoader = configLoader
        dirs = self.getConfig().get('dirs')
        for dir in dirs:
            self._getFiles(dir)
        for file in self._fileList:
            spec = importlib.util.spec_from_file_location("script", file)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)

    def register(self, name):
        """
        为全局RunPy实例注册脚本函数的装饰器

        :param name str: 脚本名称
        """
        def wrapper1(func):
            if name in self._nameFuncMap:
                logger.warning(f'Reregistering Script {name}, the old will be overwritten.')
            self._nameFuncMap[name] = func
            logger.info(f'Registered Script {name}')
            def wrapper2():
                ret = func()
                return ret
            return wrapper2
        return wrapper1

    def callFunc(self, funcName, *args):
        """
        调用名为funcName的已注册的脚本
        如果调用前未注册该脚本，则会抛出RuntimeError

        :param funcName str: 要调用的脚本名称
        :raises RuntimeError: 未注册的调用
        :raises RuntimeError: 传入的参数过少
        :raises RuntimeError: 传入的参数过多
        :raises Exception: 如果scripts配置了halt-onerror,那么脚本执行失败抛出该异常
        """
        logger.info(f'Calling Python Script {funcName}')
        func = self._nameFuncMap.get(funcName, None)
        if not func:
            logger.fatal(f'Invalid Script Name {funcName}')
            raise RuntimeError(f'Invalid Script Name {funcName}')
        argspec = inspect.getargspec(func)
        maxArgs = len(argspec.args)
        minArgs = len(argspec.args) - len(argspec.defaults) if argspec.defaults else 0
        if len(args) < minArgs:
            logger.error(f'Not Enough Aruguments to Call {funcName}, expected minimum of {minArgs}, got{len(args)}')
            raise RuntimeError(f'Not Enough Aruguments to Call {funcName}, expected minimum of {minArgs}, got{len(args)}')
        elif len(args) > maxArgs:
            logger.error(f'Too many Aruguments to Call {funcName}, expected maximum of {maxArgs}, got{len(args)}')
            raise RuntimeError(f'Too many Aruguments to Call {funcName}, expected maximum of {maxArgs}, got{len(args)}')
        try:
            ret = func(*args)
            return ret
        except Exception as e:
            if self._getConfig()['halt-onerror']:
                raise e
            else:
                logger.warning(f'Ignoring Exception When calling py scripts {funcName}: {e}')
                
    def _getConfig(self):
        return self._configLoader.getScriptsConfig()

    def _getFiles(self, path):
        for dirpath, _, filenames in os.walk(path):
            for name in filenames:
                if name[-3:] != '.py':
                    continue
                self._fileList.append(os.path.join(dirpath, name))


runpy = RunPy()

