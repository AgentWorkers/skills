---
name: UnixTime
description: "这是一个快速的 Unix 时间戳工具。它可以获取当前的 Unix 时间，将时间戳转换为日期或反之亦然，显示相对时间（即距离现在有多久），并以不同的格式显示时间。这是从终端操作 Unix 时间戳的最快捷方式。"
version: "1.0.0"
author: "BytesAgain"
tags: ["unix","time","timestamp","date","convert","epoch","utility","developer"]
categories: ["Developer Tools", "Utility"]
---# UnixTime  
Unix 时间：快速且简单。可以获取当前时间、进行时间转换以及处理相对日期。  

## 命令  
- `now` — 获取当前的 Unix 时间戳  
- `date <timestamp>` — 将时间戳转换为人类可读的日期格式  
- `stamp <date>` — 将日期转换为时间戳  
- `ago <timestamp>` — 计算从指定时间到现在过去了多久  
- `ms` — 获取当前时间的毫秒数  

## 使用示例  
```bash
unixtime now
unixtime date 1700000000
unixtime stamp "2024-06-15"
unixtime ago 1700000000
```  
---  
由 BytesAgain 提供支持 | bytesagain.com  

## 工作原理  
程序会读取输入数据，使用内置逻辑进行处理，并输出结果。所有数据仅存储在本地。  

## 提示  
- 运行 `unixtime help` 可以查看所有命令的详细信息  
- 无需使用 API 密钥  
- 支持离线使用