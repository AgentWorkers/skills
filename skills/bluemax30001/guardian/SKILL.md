---
name: guardian
description: OpenClaw安全防护机制，用于防御提示注入（prompt injection）、数据泄露（exfiltration）、工具滥用（tool abuse）以及社会工程学攻击（social engineering attacks）。
version: 1.0.0
---
# Guardian

Guardian 为 OpenClaw 部署提供了策略执行、扫描和报告功能。

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

可选的显式 Python 可执行文件：

```bash
VENV_PYTHON=/path/to/python3 ./install.sh
```

## 管理员快速参考

```bash
python3 scripts/admin.py status
python3 scripts/admin.py disable
python3 scripts/admin.py disable --until "2h"
python3 scripts/admin.py enable
python3 scripts/admin.py bypass --on
python3 scripts/admin.py bypass --off
python3 scripts/admin.py dismiss INJ-004
python3 scripts/admin.py allowlist add "safe test phrase"
python3 scripts/admin.py allowlist remove "safe test phrase"
python3 scripts/admin.py threats
python3 scripts/admin.py threats --clear
python3 scripts/admin.py report
python3 scripts/admin.py update-defs
```

在所有命令中使用 `--json` 选项以启用机器可读模式。

## 实时预扫描（第一层）

在处理用户请求之前，先使用 `RealtimeGuard`：

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="discord")
if guard.should_block(result):
    return guard.format_block_response(result)
```

**行为：**
- 仅扫描 “高风险” 和 “临界风险” 签名，以实现低延迟。
- 在高风险/临界风险的负载到达主模型/工具链之前阻止它们。
- 返回 `ScanResult(blocked, threats, score, suggested_response)`。

## 配置参考（`config.json`）

- `enabled`：Guardian 的开启/关闭开关。
- `admin_override`：绕过模式（仅记录日志并报告，不进行阻止）。
- `scan_paths`：需要扫描的路径（`["auto"]` 会自动检测常见的 OpenClaw 文件夹）。
- `db_path`：SQLite 数据库的位置（`"auto"` 表示使用 `<workspace>/guardian.db`）。
- `scan_interval_minutes`：批量扫描的间隔时间。
- `severity_threshold`：扫描器的阻止阈值（`low|medium|high|critical`）。
- `dismissed_signatures`：需要全局屏蔽的签名 ID。
- `custom_definitions_dir`：自定义定义文件的目录。
- `channels.monitor_all`：是否监控所有通道。
- `channels.exclude_channels`：需要忽略的通道。
- `alerts.notify_on_critical`：在出现临界风险时发送警报。
- `alerts.notify_on_high`：在出现高风险时发送警报。
- `alerts.daily_digest`：发送每日摘要。
- `alerts.daily_digest_time`：摘要的发送时间。
- `admin.bypass_token`：管理员绕过工作流的可选令牌。
- `admin.disable_until`：临时禁用的截止时间戳。
- `admin.trusted_sources`：需要授权的通道/来源。
- `admin.require_confirmation_for_severity`：需要确认的严重性级别。
- `false_positive_suppression.min_context_words`：用于屏蔽误报的最小上下文长度。
- `false_positive_suppression.suppress_assistant_number_matches`：避免因数字匹配过多而产生的误报。
- `false_positive_suppression.allowlist_patterns`：用于屏蔽已知误报的模式列表。
- `definitions.update_url`：定义更新的可选 URL（如果未指定，则使用默认的上游 URL）。

## 故障排除**

- 如果 `scripts/admin.py status` 命令失败，请确保 `config.json` 是有效的 JSON 文件，并且数据库路径具有写入权限。
- 如果没有检测到威胁，请确认 `definitions/*.json` 文件中存在有效的定义，并且 `enabled` 的值为 `true`。
- 如果更新检查失败，请验证对 `definitions.update_url` 的网络访问权限，并运行 `python3 definitions/update.py --version`。
- 如果仪表板导出的内容为空，请检查 `scripts/dashboard_export.py --db /path/to/guardian.db` 使用的数据库路径。
- 如果出现意外的阻止行为，请使用 `python3 scripts/admin.py threats --json` 检查最近的事件，并调整 `severity_threshold` 或允许列表模式。