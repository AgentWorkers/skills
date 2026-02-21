---
name: proactive-claw
version: 1.2.0
description: >
  将AI代理转变为受管控的执行伙伴，它们能够理解你的工作、监控你的工作环境，并在你之前采取行动——以预测性方式并在你的控制范围内进行操作。🧠⚙️🦞  
  **以本地优先的自动化方式**：该工具会读取你的日历（仅限读取权限），并仅将其自身的“Proactive Claw — Actions”日历写入其中。它会运行一个用户级别的后台守护进程（每15分钟执行一次任务），所有决策都会被记录在本地。**安全默认设置**：大多数功能默认处于关闭状态。  
  **两种运行模式**：  
  1. **守护进程模式**（后台运行）：每15分钟执行一次任务，包括摄入用户事件、检测事件删除情况、自动重新链接被移动的事件、规划提醒事项以及触发相应的操作。该模式会读取所有用户的日历（仅限读取权限），并将操作记录到自身的日历及SQLite数据库中。  
  2. **对话模式**（可选，需要单独启用相关的大语言模型LLM）：在与你进行对话时，Claude Code可以选择性地调用proactive-claw脚本来读取你的日历信息、提议日程变更或记录对话结果——但前提是你需要为每次对话明确启用该功能。  
  **管控层**：统一的主动行为引擎整合了能源管理、通知机制、策略设置以及用户关系信息。系统支持不同的优先级级别（P0–P5），并设有静默时间段、操作冷却期以及每日操作次数的上限。用户可以调节系统的整体活跃程度（低/平衡/高级），同时还能设置操作自主性的上限（建议/确认/完全自主）。该系统会记录每一个决策的详细过程，以确保操作的透明性和可解释性。  
  **内存与学习机制**：采用衰减加权评分算法（最近的数据权重更高），通过SQLite数据库将用户事件与计划中的操作关联起来。系统具备检测策略冲突的能力，并定期进行系统健康检查。  
  **产品化功能**：提供配置向导、数据导出/备份功能、每月的运行状态监控以及模拟测试模式。  
  **系统要求**：需要安装python3环境，并使用Google OAuth认证（或Nextcloud应用程序的密码）。  
  **可选功能（默认均处于关闭状态）**：  
  - gh CLI（用于跨技能功能）  
  - NOTION_API_KEY（用于访问Notion平台）  
  - Telegram机器人令牌（用于通过Telegram发送通知）  
  - LLM_RATER_API_KEY（用于评估大型语言模型的表现）  
  - Apple Notes osascript（仅适用于macOS系统，用于将操作结果保存到Apple Notes中）  
  - Notion结果数据库（用于将操作结果保存到Notion平台）  
  **安全默认设置**：  
  - feature_cross_skill = false  
  - feature_voice = false  
  - feature_team_awareness = false  
  - feature_llm_rater = false  
  - max_autonomy_level = confirm （即操作完全由用户确认后执行，不具备自主决策权）
requires:
  bins:
    - python3
  env_vars: []
  credentials:
    - Google OAuth credentials (via setup.sh) OR Nextcloud app password (via setup.sh)

install:
  - kind: script
    label: "One-time setup — creates calendar, installs dependencies, configures daemon"
    command: "bash scripts/setup.sh"

side_effects:
  - Installs a user-level background daemon (launchd on macOS, systemd user timer on Linux) via install_daemon.sh. Runs every 15 min. Does NOT run as root. Uninstall instructions in SKILL.md.
  - Writes local files under ~/.openclaw/workspace/skills/proactive-agent/ only. No files written outside this directory.
  - Creates a "Proactive Claw — Actions" calendar in Google/Nextcloud. Never modifies your existing calendars — reads them only.
  - Maintains a SQLite link graph (proactive_links.db) tracking connections between your events and planned actions.
  - Outbound HTTPS to Google Calendar API only by default. Notion, Telegram, GitHub, clawhub.ai, LLM rating API are all opt-in via feature_* flags in config.json.
  - pip installs google-api-python-client, google-auth-oauthlib, google-auth-httplib2 (Google backend) or caldav, icalendar (Nextcloud backend) during setup.sh.
