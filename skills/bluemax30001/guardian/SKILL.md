---
name: guardian
description: OpenClaw代理的安全扫描器。能够实时检测提示注入（prompt injection）、凭证泄露（credential exfiltration）以及社会工程攻击（social engineering attacks）。
version: 2.0.10
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - name: GUARDIAN_WORKSPACE
          description: "Override workspace path (optional; defaults to ~/.openclaw/workspace)"
          required: false
        - name: GUARDIAN_CONFIG
          description: "Override path to Guardian config.json (optional)"
          required: false
    permissions:
      - read_workspace
      - write_workspace
      - shell_optional
      - network_optional
---
# Guardian

这是一个专为 OpenClaw 代理设计的安全扫描工具。它通过基于正则表达式的签名匹配机制，检测提示注入（prompt injection）、凭证泄露（credential exfiltration）尝试、工具滥用（tool abuse）以及社会工程攻击（social engineering attacks）行为。

Guardian 提供两种扫描模式：

- **实时预扫描（Real-time pre-scan）**：在消息到达模型之前对其进行检查。
- **批量扫描（Batch scan）**：定期扫描工作区文件（workspace files）和对话记录（conversation logs）。

默认情况下，所有数据都存储在本地。可选组件包括：

- **Webhook 通知（Webhook notifications）**：`integrations/webhook.py`（将 JSON 数据发送到配置的 URL）。
- **HTTP API 服务器（HTTP API server）**：`scripts/serve.py`（提供扫描/报告功能）。
- **Cron 安排（Cron setup）**：`scripts/onboard.py --setup-crons`（配置扫描/报告任务的定时执行）。

扫描结果会保存在 SQLite 数据库（`guardian.db`）中。

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

## 上线检查清单（Onboarding checklist）
1) 可选：`python3 scripts/onboard.py --setup-crons`（配置扫描/报告任务的定时执行）。
2) `python3 scripts/admin.py status`（确认工具正在运行）。
3) `python3 scripts/admin.py threats`（确认威胁签名已加载；应显示“0”或“blocked”状态）。
4) 可选：`python3 scripts/serve.py --port 8090`（启动 HTTP API 服务器）。
5) 可选：在 `config.json` 中设置 `webhook_url`（启用外部警报功能）。

## 快速入门（Quick Start）

```bash
# Check status
python3 scripts/admin.py status

# Scan recent threats
python3 scripts/guardian.py --report --hours 24

# Full report
python3 scripts/admin.py report
```

## 管理命令（Admin Commands）

```bash
python3 scripts/admin.py status          # Current status
python3 scripts/admin.py enable          # Enable scanning
python3 scripts/admin.py disable         # Disable scanning
python3 scripts/admin.py threats         # List detected threats
python3 scripts/admin.py threats --clear # Clear threat log
python3 scripts/admin.py dismiss INJ-004 # Dismiss a signature
python3 scripts/admin.py allowlist add "safe phrase"
python3 scripts/admin.py allowlist remove "safe phrase"
python3 scripts/admin.py update-defs     # Update threat definitions
```

在任意命令后添加 `--json` 选项，即可获取机器可读的输出结果。

## Python API

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```

## 配置（Configuration）

编辑 `config.json` 文件：

| 设置 | 描述 |
|---|---|
| `enabled` | 全局开关（启用/禁用 Guardian 功能） |
| `severity_threshold` | 阻止行为的严重程度阈值：`low` / `medium` / `high` / `critical` |
| `scan_paths` | 需要扫描的路径（`["auto"]` 表示扫描所有常见文件夹） |
| `db_path` | SQLite 数据库路径（默认为 `<workspace>/guardian.db>`） |
| `webhook_url` | 可选：将扫描结果发送到此 URL |
| `http_server.port` | 可选：`scripts/serve.py` 服务器的端口 |

## 工作原理（How It Works）

Guardian 从 `definitions/*.json` 文件中加载威胁签名。每个签名包含一个 ID、正则表达式模式、严重程度和分类。系统会将传入的文本与所有有效的签名进行匹配。符合配置的严重程度阈值的攻击行为会被阻止，并记录到数据库中。

支持的签名类型包括：提示注入、凭证泄露模式（如 API 密钥、令牌）、数据泄露尝试、工具滥用行为以及社会工程攻击手段。