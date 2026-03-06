---
name: Proactive Claw
description: 🦞 OpenClaw 最强大的主动式引擎。它就像您的个人助手，能够从您的使用习惯中学习，并帮助您提高工作效率。
version: 1.2.35

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
它通过在合适的时间提出智能建议来帮助您提高工作效率——并且（默认情况下）只会应用您批准的建议。

**所有功能都可以本地运行。**

---

## 一目了然的安全性 ✅  
✅ 在应用任何更改之前会先询问您的意见（默认设置）  
✅ 只会记录您批准的内容（不会随意修改您的日历）  
✅ 可选的后台进程（默认关闭）  
✅ 所有功能都可以本地运行（建议使用小型/本地的评分模型）  
✅ 本地状态文件夹是透明且可删除的  

---

## 人们为何会安装它（使用一周后的感受）  
- 您会变得更加有条理。  
- 您的日历安排会更加合理（重要任务会得到适当的缓冲时间）。  
- 长时间的高效工作不会被突然的会议打断。  
- 后续任务不会被遗漏。  
- Proactive Claw 会迅速了解您的习惯：您准备工作的时长、偏好的时间、什么会被拒绝、什么总是会被接受。  
简而言之：它成为了您的个人助手。  

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

**核心理念：** Proactive Claw 会主动提出建议，但最终的决定权仍在于您（默认设置）。  

---

## 快速入门（2分钟）  
1) 安装并启动 Proactive Claw：  
```bash
bash scripts/setup.sh
```  
2) 运行安全预览功能：  
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
- **后台建议模式：** 可选的后台进程，仍需您的批准  
- **自主模式（高级）：** 仅限您明确启用后使用（建议在使用一段时间后再尝试）  

---

## 预设设置（简单易用）  
您无需调整大量设置，只需选择一个预设即可。  
**预设设置只是一个起点**。Proactive Claw 会通过您的每次互动（批准、编辑、拒绝）来不断调整自己的行为，从而更好地满足您的需求。  

### A) 平静模式（最小干扰）  
如果您希望收到高价值的建议，请选择此模式：  
- 减少提示信息  
- 只安排重要任务的准备时间  

### B) 开发模式（保护高效工作时间）  
如果您需要长时间专注工作，请选择此模式：  
- 保护您 2–3 小时的专注工作时间  
- 建议调整会议时间以避免干扰  
- 提供更长的缓冲时间和恢复时间  

### C) 日程密集型模式  
当您的日程安排非常紧凑时，请选择此模式：  
- 增加缓冲时间并设置休息间隔  
- 防止连续会议导致工作被打断  
- 提出后续任务提醒，确保任务不会被遗漏  

（如果您愿意，这些预设设置可以直接复制到 `config.json` 文件中。）  

---

## 聊天评分模型（内置；建议使用小型/本地模型）  
Proactive Claw 内置了一个评分模型，用于评估各项任务的 **重要性、紧急性及干扰风险**，从而决定：  
- 哪些任务需要您的关注，  
- 何时应该提醒您，  
- 何时应该保持沉默。  
**建议：** 使用小型且本地化的评分模型（速度快、成本低、数据私密）。  

---

## 使用场景示例  
### 1) 明天有演讲 → 需要准备  
您：明天我要向董事会展示项目计划。  
Proactive Claw（评分 = 0.92）：该任务影响较大。您通常会准备 70 分钟。  
Proactive Claw：建议您在 10:00 的会议前预留 8:40–9:50 的时间进行准备，并设置 10 分钟的缓冲时间？  

### 2) 保护高效工作时间  
Proactive Claw（评分 = 0.78）：这个会议会打断您 9:30–12:00 的高效工作时间。  
Proactive Claw：建议将会议时间调整到 13:00，或者保留原时间并设置 20 分钟的恢复时间？  