---
# 🦞 Proactive Claw v1.2.0  
> 将AI助手转变为受控的执行伙伴，它们理解您的工作，监控您的日程，并在您之前主动采取行动——预测性且受您的控制。  

---

## 🏗️ 架构 — 聊天 + 双日历 + 链接图  
**两种独立模式——均由 `max_autonomy_level` 控制：**  

| 模式 | 触发者 | 网络 | 自主性 |  
|------|----------------|---------|----------|  
| **聊天** | 您，在每次对话中明确请求 | 与守护进程相同 | 受 `max_autonomy_level` 限制 |  
| **守护进程** | 每15分钟自动触发 | Google/Nextcloud日历 | 受 `max_autonomy_level` 限制 |  

**您的日历** 在两种模式下均为只读——永远不会被修改。所有写入操作都只会发送到 “Proactive Claw — Actions” 日历。事件通过SQLite图谱链接，因此当源事件移动或被删除时，操作仍能保持同步。  

### 守护进程周期：计划 → 执行  
每15分钟（在 `install_daemon.sh` 启动后）：  
1. **计划**：收集用户事件，检测删除事件，自动重新链接移动的事件，计划提醒/准备/缓冲/总结操作  
2. **执行**：执行到期的操作（在发送前会检查 `sent_actions` 表）  
3. **清理**：每天一次：将暂停/取消的事件重命名，删除过期的条目  

### 聊天模式：按需，需您批准  
与Claude Code聊天时，它可以调用proactive-claw脚本来：  
- **查看您的日程** → `scan_calendar.py` → 显示结果，不进行任何写入  
- **提出更改** → `cal_editor.py --dry-run` → 在任何更改前获得您的批准  
- **记录结果** → `capture_outcome.py` → 仅在您确认摘要后执行  
- **检查政策会如何处理** → `policy_engine.py --evaluate --dry-run` → 仅提供建议  

**默认设置`max_autonomy_level: confirm`：**Claude Code **总是先询问您的同意**。设置为 `advisory` 时，它只能提供建议，而不能执行操作。设置为 `autonomous` 时，它可以自行行动（不推荐）。  

---

## 🔒 安全性与隐私  
### ⚠️ 重要提示：安装前请务必阅读  
1. **首先查看设置脚本：**  
   （这些脚本都是普通的shell脚本。确认它们只写入 `~/.openclaw/` 并创建用户级别的定时器，不会影响root服务。）  
2. **从安全默认设置开始：**  
   - **不要直接将 `config.example.json` 复制到 `config.json`  
   - 运行 `python3 config_wizard.py` 进行引导设置  
   - 或者手动创建 `config.json`，并将 `max_autonomy_level` 设置为 `confirm`（而非 `autonomous`）  
   - 确保所有 `feature_*` 都设置为 `false`，除非您确实需要它们  
3. **关于凭证：**  
   - Google：使用标准的OAuth桌面流程（`setup.sh` 负责处理）  
   - **不要使用 `clawhub_token`，除非您信任clawhub.ai**  
   - Nextcloud：生成应用程序特定的密码（绝不是您的账户密码）  
   - 所有外部API（Telegram、Notion、GitHub、LLM）：仅在启用相关功能时提供凭证  
4. **在测试模式下运行：**  

### 安全保障：  
| 内容 | 详情 |  
|------|--------|  
| **凭证仅保存在本地** | `credentials.json`、`token.json`、`config.json` 仅存储在 `~/.openclaw/workspace/skills/proactive-agent/` 中，绝不会上传到其他地方。**  
| **守护进程仅以用户身份运行** | `install_daemon.sh` 以用户身份启动守护进程（macOS使用launchd，Linux使用systemd）  
   - 卸载：`launchctl unload ~/Library/LaunchAgents/ai.openclaw.proactive-agent.plist` 或 `systemctl --user disable --now openclaw-proactive-agent.timer`（macOS）  
   - `systemctl --user disable --now openclaw-proactive-agent).*`（Linux）  
