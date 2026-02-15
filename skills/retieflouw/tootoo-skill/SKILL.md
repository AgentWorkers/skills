---
name: tootoo
description: 同步您的 TooToo Codex，并监控代理（agent）的配置是否与您的设定值保持一致。
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      env: []
    install: null
---

# TooToo

该工具用于将您的个人代码库（codex）从 TooToo 服务同步到本地，并监控代码库内容的一致性（alignment）。

## 命令
- `/tootoo setup <username>` — 初始设置：从 TooToo 服务获取代码库数据并生成 `SOUL.md` 文件
- `/tootoo sync` — 强制从 TooToo 服务重新同步代码库数据
- `/tootoo report` — 生成最近对话内容的一致性报告
- `/tootoo status` — 显示当前代码库内容的一致性统计信息

## 配置
请在 `openclaw.json` 文件中设置您的 TooToo 用户名：

```json5
{ skills: { entries: { "tootoo": { username: "your-username" } } } }
```