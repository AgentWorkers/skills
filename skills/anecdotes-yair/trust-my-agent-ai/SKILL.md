---
name: trustmyagent
description: 🛡️ TrustMyAgent – 专为AI代理设计的安全态势监控工具。该工具会在14个域名范围内执行41项无状态检查，并计算出代理的信任评分（0-100分）。支持仅本地运行模式（无需网络请求）和预测试模式（在正式发送请求前进行预览）。
version: 1.0
author: Anecdotes AI Labs
license: MIT
homepage: https://www.trustmyagent.ai
repository: https://github.com/Anecdotes-Yair/trust-my-agent-ai
metadata:
  openclaw:
    emoji: "🛡️"
    category: security
    tags:
      - security
      - compliance
      - monitoring
      - trust
    requires:
      bins:
        - openssl
    shared: true
    install:
      - id: python3
        kind: brew
        formula: python3
        os:
          - darwin
        bins:
          - python3
        label: "Python 3 (Homebrew)"
      - id: python3-apt
        kind: node
        os:
          - linux
        bins:
          - python3
        label: "Python 3 (system)"
---
# 🛡️ TrustMyAgent - 安全代理

**专为AI代理设计的状态less安全态势监控工具。**

TrustMyAgent会在主机机器上对14个领域执行41项只读安全检查，计算出信任评分（0-100分），并可选地将结果报告到公共的[信任中心](https://www.trustmyagent.ai/trust-center.html)仪表板。该工具是完全无状态的——不会写入任何文件，不会保留任何状态信息，也不会在未经用户明确同意的情况下安装任何后台进程。

> **开源**：所有检查逻辑都位于`run.py`文件和`checks/*.json`文件中。完整源代码可在[github.com/Anecdotes-Yair/trust-my-agent-ai](https://github.com/Anecdotes-Yair/trust-my-agent-ai)查看。

## 设置

当用户请求设置TrustMyAgent时，请引导他们完成以下步骤。**在执行每个步骤之前，先向用户展示步骤内容并等待他们的确认**。切勿默默运行命令或跳过用户的确认。

### 第1步：验证Python 3的安装

检查是否已安装Python 3：

```bash
python3 --version
```

如果未安装Python 3，请在安装前询问用户：
- macOS：`brew install python3`
- Linux：`sudo apt-get install python3` 或 `sudo apk add python3`

### 第2步：进行模拟评估

首先以**模拟模式**运行安全评估，以便用户在数据离开机器之前能够查看结果：

```bash
python3 {baseDir}/run.py --dry-run
```

此步骤会执行所有41项检查，并打印出**实际会发送的**遥测数据包内容——但实际不会发送任何数据。向用户展示结果，并让他们进行审查：
- 信任评分和等级
- 哪些检查通过了，哪些失败了
- 实际会传输的JSON数据包内容

询问用户：“您是否希望将此报告发送到信任中心仪表板？还是选择仅在本机模式下运行（不进行网络传输），或者调整任何设置？”

### 第3步：运行完整评估（需用户同意）

如果用户同意发送遥测数据：

```bash
python3 {baseDir}/run.py
```

如果用户选择仅在本机模式下运行（不发送遥测数据）：

```bash
python3 {baseDir}/run.py --local-only
```

### 第4步：安排定期评估（可选）

询问用户是否希望安排自动评估。如果同意，建议使用cron作业来设置定时任务。具体命令因代理平台而异：

**OpenClaw代理：**
```bash
openclaw cron add --name "🛡️ TrustMyAgent" --cron "*/15 * * * *" --session agent:security:main --message "Run security assessment: python3 {baseDir}/run.py"
```

**其他代理/独立代理：**
```bash
# Add to system crontab (runs every 15 minutes)
(crontab -l 2>/dev/null; echo "*/15 * * * * python3 {baseDir}/run.py --quiet") | crontab -
```

> 用户可以选择任何时间间隔，或者完全跳过定时设置。

## 发送的数据

当启用遥测功能（默认设置）时，以下数据将通过HTTPS POST方式发送到`https://www.trustmyagent.ai/api/telemetry`：

| 字段 | 举例 | 用途 |
|-------|---------|---------|
| `agent.id` | `sha256(hostname)` | 唯一标识符（基于主机名哈希生成，而非主机名本身） |
| `agent.name` | `"My Agent"` | 显示名称（来自IDENTITY.md文件或环境变量） |
| `agent.platform` | `"darwin"` | 操作系统类型（darwin/Linux） |
| `agent.detected_env` | `"macos_arm64"` | 运行时环境标签 |
| `posture.trust_tier` | `"HIGH"` | 计算出的信任等级 |
| `posture.overall_score` | `92` | 数字评分（0-100分） |
| `results[]` | `{check_id, passed, status}` | 每项检查的通过/失败状态 |
| `detections[]` | `{check_id, severity, risk}` | 失败的检查及其风险等级 |

**不发送的数据包括：**
- 任何文件内容、路径或目录列表
- 环境变量值（仅检测是否存在类似秘密的字符串）
- 进程名称、PID或命令行内容
- 网络流量、IP地址或主机名
- 凭据、令牌或API密钥
- 对话记录或用户数据

遥测端点和所有检查逻辑都是开源的。您可以使用`--dry-run`模式来验证实际发送的数据内容。

### 选择不发送遥测数据

使用`--local-only`选项可以在本地运行所有检查，而不会进行任何网络请求：

```bash
python3 {baseDir}/run.py --local-only
```

这样可以在本地完成完整的安全评估，而不会发送任何数据。

## 工作原理

1. `run.py`在主机上执行——可以通过手动触发、cron任务或代理的心跳信号来启动。
2. 使用bash命令和Python传感器执行41项安全检查（所有操作均为只读）。
3. 根据检查的通过/失败结果及风险等级计算信任评分（0-100分）。
4. 结果会在本地终端中显示。
5. （可选）通过HTTPS将结果发送到信任中心仪表板。

本地不会写入任何文件，也不会在代理机器上保留任何状态信息。

## 安全检查领域

| 领域 | 检查项目 | 重点检查内容 |
|--------|--------|-------|
| **物理环境** | PHY-001至PHY-005 | 磁盘加密、容器隔离、非root权限执行 |
| **网络** | NET-001至NET-005 | 危险端口、TLS/SSL、DNS、证书 |
| **秘密信息** | SEC-001至SEC-005, MSG-005 | 环境变量中的秘密信息、云服务凭证、私钥、对话内容泄露 |
| **代码** | COD-001至COD-004 | Git代码安全、代码库中是否包含秘密信息 |
| **日志** | LOG-001至LOG-004 | 系统日志记录、审计准备情况 |
| **技能** | SKL-001至SKL-005, MSG-001, MSG-003 | 技能清单、MCP服务器的信任状态 |
| **完整性** | INT-001至INT-005, MSG-002, MSG-006 | 后门程序、浏览器滥用行为、可疑工具调用、URL安全性 |
| **社交安全** | SOC-001至SOC-006, MSG-004 | 操作记录、会话透明度、Moltbook系统的完整性、所有者信誉 |
| **事件预防** | INC-001至INC-005 | 进程创建、系统负载、端口扫描 |
| **节点安全** | NODE-001至NODE-005 | 远程执行权限、令牌权限、执行允许列表 |
| **媒体安全** | MEDIA-002至MEDIA-003 | 临时目录权限、文件类型验证 |
| **网关安全** | GATEWAY-001至GATEWAY-002 | 绑定地址、身份验证 |
| **身份安全** | IDENTITY-001至IDENTITY-002 | DM（Direct Message）配对允许列表、群组聊天允许列表 |
| **子代理安全** | SUBAGENT-001至SUBAGENT-002 | 并发限制、目标允许列表 |

## 检查类型

### Bash检查（20项）
定义在`checks/openclaw_checks.json`文件中。每项检查都会运行一个shell命令，并根据`pass_condition`（如`equals`、`contains`、`not_contains`、`exit_code_zero`等）来评估结果。

### Python/基于消息的检查（21项）
定义在`checks/message_checks.json`和`checks/nodes_media_checks.json`文件中。这些检查通过编程方式分析秘密信息、会话记录、MCP配置文件、技能清单等。

### 平台支持
系统会自动识别macOS和Linux，并使用相应的命令。如果平台不支持某些检查，可以通过`"platforms": ["linux"]`来跳过这些检查。

## 信任等级

| 等级 | 评分 | 标签 |
|------|-------|-------|
| HIGH | 90-100 | 可用于业务 |
| MEDIUM | 70-89 | 需要审查 |
| LOW | 50-69 | 风险较高 |
| UNTRUSTED | 0-49 | 存在严重安全漏洞 |

任何严重等级的失败都会使评分上限降至49（UNTRUSTED）。如果有三个或更多高严重等级的失败，评分上限会降至69（LOW）。

## 命令行选项

| 标志 | 说明 |
|------|-------------|
| `--checks`, `-c` | 自定义检查JSON文件的路径 |
| `--timeout`, `-t` | 每项检查的超时时间（默认：30秒） |
| `--quiet`, `-q` | 最小化输出信息 |
| `--json`, `-j` | 将输出格式化为JSON并输出到标准输出 |
| `--dry-run` | 运行所有检查并显示遥测数据包，但不发送 |
| `--local-only` | 在本地运行所有检查，不进行网络请求 |
| `--no-notify` | 跳过检测结果的代理通知 |

## 配置选项

| 来源 | 说明 | 默认值 |
|---------------------|-------------|---------|
| `IDENTITY.md` | 代理的显示名称（从`# Name`部分读取） | `"Agent"` |
| `OPENCLAW_AGENT_NAME` 环境变量 | 覆盖IDENTITY.md中的名称 | — |
| `OPENCLAW_AGENT_ID` 环境变量 | 代理标识符 | 主机名的SHA256哈希值 |
| `TRUSTMYAGENT_TELEMETRY_URL` 环境变量 | 服务器端点 | `https://www.trustmyagent.ai/api/telemetry` |

## 相关文件

```
Agent/
├── SKILL.md                        # This file
├── run.py                          # Main entry point (stateless runner)
└── checks/
    ├── openclaw_checks.json        # 20 bash-based security checks
    ├── message_checks.json         # 10 Python-based message/secret sensors
    ├── nodes_media_checks.json     # 11 infrastructure checks
    └── detection_kb.json           # Risk descriptions and remediation guidance
```

## 架构

```
┌─────────────────┐                                 ┌──────────────────┐
│   Agent Host     │      POST /api/telemetry        │ 🛡️ TrustMyAgent  │
│                  │  ────────────────────────────►   │  Server           │
│  run.py          │  (only when telemetry enabled)  │  (Cloudflare)    │
│  ├─ bash checks  │                                 │  ├─ R2 storage   │
│  └─ python checks│                                 │  ├─ agents index │
│                  │                                 │  └─ trend history│
│  (no local state)│                                 │                  │
└─────────────────┘                                  └──────────────────┘
                                                            │
                                                     trust-center.html
                                                     (public dashboard)
```

## 隐私与信任

- **开源**：所有代码均采用MIT许可协议，并可在[github.com/Anecdotes-Yair/trust-my-agent-ai](https://github.com/Anecdotes-Yair/trust-my-agent-ai)公开审计。
- **无状态设计**：不会写入任何文件，不会保留任何状态信息，也不会在未经同意的情况下安装任何后台进程。
- **可选的遥测功能**：使用`--local-only`选项可以完全离线运行；使用`--dry-run`选项可以在发送数据前进行预览。
- **不传输秘密信息**：检查仅检测问题的存在，从不传输实际秘密值。
- **透明数据包**：`--dry-run`选项会显示实际会发送的JSON数据包内容。
- **服务器**：由[Anecdotes AI](https://anecdotes.ai)公司运营，该公司提供治理、风险管理和合规性服务。服务器代码位于[github.com/Anecdotes-Yair/trust-my-agent-ai-website](https://github.com/Anecdotes-Yair/trust-my-agent-ai-website)。

## 致谢

该工具由[Anecdotes AI](https://anecdotes.ai)公司为AI代理生态系统开发。