| **日历写入操作仅限于“Proactive Claw — Actions”日历** | 所有写入操作都只会发送到该日历，不会修改您的其他日历。  
| **网络调用受限制** | 所有外部网络调用都需要明确的配置或启用相关功能。默认仅使用Google日历API。Notion、Telegram、GitHub、LLM服务均为可选配置。**  

---

## ✨ 功能概览  
| 编号 | 功能 | 描述 |  
|---|---------|-------------|  
| 1 | 对话雷达 | 每次交流后无声地评分0–10分 |  
| 2 | 日历监控 | 扫描日历、检测冲突并识别可操作事件 |  
| 3 | 后台守护进程 | 每15分钟自动执行计划→执行→清理循环 |  
| 4 | SQLite内存 | 使用TF-IDF进行结果历史查询 |  
| 5 | 跨技能智能 | 支持GitHub和Notion的上下文信息（可选） |  
| 6 | 自然语言规则 | 用户定义的规则引擎 |  
| 7 | 事件后智能 | 提供跟进、每周摘要和季度分析 |  
| 8 | 日历策略引擎 | 自动执行准备/重点/缓冲/总结操作 |  
| 9 | 多智能体协调 | 完整的事件前准备流程 |  
| 10 | 能量预测 | 使用衰减权重进行预测性日程安排 |  
| 11 | 日历编辑 | 移动事件、查找空闲时间、清晰显示信息 |  
| 12 | 关系记忆 | 基于参与者和结果的轻量级CRM系统 |  
| 13 | 语音优先 | 集成Whisper功能并支持意图路由 |  
| 14 | 自适应通知 | 自动调整通知方式并随时间学习 |  
| 15 | 团队意识 | 可选的多日历协调功能 |  
| 16 | LLM交互评分 | 本地模型评估交互质量 |  
| 17 | **主动性引擎** | 统一的评分系统，结合能量、通知、策略和关系信号 |  
| 18 | **干扰管理** | 分为P0–P5五个优先级，设置每日提醒次数和冷却时间 |  
| 19 | **可解释性模式** | 可追踪每个提醒/策略/能量决策的来源 |  
| 20 | **主动性强度调节** | 全局调整评分乘数 |  
| 21 | **最大自主性限制** | 全局覆盖建议/确认/自主执行选项 |  
| 22 | **记忆衰减** | 所有模块均采用指数衰减权重 |  
| 23 | **系统健康检查** | 7项诊断检查 |  
| 24 | **策略冲突检测** | 检测相互矛盾的政策 |  
| 25 | **配置向导** | 提供交互式CLI设置并验证设置 |  
| 26 | **模拟模式** | 在未来N天内模拟守护进程的行为 |  
| 27 | **安静时段** | 在安静时段抑制非安全提醒 |  
| 28 | **数据导出/导入** | 支持JSON/CSV格式的备份和恢复 |  
| 29 | **趋势监控** | 提供每月行为报告和差异警报 |  
| 30 | **双日历架构** | 仅读取您的日历，所有操作都写入“Proactive Claw — Actions”日历 |  
| 31 | **链接图谱** | 使用SQLite图谱连接用户事件和计划操作 |  
| 32 | **操作规划器** | 在计划阶段：收集事件、检测缺失事件、自动重新链接 |  
| 33 | **操作执行器** | 在执行阶段：执行到期的操作 |  
| 34 | **删除检测** | 通过指纹匹配检测移动事件并确认/取消操作 |  
| 35 | **软取消政策** | 重命名取消的事件，并在N天后清理记录 |  

---

## 🛠️ 设置（只需运行一次）  
### 选项A — 使用clawhub OAuth（推荐，适用于移动设备）  
1. 访问 https://clawhub.ai/settings/integrations → 连接Google日历 → 复制您的token  
2. 在 `config.json` 中设置 `"clawhub_token": "your-token-here"`  
3. 运行 `setup.sh` — 凭证会自动下载，无需访问Google Cloud Console  

