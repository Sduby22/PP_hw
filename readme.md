# Interpreter - 应答机器人

## 介绍

## 应答脚本语法规则

注释: 以'#'开头的一行为注释，被忽略

```
job		: stepblock
		| stepblock job

stepdecl	: 'step' STEPNAME expressions 'endstep'

expressions	: expression
			| expression expressions

expression	: oneline
			| switch

oneline		: VAR '=' terms
			| 'speak' terms
			| 'callpy' PYFILE va_args
			| 'beep'
			| 'wait' term
			| 'call' STEPNAME va_args
			| 'hangup'

switch		: 'switch' VAR switch_body 'endswitch'
	
switch_body	: cases 
			| cases default

cases		: case 
			| case cases

case		: 'case' term oneline
default		: 'default' oneline

terms		: term | term '+' terms
term		: VAR | STR

va_args		: '' | term | term ' ' va_args
```
