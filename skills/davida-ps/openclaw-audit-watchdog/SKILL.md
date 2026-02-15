---
name: openclaw-audit-watchdog
version: 0.0.4
description: 为 OpenClaw 代理程序提供自动化的每日安全审计服务，并通过电子邮件发送审计结果。该服务能够进行深入的安全检查，并生成格式化的审计报告。
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

**如果您已经安装了 clawsec-suite，那么您可能已经拥有了 openclaw-audit-watchdog！**

openclaw-audit-watchdog 与 ClawSec Suite 搭配使用，提供关键的自动化安全审计功能。在安装该套件时，如果系统中尚未安装 audit watchdog，它会从套件中自动安装。

**优点：**
- 便捷：无需单独下载
- 安装位置固定：安装在 `~/.openclaw/skills/openclaw-audit-watchdog/`
- 保持现有设置：如果已经安装了 audit watchdog，不会被覆盖
- 一次性验证：作为套件包的一部分进行完整性检查

### 选项 B：独立安装（请参阅此页面）

您可以单独安装 openclaw-audit-watchdog，而不需要安装整个 ClawSec Suite。

**何时使用独立安装：**
- 只需要 audit watchdog，而不需要套件的其他组件
- 希望在安装套件之前先安装 audit watchdog
- 希望对 audit watchdog 的安装过程有更详细的控制

**优点：**
- 安装过程更简单
- 与套件分离
- 可以完全控制安装过程

请继续阅读以下内容以获取独立安装的详细步骤。

---

## 目标

创建（或更新）一个每日 cron 任务，该任务将执行以下操作：

1) 运行：
   - `openclaw security audit --json`
   - `openclaw security audit --deep --json`

2) 汇总审计结果（包括严重/警告/信息级别的问题以及最常见的问题）

3) 将报告发送到：
   - 用户选择的 DM 目标（频道 + 收件人 ID/处理方式）

默认调度时间：**每天晚上 23:00（11 点）**（根据所选时区）。

**报告发送方式：**
- 通过 DM 发送到最后一个活跃的会话。

## 安装流程（交互式）

为了便于 MDM（Microsoft Dynamics 365 Management Module）管理，建议使用环境变量进行配置（无需提示输入）。

**必需的环境变量：**
- `PROMPTSEC_DM_CHANNEL`（例如：`telegram`）
- `PROMPTSEC_DM_TO`（收件人 ID）

**可选的环境变量：**
- `PROMPTSEC_TZ`（IANA 时区；默认为 `UTC`）
- `PROMPTSEC_HOSTLABEL`（报告中包含的标签；默认使用 `hostname`）
- `PROMPTSEC_INSTALL_DIR`（cron 脚本在运行前用于切换目录的路径；默认为 `~/.config/security-checkup`）
- `PROMPTSEC_GIT_PULL=1`（如果通过 git 安装，脚本会执行 `git pull --ff-only`）

如果未设置环境变量或使用默认值，也可以选择交互式安装。不过，即使在这种情况下，安装过程也非常简单，因为 audit watchdog 工具几乎可以直接使用。

## 创建 cron 任务

使用 `cron` 工具创建一个 cron 任务，配置如下：
- `schedule.kind="cron"`
- `schedule_expr="0 23 * * *"`
- `schedule.tz=<installer tz>`
- `sessionTarget="isolated"`
- `wakeMode="now"`
- `payload.kind="agentTurn"`
- `payload.deliver=true`

### 载荷消息模板（agentTurn）

创建的 cron 任务将包含以下载荷消息，用于指示 audit watchdog 执行以下操作：
1) 运行审计：
   - 建议使用 JSON 格式输出，以便于解析：
     - `openclaw security audit --json`
     - `openclaw security audit --deep --json`

2) 生成简洁的文本报告：
   - 包含时间戳和主机标识（如果可用）
   - 汇总问题数量
   - 对于每个严重/警告级别的问题，显示 `checkId`、`title` 以及简短的修复建议
   - 如果深度审计失败，显示错误信息

3) 发送报告：
   - 使用 `message` 工具将报告发送到指定的用户目标

## 电子邮件发送要求

尝试按照以下优先级顺序发送电子邮件：
A) 如果部署环境中存在电子邮件通道插件，请使用：
   - `message(action="send", channel="email", target="target@example.com", message=<report>)`

B) 如果没有电子邮件通道插件，可以使用本地 sendmail：
   - 使用 `exec` 命令发送邮件：
     - `printf "%s" "$REPORT" | /usr/sbin/sendmail -t`（构造 To/Subject 标头）

如果两种方式都无法发送邮件，仍然需要通过 DM 将报告发送给用户，并在报告中注明：“注意：无法发送到 target@example.com（电子邮件通道未配置）”。

## 避免重复执行 / 更新任务

在添加新任务之前，请先执行以下操作：
- `cron.list(includeDisabled=true)`
- 如果已经存在名为 `"Daily security audit"` 的任务，请更新该任务，而不是创建重复的任务：
   - 调整任务的时区或调度时间
   - 更新 DM 目标

## 建议的命名方式

- 任务名称：`"Daily security audit (Prompt Security)"`

## 最小推荐默认配置（不要自动更改配置）

cron 任务生成的报告应提供修复建议，但不会自动执行这些建议。

除非用户明确要求，否则不要运行 `openclaw security audit --fix` 命令。