---
name: tinman
version: 0.6.3
description: 这款AI安全扫描器具备主动防御功能，支持168种检测模式和288种攻击探测方式。用户可以选择“安全”（safe）、“风险”（risky）或“Yolo”三种工作模式。该扫描器通过/tinman check机制实现代理程序的自我保护，并支持本地Oilcan事件流式传输。此外，用户还可以通过/tinman oilcan功能以通俗易懂的方式配置和管理扫描器的控制面板。
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
# Tinman – 人工智能故障模式研究工具

Tinman 是一个用于发现人工智能系统中未知故障模式的前置部署研究代理，它通过系统的实验方法来执行这些任务。

## 安全与信任说明

- 该工具明确声明需要 `install.pip` 以及相应的会话/文件权限，因为扫描过程需要分析本地的会话记录和报告输出。
- 默认的监控网关仅允许本地访问（`ws://127.0.0.1:18789`），以减少数据泄露的风险。
- 远程网关的使用需要用户明确授权（通过 `--allow-remote-gateway` 参数），并且仅应用于可信的内部终端。
- 事件流数据存储在本地文件 `~/.openclaw/workspace/tinman-events.jsonl` 中，数据会被截断处理，敏感信息会被隐藏。
- 默认情况下，Oilcan 桥接应保持本地访问模式；只有在必要时才允许远程访问。

## 主要功能

- **执行前检查**：检查工具调用是否存在安全风险（实现代理的自我保护机制）。
- **扫描近期会话**：检测是否存在命令注入、工具滥用或数据泄露等行为。
- **分类故障**：根据故障的严重程度（S0-S4）和类型进行分类。
- **提出缓解措施**：将相应的措施映射到 OpenClaw 的控制策略中（如 SOUL.md、沙箱策略、工具访问权限设置）。
- **生成报告**：以易于操作的格式呈现检测结果。
- **事件流传输**：将本地事件数据传输到 `~/.openclaw/workspace/tinman-events.jsonl` 文件中，以便在本地仪表板（如 Oilcan）中查看。
- **提供指导**：通过 `/tinman oilcan` 命令以通俗的语言展示本地 Oilcan 的配置状态。

## 命令列表

### `/tinman init`  
使用默认配置初始化 Tinman 工作空间。

**首次运行此命令以设置工作空间。**

### `/tinman check`（代理自我保护）  
在执行工具调用前检查其安全性。**这有助于代理实现自我监控。**

**判断结果：**  
- `SAFE`：允许自动执行  
- `REVIEW`：请求人工审核（处于更安全的模式）  
- `BLOCKED`：拒绝执行该操作  

**将此功能添加到 SOUL.md 中以实现自动化保护：**  

### `/tinman mode`  
设置或查看检查系统的安全模式。

| 模式 | SAFE | REVIEW (S1-S2) | BLOCKED (S3-S4) |
|------|------|----------------|-----------------|
| `safer` | 允许执行 | 请求人工审核 | 取消执行 |
| `risky` | 允许执行 | 自动批准 | 取消执行 |
| `yolo` | 允许执行 | 自动批准 | 仅发出警告 |

### `/tinman allow`  
将某些行为添加到允许列表中（从而绕过安全检查）。  

### `/tinman allowlist`  
管理允许列表的内容。  

### `/tinman scan`  
分析近期会话以检测故障模式。  
**输出结果**：将检测结果保存到 `~/.openclaw/workspace/tinman-findings.md` 文件中。  

### `/tinman report`  
显示最新的故障检测报告。  

### `/tinman watch`  
提供持续监控功能，包含两种模式：  
- **实时模式**（推荐）：通过 WebSocket 连接到网关以实现即时事件监控。  
- **轮询模式**：在网关不可用时使用轮询方式扫描会话。  

**停止监控：**  
使用相应命令停止监控。  

### `/tinman oilcan`  
以通俗的语言展示本地 Oilcan 的配置状态。  
此命令帮助用户将 Tinman 的事件数据传输到 Oilcan，并提醒用户：如果首选端口已被占用，系统可能会自动选择其他端口。  

### `/tinman sweep`  
执行主动的安全扫描，使用 288 个合成攻击探针进行检测。  
**攻击类别：**  
- `prompt_injection`（15）：命令注入（如越狱、指令覆盖）  
- `tool_exfil`（42）：窃取 SSH 密钥、凭证、云服务凭证等  
- `context_bleed`（14）：跨会话数据泄露  
- `privilege_escalation`（15）：权限提升  
- `supply_chain`（18）：恶意攻击、依赖项/更新攻击  
- `financial_transaction`（26）：钱包/种子信息盗窃、交易相关攻击  
- `unauthorized_action`（28）：未经授权的操作  
- `mcp_attack`（20）：MCP 工具滥用、服务器注入  
- `indirect_injection`（20）：通过文件、URL、文档等方式进行攻击  
- `evasion_bypass`（30）：绕过编码规则、混淆技术  
- `memory_poisoning`（25）：持久性指令注入、伪造历史记录  
- `platform_specific`（35）：针对 Windows/macOS/Linux/云平台的特定攻击  

**扫描结果**：将扫描报告保存到 `~/.openclaw/workspace/tinman-sweep.md` 文件中。  

## 故障分类  
| 分类 | 描述 | OpenClaw 控制措施 |
|----------|-------------|------------------|
| `prompt_injection` | 命令注入（如越狱、指令覆盖） | 使用 SOUL.md 的防护机制 |
| `tool_use` | 未经授权的工具访问、数据窃取尝试 | 使用沙箱的拒绝列表进行限制 |
| `context_bleed` | 跨会话数据泄露 | 实施会话隔离措施 |
| `reasoning` | 逻辑错误、异常行为 | 选择合适的模型进行检测 |
| `feedback_loop` | 群组聊天中的恶意传播 | 调整激活模式 |

## 故障严重程度  
- **S0**：仅进行观察，无需采取行动  
- **S1**：风险较低，建议监控  
- **S2**：风险中等，建议进行审查  
- **S3**：风险较高，建议采取缓解措施  
- **S4**：情况危急，需要立即采取行动  

## 示例输出  
（具体输出内容根据实际情况生成。）

## 配置  
创建 `~/.openclaw/workspace/tinman.yaml` 文件以自定义 Tinman 的行为。  

## 隐私政策  
- 所有分析操作均在本地完成  
- 无会话数据会被发送到外部  
- 检测结果仅存储在工作空间内  
- 遵守 OpenClaw 的会话隔离规则  

## 反馈/联系方式  
[twitter](https://x.com/cantshutup/)  
[Github](https://github.com/oliveskin/)