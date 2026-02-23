---
name: Proactive Claw
description: 🦞 OpenClaw 最强大的主动式引擎。它是一个能从您那里学习、并帮助您提高工作效率的个人助手。
version: 1.2.32

metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [credentials.json, config.json]
    install:
      - kind: shell
        label: "Run scripts/setup.sh to install dependencies and configure Google OAuth or Nextcloud CalDAV"
---
# 🦞 Proactive Claw

Proactive Claw 是一个 **主动执行引擎**，它能够 **与您协作** 并 **从您的行为中学习**。  
它通过在关键时刻提出智能建议来帮助您提高工作效率——并且（默认情况下）只会执行您批准的操作。

**所有功能都可以本地运行。**

---

## 一目了然的安全性 ✅  
✅ 在应用任何更改之前会先询问您的意见（默认设置）  
✅ 只会记录您批准的内容（避免意外修改日历）  
✅ 可选的后台守护进程（默认关闭）  
✅ 所有功能都可以本地运行（建议使用小型/本地的评分模型）  
✅ 本地状态文件是透明的，且可以随时删除  

---

## 为什么人们会安装它（使用一周后的感受）  
- 您会更频繁地做好充分准备。  
- 日历变得更加合理（重要任务会得到适当的缓冲时间）。  
- 长时间的高效工作不会被突然的会议打断。  
- 后续任务不会被遗漏。  
- Proactive Claw 会快速了解您的习惯：准备时间、偏好时间、您会拒绝的任务类型等。  
简而言之：它成为了您的个人助理。  

---

## 图 A — 功能流程（一目了然）  
```text
+--------------------------+        +--------------------------+
| Calendar                 |        | Chat                     |
| Google Calendar/Nextcloud|        | (your control loop)      |
+------------+-------------+        +------------+-------------+
             |  events <-> suggestions           | prompts <-> decisions
             |                                   |
             +-------------------+---------------+
                                 |
                                 v
                  +--------------------------------------+
                  |            Proactive Claw             |
                  |  - notices what's coming              |
                  |  - prioritizes what matters           |
                  |  - suggests prep / buffers / followup |
                  |  - learns from your feedback          |
                  |  - applies only what you approve      |
                  +--------------------------------------+
```  

**核心理念：** Proactive Claw 会主动提出建议，但最终的决定权仍掌握在您手中（默认设置）。  

---

## 快速入门（2分钟）  
1) 安装并启动 Proactive Claw：  
```bash
bash scripts/setup.sh
```  
2) 运行安全预览模式：  
```bash
python3 scripts/daemon.py --simulate
```  
3) 在聊天框中批准建议，然后运行该建议：  
```bash
python3 scripts/daemon.py
```  

---

## 模式选择（根据您的需求调整）  
- **建议模式（默认）：** 在应用更改前会先询问您的意见（`max_autonomy_level=confirm`）  
- **后台建议模式：** 可选的后台守护进程，仍需您批准  
- **自主模式（高级）：** 仅限您明确启用后使用（建议在使用一段时间后再尝试）  

---

## 预设设置（简单快速）  
您无需调整大量设置，只需选择一个预设即可。  
**预设设置只是一个起点**。Proactive Claw 会通过您的每次互动（批准、修改、拒绝）来不断调整自己的行为，从而更好地满足您的需求。  

### A) 平静模式（最小干扰）  
如果您希望收到高价值的建议，请选择此模式：  
- 减少提示信息  
- 仅安排重要任务的准备时间  

### B) 高效工作保护模式  
如果您需要长时间专注工作，请选择此模式：  
- 保护您 2–3 小时的专注时间  
- 建议调整会议时间以避免干扰  
- 提供更长的缓冲时间与恢复时间  

### C) 高密度会议周模式  
当您的日程安排非常紧凑时，选择此模式：  
- 自动添加缓冲时间与休息时间  
- 防止连续会议导致工作效率下降  
- 提醒您完成后续任务  

（这些预设设置可以通过在 `config.json` 文件中复制粘贴来轻松配置。）  

---

## 聊天评分模型（内置；建议使用小型/本地模型）  
Proactive Claw 内置了一个评分模型，用于评估各项任务的 **重要性、紧急性及干扰风险**，从而决定：  
- 哪些任务需要您的关注  
- 何时应该提醒您  
- 何时应该保持安静  

**建议：** 使用小型、本地的评分模型（运行速度快、占用资源少且私密性高）。  
您的日历管理系统可以使用更复杂的评分模型，但评分逻辑应保持简洁高效。  

---

## 实际使用场景（示例）  
### 1) 明天有演讲 → 需要准备  
您：明天我要向董事会展示项目计划。  
Proactive Claw（评分 = 0.92）：此任务影响较大，您通常会准备 70 分钟。  
Proactive Claw：建议将 **08:40–09:50** 安排为准备时间，并在 10:00 的会议前设置 10 分钟的缓冲时间？  

### 2) 保护高效工作时间  
Proactive Claw（评分 = 0.78）：这个会议会打断您 9:30–12:00 的高效工作时间。  
Proactive Claw：建议将会议时间调整到 13:00，或保留原时间并添加 20 分钟的恢复时间？  

### 3) 连续会议安排  
Proactive Claw（评分 = 0.81）：明天有连续的会议（10:00–14:00）。  
Proactive Claw：建议在会议之间添加 10 分钟的缓冲时间，并在中午安排 25 分钟的休息时间？  

