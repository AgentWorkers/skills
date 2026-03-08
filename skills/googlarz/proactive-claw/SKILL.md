---
name: Proactive Claw
description: 🦞 OpenClaw 最强大的主动式辅助工具。它是一个能够根据你的使用习惯进行学习、并帮助你提高工作效率的个人助手。
version: 1.2.41

metadata:
  openclaw:
    requires:
      bins: [python3]
      config: [credentials.json, config.json]
    install:
      - kind: shell
        label: "Run scripts/setup.sh --doctor, install required deps manually, then run scripts/setup.sh"
---
# 🦞 Proactive Claw

Proactive Claw 是一个**主动执行引擎**，它能够与您协作，并从您的行为中学习。它通过在恰当的时刻提出智能建议来帮助您提高工作效率——并且（默认情况下）只执行您批准的操作。

**所有功能都可以本地运行。**

---

## 一目了然的安全性 ✅

✅ 在应用任何更改之前会先询问您的意见（默认设置）  
✅ 只会记录您批准的内容（不会意外修改您的日历）  
✅ 以本地数据为核心（不依赖外部集成工具）  
✅ 所有功能都可以本地运行（建议使用小型/本地的评分模型）  
✅ 本地状态文件是透明且可删除的  

---

## 人们为什么选择安装它（使用一周后的感受）

- 您会更有条不紊地安排时间。  
- 您的日历会更加合理（重要任务会得到适当的缓冲时间）。  
- 长时间的高强度工作不会被突然的会议打断。  
- Proactive Claw 会快速了解您的习惯：准备时间、偏好时间、您会拒绝的任务以及总是接受的任务。  
简而言之：它将成为您的个人助理。

---

## 图 A — 功能流程（一目了然的运作方式）

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

**关键理念：** Proactive Claw 会主动提出建议，但最终的决定权仍在于您（默认设置）。  

---

## 快速上手（2分钟）

1) 运行准备状态检查：  
```bash
bash scripts/setup.sh --doctor
```

2) 如果缺少依赖项，会显示一个安装命令：  
```bash
bash scripts/setup.sh --print-install-cmd google
# or: bash scripts/setup.sh --print-install-cmd nextcloud
```

3) 建立日历连接：  
```bash
bash scripts/setup.sh
```

4) 运行安全预览：  
```bash
bash scripts/quickstart.sh
```

5) 在聊天中批准建议，然后执行该建议：  
```bash
python3 scripts/daemon.py
```

---

## 模式选择（根据您的需求调整）

- **建议模式（默认）：** 在应用更改前会先询问您的意见 (`max_autonomy_level=confirm`)  
- **后台模式（手动）：** 您可以自行运行本地守护进程 (`python3 scripts/daemon.py --loop`)  
- **自主模式（高级）：** 仅在使用一段时间后推荐使用  

---

## 预设设置（简单配置）

您无需调整大量设置，只需选择一个预设即可。  
**预设设置只是一个起点。** Proactive Claw 会通过您的每次互动（批准、编辑、拒绝）来不断调整自己的行为，从而更好地满足您的需求。  

### A) 平静模式（最小干扰）  
如果您只需要高价值的建议，请选择此模式：  
- 减少提示信息  
- 只为重要任务预留准备时间  

### B) 构建模式（保护长时间工作）  
如果您需要长时间专注地编写代码或进行构建工作，请选择此模式：  
- 保护您2–3小时的高强度工作时段  
- 建议调整会议时间以避免干扰  
- 提供更长的缓冲时间和恢复时间  

### C) 日程密集型模式  
当您的日程安排非常紧凑时，请选择此模式：  
- 为任务添加缓冲时间并设置恢复休息  
- 防止连续的任务导致工作节奏被打乱  
- 提醒您跟进未完成的任务  

（如果您需要，这些预设设置可以直接复制到 `config.json` 文件中。）

---

## 聊天评分模型（内置；建议使用小型/本地模型）

Proactive Claw 内置了一个评分模型，用于评估各项任务的**重要性、紧急性和干扰风险**，从而判断：  
- 哪些任务最重要，  
- 何时应该提醒您，  
- 何时应该保持沉默。  
**建议：** 使用小型且本地化的评分模型（速度快、成本低、数据私密）。  

---

## 使用场景示例（简短说明）

### 1) 明天有演讲 → 需要准备  
您：明天我要向董事会汇报项目计划。  
Proactive Claw（评分 = 0.92）：这项任务影响较大。您通常会为演讲准备约70分钟的时间。  
Proactive Claw：建议您将**08:40–09:50**预留为准备时间，并在10:00的会议前设置10分钟的缓冲时间？  

### 2) 保护长时间工作  
Proactive Claw（评分 = 0.78）：这次会议会打断您9:30–12:00的高强度工作时段。  
Proactive Claw：建议将会议时间调整到13:00，或者保留原时间并在会议后设置20分钟的恢复时间？  

