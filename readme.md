# RobotSL - 应答机器人

## 介绍

RobotSL 提供了一种相对简单的文法来描述在线客服机器人的自动应答逻辑。文法中内置了几种命令，
例如向用户发送消息，等待用户回复，挂断电话，发送滴声等。RobotSL同时支持基于Python脚本的拓展
功能，即用户可以自行编写外部的Python脚本来增强RobotSL的功能。例如从数据库中查询数据，写入数据
的功能等。

## 应答脚本语法规则

### 注释

注释: 以'#'开头的一行为注释，被忽略

### 内置命令

RobotSL内置了以下几种命令

- `speak [terms]`: 向客户发送信息
- `wait [timeStr]`: 等待一段时间并返回客户的回复
- `hungup`: 中断此次会话
- `switch .. case .. default ..`: 根据条件选择对应的分支
- `callpy SCRIPT_NAME ARGS`: 调用外部的Python扩展脚本

### 语法BNF定义

语法的详细定义如下（BNF定义）：
```
job		: stepblock
		| stepblock job

stepdecl	: 'step' STEPNAME expressions 'endstep'

expressions	: empty
			| expression expressions

expression	: oneline
			| switch

oneline		: VAR '=' terms
			| 'speak' terms
			| 'callpy' PYFILE va_args
			| 'beep'
			| 'wait' terms
			| 'call' STEPNAME va_args
			| 'hangup'

switch		: 'switch' VAR switch_body 'endswitch'
	
switch_body	: cases 
			| cases default

cases		: empty 
			| case cases

case		: 'case' terms oneline
default		: 'default' oneline

terms		: term | term '+' terms
term		: VAR | STR

va_args		: empty | term ' ' va_args
```

### 文法规定

由上述的语法BNF定义可知：
- 一个脚本文件必须由许多的step组成。
- 每个step由不同的expressions组成
- switch语句的每个case只能执行一个语句，如果想执行多个语句需要自行定义一个step

额外规定：
- 每个文件必须有一个Main step,作为脚本的入口step

### 示例脚本

见[example.job](./example.job)

## 使用说明

### 配置文件

程序运行时会读取工作目录下的`config.yaml`, 配置文件的格式及语义如下.
```yaml
# working dir of scripts and main interpreter.
pwd: .

# runtime config
runtime:
  # path of user database, will be injected into scripts.
  user-db: ./data/random-users.py

job:
  path: ./example.job
  # halts program on job scripts syntax errors.
  halt-onerror: false

# python scripts dirs
scripts: 
  # halts robot on runpy errors or timeouts.
  halt-onerror: false
  dirs: 
    - ./scripts/
```

### 基本使用

1. 安装依赖

- 安装Python3.10
- 安装pip依赖`pip3 install -r requirements.txt`

2. 在配置文件中设置好自己的脚本文件路径
```yaml
job:
  path: ./example.job
```

3. 执行Main.py

```bash
$ python3 Main.py
```

## 开发文档

见 [development.md](./docs/development.md)
