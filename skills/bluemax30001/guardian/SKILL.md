---
name: guardian
description: OpenClaw安全防护机制：用于防范提示注入（prompt injection）、数据泄露（exfiltration）、工具滥用（tool abuse）以及社会工程学攻击（social engineering attacks）。
version: 1.1.0
---
# Guardian

## ⚡ **代理** — 每次阅读此文件时请先执行以下操作

**步骤 1 — 检查 Guardian 是否需要激活：**

```bash
# Check for pending activation marker (written by install.sh)
ls .guardian-activate-pending 2>/dev/null && echo "NEEDS_ACTIVATION" || \
python3 skills/guardian/scripts/onboard.py --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','unknown'))"
```

- 如果输出为 `NEEDS_ACTIVATION`，或者输出中未包含 `onboarded`，则**立即执行步骤 2–5**  
- 如果输出为 `onboarded`，则 Guardian 已激活，可以直接进入正常操作。

**步骤 2 — 激活 Guardian 并通知用户：**

```bash
python3 skills/guardian/scripts/onboard.py
```

记录完整的输出内容。该输出包含三个部分：  
1. **代理简介**（SECTION 1）：确认 `GUARDIAN.md` 文件已被写入工作区的根目录。无需发送任何内容。  
2. **管理员通知**（SECTION 2）：**立即通过用户的常用通讯工具（如 Telegram/Discord/Signal）将此信息发送给用户**。不要仅将其显示在聊天回复中。  
3. **设置检查清单**（SECTION 3）：**也将此清单发送给用户**。清单中会显示当前正在运行的服务、缺失的配置项以及可复制的 cron 命令。

**步骤 3 — 设置后台扫描功能（至关重要）：**

检查是否需要配置 cron 作业：  

```bash
python3 skills/guardian/scripts/onboard.py --status
```

如果发现有未配置的 cron 作业（标记为 ❌），请执行以下操作：  

```bash
python3 skills/guardian/scripts/onboard.py --setup-crons
```

该操作会自动安装缺失的 cron 作业。并向用户确认：“后台扫描功能现已激活。”

如果 `--setup-crons` 命令执行失败（可能是权限问题），请向用户展示 `--status` 命令的输出结果中的手动 cron 配置内容，并告知用户运行 `crontab -e` 后将配置内容粘贴到系统中的 cron 表中。

**步骤 4 — 配置审核：**

```bash
python3 skills/guardian/scripts/onboard.py --config-review
```

将审核结果发送给用户。该结果会显示已设置的配置项，并指出需要修改的地方。

**步骤 5 — 确认并清理：**

向用户发送最终确认信息：  
> “✅ Guardian 现已完全启动。后台扫描功能正在运行，您的仪表盘可在 [URL] 查看，系统会针对任何威胁发出警报。您已受到保护。”

然后删除任何表示任务待处理的标记（如果存在）：  
```bash
rm -f .guardian-activate-pending
```

> 如果 `onboard.py` 文件还不存在，请先运行 `./install.sh`。

---

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

`install.sh` 脚本会自动执行初始化流程。但是，**代理**（即您）必须将初始化结果通知给用户——脚本本身无法直接通过 Telegram/Discord 发送通知。

**可选的 Python 可执行文件：**  
```bash
VENV_PYTHON=/path/to/python3 ./install.sh
```

---

## 重新执行初始化流程

在配置发生任何更改后，请重新运行初始化流程：  
```bash
python3 skills/guardian/scripts/onboard.py --refresh
```  
随后将更新后的通知发送给用户。

**修改仪表盘 URL：**  
```bash
python3 skills/guardian/scripts/onboard.py --refresh --dashboard-url http://YOUR-SERVER-IP:PORT/guardian.html
```

---

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

在任何命令前使用 `--json` 选项以启用机器可读的模式。

---

## 实时预扫描（第一层防护）

在处理用户请求之前，请使用 `RealtimeGuard`：  

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="discord")
if guard.should_block(result):
    return guard.format_block_response(result)
```

**功能说明：**  
- 仅对 “高风险” 和 “危急风险” 的签名进行实时扫描，以降低延迟。  
- 在这些签名到达主模型/工具链之前将其拦截。  
- 返回扫描结果（`ScanResult(blocked, threats, score, suggested_response)`）。

---

## 配置参考（`config.json`）  

- `enabled`：控制 Guardian 的开关（开启/关闭）。  
- `admin_override`：绕过常规规则的模式（仅记录日志并报告，不进行拦截）。  
- `scan_paths`：需要扫描的路径列表（`["auto"]` 表示自动检测常见的 OpenClaw 文件夹）。  
- `db_path`：SQLite 数据库的位置（默认为 `<workspace>/guardian.db`）。  
- `scan_interval_minutes`：批量扫描的间隔时间。  
- `severity_threshold`：拦截的阈值（`low|medium|high|critical`）。  
- `dismissed_signatures`：需要全局屏蔽的签名 ID。  
- `custom_definitions_dir`：自定义定义文件的目录。  
- `channels.monitor_all`：是否监控所有通道。  
- `channelsexclude_channels`：需要排除的通道列表。  
- `alerts.notify_on_critical`：是否在检测到危急风险时发送警报。  
- `alerts.notify_on_high`：是否在检测到高风险时发送警报。  
- `alerts.daily_digest`：是否发送每日摘要信息。  
- `alerts.daily_digest_time`：摘要信息的发送时间。  
- `admin.bypass_token`：管理员用于绕过常规规则的临时令牌。  
- `admin.disable_until`：临时禁用的截止时间戳。  
- `admin.trusted_sources`：允许接收特殊请求的信任通道/来源。  
- `admin.requireconfirmation_for_severity`：需要管理员确认的严重风险等级。  
- `false_positive_suppression.min_context_words`：用于屏蔽误报的最小上下文长度。  
- `false_positive_suppression.suppress_assistant_number_matches`：用于避免因数字匹配导致的误报的规则。  
- `false_positive_suppression.allowlist_patterns`：用于屏蔽已知误报的模式列表。  
- `definitions.update_url`：定义更新的可选 URL（默认为上游提供的 URL）。  

---

## 独立仪表盘

Guardian 配备了自包含的仪表盘（无需完整的 NOC（网络运营中心）堆栈）：  

```bash
cd skills/guardian/dashboard
python3 -m http.server 8091
# Open: http://localhost:8091/guardian.html
```

或者，如果已安装 Guardian，您也可以通过 NOC 仪表盘的 Guardian 标签来查看相关数据。

---

## 故障排除：**

- 如果 `scripts/admin.py status` 命令执行失败，请确保 `config.json` 是有效的 JSON 格式，并且数据库路径具有写入权限。  
- 如果未检测到任何威胁，请确认 `definitions/*.json` 文件中包含有效的签名定义，并且 `enabled` 的值为 `true`。  
- 如果更新配置时出现问题，请检查网络是否能够访问 `definitions.update_url`，并运行 `python3 definitions/update.py --version` 命令。  
- 如果仪表盘显示为空数据，请检查 `scripts/dashboard_export.py --db /path/to/guardian.db` 命令使用的数据库路径是否正确。  
- 如果出现异常拦截情况，请使用 `python3 scripts/admin.py threats --json` 命令检查最近的事件，并调整 `severity_threshold` 或 `allowlist_patterns` 配置。