### 3) 连续的工作日  
Proactive Claw（评分 = 0.81）：明天从10:00到14:00有一连串会议。  
Proactive Claw：建议在会议之间添加10分钟的缓冲时间，并在中午安排25分钟的休息时间？  

### 4) 常被忽略的跟进任务  
您：我承诺会发送会议总结。  
Proactive Claw（评分 = 0.66）：这项任务很紧急。  
Proactive Claw：建议在会议结束后立即（或17:10）安排20分钟的跟进时间？  

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

## 0) 确保系统满足以下要求  
- 您的机器上安装了 `python3`  
- 如果使用 Google 后端：需要 `credentials.json`（OAuth 客户端配置文件）  
  或  
- 如果使用 Nextcloud 后端：需要 CalDAV URL 和应用密码（或访问令牌）  

---

## 1) 验证依赖项并配置基础设置  
```bash
bash scripts/setup.sh --doctor
bash scripts/setup.sh --print-install-cmd google
# install dependencies manually
bash scripts/setup.sh
```

## 2) 选择日历后端  

### 选项 A — Google 日历（使用 OAuth）  
您需要提供：`credentials.json`（OAuth 客户端配置文件）  
Proactive Claw 会生成 `token.json` 文件（用于 OAuth 认证）。  

### 选项 B — Nextcloud（使用 CalDAV）  
您需要提供：CalDAV 基本 URL 和应用密码  

## 3) 配置应用程序行为  

通过交互式向导完成配置：  
```bash
python3 scripts/config_wizard.py
```  
默认设置保证了系统的安全性：  
```bash
python3 scripts/config_wizard.py --defaults
```  

## 4) 核心组件  
- 包含 `scripts/daemon.py` 文件，用于手动运行 Proactive Claw。  
- 发布的软件包中不包含跨技能连接工具、团队协作功能、守护进程安装程序、远程 OAuth 配置工具以及语言模型评分器。  

---

## 常见问题解答  

### 这个工具会弄乱我的日历吗？  
默认情况下：**不会**。Proactive Claw 仅会在聊天中提出建议，并且只执行您批准的操作（`max_autonomy_level = confirm`）。  

### 数据存储在哪里？  
数据存储在本地路径：`~/.openclaw/workspace/skills/proactive-claw/`  

### 所有功能都可以在本地运行吗？  
是的，所有功能都可以本地运行。虽然建议使用小型/本地的评分模型，但日历数据仍会同步到您选择的日历服务。  

### 如果没有 Google 账户也可以使用吗？  
可以，您可以使用 **Nextcloud（CalDAV）** 作为日历后端。  

### 核心组件包含守护进程安装程序吗？  
不包含。核心组件仅提供 `scripts/daemon.py` 文件用于手动运行 Proactive Claw，不包含自动启动的守护进程安装程序。  

### “学习”是什么意思？  
Proactive Claw 会通过您的操作（批准、编辑等）逐渐了解您的习惯：准备时间、偏好时间、任务类型以及您的工作规则。  

### 聊天评分模型是什么？  
这是一个轻量级的评分模型，通过数字分数（如0.66、0.92）来判断任务的重要性，并决定何时提醒您。建议使用小型/本地的评分模型。  

---

## 常见问题及解决方法  

- **提示过多**：尝试使用“平静模式”；多次拒绝建议后，Proactive Claw 会自动调整行为。  
- **建议不够主动**：运行 `python3 scripts/daemon.py --loop` 以持续进行本地扫描。  
- **准备时间的设置不正确**：重新调整相关设置，系统会逐渐适应。  
- **OAuth 问题**：重新运行安装流程；如有必要，可以撤销令牌并重新登录。  

---

## 卸载方法  
1) 删除以下文件：`~/.openclaw/workspace/skills/proactive-claw/`  
2) 如果您使用了 Google 账户，请撤销相应的 OAuth 访问权限：`myaccount.google.com/permissions`  

---

## 术语解释  

- **准备时间（Prep block）**：为某项任务预留的准备时间。  
- **缓冲时间（Buffer）**：防止日程冲突的短暂间隔。  
- **高强度工作（Deep work）**：需要持续专注的工作时段。  
- **守护进程（Daemon）**：在后台运行的程序（`python3 scripts/daemon.py --loop`）。  
- **评分（Score）**：0–1之间的数字，表示任务的重要性和紧急程度。  

---

## 如何进一步提升 Proactive Claw 的性能：  
1) 提供您的配置文件（如 `config.example.json`），以便我们能方便地将预设设置复制到配置文件中。  
2) 指定评分结果的显示格式（0.92 或 92/100），哪种更易于理解。  
3) 如果您需要更高级的自主设置，可以单独添加相关内容。