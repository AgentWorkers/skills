---
name: UnixTime
description: "这是一个快速的 Unix 时间戳工具。它可以获取当前的 Unix 时间，将时间戳转换为日期并反向转换，显示相对时间（即距离现在有多久），以及以不同的格式显示时间。这是从终端操作 Unix 时间戳的最快捷方式。"
version: "1.0.0"
author: "BytesAgain"
tags: ["unix","time","timestamp","date","convert","epoch","utility","developer"]
categories: ["Developer Tools", "Utility"]
---# UnixTime  
Unix时间：快速且简单。可以获取当前时间、进行时间转换以及处理相对日期。  

## 命令  
- `now` — 获取当前的Unix时间戳  
- `date <timestamp>` — 将时间戳转换为人类可读的日期格式  
- `stamp <date>` — 将日期转换为Unix时间戳  
- `ago <timestamp>` — 计算从现在起过去了多长时间  
- `ms` — 获取当前时间的毫秒数  

## 使用示例  
```bash
unixtime now
unixtime date 1700000000
unixtime stamp "2024-06-15"
unixtime ago 1700000000
```  
---  
由BytesAgain（bytesagain.com）提供支持  

- 运行 `unixtime help` 可查看所有命令的详细信息  

## 输出结果  
所有输出结果都会显示在标准输出（stdout）中。可以使用 `unixtime run > output.txt` 将输出内容保存到文件中。