---
name: samma-suit
description: 为你的 OpenClaw 代理添加 8 层安全治理机制：预算控制、权限管理、审计日志记录、紧急停止功能（kill switch）、身份验证与签名、技能审核、进程隔离以及网关保护。
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      env: ["SAMMA_API_KEY"]
      bins: []
    primaryEnv: "SAMMA_API_KEY"
user-invocable: true
command-dispatch: prompt
---

# Sammā Suit — OpenClaw的安全治理框架

您将帮助用户安装和配置Sammā Suit，这是一个开源的安全框架，它为OpenClaw添加了8层强制性的治理机制，这些机制以生命周期钩子的形式实现。

## 功能介绍

Sammā Suit通过拦截OpenClaw的插件钩子来执行以下安全控制：
- **NIRVANA**（涅槃）：当代理程序被终止时，会阻止所有操作。
- **DHARMA**（佛法）：检查工具的使用权限是否在允许的范围内。
- **SANGHA**（僧团）：通过允许列表和AST扫描来阻止未经批准的技能的使用。
- **KARMA**（因果报应）：为每个代理设置每月的支出上限。
- **BODHI**（菩提）：为每个代理设置超时限制、令牌限制和资源限制。
- **METTA**（慈悲）：对所有出站消息进行Ed25519加密签名。
- **SILA**（戒律）：记录所有的工具调用、消息和会话事件。

## 安装方法

运行：