---
name: shell-security-ultimate
version: 2.2.1
description: "在代理程序执行每个shell命令之前，将其分类为“SAFE”（安全）、“WARN”（警告）或“CRIT”（严重）。"
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
    notes:
      security: "Instruction-only skill that classifies shell commands before execution — it does NOT execute commands itself. Teaches the agent to label every command as SAFE, WARN, or CRIT and enforce approval gates. No binaries, no network calls, no credentials. All logic runs within the existing LLM context."
---
# Shell 安全终极版（Shell Security Ultimate）

您的代理程序拥有 root 权限。它执行的每一个命令都可能带来风险——只需一次错误的判断，就可能导致执行 `rm -rf /` 或 `curl | bash` 等危险操作（这些命令可能来自陌生人的代码库）。

这款工具将防止此类情况的发生。

## 工作原理

在执行之前，每个 shell 命令都会被分类：

- 🟢 **安全（SAFE）**：仅具有读取权限，不会对系统造成任何损害。可以正常执行。
- 🟡 **警告（WARN）**：可能修改系统状态。系统会记录该命令并标记为需要关注。
- 🔴 **危险（CRIT）**：可能对系统造成破坏性或不可逆的影响。在您明确允许之前，此类命令将被阻止。

没有任何命令会在未经分类的情况下被执行。系统不会悄悄地执行 `chmod 777` 来更改文件权限，也不会默默地执行 `dd if=/dev/zero` 来清除磁盘数据。您的代理程序不会因为误解任务而意外地发送您的 SSH 密钥，不会随意格式化磁盘，更不会执行 `DROP TABLE users` 等破坏性操作。

## 主要功能：

- **每次执行命令前都会进行分类**。
- **详细的操作日志**：让您清楚地了解每个命令的执行内容及其被允许的原因。
- **全面的控制权限**：您可以批准、拒绝或升级任何级别的操作。

## 适用对象：

任何将 AI 代理程序赋予 shell 权限并希望安心睡觉的用户。

*欢迎克隆、分支或修改该项目，然后让它成为您自己的工具。*

👉 查看完整项目：[github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)