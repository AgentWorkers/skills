---
name: guardian
description: '“我听说 OpenClaw 存在安全风险，该如何加强它的安全性呢？”安装 Guardian 就可以了。就这么简单。'
version: 2.0.5
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - name: GUARDIAN_WORKSPACE
          description: "Override workspace path (optional; falls back to OPENCLAW_WORKSPACE then ~/.openclaw/workspace)"
          required: false
        - name: OPENCLAW_WORKSPACE
          description: "OpenClaw workspace root path (optional; used as fallback for DB and config resolution)"
          required: false
        - name: GUARDIAN_CONFIG
          description: "Override path to Guardian config.json (optional)"
          required: false
    permissions:
      - read_workspace
      - write_workspace
      - shell_optional
    notes: >
      Guardian is a defensive security scanner. It reads workspace files and writes
      to a local SQLite database (guardian.db). No network access occurs at runtime;
      definition updates are an explicit operator-triggered action (definitions/update.py).
---
# Guardian

Guardian 负责扫描传入的消息和工作区文件，以检测恶意代码注入、凭证泄露等威胁。它会在每个用户请求时执行轻量级的实时预扫描，并定期对工作区文件进行批量扫描。

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

然后运行入职引导程序以完成设置：

```bash
python3 skills/guardian/scripts/onboard.py
```

## 状态检查

```bash
python3 skills/guardian/scripts/admin.py status
```

## 执行扫描

```bash
# Quick report — threats in the last 24 hours
python3 skills/guardian/scripts/guardian.py --report --hours 24

# Full report
python3 skills/guardian/scripts/admin.py report
```

## 管理命令

```bash
python3 scripts/admin.py status
python3 scripts/admin.py disable
python3 scripts/admin.py disable --until "2h"
python3 scripts/admin.py enable
python3 scripts/admin.py bypass --on
python3 scripts/admin.py bypass --off
python3 scripts/admin.py dismiss INJ-004
python3 scripts/admin.py allowlist add "safe phrase"
python3 scripts/admin.py allowlist remove "safe phrase"
python3 scripts/admin.py threats
python3 scripts/admin.py threats --clear
python3 scripts/admin.py update-defs
```

在任意命令后添加 `--json` 选项，即可获取机器可读的输出结果。

## 实时预扫描

使用 `RealtimeGuard` 在威胁到达系统之前将其拦截：

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="discord")
if guard.should_block(result):
    return guard.format_block_response(result)
```

仅对 “高风险” 和 “严重风险” 的威胁进行实时扫描，以降低延迟。

## 配置（`config.json`）

关键配置项：

| 设置 | 描述 |
|---|---|
| `enabled` | 启用/禁用 Guardian 的开关 |
| `admin_override` | 绕过防护模式（仅记录日志，不进行阻止） |
| `severity_threshold` | 阻止威胁的严重程度：`低风险`、`中等风险`、`高风险`、`严重风险` |
| `scan_paths` | 需要扫描的路径（`["auto"]` 会自动检测常用文件夹） |
| `db_path` | SQLite 数据库的位置（`"auto"` 会自动设置为 `<workspace>/guardian.db`） |
| `scan_interval_minutes` | 批量扫描的间隔时间（以分钟为单位） |
| `alerts.notify_on_critical` | 发送严重风险警报 |
| `alerts.notify_on_high` | 发送高风险警报 |
| `alerts.daily_digest` | 每日发送汇总报告 |

## 独立控制面板

```bash
cd skills/guardian/dashboard
python3 -m http.server 8091
# Open: http://localhost:8091/guardian.html
```

## 故障排除

- 如果 `admin.py status` 命令执行失败，请确保 `config.json` 是有效的 JSON 格式，并且数据库路径具有写入权限。
- 如果未检测到任何威胁，请确认 `definitions/*.json` 文件中存在相应的威胁定义，并且 `enabled` 的值为 `true`。
- 如果出现意外阻止行为，请使用 `python3 scripts/admin.py threats --json` 命令进行检查，并调整 `severity_threshold` 或添加允许列表模式。
- 如果更新检查失败，请验证对 `definitions.update_url` 的网络访问权限，并运行 `python3 definitions/update.py --version` 命令。