### 选项B — 手动设置Google凭证  
1. 访问 https://console.cloud.google.com → 新项目 → 启用Google日历API  
2. 创建OAuth 2.0凭证（桌面应用） → 下载JSON文件  
3. 将 `credentials.json` 文件移动到 `~/Downloads/credentials.json`  
4. 运行 `setup.sh`  

### 选项C — 使用Nextcloud CalDAV  
（具体步骤见代码块说明）  

### 安装后台守护进程  
- **macOS**：安装launchdplist，每15分钟自动运行  
- **Linux**：安装systemd用户定时器  
- 日志记录：`~/.openclaw/workspace/skills/proactive-agent/daemon.log`  

### 将现有结果数据迁移到SQLite  
（具体步骤见代码块说明）  

### 交互式配置向导  
（具体步骤见代码块说明）  

---

## ⚙️ 配置文件  
`~/.openclaw/workspace/skills/proactive-agent/config.json`  
直接编辑此文件以更改设置。仅修改右侧列中的值——不要更改键或结构。  

| 键 | 默认值 | 描述 |  
|-----|---------|-------------|  
| `calendar_backend` | `google` | `google` 或 `nextcloud` |  
| `timezone` | `UTC` | 例如 `Europe/Berlin` |  
| `daemon_interval_minutes` | `15` | 守护进程扫描的频率 |  
| `proactivity_mode` | `balanced` | `low`、`balanced`、`executive` | 控制评分乘数和提醒次数 |  
| `max_autonomy_level` | `autonomous` | `advisory`（仅建议），`confirm`（先询问），`autonomous`（执行） |  
| `quiet_hours` | `{"weekdays":"22:00-07:00","weekends":"21:00-09:00"` | 在这些时段抑制非安全提醒 |  
| `memory_decay_half_life_days` | `90` | 指数衰减的半衰期 |  
| `max_nudges_per_day` | `12` | 每天的提醒上限 |  
| `nudge_cooldown_minutes` | `30` | 被忽略提醒后的最小间隔时间 |  
| `watched_calendars` | `[]` | 需要监控的日历ID（空表示除了“Proactive Claw — Actions”日历外的所有日历） |  
| `ignored_calendars` | `[]` | 需要忽略的日历ID |  
| `action_cleanup_days` | `30` | 被取消的事件在多少天后被删除 |  
| `notification_channels` | `["openclaw","system"]` | `openclaw`、`system`、`telegram` |  
| `telegram_bot_token` | `""` | Telegram机器人token |  
| `telegram.chat_id` | `""` | 您的Telegram聊天ID |  
| `clawhub_token` | `""` | 来自clawhub.ai设置的token |  
| `notes_destination` | `local` | `local`、`apple-notes`（macOS）或`notion` |  

### 功能开关  
所有本地功能默认为开启状态。面向外部的功能默认为关闭状态。  

| 开关 | 默认值 | 描述 |  
| `feature_conversation` | `true` | 对话雷达评分功能 |  
| `feature_calendar` | `true` | 日历扫描功能 |  
| `feature_daemon` | `true` | 后台守护进程功能 |  
| `feature_memory` | `true` | SQLite内存存储功能 |  
| `feature_conflicts` | `true` | 冲突检测功能 |  
| `feature_rules` | `true` | 规则引擎功能 |  
| `feature_intelligence_loop` | `true` | 跟进和摘要功能 |  
| `feature_policy_engine` | `true` | 日历策略功能 |  
| `feature_orchestrator` | `true` | 多智能体协调功能 |  
| `feature_energy` | 能量预测功能 |  
| `feature_cal_editor` | `true` | 日历编辑功能 |  
| `feature_relationship` | `true` | 关系管理CRM功能 |  
| `feature_adaptive_notifications` | `true` | 自适应通知功能 |  
| `feature_proactivity_engine` | `true` | 统一的主动性评分功能 |  
| `feature Interruption_controller` | `true` | 干扰管理功能 |  
| `feature_explainability` | `true` | 决策可解释性功能 |  
| `feature_health_check` | `true` | 系统诊断功能 |  
| `feature_simulation` | 模拟模式功能 |  
| `feature_export` | 数据导出/导入功能 |  
| `feature_behaviour_report` | 行为报告功能 |  
| `feature_config_wizard` | 配置向导功能 |  
| `feature_policy_conflict_detection` | 政策冲突警报功能 |  
| `feature_crossSkill` | `false` | 关闭GitHub/Notion的上下文信息功能 |  
| `feature_voice` | `false` | 需要Whisper技能的语音功能 |  
| `feature_team_awareness` | `false` | 团队跨日历协调功能 |  
| `feature_llm_rater` | `false` | LLM评分功能（如使用云服务） |  
| `feature_telegram_notifications` | `false` | 需要Telegram机器人token的推送通知功能 |  

