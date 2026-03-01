---
name: clawguardian
description: OpenClaw代理的多层安全防护体系中的一层。该层能够拦截提示注入（prompt injection）、数据泄露尝试（exfiltration attempts）、工具滥用（tool abuse）以及社会工程攻击（social engineering attacks），防止这些威胁影响到模型（model）。它可以与OpenClaw内置的安全限制机制（built-in capability restrictions）结合使用，实现深度防御（defense-in-depth）。
version: 2.3.0
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

**OpenClaw代理的多层安全防护体系中的其中一层**

真正的代理安全需要多层次的保护：OpenClaw内置的限制功能和审批机制用于控制代理的行为；而Guardian则负责拦截恶意输入，防止这些输入到达模型（即处理代理“能看到”的内容）。

Guardian提供了基于签名的预模型扫描功能，能够检测提示注入（prompt injection）、凭证泄露尝试（credential exfiltration attempts）、工具滥用（tool abuse）以及社会工程攻击（social engineering attacks）等威胁。不过，它本身并不是一个完整的安全解决方案。应将其与OpenClaw的工具白名单（tool allowlists）、审批机制（approval gates）以及沙箱执行环境（sandboxed execution）结合使用，以实现深度防御。

Guardian支持两种扫描模式：

- **实时预扫描（Real-time pre-scan）**：在每条消息到达模型之前对其进行检查。
- **批量扫描（Batch scan）**：定期扫描工作区文件（workspace files）和对话记录（conversation logs）。

所有扫描数据都存储在本地。可以通过`scripts/onboard.py --setup-crons`命令来设置Cron任务进行定期扫描。

扫描结果会保存在SQLite数据库（`guardian.db`）中。

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

## 安装流程及注意事项
该软件包包含可执行脚本（包括`install.sh`）和Python模块。在生产环境中运行之前，请务必先仔细阅读`install.sh`脚本。`install.sh`负责完成本地配置和验证；可选的辅助脚本`onboard.py`用于设置Cron任务。

## 上线检查清单
1) 可选：`python3 scripts/onboard.py --setup-crons`（用于设置Cron任务）
2) `python3 scripts/admin.py status`（确认系统是否正在运行）
3) `python3 scripts/admin.py threats`（确认签名库是否已加载；应显示“0”或“blocked”状态）
4) 可选：根据您的环境需求，查看`config.json`文件中的`scan_paths`和`threshold`配置。

### 首次加载/自动激活
`install.sh`执行完成后，它会在工作区根目录下创建一个名为`.guardian-activate-pending`的文件（路径为`~/.openclaw/workspace/.guardian-activate-pending`）。当OpenClaw下次加载时，会自动触发`onboard.py`进行激活流程。激活完成后，该文件会被删除。如果您希望手动完成激活，只需删除该文件即可（`rm ~/.openclaw/workspace/.guardian-activate-pending`）。

## 扫描范围与隐私保护
Guardian会扫描配置的工作区路径以检测威胁。根据`scan_paths`的设置，扫描范围可能包括工作区中的其他技能配置文件（skill/config files）。如果处理敏感文件，请在`config.json`中设置更严格的扫描路径。

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

在命令前添加`--json`参数可获取机器可读的输出结果。

## Python API

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```

## 环境变量
- `GUARDIAN_WORKSPACE`（可选的工作区配置覆盖值）
- `OPENCLAW_WORKSPACE`（可选的备用工作区配置覆盖值）
- `GUARDIAN_CONFIG`（可选的Guardian配置文件路径）
- `OPENCLAW_CONFIG_PATH`（可选的OpenClaw配置文件路径）

## 配置
请编辑`config.json`文件：

| 设置 | 说明 |
|---|---|
| `enabled` | 全局开关（启用/禁用Guardian） |
| `severity_threshold` | 阻止行为的严重程度阈值：`low` / `medium` / `high` / `critical` |
| `scan_paths` | 需要扫描的路径列表（示例：`["auto"]`表示扫描所有常见文件夹） |
| `db_path` | SQLite数据库路径（默认为`<workspace>/guardian.db`） |

## 工作原理
Guardian从`definitions/*.json`文件中加载威胁签名信息。每个签名包含一个ID、正则表达式模式、严重程度和分类。系统会将传入的文本与所有有效的签名进行匹配；超过配置的严重程度阈值的请求会被阻止并记录到数据库中。

支持的威胁类型包括：提示注入、凭证泄露、工具滥用以及社会工程攻击等。