---
name: guardian
description: '“我听说 OpenClaw 存在安全风险，该如何加强其安全性呢？”安装 Guardian 就可以了。就这么简单。'
version: 2.0.3
---
# Guardian

## ⚡ **代理** — 每次阅读此文件时，请先执行以下操作

**步骤 1 — 检查 Guardian 是否需要激活：**

```bash
# Check for pending activation marker (written by install.sh)
ls .guardian-activate-pending 2>/dev/null && echo "NEEDS_ACTIVATION" || \
python3 skills/guardian/scripts/onboard.py --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','unknown'))"
```

- 如果输出为 `NEEDS_ACTIVATION`，或者输出中未包含 `onboarded`，则 **立即执行步骤 2–5**  
- 如果输出为 `onboarded`，则 Guardian 已激活，可以直接进入正常操作

**步骤 2 — 激活 Guardian 并通知用户：**

```bash
python3 skills/guardian/scripts/onboard.py
```

捕获完整的输出结果。该输出包含三个部分：
1. **SECTION 1 — 代理简要说明**：确认 `GUARDIAN.md` 文件已被写入工作区的根目录。无需发送任何内容。  
2. **SECTION 2 — 管理员通知**：**立即通过用户的常用通讯渠道（Telegram/Discord/Signal）发送此信息**。不要仅将其显示在聊天回复中。  
3. **SECTION 3 — 设置检查清单**：**也发送给用户**。该清单会显示当前正在运行的内容、缺失的配置项以及可粘贴的 cron 命令。

**步骤 3 — 设置后台扫描（关键步骤）：**

检查是否需要配置 cron 任务：

```bash
python3 skills/guardian/scripts/onboard.py --status
```

如果出现任何 ❌ 标记的项，请执行以下操作：

```bash
python3 skills/guardian/scripts/onboard.py --setup-crons
```

这将自动安装缺失的 cron 任务。并向用户确认：“后台扫描现已激活。”

如果 `--setup-crons` 命令失败（可能是权限问题），请向用户展示 `--status` 命令的输出结果中的手动 cron 语句，并告知他们运行 `crontab -e` 后将内容粘贴到系统中。

**步骤 4 — 配置审核：**

```bash
python3 skills/guardian/scripts/onboard.py --config-review
```

将审核结果发送给用户。该结果会显示已设置的配置项，并指出需要修改的地方。

**步骤 5 — 确认并清理：**

向用户发送最终确认信息：
> “✅ Guardian 现已完全启用。后台扫描正在运行，您的仪表板位于 [URL]，系统会向您发送任何威胁警报。您已受到保护。”

然后删除任何存在的待处理标记：
```bash
rm -f .guardian-activate-pending
```

> 如果 `onboard.py` 文件还不存在，请先运行 `./install.sh`。

---

## 🎯 **代理** — 当用户未明确请求技能时

当用户说“使用 Guardian 技能”时，无需询问具体需求，而是提供 **简洁的状态信息及操作菜单**：

**步骤 1 — 获取当前状态：**

```bash
python3 skills/guardian/scripts/admin.py status --json 2>/dev/null
```

**步骤 2 — 按如下格式生成响应：**

```
🛡️ **Guardian Security Status**

**Current State:**
• Status: [enabled/disabled]
• Mode: [realtime/bypass if admin_override is true]
• Severity threshold: [low/medium/high/critical]
• Recent threats: [count from last 24h]
• Background scanning: [active/inactive based on cron status]

**Quick Actions:**
1️⃣ **Scan now** — `python3 skills/guardian/scripts/guardian.py --report --hours 24`
2️⃣ **View dashboard** — [dashboard URL from config]
3️⃣ **Show recent threats** — `python3 skills/guardian/scripts/admin.py threats`
4️⃣ **Update definitions** — `python3 skills/guardian/scripts/admin.py update-defs`
5️⃣ **Full security report** — `python3 skills/guardian/scripts/admin.py report`
6️⃣ **Modify config** — Edit `skills/guardian/config.json`

What would you like to do?
```