### 4) 常被遗漏的后续任务  
您：我承诺会发送会议总结。  
Proactive Claw（评分 = 0.66）：此任务时间紧迫。  
Proactive Claw：建议在会议结束后立即（或 17:10）提醒您发送总结？  

---

## 图 B — 技术架构（后端支持：Google 或 Nextcloud）  
```text
TECHNICAL ARCHITECTURE (backend = Google OR Nextcloud)

             +----------------------------------------------+
             |        Calendar backend (choose ONE)         |
             |  +-----------------------+  OR  +----------+ |
             |  | Google (OAuth/API)    |      | Nextcloud| |
             |  +-----------------------+      | (CalDAV) | |
             |                                 +----------+ |
             +-----------------------+----------------------+
                                     ^
        events / changes (propose+apply, Actions only)       |
                                     |
                                     v
+----------------------+      +------------------------------------------+      +----------------------+
|  OpenClaw Chat UI    | <--> |           Proactive Claw Core            | <--> |  Local state         |
| prompts <-> decisions|      | 1) Ingest: events + chat signals         |      | config/token/SQLite  |
| feedback loop        |      | 2) Score: urgency/importance (local rec) |      | logs (optional)      |
+----------------------+      | 3) Plan : prep + buffers + follow-ups    |      +----------------------+
                              | 4) Approve (default): ask/confirm in chat|
                              | 5) Apply : write approved changes        |
                              | 6) Learn : from your approvals/edits     |
                              +------------------------------------------+
                                     ^
                                     |
                           Optional (explicit opt-in)
                                     |
                                     v
                              +----------------------+
                              | Optional daemon      |
                              | periodic scan/suggest|
                              +----------------------+
```  

---

## 安装说明  
## 0) 确保系统要求  
- 您的计算机上安装了 Python 3  
- 如果使用 Google 后端：需要 `credentials.json`（OAuth 客户端配置文件）  
  或  
- 如果使用 Nextcloud 后端：提供 CalDAV URL 和应用密码（或访问令牌）  

## 1) 安装依赖项并配置启动参数  
```bash
bash scripts/setup.sh
```  

## 2) 选择日历后端  
### 选项 A — Google 日历（OAuth）  
您需要提供 `credentials.json`（OAuth 客户端配置文件）。  
Proactive Claw 会自动生成 `token.json` 文件。  

### 选项 B — Nextcloud（CalDAV）  
您需要提供 CalDAV 基本 URL 和应用密码。  

## 3) 配置 Proactive Claw 的行为  
通过交互式向导完成配置：  
```bash
python3 scripts/config_wizard.py
```  
默认设置保证了使用的安全性：  
```bash
python3 scripts/config_wizard.py --defaults
```  

## 4) 可选的后台运行模式  
```bash
bash scripts/install_daemon.sh
```  

---

## 常见问题解答  
### 这会弄乱我的日历吗？  
**不会**。Proactive Claw 仅会在聊天框中提出建议，并且只会执行您批准的操作（`max_autonomy_level = confirm`）。  

### 数据存储在哪里？  
数据会存储在本地路径：`~/.openclaw/workspace/skills/proactive-claw/`  

### 所有功能都可以在本地运行吗？  
是的，所有功能都可以本地运行。虽然建议使用小型/本地的评分模型，但日历数据仍会同步到您的日历服务。  

### 没有 Google 日历也可以使用吗？  
可以，您可以使用 Nextcloud（CalDAV）作为日历后端。  

### 什么是可选的后台守护进程？  
这是一个用户级别的调度程序（无需管理员权限），它会定期运行以提供更智能的建议。默认情况下是关闭的。  

### “学习”指的是什么？  
Proactive Claw 会通过您的操作（批准、修改等）逐渐了解您的偏好：准备时间、偏好时间、缓冲时间设置、重要会议类型等。  

### 聊天评分模型是什么？  
这是一个轻量级的评分系统，会为各项任务分配数值评分（如 0.66、0.92），以判断其重要性和提醒时机。建议使用小型/本地的评分模型。  

---

## 常见问题及解决方法  
- **提示过多** → 选择“平静模式”；多次拒绝建议后系统会自动调整  
- **建议不够主动** → 启用后台守护进程并提高评分敏感度  
- **准备时间的设置不正确** → 重新调整设置；系统会逐渐优化  
- **OAuth 问题** → 重新运行安装流程；必要时重新获取访问令牌  

---

## 卸载方法  
1) 如果安装了后台守护进程，请将其卸载  
2) 删除相关文件：`~/.openclaw/workspace/skills/proactive-claw/`  
3) 如果使用了 Google 日历服务，请撤销 Google 的 OAuth 访问权限：  
   `myaccount.google.com/permissions`  

---

## 术语解释  
- **准备时间（Prep block）**：为某项任务预留的准备时间  
- **缓冲时间（Buffer）**：防止日程冲突的短暂间隔  
- **高效工作（Deep work）**：连续、不间断的工作时段  
- **后台守护进程（Daemon）**：可选的背景调度程序（默认关闭）  
- **评分（Score）**：0–1 的数值，表示任务的重要性和紧急性  

---

## 如何进一步提升 Proactive Claw 的性能：  
1) 提供配置文件（如 `config.example.json`），以便我们能更方便地调整预设设置。  
2) 指定评分显示格式（0.92 或 92/100），哪种更易于阅读。  
3) 是否需要为“自主模式”添加单独的说明部分（可选）。