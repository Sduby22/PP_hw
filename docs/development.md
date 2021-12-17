# RobotSL 开发文档

## 风格

### 代码注释风格

编写代码应该为提供的公开接口编写注释，注释的风格统一使用[Doxygen Python](https://www.doxygen.nl/manual/docblocks.html#pythonblocks)风格
应提供函数的描述，传入各参数的类型及描述，以及可能抛出的异常的描述。

示例注释如下：

```python
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

        # ...
```

### 命名风格

命名应遵循以下风格：

- 类名统一使用大驼峰命名法，如： `RunPy, Parser`等
- 类的公开接口使用小驼峰命名法，如： `getInstance， callFunc`
- 类的私有方法使用下划线+小驼峰命名法，如： `_helper, _getConfig`

### 文件组织

文件组织应注意一下几点：

- 每个类单独放在一个文件中，该文件和类名一致
- 如果是有层级关系的类，低层的类应该放在更深层次的文件夹中。
比如`Interpreter`类由`Parser`与`Lexer`组成，是很明显的层级关系。此时`Lexer.py`和`Parser.py`应该放在
`Interpreter`的子目录中
- 每个模块子目录由一个`__init__.py`统一管理哪些暴露至外部，哪些隐藏

## 设计和实现



## 接口

## 测试

## 记法