**步骤 3 — 如果状态查询命令失败：**
返回简化的响应：
```
🛡️ **Guardian Security**

Guardian provides real-time threat detection and workspace scanning.

**Available actions:**
• Run a security scan
• View the dashboard
• Check recent threats
• Update threat definitions
• Review/modify configuration

What would you like me to help with?
```

---

## 安装

**`install.sh` 脚本会自动执行初始化流程。但是**，必须由 **代理**（即您）将通知结果发送给用户——脚本本身无法直接发送到 Telegram/Discord。**

（可选的 Python 可执行文件：）
```bash
VENV_PYTHON=/path/to/python3 ./install.sh
```

---

## 重新执行初始化流程

在任何配置更改后，重新运行初始化流程：
```bash
python3 skills/guardian/scripts/onboard.py --refresh
```
然后向用户发送更新后的通知。

如果需要更改仪表板 URL，可以执行以下操作：
```bash
python3 skills/guardian/scripts/onboard.py --refresh --dashboard-url http://YOUR-SERVER-IP:PORT/guardian.html
```

---

## 管理员快速参考

**在任何命令前使用 `--json` 选项，以机器可读的方式获取配置信息。**

---

## 实时预扫描（第一层防护）

在处理用户请求之前，先使用 `RealtimeGuard` 进行扫描：

**行为：**
- 仅扫描 **高风险** 和 **临界风险** 的签名，以减少延迟。
- 在高风险/临界风险的负载到达主模型/工具链之前将其拦截。
- 返回 `ScanResult(blocked, threats, score, suggested_response)`。

---

## 配置参考（`config.json`）

- `enabled`：控制 Guardian 的开关（开启/关闭）。
- `admin_override`：绕过默认设置的模式（仅记录日志和报告，不进行拦截）。
- `scan_paths`：需要扫描的路径列表（`["auto"]` 会自动检测 OpenClaw 的常用文件夹）。
- `db_path`：SQLite 数据库的位置（默认为 `<workspace>/guardian.db`）。
- `scan_interval_minutes`：批量扫描的间隔时间。
- `severity_threshold`：扫描的拦截阈值（`low|medium|high|critical`）。
- `dismissed_signatures`：需要全局屏蔽的签名 ID。
- `custom_definitions_dir`：自定义定义文件的目录。
- `channels.monitor_all`：是否监控所有通道。
- `channels.exclude_channels`：需要排除的通道。
- `alerts.notify_on_critical`：是否在收到临界风险警报时发送通知。
- `alerts.notify_on_high`：是否在收到高风险警报时发送通知。
- `alerts.daily_digest`：是否每天发送摘要信息。
- `alerts.daily_digest_time`：摘要信息的发送时间。
- `admin.bypass_token`：管理员用于绕过某些操作的令牌。
- `admin.disable_until`：临时禁用的截止时间。
- `admin.trusted_sources`：允许通过这些渠道/来源发送请求。
- `admin.require_confirmation_for_severity`：需要确认的警报严重等级。
- `false_positive_suppression.min_context_words`：用于屏蔽误报的最小上下文长度。
- `false_positive_suppression.suppress_assistant_number_matches`：用于避免误报的规则。
- `false_positive_suppression.allowlist_patterns`：用于屏蔽已知误报的模式列表。
- `definitions.update_url`：自定义定义文件的更新 URL（默认使用上游提供的 URL）。

### 控制界面集成

Guardian 的配置信息现在会显示在 OpenClaw 的控制界面（http://localhost:18789）的 **Config** 面板中（路径为 `skills.guardian.config`）。界面会显示以下配置项：
- `enabled`
- `severity_threshold`
- `scan_interval_minutes`
- `trusted_sources`
- `alerts.notify_on_critical`
- `alerts.notify_on_high`
- `alerts.daily_digest`
- `alerts.daily_digest_time`

Guardian 会首先从 `openclaw.json` 中读取这些配置项；如果该文件不存在，则会从 `skills/guardian/config.json` 中获取配置。

---

## 允许列表功能（误报抑制）

