---
name: CurrConv
description: "这是一个使用实时汇率的货币转换器。支持在世界范围内的货币之间进行转换，可以查看当前的汇率、汇率历史记录，并同时比较多种货币。通过免费的API，该工具支持USD、EUR、GBP、JPY、CNY以及150多种其他货币的兑换。"
version: "1.0.0"
author: "BytesAgain"
tags: ["currency","converter","exchange","rate","money","finance","forex","international"]
categories: ["Finance", "Utility"]
---# CurrConv  
支持实时汇率转换，可立即查询货币兑换信息。  
## 命令  
- `convert <金额> <源货币> <目标货币>` — 在两种货币之间进行兑换  
- `rate <源货币> <目标货币>` — 获取当前汇率  
- `rates <基础货币>` — 显示主要货币的汇率  
- `list` — 列出所有支持的货币  

## 使用示例  
```bash
currconv convert 100 USD EUR
currconv convert 1000 CNY USD
currconv rate GBP JPY
currconv rates USD
```  
---  
由 BytesAgain 提供支持 | bytesagain.com  

## 工作原理  
程序接收用户输入，通过内置逻辑进行处理，然后输出结果。  

## 提示  
- 使用 `currconv help` 可查看所有可用命令  
- 无需 API 密钥  
- 支持离线使用