---
name: openclaw-audit-watchdog
version: 0.1.0
description: 为 OpenClaw 代理执行自动化的每日安全审计，并通过电子邮件发送审计结果。这些审计会深入检查系统安全状况，并生成格式化的报告。
homepage: https://clawsec.prompt.security
metadata: {"openclaw":{"emoji":"🔭","category":"security"}}
clawdis:
  emoji: "🔭"
  requires:
    bins: [bash, curl]
---
# Prompt Security Audit (openclaw)

## 安装选项

您可以通过两种方式获取 openclaw-audit-watchdog：

### 选项 A：随 ClawSec Suite 一起安装（推荐）

**如果您已经安装了 clawsec-suite，那么您可能已经拥有 openclaw-audit-watchdog！**

openclaw-audit-watchdog 与 ClawSec Suite 一起提供关键的自动化安全审计功能。在安装该套件时，如果系统尚未安装 audit watchdog，它会从套件中自动安装。

**优点：**
- 便捷：无需单独下载
- 安装位置固定：安装在 `~/.openclaw/skills/openclaw-audit-watchdog/`
- 保持现有设置：如果已安装 audit watchdog，不会被覆盖
- 一次性验证：作为套件包的一部分进行完整性检查

### 选项 B：独立安装（请参阅此页面）

您可以独立安装 openclaw-audit-watchdog，而不需要安装整个套件。

**何时使用独立安装：**
- 只需要 audit watchdog，而不需要套件的其他组件
- 希望在安装套件之前先安装 audit watchdog
- 希望对 audit watchdog 的安装过程有更详细的控制

请继续阅读以下内容以获取独立安装的说明。

---

## 目标

创建（或更新）一个每日定时任务，该任务将执行以下操作：

1. 运行：
   - `openclaw security audit --json`
   - `openclaw security audit --deep --json`

2. 汇总审计结果（包括严重/警告/信息等级的结果以及最主要的发现）

3. 将报告发送到：
   - 用户指定的 DM 目标（频道 + 收件人 ID/处理方式）

默认调度时间：**每天 23:00（晚上 11 点）**，以所选时区为准。

**报告发送方式：**
- 通过 DM 发送到最后一个活跃的会话。

## 使用示例

### 示例 1：快速启动（使用环境变量）

对于自动化/MDM 部署，在调用之前设置环境变量：

```bash
export PROMPTSEC_DM_CHANNEL="telegram"
export PROMPTSEC_DM_TO="@yourhandle"
export PROMPTSEC_TZ="America/New_York"
export PROMPTSEC_HOST_LABEL="prod-server-01"

# Then invoke the skill
/openclaw-audit-watchdog
```

该技能将自动配置并创建定时任务，无需额外提示。

### 示例 2：交互式设置

如果未设置环境变量，技能会提供最少的提示：

```
User: /openclaw-audit-watchdog

Agent: Setting up daily security audit watchdog...
       What channel should I use for delivery? (e.g., telegram, slack)
User: telegram

Agent: What's the recipient ID or handle?
User: @myhandle

Agent: Which timezone for the 23:00 daily run? (default: UTC)
User: America/Los_Angeles

Agent: ✓ Created cron job "Daily security audit (Prompt Security)"
       Schedule: Daily at 23:00 America/Los_Angeles
       Delivery: telegram → @myhandle
```

### 示例 3：更新现有任务

如果已经存在定时任务，该技能会更新现有任务，而不会创建重复的任务：

```
User: /openclaw-audit-watchdog

Agent: Found existing "Daily security audit (Prompt Security)" job.
       Current: Daily at 23:00 UTC → telegram:@oldhandle

       Update delivery target? (current: telegram:@oldhandle)
User: slack:#security-alerts

Agent: ✓ Updated cron job
       Schedule: Daily at 23:00 UTC
       Delivery: slack:#security-alerts
```

### 示例 4：报告内容

每天在预定时间，您将收到如下格式的报告：

```
🔭 Daily Security Audit Report
Host: prod-server-01
Time: 2026-02-16 23:00:00 America/New_York

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Standard Audit: 12 checks passed, 2 warnings
✓ Deep Audit: 8 probes passed, 1 critical

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL FINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[CRIT-001] Unencrypted API Keys Detected
→ Remediation: Move credentials to encrypted vault or use environment variables

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WARNINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[WARN-003] Outdated Dependencies Found
→ Remediation: Run `openclaw security audit --fix` to update

[WARN-007] Weak Permission on Config File
→ Remediation: chmod 600 ~/.openclaw/config.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run `openclaw security audit --deep` for full details.
```

### 示例 5：自定义调度

希望设置不同的调度时间？请在调用之前进行设置：

```bash
# Run every 6 hours instead of daily
export PROMPTSEC_SCHEDULE="0 */6 * * *"
/openclaw-audit-watchdog
```

### 示例 6：管理多个服务器

对于管理多个服务器的情况，请使用不同的主机标签：

```bash
# On dev server
export PROMPTSEC_HOST_LABEL="dev-01"
export PROMPTSEC_DM_TO="@dev-team"
/openclaw-audit-watchdog

# On prod server
export PROMPTSEC_HOST_LABEL="prod-01"
export PROMPTSEC_DM_TO="@oncall"
/openclaw-audit-watchdog
```

每个服务器的报告都会包含明确的主机标识。

### 示例 7：抑制已审核的发现结果

要抑制已审核并获认可的发现结果，请使用 `--enable-suppressions` 标志，并确保配置文件中包含 `"enabledFor": ["audit"]` 这一行：

