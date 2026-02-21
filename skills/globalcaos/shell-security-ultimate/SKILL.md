---
name: shell-security-ultimate
version: 2.2.0
description: "在代理程序执行每个shell命令之前，将其分类为“SAFE”、“WARN”或“CRIT”。"
metadata:
  openclaw:
    owner: kn7623hrcwt6rg73a67xw3wyx580asdw
    category: security
    tags:
      - shell
      - command-classification
      - risk-management
      - agent-safety
    license: MIT
---
# Shell Security Ultimate

您的代理拥有 root 权限。它执行的每一个命令都可能因为错误的判断而导致严重的后果，比如执行 `rm -rf /` 或从陌生人提供的仓库中执行 `curl | bash`。

这款工具将防止这种情况的发生。

## 工作原理

在执行之前，每个 shell 命令都会被分类：

- 🟢 **安全** — 仅具有读取权限，不会造成任何危害。可以正常执行。
- 🟡 **警告** — 可能会修改系统状态。系统会记录该命令并标记为危险操作。
- 🔴 **危险** — 具有破坏性或不可逆的影响。在您明确允许之前，此类命令将被阻止。

没有任何命令会在未经分类的情况下被执行。系统不会悄悄地执行 `chmod 777` 或 `dd if=/dev/zero` 等操作。您的代理不会不小心将您的 SSH 密钥发送出去，也不会因为误解任务而执行删除用户表 (`DROP TABLE users`) 等操作。

## 使用收益

- 每个命令在执行前都会被进行分类。
- 详细的操作日志记录，让您清楚地了解哪些命令被执行以及为什么被允许执行。
- 全面的控制权限：您可以批准、拒绝或升级任何操作。

## 适用对象

任何为 AI 代理提供 shell 权限并希望安心睡觉的人。

*克隆它、修改它，或者将其据为己有吧。*

👉 探索完整项目：[github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)