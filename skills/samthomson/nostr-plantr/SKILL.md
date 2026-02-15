---
name: nostr-plantr
description: Plantr IoT 数据（型号 34419 和 4171）的专用技能。
---
# nostr-plantr

这是一个专门用于处理 Plantr IoT 设备（型号 34419 和 4171）数据的技能。

## 依赖项
- 需要以下技能的核心 nak 命令：`skills/nostr-nak/SKILL.md`

## 配置
- **花盆类型**：`34419`
- **活动日志类型**：`4171`

## 使用方法
查询浇水历史记录：
`script -q -c "nak req -k 4171 <relay> -l 20" /dev/null | cat`