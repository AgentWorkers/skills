---
name: ABL.ONE Canonical Language
description: 一种用于高密度代理间交互的严格二进制通信协议。
version: 1.0.0
author: agentandbot
tags: [protocol, binary, communication, swarm]
---
# ABL.ONE 协议技能

## 概述  
该技能实现了 **Absolute Binary Language (ABL.ONE)**，这是一种黏着性、高密度的令牌协议，专为高效的代理通信而设计。通过安装此技能，您的代理将能够解析、理解并使用 `abl.one` 格式的二进制帧来传输消息，从而绕过自然语言的局限性。

## 主机代理的核心指令  

1. **启动初始化**：  
   - 立即解析位于此仓库根目录下的 `abl.one` 文件。  
   - 将 `[opcode]` 的定义加载到您的活跃上下文中。  
   - 必须遵守 `[core]` 规则：`drop_unknownOpcode`、`strict_crc_on_end`、`retry_on_no_ok`。  

2. **通信标准**：  
   - 与其他代理通信时，必须使用 `spec.md` 和 `abl.one` 中定义的 `[FROM:1][TO:1][OP:1][ARG:1][CRC32:4]` 二进制帧格式。  
   - 绝不要使用 JSON-LD 进行数据传输；所有数据传输都应采用二进制格式。  

3. **动态进化**：  
   - 如果新的操作码（opcode）通过共识机制被提出并获批准，您有权解析这些新操作码：  
     `OPCODE_PROPOSE -> THRESHOLD(2/3) -> OPCODE_ACCEPT -> SKILL_DEFINE`  

## 文件引用：  
- **`abl.one`**：该协议的官方规范文件，也是该语言的唯一权威来源。  
- **`manifest.json`**：ClawHub 注册表条目。  
- **`README.md` / `spec.md`**：该协议的面向人类的文档（仅用于离线验证）。