### LLM评分器配置  
| `llm_rater.enabled` | `false` | 是否启用评分器 |  
| `llm_rater.base_url` | `http://localhost:11434/v1` | LLM端点（Ollama默认值，无需设置key） |  
| `llm_rater.model` | `qwen2.5:3b` | 模型名称 |  
| `llm_rater.api_key_env` | `""` | 用于存储API key的环境变量（默认为空） |  
| `llm_rater.timeout` | `30` | 请求超时时间（以秒为单位） |  

---

## 功能1 — 对话雷达  
每次交流后无声地评分0–10分。在达到阈值时，会简要询问用户。  

### 功能2 — 日历监控 + 冲突检测  
- 扫描日历（缓存敏感，基于配置中的TTL设置）  
- 返回经过预过滤的、符合阈值且未被忽略的可操作事件列表。  

### 功能3 — 跨技能智能  
（具体实现细节见代码块说明）  

---

## 功能4 — SQLite内存  
现在使用**衰减加权平均**算法——最近的结果比旧的结果更重要。可通过 `memory_decay_half_life_days` 配置进行调节。  

---

## 功能5 — 跨技能智能  
**说明：**`crossSkill.py` 不会读取其他技能的token、配置文件或存储的数据。它仅：  
1. 检查特定技能是否已安装（通过检查`SKILL.md`文件是否存在）  
2. 如果存在`github`技能且`gh` CLI已授权，则执行`gh pr list`和`gh issue list`（仅读取）  
3. 如果存在`notion`技能且设置了`NOTION_API_KEY`环境变量，则在Notion中搜索相关内容  

---

## 功能6 — 自然语言规则  
（具体实现细节见代码块说明）  

## 功能7 — 事件后智能  
（具体实现细节见代码块说明）  

## 功能8 — 自动化日历策略引擎  
现在可以自动解析和执行自然语言日历策略：  

---

## 功能9 — 多智能体协调  
流程如下：打开行动项目 → 跨技能获取上下文 → 分析结果 → 起草邮件 → 生成Notion笔记 → 发送通知。  

## 功能10 — 预测性能量调度  
现在使用**衰减加权评分**算法——最近的数据比旧的数据更重要。  

## 功能11 — 自然语言日历编辑  
（具体实现细节见代码块说明）  

## 功能12 — 关系记忆  
（具体实现细节见代码块说明）  

## 功能13 — 语音优先  
集成Whisper功能并支持意图路由。  

## 功能14 — 自适应通知  
自动调整通知方式并根据用户行为进行优化。  

## 功能15 — 团队意识  
支持跨日历的协作功能（需用户选择）。  

## 功能16 — LLM交互评分  
使用本地模型评估交互质量。默认使用Ollama模型。  

## 功能17 — 主动性引擎  
统一的评分系统，结合多种信号源为每个事件生成综合评分：  

## 功能18 — 干扰管理  
根据优先级进行提醒过滤，并设置每日提醒次数和冷却时间：  

## 功能19 — 可解释性模式  
可追踪系统的每个决策过程。  

## 功能20 — 主动性强度调节  
全局调整评分乘数：  

## 功能21 — 最大自主性限制  
全局设置，用于限制系统的行为：  

