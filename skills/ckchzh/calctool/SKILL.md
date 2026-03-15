---
name: CalcTool
description: "这是一个具备科学计算功能的命令行计算器。支持基本算术运算、百分比计算、单位转换、小费计算、贷款还款计算，以及各种科学函数（平方根、幂运算、对数、三角函数）的运算。用户无需打开任何其他应用程序，即可通过终端快速完成数学计算。"
version: "1.0.0"
author: "BytesAgain"
tags: ["calculator","math","arithmetic","scientific","convert","finance","utility"]
categories: ["Utility", "Productivity"]
---# CalcTool
一个来自终端的快速数学计算工具，支持基础数学、科学计算和财务计算。
## 命令
- `eval <expression>` — 计算数学表达式的值
- `percent <value> <percent>` — 计算百分比
- `tip <amount> [percent]` — 小费计算器
- `loan <amount> <rate> <years>` — 贷款还款计算器
- `convert <value> <from> <to>` — 单位转换
- `sci <function> <value>` — 科学计算（平方根/对数/正弦/余弦/正切）
## 使用示例
```bash
calctool eval "2 * (3 + 4) / 5"
calctool percent 250 15
calctool tip 85.50 20
calctool loan 300000 6.5 30
```
---
由 BytesAgain 提供支持 | bytesagain.com

## 提示
- 运行 `calctool help` 可查看所有命令的详细信息