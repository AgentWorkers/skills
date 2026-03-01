---
name: clawguardian
description: 专为 OpenClaw 代理设计的本地优先安全扫描器。通过内置的签名库，能够检测命令注入、数据泄露行为、工具滥用以及社会工程攻击等安全威胁。
version: 2.2.0
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

这是一个用于 OpenClaw 代理的安全扫描工具。它通过基于正则表达式的签名匹配来检测提示注入、凭证泄露尝试、工具滥用行为以及社会工程攻击。

Guardian 提供两种扫描模式：

- **实时预扫描**：在消息到达模型之前对其进行检查。
- **批量扫描**：定期扫描工作区文件和对话记录。

所有数据都存储在本地。此次版本移除了可选的 Webhook/API 连接方式，以降低管理风险。您仍可以通过 `scripts/onboard.py --setup-crons` 来设置定时扫描任务。

扫描结果会保存在 SQLite 数据库（`guardian.db`）中。

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

## 安装流程及注意事项
该软件包包含可执行脚本（包括 `install.sh`）和 Python 模块。在生产环境中运行之前，请先仔细阅读并检查 `install.sh` 脚本。`install.sh` 脚本负责本地设置和验证；可选的辅助脚本 `onboard.py` 用于配置定时扫描任务。

## 上线检查清单
1) 可选：`python3 scripts/onboard.py --setup-crons`（配置定时扫描任务）
2) `python3 scripts/admin.py status`（确认系统是否正常运行）
3) `python3 scripts/admin.py threats`（确认签名库是否已加载；应显示 0 或 blocked）
4) 可选：根据您的环境配置 `config.json` 中的 `scan_paths` 和 `threshold` 值。

### 首次加载/自动激活
`install.sh` 完成安装后，会在工作区根目录下创建一个名为 `.guardian-activate-pending` 的文件（路径：`~/.openclaw/workspace/.guardian-activate-pending`）。当 OpenClaw 下次加载时，它会自动触发 `onboard.py` 脚本以完成激活流程。激活完成后，该文件会被删除。如果您希望手动激活，只需删除该文件即可（`rm ~/.openclaw/workspace/.guardian-activate-pending`）。

## 扫描范围与隐私保护
Guardian 会扫描配置的工作区路径以检测威胁。根据 `scan_paths` 的设置，扫描范围可能包括 OpenClaw 工作区中的其他技能配置文件。如果处理敏感文件，请在 `config.json` 中设置更严格的扫描路径。

## 快速入门

```bash
# Check status
python3 scripts/admin.py status

# Scan recent threats
python3 scripts/guardian.py --report --hours 24

# Full report
python3 scripts/admin.py report
```

## 管理命令

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

在命令前加上 `--json` 选项，即可获得机器可读的输出结果。

## Python API

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```

## 环境变量
- `GUARDIAN_WORKSPACE`（可选的工作区路径）
- `OPENCLAW_WORKSPACE`（可选的备用工作区路径）
- `GUARDIAN_CONFIG`（可选的 Guardian 配置文件路径）
- `OPENCLAW_CONFIG_PATH`（可选的 OpenClaw 配置文件路径）

## 配置
请编辑 `config.json` 文件：

| 设置 | 描述 |
|---|---|
| `enabled` | 全局开关（开启/关闭 Guardian 功能） |
| `severity_threshold` | 阻止行为的严重程度阈值：`low` / `medium` / `high` / `critical` |
| `scan_paths` | 需要扫描的路径（`["auto"]` 表示扫描所有常见文件夹） |
| `db_path` | SQLite 数据库路径（默认为 `<workspace>/guardian.db`） |

## 工作原理
Guardian 从 `definitions/*.json` 文件中加载威胁签名。每个签名包含一个 ID、正则表达式模式、严重程度和分类。系统会将传入的文本与所有有效的签名进行匹配。符合配置严重程度阈值的请求会被阻止并记录到数据库中。

支持的威胁类型包括：提示注入、凭证泄露（如 API 密钥、令牌）、数据泄露尝试、工具滥用行为以及社会工程攻击手段。