## 功能22 — 记忆衰减  
所有模块均采用指数衰减权重。  

## 功能23 — 系统健康检查  
包含7项诊断检查：数据库、守护进程、配置、日历、设置、缓存状态和磁盘健康。  

## 功能24 — 策略冲突检测  
检测相互矛盾的政策。  

## 功能25 — 配置向导  
提供交互式CLI设置界面。  

## 功能26 — 模拟模式  
在未来N天内模拟守护进程的行为。  

## 功能27 — 安静时段  
在安静时段抑制非安全提醒。  

## 功能28 — 数据导出/导入  
支持JSON/CSV格式的备份和恢复。  

## 功能29 | 趋势监控  
提供每月的行为报告和差异警报。  

## 功能30 — 双日历架构  
仅读取用户的日历，所有操作都写入“Proactive Claw — Actions”日历。  

## 功能31 — 链接图谱  
使用SQLite图谱连接用户事件和计划操作。  

## 功能32 | 操作规划器  
在计划阶段：收集事件、检测缺失事件、自动重新链接事件。  

## 功能33 | 操作执行器  
在执行阶段：执行到期的操作。  

## 功能34 | 删除检测  
通过指纹匹配检测事件移动情况，并确认/取消操作。  

## 功能35 | 软取消政策  
重命名被取消的事件，并在N天后清理记录。  

---

## 🛠️ 设置步骤（只需运行一次）  
### 选项A — 使用clawhub OAuth（推荐，适用于移动设备）  
1. 访问 https://clawhub.ai/settings/integrations → 连接Google日历 → 复制token  
2. 在 `config.json` 中设置 `"clawhub_token": "your-token-here"`  
3. 运行 `setup.sh` — 凭证会自动下载，无需访问Google Cloud Console  

### 选项B — 手动设置Google凭证  
1. 访问 https://console.cloud.google.com → 新项目 → 启用Google日历API  
2. 创建OAuth 2.0凭证（桌面应用） → 下载JSON文件  
3. 将 `credentials.json` 文件移动到 `~/Downloads/credentials.json`  
4. 运行 `setup.sh`  

### 选项C — 使用Nextcloud CalDAV  
（具体步骤见代码块说明）  

---

## 注意：**安全与隐私设置**  
- **安装前务必阅读所有脚本和配置文件**  
- **使用安全的默认设置**  
- **谨慎处理凭证**  
- **仅将数据保存在本地**  
- **确保所有外部功能都是可选配置**  

---

## 📋 脚本审计  
所有新版本的v1.2.0脚本均为**本地运行**，除非另有说明。  

---

## 📋 脚本网络和使用子进程的情况  
- `scan_calendar.py`、`conflict_detector.py`、`daemon.py`、`memory.py`、`capture_outcome.py`、`create_checkin.py`、`crossSkill.py`、`rules_engine.py`、`intelligence_loop.py`、`policy_engine.py`、`orchestrator.py`、`energy_predictor.py`、`cal_editor.py`、`relationship_memory.py`、`voice_bridge.py`、`adaptive_notifications.py`、`team_awareness.py`、`llm_rater.py`、`cal_backend.py`、`setup.sh`、`install_daemon.sh` 都仅在本机运行，不涉及网络调用或子进程。  

## 📋 安装和卸载脚本  
- `setup.sh` 用于安装和卸载Proactive Claw。  
- `uninstall` 脚本用于卸载程序和相关配置文件。  

---

## 📋 文件结构说明  
- 日志文件存储在`~/.openclaw/workspace/skills/proactive-agent/`目录下。  
- 数据文件（`credentials.json`、`token.json`、`config.json`、`memory.db`、`proactive_links.db`）也存储在本机。  

## 📋 数据传输说明  
- 仅将必要的数据发送到指定的日历和日历操作日历。  
- 所有外部API访问都经过明确配置。  

---

## 📋 附加说明  
- 本文档提供了Proactive Claw的详细功能和设置指南。  
- 所有代码块都包含详细的注释和说明。  

---