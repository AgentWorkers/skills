---
name: coral-memory
description: "**已弃用** — 请改用 `persistent-agent-memory`。此功能已被 `persistent-agent-memory` 取代（可通过 `clawhub install persistent-agent-memory` 安装）。"
metadata:
  {
    "openclaw": {
      "requires": { "env": ["CORAL_API_KEY"], "bins": ["curl", "python3"] },
      "primaryEnv": "CORAL_API_KEY",
      "homepage": "https://coralbricks.ai",
      "privacyPolicy": "https://www.coralbricks.ai/privacy",
      "emoji": "🧠",
    },
  }
---
# Coral Memory — 已弃用

**此技能已被弃用。** 请改用 **persistent-agent-memory**：

```bash
clawhub install persistent-agent-memory
```

`persistent-agent-memory` 技能提供了相同的功能（按含义存储、检索和删除“记忆”），并包含了最新的改进。

有关更多详细信息，请参阅 [AI 代理的持久化代理内存](https://www.coralbricks.ai/blog/persistent-memory-openclaw)。