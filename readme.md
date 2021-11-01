# Interpreter - 应答机器人

## 介绍

## 应答脚本语法规则

注释: 以'#'开头的一行为注释，被忽略

```
outstep		: stepblock
		| stepblock '\n' outstep

stepblock	: 'step' STEPNAME '\n' expressions '\n' 'endstep'

expressions	: expression
		| expression '\n' expressions

expression	: oneline
		| multiline

oneline		: VAR '=' terms
		| 'speak' terms
		| 'callpy' PYFILE va_args
		| 'beep'
		| 'wait' term
		| 'call' STEPNAME va_args
		| 'hangup'

multiline	: if
		| switch

switch		: 'switch' VAR '\n' switch_body '\n' 'endswitch'
switch_body	: cases | cases '\n' default
cases		: case | case '\n' cases
case		: 'case' term oneline
default		: 'default' oneline

if : 'if' condition '\n' expressions '\n' 'endif' 
condition : term binary_operator term

terms		: term | term '+' terms
term		: VAR | STR

va_args		: '' | term | term ' ' va_args

binary_operator : '==' | '<' | '>' | '<=' | '>=' | '!='
```
