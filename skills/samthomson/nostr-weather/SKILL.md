---
name: nostr-weather
description: 专为 NIP-Weather IoT 数据设计的专业技能，由 nostr-nak 提供技术支持。
---
# nostr-weather

这是一个专门用于处理 NIP-Weather 物联网数据的技能。

## 依赖项
- 需要以下技能的核心 nak 命令：`skills/nostr-nak/SKILL.md`

## 配置
- **元数据类型**：`16158`
- **读取类型**：`4223`

## 使用方法
查询最新的数据读数：
`script -q -c "nak req -k 4223 -a <pubkey> <relay> -l 1" /dev/null | cat`