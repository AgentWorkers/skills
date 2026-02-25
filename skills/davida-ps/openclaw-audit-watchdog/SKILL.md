---
name: openclaw-audit-watchdog
version: 0.1.1
description: 针对 OpenClaw 代理的自动化每日安全审计，支持通过电子邮件发送审计结果。该系统能够执行深入的安全检查，并生成格式化的审计报告。
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

**如果您已经安装了 clawsec-suite，那么您可能已经拥有这个工具了！**

openclaw-audit-watchdog 与 ClawSec Suite 捆绑在一起，提供关键的自动化安全审计功能。在安装该套件时，如果您的系统中还没有 audit watchdog，它会从捆绑的副本中自动安装。

**优点：**
- 方便：无需单独下载
- 安装位置固定：安装在 `~/.openclaw/skills/openclaw-audit-watchdog/`
- 保持现有设置：如果已经安装了 audit watchdog，它不会被覆盖
- 一次性验证：作为套件包的一部分进行完整性检查

### 选项 B：独立安装（请参阅此页面）

您可以独立安装 openclaw-audit-watchdog，而不需要安装整个套件。

**何时使用独立安装：**
- 只需要 audit watchdog，而不需要套件的其他组件
- 您希望在安装套件之前先安装 audit watchdog
- 您希望对自己的安装过程有更明确的控制

请继续阅读以下内容以获取独立安装的详细说明。

---

## 目标

创建（或更新）一个每日定时任务，该任务将执行以下操作：

1. 运行：
   - `openclaw security audit --json`
   - `openclaw security audit --deep --json`

2. 总结审计结果（包括严重/警告/信息级别的问题以及主要问题）

3. 将报告发送到：
   - 用户指定的 DM 目标（频道 + 收件人 ID/处理方式）

默认调度时间：**每天晚上 11 点（23:00）**，以您选择的时区为准。

**报告发送方式：**
- 通过 DM 发送到最后一个活跃的会话。

## 使用示例

### 示例 1：快速启动（使用环境变量）

对于自动化部署或 MDM 部署，在调用之前设置环境变量：

```bash
export PROMPTSEC_DM_CHANNEL="telegram"
export PROMPTSEC_DM_TO="@yourhandle"
export PROMPTSEC_TZ="America/New_York"
export PROMPTSEC_HOST_LABEL="prod-server-01"

# Then invoke the skill
/openclaw-audit-watchdog
```

该工具会自动配置并创建定时任务，无需额外提示。

### 示例 2：交互式设置

如果未设置环境变量，工具会提供最少的提示：

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

如果已经存在定时任务，该工具会更新现有任务，而不是创建重复的任务：

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

### 示例 5：自定义调度时间

如果您需要不同的调度时间，请在调用之前进行设置：

```bash
# Run every 6 hours instead of daily
export PROMPTSEC_SCHEDULE="0 */6 * * *"
/openclaw-audit-watchdog
```

### 示例 6：管理多个服务器

如果您需要管理多个服务器，请使用不同的主机标签：

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

### 示例 7：屏蔽已审核并接受的问题

要屏蔽已审核并接受的问题，请使用 `--enable-suppressions` 标志，并确保配置文件中包含 `"enabledFor": ["audit"]` 这一行：

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

被屏蔽的问题仍然会出现在报告中，但不会计入严重/警告问题的总数中。

## 屏蔽 / 允许列表

审计流程支持一种可选的屏蔽机制，用于管理已审核的问题。要启用屏蔽功能，必须同时满足两个条件：

### 启用要求

1. **命令行标志：** 在调用时必须传递 `--enable-suppressions` 标志。
2. **配置文件中的设置：** 配置文件中必须包含 `"enabledFor"`，并且数组中包含 `"audit"`。

如果缺少任何一个条件，所有问题都会被正常报告，屏蔽列表将被忽略。

### 配置文件的位置（共 4 种方式）

1. 显式传递 `--config <路径>` 参数
2. 使用 `OPENCLAW_AUDIT_CONFIG` 环境变量
3. 文件路径 `~/.openclaw/security-audit.json`
4. 文件路径 `.clawsec/allowlist.json`

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

### 配置文件中的关键设置

