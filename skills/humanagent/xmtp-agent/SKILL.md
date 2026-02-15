---
name: xmtp-agents
description: >
  Building and extending XMTP agents with the Agent SDK.
  Use when: (1) creating or configuring an XMTP agent, (2) implementing agent features (commands, attachments, reactions, groups, transactions, inline actions, or domain resolution).
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP代理

在XMTP网络上构建基于事件驱动的消息代理。此技能是入门级内容；如需实现特定功能，请使用以下子技能。

## 适用场景

- 新建或配置XMTP代理时
- 需要添加功能时：命令处理、附件处理、响应机制、群组管理、支付功能、内联操作或地址/域名解析等

## 子技能

| 子技能 | 适用场景 |
|---------|---------|
| **building-agents** | 代理设置、环境变量配置、文本处理、生命周期事件管理、中间件开发 |
| **handling-commands** | 命令解析、验证器、消息过滤、类型检查 |
| **handling-attachments** | 文件发送/接收、远程附件处理、上传至存储系统 |
| **sending-reactions** | 响应消息的发送与接收、响应逻辑设计 |
| **managing-groups** | 群组创建、成员添加、角色分配、安装欢迎信息设置 |
| **handling-transactions** | USDC转账处理、账户余额查询、交易记录管理 |
| **creating-inline-actions** | 内联操作实现、确认/选择辅助功能、配置菜单设计 |
| **resolving-domains** | 地址解析、Farcaster用户资料处理、提及内容提取 |

## 使用方法

1. 选择与任务匹配的子技能（例如：处理命令 → 使用`handling-commands`）。
2. 阅读该子技能对应的`SKILL.md`文件及其`rules/`文件以获取详细步骤。
3. 如需了解SDK或API的详细信息，请参考`xmtp-docs`技能（通过索引查找具体页面）。

## 快速入门

1. 安装代理SDK。
2. 根据环境变量创建代理实例。
3. 使用`building-agents`子技能中的方法处理文本消息。
4. 对于命令处理、附件处理、响应机制、群组管理、交易处理、内联操作或地址解析等功能，分别使用相应的子技能。

```bash
npm install @xmtp/agent-sdk
```