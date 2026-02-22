---
name: proactive-claw
version: 1.2.12
description: >
  🦞 你的AI能够提前规划你的日程——它不仅具备响应能力，还具有主动预测的能力。  
  📅 它会读取日历信息和聊天记录，从而规划提醒事项、准备相关资料，并在完成后进行总结；所有操作都会记录到它自己的“Proactive Claw — Actions”日历中。该AI支持两种运行模式：  
  - ⚙️ 背景守护进程模式（每15分钟自动执行计划、执行任务并清理临时文件，无需root权限）；  
  - 💬 对话模式（根据你的需求手动触发）。  
  🔒 默认情况下，AI的自主执行权限处于关闭状态。系统支持优先级分级（P0–P5），并设有安静时段和冷却机制，以确保操作的透明度和可解释性。该AI拥有35项实用功能，仅使用本地的SQLite数据库进行数据存储，且不发送任何遥测数据。  
  📦 安装步骤：  
  运行`bash scripts/setup.sh`脚本；通过`pip`安装所需的日历相关库；通过浏览器完成Google OAuth认证（需提供`credentials.json`文件）；或从`config.json`文件中读取Nextcloud应用程序的密码；创建“Proactive Claw — Actions”日历；可选地安装用户级别的`launchd`或`systemd`守护进程。所有数据文件都会保存在`~/.openclaw/workspace/skills/proactive-claw/`目录下，安装过程无需root权限。  
  ⚠️ 所有功能默认都是关闭状态。在正式使用前，请务必仔细阅读`setup.sh`脚本中的说明。  
  可选扩展功能包括：与Telegram、Notion或GitHub的集成，以及使用大型语言模型（LLM）进行任务评估——这些功能都需要用户明确选择是否启用。
emoji: 🦞
homepage: https://clawhub.ai/skills/proactive-claw
primaryEnv: GOOGLE_CREDENTIALS_PATH

requires:
  bins:
    - python3
    - bash
  env:
    - GOOGLE_CREDENTIALS_PATH
  config:
    - credentials.json (Google OAuth) OR nextcloud.password (Nextcloud app password)

install:
  - kind: uv
    label: "One-time setup: pip installs deps, Google OAuth or Nextcloud auth, creates action calendar, optional user-level daemon"
    package: "bash scripts/setup.sh"

side_effects:
  - Runs bash scripts/setup.sh — pip installs google-api-python-client/caldav, Google OAuth browser flow or Nextcloud credentials, creates "Proactive Claw — Actions" calendar.
  - Optionally installs user-level daemon (launchd macOS / systemd Linux) via install_daemon.sh. Runs every 15 min as your user. NOT root. Uninstall instructions in SKILL.md.
  - Writes only to ~/.openclaw/workspace/skills/proactive-claw/ — credentials.json, token.json, config.json, memory.db, proactive_links.db, daemon.log.
  - Writes to "Proactive Claw — Actions" calendar only. All other calendars read-only — never modified.
  - Outbound HTTPS: Google Calendar API by default. Notion/Telegram/GitHub/clawhub.ai/LLM require explicit feature_* opt-in.
---
# 🦞 Proactive Claw v1.2.12

> 将AI代理转变为受控的执行伙伴，它们理解您的工作，监控您的日程，并在您之前采取行动——以预测性和可控制的方式。

---

## 🏗️ 架构

**两种独立模式——均由 `max_autonomy_level` 控制：**

| 模式 | 触发条件 | 自主性 |
|------|---------|----------|
| 💬 **聊天** | 您在对话中明确请求 | 受 `max_autonomy_level` 限制 |
| ⚙️ **后台守护进程** | 每15分钟自动触发 | 受 `max_autonomy_level` 限制 |

**在两种模式下，您的日历都是只读的——永远不会被修改。所有写入操作都只会发送到 “Proactive Claw — Actions” 日历。事件通过SQLite图谱关联，因此当源事件移动或被删除时，操作会保持同步。**

### ⚙️ 守护进程周期：计划 → 执行 → 清理

每15分钟（在 `install_daemon.sh` 启动后）：

1. **计划** — 收集用户事件，检测删除事件，自动重新关联移动的事件，计划提醒/准备/缓冲/总结操作
2. **执行** — 以幂等方式触发应执行的操作（在发送前检查 `sent_actions` 表）
3. **清理** — 每天一次：将暂停/取消的事件重命名为 `🦞 [Paused] Original Title`，删除超过 `action_cleanup_days` 的取消条目

### 💬 聊天模式：按需，需您批准

在与Claude Code聊天时，它可以调用proactive-claw脚本来：

| 操作 | 脚本 | 效果 |
|--------|--------|--------|
| 查看您的日程 | `scan_calendar.py` | 显示结果 — 不会写入日历 |
| 提出更改建议 | `cal_editor.py --dry-run` | 在任何更改之前需要您的批准 |
| 记录结果 | `capture_outcome.py` | 仅在您确认摘要后记录 |
| 检查政策 | `policy_engine.py --evaluate --dry-run` | 仅提供建议 |

在 `max_autonomy_level: confirm`（默认值）下，Claude Code **总是先询问您的同意**。在 `autonomous` 模式下，它可以自行行动（不推荐）。