- `"enabledFor": ["audit"]` -- 启用审计屏蔽功能（同时需要 `--enable-suppressions` 标志）
- `"enabledFor": ["advisory"]` -- 仅启用建议性问题的屏蔽（对审计结果无影响）
- `"enabledFor": ["audit", "advisory"]` -- 两种类型的问题都支持屏蔽
- 如果 `enabledFor` 为空或缺失，则不启用屏蔽功能（安全默认设置）

### 匹配规则

- **checkId：** 与审计问题的标识符完全匹配（例如 `skills.code_safety`）
- **skill：** 与问题中提到的技能名称不区分大小写地匹配
- 问题只有满足这两个条件才会被屏蔽

## 安装流程（交互式）

为了便于 MDM 部署，建议使用环境变量（无需提示）。

**必需的环境变量：**
- `PROMPTSEC_DM_CHANNEL`（例如 `telegram`）
- `PROMPTSEC_DM_TO`（收件人 ID）

**可选的环境变量：**
- `PROMPTSEC_TZ`（IANA 时区；默认为 `UTC`）
- `PROMPTSEC_HOSTLABEL`（报告中包含的主机标签；默认使用 `hostname`）
- `PROMPTSEC_INSTALL_DIR`（cron 脚本运行前用于切换目录的路径；默认为 `~/.config/security-checkup`）
- `PROMPTSEC_GIT_pull=1`（如果通过 git 安装，脚本会执行 `git pull --ff-only`）

**路径解析规则：**
- 在 `bash`/`zsh` 中，使用 `PROMPTSEC_INSTALL_DIR="$HOME/.config/security-checkup"`（或绝对路径）。
- 不要使用单引号括起来的路径，例如 `'$HOME/.config/security-checkup'`。
- 在 PowerShell 中，使用：`$env:PROMPTSEC_INSTALL_DIR = Join-Path $HOME ".config/security-checkup"`。
- 如果路径解析失败，设置过程会立即退出并显示错误信息，而不会创建 `$HOME` 目录。

如果未设置环境变量或使用默认值，建议使用交互式安装方式。不过，即使在这种情况下，工具的配置也非常简单。

## 创建定时任务

使用 `cron` 工具创建定时任务，配置如下：
- `schedule.kind="cron"`
- `schedule.expr="0 23 * * *"`
- `schedule.tz=<installer tz>`
- `sessionTarget="isolated"`
- `wakeMode="now"`
- `payload.kind="agentTurn"`
- `payload.deliver=true`

### 载荷消息模板（agentTurn）

创建定时任务时，需要指定以下载荷消息，以指示脚本执行以下操作：

1. 运行审计：
   - 使用 JSON 格式输出，以便于解析：
     - `openclaw security audit --json`
     - `openclaw security audit --deep --json`

2. 生成简洁的文本报告：
   - 包含时间戳和主机标识（如果可用）
   - 按问题类型统计数量：
     - 对于严重/警告级别的问题，显示 `checkId`、问题标题以及相应的修复建议
   - 如果深度检查失败，显示检查错误信息

3. 发送报告：
   - 使用 `message` 工具将报告发送到指定的用户：

### 电子邮件发送方式

优先尝试电子邮件发送：
   A) 如果系统中配置了电子邮件通道插件，使用以下命令：
     - `message(action="send", channel="email", target="target@example.com", message=<report>)`

   B) 如果没有电子邮件通道插件，可以使用 `sendmail`：
     - `exec` 命令：`printf "%s" "$REPORT" | /usr/sbin/sendmail -t`（构建发送者和主题字段）

   如果两种方式都无法使用，仍然会通过 DM 发送报告，并提示：“无法发送到 target@example.com（电子邮件通道未配置）”。

## 任务的可重复执行性 / 更新

在添加新任务之前，请执行以下操作：
- `cron.list(includeDisabled=true)`
- 如果已经存在名为 `"Daily security audit"` 的任务，直接更新该任务，而不是创建重复的任务：
   - 调整任务的调度时间和表达式
   - 更新 DM 的接收目标

## 建议的命名规则

- 任务名称：`"Daily security audit (Prompt Security)"`

## 最小推荐默认设置（不建议自动修改配置）

定时任务的报告应提供修复建议，但不应自动执行修复操作。
除非明确要求，否则不要运行 `openclaw security audit --fix`。