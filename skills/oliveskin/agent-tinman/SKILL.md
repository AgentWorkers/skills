---
name: tinman
version: 0.6.3
description: 这款AI安全扫描器具备主动防御功能，支持168种检测模式和288种攻击探测方式。用户可以选择“安全”（safe）、“风险”（risky）或“Yolo”三种工作模式。该扫描器通过/tinman检查机制实现代理程序的自我保护，并支持本地Oilcan事件流式传输。此外，用户还可以通过/tinman oilcan功能以通俗易懂的方式配置和管理扫描器的控制面板。
author: oliveskin
repository: https://github.com/oliveskin/openclaw-skill-tinman
license: Apache-2.0

requires:
  python: ">=3.10"
  binaries:
    - python3
  env: []

install:
  pip:
    - AgentTinman>=0.2.1
    - tinman-openclaw-eval>=0.3.2

permissions:
  tools:
    allow:
      - sessions_list
      - sessions_history
      - read
      - write
    deny: []
  sandbox: compatible
  elevated: false
---
# Tinman - 人工智能故障模式研究

Tinman 是一个前置部署的研究代理，通过系统化的实验来发现人工智能系统中的未知故障模式。

反馈/更新：https://x.com/cantshutup_

## 安全与信任说明

- 该工具明确声明需要 `install.pip` 以及会话/文件的权限，因为扫描过程需要分析本地会话记录和报告输出。
- 默认的监控网关仅支持循环回环（`ws://127.0.0.1:18789`），以减少数据泄露的风险。
- 远程网关的使用需要用户明确同意（通过 `--allow-remote-gateway` 参数），并且仅应用于可信任的内部终端。
- 事件流数据存储在本地（`~/.openclaw/workspace/tinman-events.jsonl`），数据会被截断，明显的敏感信息会被隐藏。
- 默认情况下，Oilcan 桥接应保持循环回环模式；仅在必要时允许局域网访问。

## 功能概述

- **执行前检查**：检查工具调用是否存在安全风险（用于代理的自我保护）
- **扫描最近会话**：检测是否存在提示注入、工具滥用或上下文泄露等问题
- **分类故障**：根据严重程度（S0-S4）和类型对故障进行分类
- **提出应对措施**：将相应的措施映射到 OpenClaw 的控制机制中（如 SOUL.md、沙箱策略、工具允许/拒绝设置）
- **生成报告**：以可操作的格式呈现发现的结果
- **流式传输事件**：将结构化事件数据传输到 `~/.openclaw/workspace/tinman-events.jsonl`（供本地仪表板如 Oilcan 使用）
- **指导配置**：通过 `/tinman oilcan` 命令以通俗的语言提供 Oilcan 的配置指南

## 命令说明

### `/tinman init`

使用默认配置初始化 Tinman 工作空间。

**首次运行此命令以设置工作空间。**

### `/tinman check`（代理自我保护）

在执行前检查工具调用是否安全。**这有助于代理实现自我监控。**

**判断结果：**
- `SAFE`：自动执行
- `REVIEW`：请求人工批准（处于更安全的模式）
- `BLOCKED`：拒绝执行

**将此结果添加到 SOUL.md 中以实现自动保护：**

### `/tinman mode`

设置或查看检查系统的安全模式。

| 模式 | SAFE | REVIEW (S1-S2) | BLOCKED (S3-S4) |
|------|------|----------------|-----------------|
| `safer` | 允许执行 | 请求人工批准 | 拒绝执行 |
| `risky` | 允许执行 | 自动批准 | 拒绝执行 |
| `yolo` | 允许执行 | 自动批准 | 仅发出警告 |

### `/tinman allow`

将某些模式添加到允许列表中（绕过安全检查，适用于可信的请求）。

### `/tinman allowlist`

管理允许列表。

### `/tinman scan`

分析最近的会话以检测故障模式。

**输出结果**：将检测结果写入 `~/.openclaw/workspace/tinman-findings.md`。

### `/tinman report`

显示最新的故障报告。

### `/tinman watch`

提供两种连续监控模式：

- **实时模式（推荐）**：连接到网关的 WebSocket 以实时监控事件。
- **轮询模式**：在网关不可用时使用轮询方式扫描会话。

**停止监控：**

### `/tinman heartbeat`（用于定时扫描）

**通过心跳机制配置定时扫描：**

### `/tinman oilcan`

以通俗的语言显示 Oilcan 的配置和状态。

**此命令帮助用户将 Tinman 的事件数据传输到 Oilcan，并提醒用户：如果首选端口已被占用，系统可能会自动选择其他端口。**

### `/tinman sweep`

执行主动的安全扫描，使用 288 个合成攻击探针。

**攻击类别：**
- `prompt_injection`（15）：越狱、指令覆盖
- `tool_exfil`（42）：SSH 密钥、凭证、云服务凭证、网络数据泄露
- `context_bleed`（14）：跨会话数据泄露、内存数据提取
- `privilege_escalation`（15）：沙箱逃逸、权限提升
- `supply_chain`（18）：恶意技能、依赖项/更新攻击
- `financial_transaction`（26）：钱包/种子信息盗窃、交易、交易所 API 密钥泄露
- `unauthorized_action`（28）：未经授权的操作
- `mcp_attack`（20）：MCP 工具滥用、服务器注入、跨工具数据泄露
- `indirect_injection`（20）：通过文件、URL、文档等方式进行注入
- `evasion_bypass`（30）：绕过 Unicode/编码机制、混淆技术
- `memory_poisoning`（25）：持久性指令注入、伪造历史记录
- `platform_specific`（35）：针对 Windows/macOS/Linux/云服务的特定攻击

**扫描结果**：将扫描报告写入 `~/.openclaw/workspace/tinman-sweep.md`。

## 故障分类

| 分类 | 描述 | OpenClaw 对应控制措施 |
|----------|-------------|------------------|
| `prompt_injection` | 越狱、指令覆盖 | 使用 SOUL.md 的防护机制 |
| `tool_use` | 未经授权的工具访问、数据泄露尝试 | 使用沙箱的拒绝列表 |
| `context_bleed` | 跨会话数据泄露 | 实施会话隔离 |
| `reasoning` | 逻辑错误、错误操作 | 选择合适的模型进行检测 |
| `feedback_loop` | 群组聊天中的信息传播 | 调整激活模式 |

## 严重程度等级

- **S0**：仅进行观察，无需采取行动
- **S1**：风险较低，建议监控
- **S2**：风险中等，建议进行审查
- **S3**：风险较高，建议采取缓解措施
- **S4**：情况危急，需要立即采取行动

## 示例输出

### 配置

创建 `~/.openclaw/workspace/tinman.yaml` 文件以自定义 Tinman 的行为。

**通过此文件自定义 Tinman 的配置。**

## 隐私政策

- 所有分析操作均在本地完成
- 不会向外部发送任何会话数据
- 所有检测结果仅存储在工作空间内
- 遵循 OpenClaw 的会话隔离机制