允许列表可以完全跳过对符合特定模式的消息的扫描。这对于已知安全的系统消息非常有用，因为这些消息可能会被误判为威胁。

### 当前的允许列表模式

默认配置包含以下模式，用于保护 OpenClaw 的内部系统消息：

```json
"allowlist_patterns": [
  "WORKFLOW_AUTO\\.md",
  "(?i)openclaw\\s+(internal|system|post-compaction|audit)",
  "(?i)post-compaction\\s+(audit|restore|protocol)",
  "(?i)system\\s+(reminder|protocol|message).*(?:read|follow|check).*(?:SOUL\\.md|USER\\.md|MEMORY\\.md|WORKFLOW_AUTO\\.md)"
]
```

这些模式可以保护：
- **WORKFLOW_AUTO.md** 文件——系统工作流程恢复相关的消息。
- **OpenClaw 内部消息**——系统审计和状态更新消息。
- **Post-compaction protocols**——系统文件恢复和代理启动相关的消息。
- **System file reminders**——用于提示用户阅读 SOUL.md、USER.md、MEMORY.md 的提示信息。

### 添加允许列表模式

**推荐通过 CLI 添加模式：**
```bash
python3 scripts/admin.py allowlist add "PATTERN"
python3 scripts/admin.py allowlist remove "PATTERN"
```

**手动修改 `config.json`：**
```json
{
  "false_positive_suppression": {
    "allowlist_patterns": [
      "your-safe-pattern-here"
    ]
  }
}
```

### 安全最佳实践

**✅ 应该这样做：**
- 使用能够识别系统内部进程的特定模式。
- 在部署前彻底测试这些模式。
- 记录每个模式的安全性依据。

**不应该这样做：**
- 添加可能匹配用户输入的通用模式。
- 仅基于消息内容来设置允许列表。
- 将允许列表作为签名调整的临时解决方案。
- 添加包含 `.*` 或其他通配符的模式。

### 测试允许列表模式

```bash
cd skills/guardian

# Test a specific message
python3 -c "from core.scanner import quick_scan; import json; \
  result = quick_scan('YOUR MESSAGE HERE'); \
  print('Allowlisted:', result.get('allowlisted', False)); \
  print('Clean:', result['clean'])"

# Run allowlist test suite
python3 test_allowlist.py
```

### 示例

**安全模式（✅）：**
```json
"WORKFLOW_AUTO\\.md"
```
仅匹配包含 “WORKFLOW_AUTO.md” 的消息——这是系统特有的文件名。

**不安全的模式（❌）：**
```json
".*system.*"
```
该模式过于宽泛，会匹配任何包含 “system” 的用户消息。

**平衡模式（✅）：**
```json
"(?i)openclaw\\s+internal:\\s+"
```
该模式足够具体，需要以 “OpenClaw internal:” 为前缀——只有系统消息才会使用这个前缀。

---

## 独立仪表板

Guardian 配备了独立的仪表板（无需完整的 NOC（网络操作中心）堆栈：

```bash
cd skills/guardian/dashboard
python3 -m http.server 8091
# Open: http://localhost:8091/guardian.html
```

或者，如果已安装 Guardian，也可以通过 NOC 仪表板的 Guardian 标签来访问该仪表板。

---

## 故障排除**

- 如果 `scripts/admin.py` 命令执行失败，请确保 `config.json` 是有效的 JSON 格式，并且数据库路径具有写入权限。
- 如果没有检测到任何威胁，请确认 `definitions/*.json` 文件中存在有效的定义文件，并且 `enabled` 的配置项设置为 `true`。
- 如果更新检查失败，请验证对 `definitions.update_url` 的网络访问权限，并运行 `python3 definitions/update.py --version` 命令。
- 如果仪表板显示为空，请检查 `scripts/dashboard_export.py --db /path/to/guardian.db` 使用的数据库路径是否正确。
- 如果出现异常拦截情况，请使用 `python3 scripts/admin.py threats --json` 命令检查最近的事件，并调整 `severity_threshold` 或允许列表模式。