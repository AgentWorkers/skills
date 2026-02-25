---
name: clawguardian
description: 专为 OpenClaw 代理设计的本地优先安全扫描器。通过内置的签名库，能够检测命令注入、数据泄露行为、工具滥用以及社会工程攻击等安全威胁。
version: 2.0.16
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - GUARDIAN_WORKSPACE
        - GUARDIAN_CONFIG
        - OPENCLAW_WORKSPACE
        - OPENCLAW_CONFIG_PATH
    permissions:
      - read_workspace
      - write_workspace
      - shell_optional
      - network_optional
---
# Guardian

这是一个专为 OpenClaw 代理设计的安全扫描工具，能够通过基于正则表达式的签名匹配机制，检测提示注入（prompt injection）、凭证泄露（credential exfiltration）尝试、工具滥用（tool abuse）以及社会工程攻击（social engineering attacks）行为。

Guardian 提供两种扫描模式：

- **实时预扫描（Real-time pre-scan）**：在消息到达模型之前对其进行检查。
- **批量扫描（Batch scan）**：定期扫描工作区文件（workspace files）和对话日志（conversation logs）。

所有扫描数据均存储在本地。此次更新移除了可选的 Webhook/API 连接方式，以降低审核风险。用户仍可通过 `scripts/onboard.py --setup-crons` 命令来配置定时扫描任务（cron setup）。

扫描结果会保存到 SQLite 数据库（`guardian.db`）中。

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

## 安装流程及注意事项
该软件包包含可执行脚本（包括 `install.sh`）和 Python 模块。在生产环境中使用前，请务必先仔细阅读并测试 `install.sh` 脚本。`install.sh` 脚本负责完成本地配置和验证；辅助脚本 `onboard.py` 用于配置定时扫描任务（可选）。

## 上线检查清单（Onboarding checklist）：
1. （可选）：`python3 scripts/onboard.py --setup-crons`（配置定时扫描任务）
2. `python3 scripts/admin.py status`（确认系统是否正常运行）
3. `python3 scripts/admin.py threats`（确认威胁检测功能是否启用；应显示“0”或“blocked”状态）
4. （可选）：根据您的环境需求，检查 `config.json` 文件中的扫描路径（scan_paths）和阈值设置。

## 扫描范围与隐私保护
Guardian 会扫描您配置的工作区路径以检测潜在威胁。根据 `scan_paths` 的设置，扫描范围可能还包括其他技能配置文件（skill/config files）。如果处理敏感文件，请在 `config.json` 中设置更严格的扫描路径限制。

## 快速入门

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

在命令后添加 `--json` 选项，即可获取机器可读的输出结果。

## Python API

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```

## 系统环境变量
- `GUARDIAN_WORKSPACE`（可选的工作区路径配置）
- `OPENCLAW_WORKSPACE`（可选的备用工作区路径）
- `GUARDIAN_CONFIG`（可选的 Guardian 配置文件路径）
- `OPENCLAW_CONFIG_PATH`（可选的 OpenClaw 配置文件路径）

## 配置文件（Configuration）
请编辑 `config.json` 文件以进行配置：

| 设置 | 描述 |
|---|---|
| `enabled` | 是否启用 Guardian 功能 |
| `severity_threshold` | 威胁阻断阈值：`low` / `medium` / `high` / `critical` |
| `scan_paths` | 需要扫描的路径列表（示例：`["auto"]` 表示扫描所有常见文件夹） |
| `db_path` | SQLite 数据库路径（默认：`<workspace>/guardian.db`） |

## 工作原理
Guardian 从 `definitions/*.json` 文件中加载威胁签名信息。每个签名包含一个唯一 ID、正则表达式模式、严重程度等级和分类。系统会将传入的文本与所有有效的签名进行匹配；符合设定严重等级阈值的威胁行为将被阻断并记录到数据库中。

支持的威胁类型包括：提示注入、凭证泄露（如 API 密钥、访问令牌）、数据泄露尝试、工具滥用行为以及社会工程攻击手段。