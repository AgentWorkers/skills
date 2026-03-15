---
name: UUIDGen
description: "UUID生成器及唯一标识符生成工具。支持生成UUID v4（随机类型）、UUID v1（基于时间的类型）、短ID、nano ID以及自定义长度的随机字符串。具备验证UUID格式的功能，能够解析UUID的各个组成部分，并可批量生成唯一标识符。这是开发者必备的实用工具。"
version: "1.0.0"
author: "BytesAgain"
tags: ["uuid","generator","random","id","unique","developer","utility"]
categories: ["Developer Tools", "Utility"]
---# UUIDGen  
生成唯一的标识符。支持 UUID、短 ID 和 nano ID 等多种格式。  
## 命令  
- `v4`：生成 UUID v4（随机值）  
- `batch [n]`：批量生成多个 UUID  
- `short [length]`：生成指定长度的随机短 ID  
- `validate <uuid>`：检查字符串是否为有效的 UUID  
- `parse <uuid>`：解析 UUID 的各个组成部分  

## 使用示例  
```bash
uuidgen v4
uuidgen batch 10
uuidgen short 8
uuidgen validate "550e8400-e29b-41d4-a716-446655440000"
```  
---  
由 BytesAgain 提供支持 | bytesagain.com  

- 运行 `uuidgen help` 可查看所有命令的详细信息。  

## 适用场景  
- 从终端快速生成 UUID  
- 自动化流程中的标识符生成需求