---
name: ectoclaw
description: >
  OpenClaw代理的加密审计账本和AI防火墙：  
  该系统会记录每个代理的所有操作（消息、技能、使用的工具、插件、内存状态以及模型数据），并将这些信息存储在一个不可篡改的、基于哈希链的账本中。这些记录会附带Ed25519签名和Merkle证明以确保数据完整性。系统还配备了策略引擎，用于定义数据块的创建规则、数据内容的审核规则、标记规则以及审批流程。用户可以导出合规性报告和验证结果。该解决方案能够有效防范命令注入攻击、凭证窃取以及未经授权的代理行为。
homepage: https://github.com/EctoSpace/EctoClaw
metadata:
  openclaw:
    requires:
      bins: []
    install:
      - id: node
        kind: node
        package: ectoclaw
        bins: ["ectoclaw"]
        label: "Install EctoClaw (npm)"
    primaryEnv: ECTOCLAW_URL
tags:
  - security
  - audit
  - compliance
  - cryptography
  - governance
  - firewall
  - policy
  - forensics
  - agent-security
  - audit-trail
---
# EctoClaw — 专为 OpenClaw 设计的加密审计日志系统与 AI 防火墙

## 配置

- **ECTOCLAW_URL**: EctoClaw 服务器的 URL（默认值：http://localhost:3210）

