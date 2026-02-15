---
name: session-cleaner
description: 将原始的 OpenClaw 会话 JSONL 转录内容转换为格式清晰、易于阅读的 Markdown 文本。移除工具调用、元数据以及系统生成的冗余信息，同时保留对话内容。
---

# 会话清理器

该工具可将原始的 OpenClaw/Clawdbot 会话 JSONL 文件转换为格式规范的 Markdown 文本。

## 功能介绍

- 读取 `.jsonl` 格式的会话文件
- 删除工具调用记录、系统元数据以及无关内容
- 仅保留人类用户与助手之间的对话内容
- 支持跨多个代理（agent）进行批量处理

## 所需脚本

- `session-cleaner.mjs`：主要清理脚本（基于 Node.js）
- `session-cleaner-spock.sh`：用于批量清理 Spock 会话的脚本
- `session-cleaner-scotty-remote.sh`：通过 SSH 远程清理 Scotty 会话的脚本