### 3) 连续多场会议 → 设置缓冲时间  
Proactive Claw（评分 = 0.81）：明天有连续两场会议（10:00–14:00）。  
Proactive Claw：建议在会议之间设置 10 分钟的缓冲时间，并在中午安排 25 分钟的休息时间？  

### 4) 需要提醒的后续任务  
您：我承诺会发送会议总结。  
Proactive Claw（评分 = 0.66）：该任务时间紧迫。  
Proactive Claw：建议在会议结束后立即或 17:10 发送总结？  

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
## 0) 系统要求  
- 您的计算机上必须安装 Python 3  
- 如果使用 Google 后端：需要 `credentials.json`（OAuth 客户端凭证）  
  或  
- 如果使用 Nextcloud 后端：需要 CalDAV URL 和应用密码（或访问令牌）  

## 1) 安装依赖项并配置启动参数  
```bash
bash scripts/setup.sh
```  

## 2) 选择日历后端  
### 选项 A — Google 日历（OAuth）  
您需要提供 `credentials.json`（OAuth 客户端凭证）。  
Proactive Claw 会生成 `token.json` 文件（用于 OAuth 认证）。  

### 选项 B — Nextcloud（CalDAV）  
您需要提供 CalDAV 基本 URL 和应用密码。  

## 3) 配置行为  
使用交互式向导完成设置：  
```bash
python3 scripts/config_wizard.py
```  
默认设置非常安全：  
```bash
python3 scripts/config_wizard.py --defaults
```  

## 4) 可选的后台运行功能  
```bash
bash scripts/install_daemon.sh
```  

---

## 常见问题解答  
### 这会弄乱我的日历吗？  
**不会**。Proactive Claw 会在聊天框中提出建议，且只会应用您批准的内容（`max_autonomy_level = confirm`）。  

### 数据存储在哪里？  
数据存储在本地路径：`~/.openclaw/workspace/skills/proactive-claw/`  

### 所有功能都能本地运行吗？  
可以。虽然推荐使用小型/本地的评分模型，但日历数据仍会同步到您选择的云服务。  

### 没有 Google 也可以使用吗？  
可以，只需使用 Nextcloud（CalDAV）后端。  

### 什么是可选的后台进程？  
这是一个用户级别的调度程序（无需管理员权限），会定期运行以提供主动建议。该功能默认是关闭的。  

### “学习”指的是什么？  
Proactive Claw 会通过您的操作（批准、编辑）逐渐了解您的习惯：准备时间、偏好时间、缓冲时间设置、重要会议类型等。  

### 聊天评分模型是什么？  
这是一个简单的评分系统，通过数字分数（如 0.66、0.92）来评估任务的重要性及提醒的时机。建议使用小型/本地的评分模型。  

---

## 常见问题及解决方法  
- **提示过多** → 选择“平静模式”；多次拒绝建议后系统会自动调整  
- **建议不够主动** → 启用后台进程；提高评分敏感度  
- **准备时间的设置不正确** → 重新调整建议时间；系统会逐渐适应  
- **OAuth 问题** → 重新运行安装流程；如有必要，撤销令牌并重新登录  

---

## 卸载方法  
1) 如果安装了后台进程，请将其卸载  
2) 删除相关文件：`~/.openclaw/workspace/skills/proactive-claw/`  
3) 如果使用了 Google 后端，撤销 Google 的 OAuth 访问权限：  
`myaccount.google.com/permissions`  

---

## 术语解释  
- **准备时间**：为某项任务预留的时间  
- **缓冲时间**：防止日程冲突的短暂间隔  
- **高效工作时间**：连续不间断的工作时段  
- **后台进程**：可选的后台调度程序（默认关闭）  
- **评分**：0–1 的数字，表示任务的重要性或紧急程度  

---

## 如何进一步优化 Proactive Claw？  
1) 提供配置文件（如 `config.example.json`），以便我们能方便地修改预设设置。  
2) 指定评分显示格式（0.92 或 92/100，哪种更易于理解）。  
3) 是否希望将“高级设置”单独列出（是否包含在主文档中）。