> 源代码和安装脚本完全开源，可在 [https://github.com/EctoSpace/EctoClaw](https://github.com/EctoSpace/EctoClaw) 获取。

### 安全性 / 认证

- EctoClaw 设计为在本地主机或您控制的私有网络中运行。
- 如果您需要将 ECTOCLAW_URL 公开到外部网络，请为其设置自己的认证和访问控制机制（例如，使用带认证功能的反向代理）。
- **严禁** 将 ECTOCLAW_URL 指向不受信任的第三方主机，因为审计日志可能包含敏感信息、工具输出和内存内容。

## 命令

### 列出审计会话
- 当用户请求查看审计会话时，列出最近的会话或检查审计历史记录：
  - 调用 `GET {ECTOCLAW_URL}/api/sessions?limit=10`
  - 响应结果将以可读的列表形式显示会话 ID、状态、事件数量和目标。

### 创建审计会话
- 当用户请求开始新的审计或跟踪操作时：
  - 调用 `POST {ECTOCLAW_URL}/api/sessions`，并传入 JSON 格式的数据：`{"goal": "<用户指定的目标>"}``
  - 可选地添加 `policy_name` 以关联策略：`{"goal": "<目标>", "policy_name": "<策略名称>"}``
  - 返回会话 ID、目标哈希值和公钥。

### 记录事件
- 当用户需要记录操作或跟踪具体行为时：
  - 调用 `POST {ECTOCLAW_URL}/api/sessions/{session_id}/events`
  - JSON 格式的数据包含事件类型（`MessageReceived`、`MessageSent`、`SkillInvoked` 等）和事件详细信息
  - 支持的事件类型示例：`MessageReceived`、`MessageSent`、`SkillInvoked`、`SkillResult`、`ToolCall`、`ToolResult`、`PluginAction`、`PluginResult`、`ModelRequest`、`ModelResponse`、`MemoryStore`、`MemoryRecall`、`ApprovalRequired`、`ApprovalDecision`
  - 返回事件内容哈希值、序列号和 Ed25519 签名。

### 验证会话完整性
- 当用户需要验证会话或检查哈希链的完整性时：
  - 调用 `GET {ECTOCLAW_URL}/api/sessions/{session_id}/verify`
  - 返回哈希链是否有效以及已检查的事件数量。

### 获取会话详情
- 当用户需要查询特定会话的详细信息时：
  - 调用 `GET {ECTOCLAW_URL}/api/sessions/{session_id}`
  - 显示会话的完整信息，包括目标、目标哈希值、状态、策略、时间戳、事件数量和公钥。

### 封锁会话
- 当用户需要完成或关闭审计会话时：
  - 调用 `POST {ECTOCLAW_URL}/api/sessions/{session_id}/seal`
  - 返回会话的锁定状态和最终的 Merkle 根哈希值。

### 获取审计指标
- 当用户需要审计指标或统计信息时：
  - 调用 `GET {ECTOCLAW_URL}/api/metrics`
  - 显示总会话数、活跃会话数、已锁定会话数、总事件数以及事件类型分布。

### 获取合规性报告
- 当用户需要合规性报告或 Merkle 证明时：
  - 调用 `GET {ECTOCLAW_URL}/api/sessions/{session_id}/compliance`
  - 显示 Merkle 根哈希值和事件哈希值。

### 获取特定事件的 Merkle 证明
- 当用户需要验证某个事件是否存在于审计日志中时：
  - 调用 `GET {ECTOCLAW_URL}/api/sessions/{session_id}/merkle?leaf={event_index}`
  - 显示 Merkle 根哈希值和事件包含路径。

### 验证 Merkle 证明
- 当用户提供 Merkle 证明以供验证时：
  - 调用 `POST {ECTOCLAW_URL}/api/merkle/verify` 并传入证明数据
  - 返回证明的有效性。

### 生成审计报告
- 当用户需要完整的审计报告时：
  - 调用 `GET {ECTOCLAW_URL}/api/reports/{session_id}?format=json`
  - 若需要 HTML 格式的报告：`GET {ECTOCLAW_URL}/api/reports/{session_id}?format=html`
  - 提供包含事件和验证状态的完整会话报告。

### 列出策略
- 当用户需要查看当前配置的策略时：
  - 调用 `GET {ECTOCLAW_URL}/api/policies`
  - 显示每个策略的名称及其配置信息。

### 创建或更新策略
- 当用户需要设置审计规则时：
  - 调用 `PUT {ECTOCLAW_URL}/api/policies/{name}`，并传入策略配置（TOML 格式）
  - 返回策略的保存状态。

### 实时监控事件流
- 当用户需要实时监控审计活动时：
  - 连接到 `GET {ECTOCLAW_URL}/api/stream`（服务器发送的事件）
  - 实时接收并显示发生的事件。

### 检查服务器状态
- 当用户需要确认 EctoClaw 是否正在运行时：
  - 调用 `GET {ECTOCLAW_URL}/health`
  - 返回服务器的状态、版本和名称。

## EctoClaw 的记录内容

所有 OpenClaw 的生命周期事件都会被记录为带有签名的日志条目：

| **事件类型** | **记录内容** |
|------------|-------------|
| **MessageReceived** | 来自任何渠道的入站消息 |
| **MessageSent** | 代理发出的出站响应 |
| **SkillInvoked** | 调用技能及其参数 |
| **SkillResult** | 技能执行结果 |
| **ToolCall** | 调用外部工具（shell、文件、HTTP、浏览器） |
| **ToolResult** | 工具执行结果和观察数据 |
| **PluginAction** | 插件生命周期事件 |
| **ModelRequest** | 基于提示的 LLM API 调用 |
| **ModelResponse** | LLM 的响应结果 |
| **MemoryStore** | 内存读写操作 |
| **MemoryRecall** | 内存读取操作 |
| **PolicyViolation** | 被阻止或标记的操作 |
| **ApprovalRequired** | 需要人工审核的操作 |
| **ApprovalDecision** | 人工审核结果 |
| **SessionSeal** | 使用 Merkle 根哈希值完成的会话 |
| **KeyRotation** | Ed25519 签名密钥的更新 |

> 请仅将数据发送到您自己操作且信任的 EctoClaw 实例。请将审计日志视为高度敏感的信息，并采取相应的保护措施。

## 加密完整性

所有事件都经过以下处理：
1. **SHA-256 哈希处理**：每个事件的哈希值都包含前一个事件的哈希值。
2. **Ed25519 签名**：每个事件和每个会话都带有防篡改的数字签名。
3. **Merkle 树结构**：支持对任意单个事件进行 O(log n) 复杂度的包含性验证。

## 快速入门（适用于新用户）

```bash
npm install ectoclaw
npx ectoclaw serve --dev
# Dashboard: http://localhost:3210/dashboard/
```

## 链接

- [GitHub 仓库](https://github.com/EctoSpace/EctoClaw)
- [NPM 包](https://www.npmjs.com/package/ectoclaw)
- [官方网站](https://ectospace.com/EctoClaw)
- [EctoLedger（Rust 企业版）](https://github.com/EctoSpace/EctoLedger)