```bash
# Create or edit the suppression config
cat > ~/.openclaw/security-audit.json <<'JSON'
{
  "enabledFor": ["audit"],
  "suppressions": [
    {
      "checkId": "skills.code_safety",
      "skill": "clawsec-suite",
      "reason": "First-party security tooling — reviewed by security team",
      "suppressedAt": "2026-02-15"
    }
  ]
}
JSON

# Run with suppressions enabled
/openclaw-audit-watchdog --enable-suppressions
```

被抑制的发现结果仍会出现在报告中，但不会计入严重/警告的总数中。

## 抑制/允许列表

审计流程支持一种可选的抑制机制，用于管理已审核的发现结果。启用抑制功能需要满足两个独立条件：

### 启用要求

1. **命令行标志：** 在调用时必须传递 `--enable-suppressions` 标志。
2. **配置文件中的设置：** 配置文件必须包含 `"enabledFor"` 且数组中包含 `"audit"`。

如果缺少任何一个条件，所有发现结果都将被正常报告，抑制列表将被忽略。

### 配置文件的位置（共 4 种方式）

1. 明确指定 `--config <path>` 参数
2. `OPENCLAW_AUDIT_CONFIG` 环境变量
3. `~/.openclaw/security-audit.json`
4. `.clawsec/allowlist.json`

### 配置文件格式

```json
{
  "enabledFor": ["audit"],
  "suppressions": [
    {
      "checkId": "skills.code_safety",
      "skill": "clawsec-suite",
      "reason": "First-party security tooling — reviewed by security team",
      "suppressedAt": "2026-02-15"
    }
  ]
}
```

### 抑制规则的语义

- `"enabledFor": ["audit"]` -- 启用审计结果的抑制（同时需要 `--enable-suppressions` 标志）
- `"enabledFor": ["advisory"]` -- 仅抑制建议性审计结果（对审计结果无影响）
- `"enabledFor": ["audit", "advisory"]` -- 两种审计流程都遵循抑制规则
- 如果 `enabledFor` 未设置或为空，则不启用抑制功能（安全默认设置）

### 匹配规则

- **checkId：** 与审计结果的检查标识符完全匹配（例如，`skills.code_safety`）
- **skill：** 与审计结果中的技能名称不区分大小写地匹配
- 必须同时满足这两个条件，发现结果才会被抑制

## 安装流程（交互式）

为了便于 MDM 部署，建议使用环境变量（无需提示）。

**必需的环境变量：**
- `PROMPTSEC_DM_CHANNEL`（例如 `telegram`）
- `PROMPTSEC_DM_TO`（收件人 ID）

**可选的环境变量：**
- `PROMPTSEC_TZ`（IANA 时区；默认为 `UTC`）
- `PROMPTSEC_HOST_LABEL`（报告中包含的主机标签；默认使用 `hostname`）
- `PROMPTSEC_INSTALL_DIR`（cron 脚本运行前使用的路径；默认为 `~/.config/security-checkup`）
- `PROMPTSEC_GIT_pull=1`（如果通过 git 安装，脚本会执行 `git pull --ff-only`）

如果未设置环境变量或使用默认值，可以使用交互式安装方式。不过，即使在这种情况下，工具的配置也非常简单。

## 创建定时任务

使用 `cron` 工具创建定时任务，配置如下：
- `schedule.kind="cron"`
- `schedule_expr="0 23 * * *"`
- `schedule.tz=<installer tz>`
- `sessionTarget="isolated"`
- `wakeMode="now"`
- `payload.kind="agentTurn"`
- `payload.deliver=true`

### 载荷消息模板（agentTurn）

创建定时任务时，需要指定以下载荷消息，以指示脚本执行以下操作：
1. 运行审计：
   - 建议使用 JSON 格式输出，以便于解析：
     - `openclaw security audit --json`
     - `openclaw security audit --deep --json`
2. 生成简洁的文本报告：
   - 包含时间戳和主机标识（如果可用）
   - 汇总各等级的发现结果（严重/警告/信息）
   - 对于每个严重/警告级别的发现结果，包含 `checkId`、标题以及简短的修复建议
   - 如果深度检查失败，还需包含错误信息
3. 发送报告：
   - 使用 `message` 工具将报告通过 DM 发送到指定的用户

### 电子邮件发送要求

优先尝试以下方式发送报告：

A) 如果部署中配置了电子邮件通道插件，使用：
   - `message(action="send", channel="email", target="target@example.com", message=<report>)`

B) 如果没有电子邮件通道插件，可以使用本地 sendmail：
   - 执行 `exec` 命令：`printf "%s" "$REPORT" | /usr/sbin/sendmail -t`（构建 To/Subject 标头）

如果这两种方式都不可行，仍然需要通过 DM 发送报告，并在报告中注明：“注意：无法发送到 target@example.com（电子邮件通道未配置）”。

## 任务的可重复执行性/更新

在添加新任务之前，请执行以下操作：
- `cron.list(includeDisabled=true)`
- 如果存在名为 `"Daily security audit"` 的任务，直接更新该任务，而不是创建重复的任务：
  - 调整任务的调度时间和表达式
  - 更新 DM 收件人信息

## 建议的命名规则

- 任务名称：`Daily security audit (Prompt Security)`

## 最小推荐默认设置（不建议自动更改配置）

定时任务的报告应提供修复建议，但不会自动应用这些建议。
除非用户明确要求，否则不要运行 `openclaw security audit --fix` 命令。