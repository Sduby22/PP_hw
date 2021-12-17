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

### 提交描述风格

commit的描述应遵循[Angular提交规范](https://zj-git-guide.readthedocs.io/zh_CN/latest/message/Angular%E6%8F%90%E4%BA%A4%E4%BF%A1%E6%81%AF%E8%A7%84%E8%8C%83/)

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

如
```
69f08ff build: requirements.txt
7e43562 feat(Lexer): add lexer
4ee7e0f test: add config test cases
9156faf ci: add python req.txt
3c0a247 ci: add gitlab ci
3d2b9f5 build: add pip requirements
3be2ae7 feat(ConfigLoader): add config loader&v
```

## 设计和实现

### 数据结构

#### 抽象语法树
本文法的抽象语法树节点由二元组组成，第一个元素是一个描述表达式类型的元组

第二个元素是一个列表，内含该语法树节点的所有子节点

如example.job的Main step的抽象语法树如下
```
	('stepdecl', 'Main')
		('expression', 'callpy')
			('id', 'GetName')
			('va_args',)
				('var', '_number')
		('expression', 'assign', 'name')
			('terms',)
				('var', '_ret')
		('expression', 'speak')
			('terms',)
				('str', '你好')
				('var', 'name')
				('str', ', 请问有什么可以帮您？')
		('expression', 'wait')
			('terms',)
				('str', '100')
		('expression', 'switch', '_input_keyword')
			('case', '话费')
				('expression', 'call')
					('id', 'Balance')
					('va_args',)
			('case', '投诉')
				('expression', 'call')
					('id', 'Complaint')
					('va_args',)
			('case', '客服')
				('expression', 'call')
					('id', 'Service')
					('va_args',)
			('case', '充值')
				('expression', 'call')
					('id', 'Topup')
					('va_args',)
			('default',)
				('expression', 'call')
					('id', 'Sorry')
					('va_args',)
		('expression', 'call')
			('id', 'Thanks')
			('va_args',)
```

#### 调用栈&变量

程序的调用栈由底层的Python Interpreter维护，变量由Runtime使用一个哈希表维护

### 模块划分

程序分为以下四个模块:

- `ConfigLoader`: 加载配置文件，对配置文件做必要的完整性检查，提供不同模块获取相应配置的接口
- `Runtime`: 提供文法中基本命令的实现，继承Runtime类可以重写所有的基本类型，是定制人机接口的基石
- `Interpreter`： 提供DSL脚本的解析与执行，维护调用栈，调用Runtime内的命令接口。
- `RunPy`: 提供文法中callpy命令的实现，通过注册外部Python脚本保证了可拓展性

模块关系图如下

### 功能

程序提供了可定制，可拓展的DSL解析，执行工具。具体功能见[用户文档](../readme.md)

### 文档

除程序内各接口的注释文档外，RobotSL还提供了[开发文档](./development.md)和[用户文档](../readme.md)

## 接口

### 程序间接口

见模块划分一节。

自行编写外部Python脚本的流程如下
```python
# 首先引入RunPy模块
from src import RunPy

import sqlite3

# 调用getInstance类方法获取全局的runpy实例
runpy = RunPy.getInstance()

# 编写完脚本函数以后，只需要加上runpy.register装饰器并传入你想赋予的
# 脚本名称就可以了，之后便可以使用callpy命令调用
@runpy.register('GetName')
def getname(number):
    conn = sqlite3.connect('data/random_users.db')
    cur = conn.cursor()
    cur = cur.execute('select name from users where number = (?)', (number,))
    res = cur.fetchone()[0]
    conn.close()
    return res
```

### 人机接口

人机接口通过`Runtime`模块实现，具体包括实现程序如何向用户输出/用户如何向程序输入等接口。
RobotSL提供一个[基本的Runtime实现](../src/Runtime.py), 此Runtime实现了基本的控制台输入
输出，如果想拓展可以通过重写Runtime的方法来拓展。比如将控制台输出重载为电话语音，或是
重载为网络的向客户端发送信息等。

## 测试

### 测试桩

程序的测试桩编写均在[test.py](../tests.py)下, 对于单个模块的测试均需要构造一个临时的其它模块，
或是提供一个临时的语法数测试执行等等。

例如以下测试桩就构造了临时的runpy测试对象，临时注册的脚本函数用来测试函数的参数个数
```python
class RunpyTest(unittest.TestCase):
    runpy = RunPy.getInstance()
    runpy.init(goodconf)

    @runpy.register('test1')
    def _testFunc(self, arg1, arg2, arg3=1):
        return arg1+arg2+arg3

    def test_runpy_default_arg(self):
        ret = self.runpy.callFunc('test1', self, 1, 0)
        self.assertEqual(ret, 2)

```

### 自动测试脚本

由于我们使用了python的`unittest`库, 所以任何以test_开头的测试桩函数都会被自动执行，也就不需要我们
手动写测试脚本了。测试桩/脚本见[test.py](../tests.py)

测试中使用的数据/文件在tests文件夹中, 包含DSL脚本，配置文件的测试文件

### 测试覆盖范围

RobotSL编写的测试覆盖了以下范围：

- `ConfigLoader`: 是否能够正确验证配置文件的正确性，处理缺省值等
- `Lexer`: 是否能够正确识别出不同的字符串（有无转义等）和其他的token
- `Parser`: 是否能够正确识别出测试的DSL脚本文件，并打印出语法树
- `Runtime`: 是否能够正确处理Interpreter的设置变量，提取变量关键字等接口调用
- `Runpy`: 是否能够正确注册/调用脚本函数，并检测是否提供了正确数量的参数

### Gitlab CI配置

每次push的时候都会触发Gitlab CI Runner的运行，流水线流程如下

```yaml
before_script:
  - pip3 install -r requirements.txt

gen_random_users:
  stage: build
  script:
    - cd data
    - sqlite3 random_users.db < DDL.sql
    - python3 GenRandomUsers.py

tests:
  stage: test
  script:
    - python3 tests.py
```

- 安装依赖
- 生成随机用户数据库
- 运行测试脚本

## 记法

### 配置文件语法描述

见使用文档[readme](../readme.md)

### DSL文法描述

见使用文档[readme](../readme.md)
