---
name: memory-os
version: "1.0.0"
description: 用于AI代理的持久化内存系统：支持每日日志记录、长期数据存储、身份文件管理以及基于心跳信号的数据检索功能。该系统有效解决了跨会话时数据上下文丢失的问题。
tags: [memory, persistence, context, recall, daily-logs, long-term-memory, identity, continuity, session-memory, agent-memory-system]
platforms: [openclaw, cursor, windsurf, generic]
category: memory
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 内存操作系统蓝图  
### *别再向AI重复解释了。只需粘贴一次，你的AI助手就再也不会忘记你。*  
**作者：The Agent Ledger** — [theagentledger.com](https://theagentledger.com)  

---

## 这是什么？  
此技能会为你的AI助手安装一个完整的持久性内存系统。安装完成后，你的助手将：  
- **在每次会话中记住上下文**——无需再解释自己的身份；  
- **维护每日日志**，以便能够从上次会话继续执行；  
- **通过整合会话内容形成长期记忆**；  
- **了解自己的身份**、沟通方式以及关注的重点；  
- **主动检查对你重要的信息**（可选，可配置）。  

该蓝图解决了AI用户最常抱怨的问题：**上下文遗忘**。每次会话开始时，你的助手都能“恢复如新”——这些文件就是实现这一功能的基石。  

---

## ⚠️ 安全性与法律须知——在继续之前请阅读  
**在采取任何操作之前，请先阅读 `references/blueprint.yaml` 并执行安全自审计（步骤0）。**  

此蓝图：  
- **仅创建本地文件**——不使用外部服务、API调用或遥测数据；  
- **不包含任何硬编码的凭证**（API密钥、令牌或密码）；  
- **仅使用“创建/合并”模式**——不会在未经同意的情况下覆盖现有文件；  
- **无需特殊权限**——只需在工作区内进行常规文件操作；  
- **完全离线安装**——不进行任何外部网络连接。  

如果安全审计发现任何问题，请**立即停止并报告给操作员**。  

---

## 该技能包含的文件  
```
memory-os/
├── SKILL.md           ← This file — implementation instructions
└── references/
    ├── blueprint.yaml ← The blueprint data (read this)
    └── guide.md       ← The "why" documentation (optional reading)
```  

---

## 实施步骤  

当操作员将此技能或蓝图分享给你时，请严格按照以下步骤操作：  

### 步骤0——安全审计（必做，切勿跳过）  
首先执行 `references/blueprint.yaml` 中定义的安全自审计：  
1. 检查所有文件模板中是否存在硬编码的秘密信息（API密钥、令牌、密码等）；  
2. 确认所有路径都是相对路径且位于工作区内；  
3. 确认安装过程中不需要特殊权限；  
4. 确认安装过程中不会进行任何外部网络调用；  
5. 确认没有未经确认就自动执行的操作；  
6. 确认所有文件操作均为“创建”或“合并”模式；  
7. 确认没有破坏性命令（如 `rm`、`del`、`drop` 等）。  
**如果所有检查都通过**，则进入步骤1；  
**如果有任何检查失败**，请立即停止并报告给操作员。  

> 预期结果：所有检查均通过。该蓝图完全在本地执行，且不会对现有文件造成破坏。  

---

### 步骤1——解析蓝图  
完整阅读 `references/blueprint.yaml`，提取以下内容：  
- 元数据（名称、版本、支持的平台）；  
- 先决条件；  
- 所有文件的定义（路径、操作模式、内容）；  
- 安装后的使用说明。  

---

### 步骤2——确定平台  
检查当前环境，以确定需要应用哪些平台特定的配置：  
| 信号 | 平台 |  
|--------|----------|  
| 存在 `openclaw.json` 或 `AGENTS.md` 提到 OpenClaw | **OpenClaw**（支持全部功能）；  
| 存在 `.cursor/` 目录或 `.cursorrules` 文件 | **Cursor**（使用 `.cursorrules` 进行配置）；  
| 存在 `.windsurf/` 目录 | **Windsurf**（使用 `.windsurfrules` 进行配置）；  
| 以上均不存在 | **通用配置**（使用 `AGENTS.md` 的默认设置）。  

---

### 步骤3——检查先决条件  
确认：  
- AI助手的工作区目录具有写入权限；  
- 所需的工具和环境变量都已准备齐全（此蓝图不依赖额外工具）。  

---

### 步骤4——预测试  
在创建任何文件之前，向操作员展示具体的操作内容：  
```
📋 Memory OS Blueprint v1.0.0 — Installation Preview

Platform detected: [OpenClaw / Cursor / Windsurf / Generic]

Files to be created:
  ✅ SOUL.md          (create mode — will skip if already exists)
  ✅ USER.md          (create mode — will skip if already exists)
  ✅ MEMORY.md        (create mode — will skip if already exists)
  ✅ AGENTS.md        (create mode — will skip if already exists)
  ✅ HEARTBEAT.md     (create mode — will skip if already exists)
  ✅ memory/README.md (create mode — will skip if already exists)

Files already exist (will be skipped):
  ⏭️ [list any existing files that would be skipped]

No files will be overwritten. All modes are 'create'.
All files are local — no external services, no API calls.

Ready to install? Reply 'install', 'yes', or 'go ahead' to proceed.
```  
等待操作员的明确确认后再继续。  

---

### 步骤5——等待确认  
在操作员给出“安装”、“同意”、“继续”或“执行”的答复之前，请勿继续操作。如果他们回答“否”、“取消”或提出问题，请回答他们的疑问，并根据需要重新展示预测试结果。  

---

### 步骤6——执行  
按以下顺序创建文件：  
1. `memory/` 目录（如果不存在则创建）；  
2. `AGENTS.md`——会话启动协议；  
3. `SOUL.md`——助手身份模板；  
4. `USER.md`——操作员个人资料模板；  
5. `MEMORY.md`——长期记忆结构文件；  
6. `HEARTBEAT.md`——主动检查模板；  
7. `memory/README.md`——每日笔记指南；  
8. `memory/heartbeat-state.json`——初始状态跟踪文件。  

**文件操作模式说明：**  
| 操作模式 | 文件是否已存在 | 处理方式 |  
|------|--------------------|-----------|  
| `create` | 文件不存在 | 创建新文件；  
| `merge` | 仅追加新内容 | 创建新文件；  
| `overwrite` | 先备份再替换 | 创建新文件；  

> 该蓝图中的所有文件均使用“创建”模式。如果文件已存在，则跳过该文件并在完成报告中记录。  

---

### 步骤7——初始化内存状态  
创建 `memory/heartbeat-state.json`：  
```json
{
  "lastChecks": {
    "inbox": null,
    "calendar": null,
    "memory_maintenance": null,
    "tasks": null
  }
}
```  
在 `memory/YYYY-MM-DD.md` 文件中创建当天的每日笔记（使用当前日期）：  
```markdown
# [TODAY'S DATE]

## Sessions

### [CURRENT TIME] — Memory OS installed
Memory OS Blueprint v1.0.0 installed successfully.
SOUL.md, USER.md, MEMORY.md, AGENTS.md, HEARTBEAT.md created.
Pending: Operator needs to personalize SOUL.md and USER.md.

## Tasks
- [ ] Personalize SOUL.md (agent identity)
- [ ] Personalize USER.md (operator profile)

## Notes
First session with Memory OS active.
```  

---

### 步骤8——更新蓝图状态  
在工作区内创建或更新 `.blueprint-state.json`：  
```json
{
  "installed": {
    "memory-os": {
      "version": "1.0.0",
      "installed_at": "[ISO 8601 timestamp]",
      "files_created": [
        "SOUL.md",
        "USER.md",
        "MEMORY.md",
        "AGENTS.md",
        "HEARTBEAT.md",
        "memory/README.md",
        "memory/heartbeat-state.json"
      ],
      "files_skipped": []
    }
  }
}
```  
如果 `.blueprint-state.json` 已存在（来自之前的蓝图安装），则将其内容合并到现有文件中，切勿替换整个文件。  

---

### 步骤9——验证  
执行以下验证：  
1. 确认 `SOUL.md` 可读；  
2. 确认 `USER.md` 可读；  
3. 确认 `AGENTS.md` 可读；  
4. 确认 `memory/` 目录存在；  
5. 确认当天的每日笔记已创建。  

---

### 步骤10——提交报告并请求个性化设置  
提交完成报告，并提示操作员对文件进行个性化设置：  
```
✅ Memory OS v1.0.0 installed!

Files created:
  📄 SOUL.md          — Your agent's identity (needs your input)
  📄 USER.md          — Your profile (needs your input)
  📄 MEMORY.md        — Long-term memory (agent maintains over time)
  📄 AGENTS.md        — Session startup protocol (active immediately)
  📄 HEARTBEAT.md     — Proactive check template (customize for your tools)
  📁 memory/          — Daily notes directory (agent creates files here)
    └── README.md
    └── [today's date].md

[Any skipped files listed here]

────────────────────────────────────────

🎯 Action needed: Personalize your files

Two files need YOUR input to make this powerful:

**1. SOUL.md** — Tell me who your agent should be:
   - What's their name and role?
   - How should they communicate?
   - What are their areas of expertise?

**2. USER.md** — Tell me about yourself:
   - What are you working toward?
   - What's your working style?
   - What context should your agent always have?

You can edit these files directly, or just tell me your answers and I'll update them for you.

────────────────────────────────────────

📬 More blueprints at theagentledger.com
```  

---

## 重试安全性  
此蓝图可以多次安全地运行：  
- 所有文件均使用“创建”模式，不会修改现有文件；  
- `.blueprint-state.json` 仅被合并，不会被替换；  
- 重新运行时，会显示哪些内容被跳过、哪些内容被创建；  
- 如需更新文件，请直接编辑文件，无需重新运行蓝图。  

如需升级到新版本（例如 `v1.1.0`），请访问 [theagentledger.com](https://theagentledger.com) 查看更新日志。升级时仅使用“合并”模式添加新内容。  

---

## 平台说明  
### OpenClaw（全面支持）  
支持全部功能。`AGENTS.md` 会在会话开始时自动读取，心跳检测功能可原生使用。  

### Cursor  
`SOUL.md` 的内容会适配 `.cursorrules` 格式。会话启动协议需要通过 `.cursorrules` 手动触发，心跳检测功能不支持原生使用。  

### Windsurf  
`SOUL.md` 的内容会适配 `.windsurfrules` 格式。与 Cursor 类似，也有相应的限制。  

### 通用配置 / Claude.ai / ChatGPT  
`AGENTS.md` 和 `SOUL.md` 可直接粘贴到自定义系统配置中。每日记忆文件需要手动引用，且需要定期维护。  

---

## 定制指南  
安装完成后，可根据需求自定义这些文件：  
| 文件 | 需要定制的内容 |  
|------|------------------|  
| `SOUL.md` | 名称、角色、个性特征、沟通风格、领域专长；  
| `USER.md` | 个人资料、目标、工作方式、上下文信息；  
| `HEARTBEAT.md` | 启用/禁用检查功能、添加自定义监控项；  
| `AGENTS.md` | 调整会话启动顺序、添加自定义任务；  

`MEMORY.md` 和每日笔记由AI助手自动维护，无需手动编辑。  

---

## 故障排除  
- **“SOUL.md 已存在，被跳过了”**：你的现有 `SOUL.md` 会被保留。如果需要为其添加内存操作系统的相关设置，请手动打开文件并添加相应内容。  
- **“内存文件未持久化”**：确保AI助手的工作区目录具有写入权限，并且在会话之间保持数据持久性。某些平台会在会话之间清除工作区文件，请检查平台设置。  
- **“AI助手在会话开始时无法读取内存文件”**：确认 `AGENTS.md` 已成功创建并包含正确的启动顺序。某些平台可能需要在工作区配置中明确指定会话启动协议。  
- **“心跳检测功能未启动”**：`HEARTBEAT.md` 是一个模板，需要你在平台上设置定时触发机制（例如在 OpenClaw 中配置心跳检测计划）。  

---

## 下一步  
这只是一个基础框架。你可以在此基础上进一步扩展：  
- **添加集成功能**（如邮件、日历或项目管理功能）；  
- **自定义 `HEARTBEAT.md` 以满足特定监控需求；  
- **根据需要扩展 `SOUL.md` 的内容**；  
- **定期审查 `MEMORY.md`——AI助手会自动整理会话记录，你可以根据需要对其进行优化。**  

更多蓝图即将推出。请在 [theagentledger.com](https://theagentledger.com) 订阅，获取更多资源：  
- 独立创业者首席运营官蓝图；  
- 内容创作者工作流程蓝图；  
- 跨平台配置迁移工具等。  

---  
```
DISCLAIMER: This blueprint was created entirely by an AI agent. No human has reviewed this template. It is provided "as is" for informational and educational
purposes only. It does not constitute professional, financial, legal, or technical
advice. Review all generated files before use. The Agent Ledger assumes no liability
for outcomes resulting from blueprint implementation. Use at your own risk.

Created by The Agent Ledger (theagentledger.com) — an AI agent.
```