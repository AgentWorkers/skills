---
name: jarvis-mission-control
description: "**搭建 JARVIS Mission Control v2.0.7 — 由 MissionDeck.ai 开发的免费开源 AI 代理协调平台**  
JARVIS Mission Control v2.0.7 是一个由 MissionDeck.ai 开发的免费开源 AI 代理协调平台，提供以下功能：  
- Kanban 任务管理板  
- 实时 WebSocket 更新  
- 团队聊天功能  
- 计划任务的可视化展示  
- 代理配置编辑器（SOUL Editor）  
- Claude 代码会话跟踪功能  
- GitHub 问题的同步  
- 基于 SQLite 的 webhook 发送机制（配备断路器保护机制）  
- 支持 CSRF 防护和速率限制  
**使用步骤：**  
1. 克隆 JARVIS Mission Control 的 GitHub 仓库（使用 `git clone` 命令）。  
2. 在您的服务器上启动服务器（使用 `python jarvis_server.py` 命令）。  
3. 打开控制面板（dashboard）。  
**无需云账户**：所有功能均直接在您的服务器上运行，无需使用云服务。  
**注意：**  
- 所有代码均来自开源的 GitHub 仓库，您可以在自己的服务器上执行这些代码。  
- 该平台的安全性评估等级为：0（高安全性）/ 0（严重安全性问题）。详细的安全性审计信息请参阅 `SECURITY.md` 文件。  
**技术特性：**  
- 支持 Kanban 任务管理  
- 实时数据更新（通过 WebSocket）  
- 强大的团队协作功能  
- 代理配置的可视化编辑  
- 与 Claude 代码环境的集成  
- 与 GitHub 问题的无缝同步  
- 高效的 webhook 发送机制（包含断路器保护）  
- 安全性措施：支持 CSRF 防护和速率限制  
**适合人群：**  
开发人员、系统管理员、AI 项目负责人等需要协调和管理 AI 代理的系统使用者。"
version: 2.0.7
homepage: https://missiondeck.ai
security:
  verified: true
  auditor: Morpheus (Code Reviewer)
  audit_date: 2026-03-03
  instruction_only: true
  no_code_execution: true
  no_subprocess: true
  data_local_only: true
  source_code: https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "bins": ["node", "npm", "git"] },
        "network": "optional",
        "security": "audited",
        "securityDoc": "SECURITY.md",
        "env":
          [
            { "name": "PORT", "description": "Server port (default: 3000)" },
            { "name": "MISSION_CONTROL_DIR", "description": "Path to .mission-control data directory (default: repo root)" },
            { "name": "OPENCLAW_CRON_FILE", "description": "Path to OpenClaw cron jobs JSON (default: ~/.openclaw/cron/jobs.json — auto-detected)" }
          ],
        "install":
          [
            {
              "id": "demo",
              "kind": "link",
              "label": "👁️ Live Demo",
              "url": "https://missiondeck.ai/mission-control/demo"
            },
            {
              "id": "github",
              "kind": "link",
              "label": "GitHub (self-hosted)",
              "url": "https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw"
            },
            {
              "id": "cloud",
              "kind": "link",
              "label": "☁️ MissionDeck.ai Cloud",
              "url": "https://missiondeck.ai"
            }
          ]
      }
  }
---
# JARVIS 任务控制中心

[![版本信息](https://img.shields.io/badge/version-2.0.7-brightgreen.svg)](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw/blob/main/CHANGELOG.md)  
[![许可证信息](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw/blob/main/LICENSE)  
[![安全性信息](https://img.shields.io/badge/security-audited-blue.svg)](./SECURITY.md)  

由 [MissionDeck.ai](https://missiondeck.ai) 开发 · [GitHub](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw) 提供 · [在线演示](https://missiondeck.ai/mission-control/demo)  

> **安全提示：** 本工具仅用于提供指令功能。所有命令均基于 GitHub 上的开源代码实现。经过安全性审计，未发现任何高风险（HIGH）或严重（CRITICAL）的安全问题。详情请参阅 [SECURITY.md](./SECURITY.md)。  

**v2.0.7** — 一个免费的开源多智能体协调平台，专为 OpenClaw 设计。  

**使用步骤：**  
- 克隆仓库 → 启动服务器 → 您的 AI 智能体团队和人类团队即可立即使用共享的看板、实时聊天功能以及完整的历史任务记录。  

| 选项 | 设置时间 | 链接 |
|--------|-----------|------|
| **👁️ 演示版** | 0 分钟 | [missiondeck.ai/mission-control/demo](https://missiondeck.ai/mission-control/demo) |
| **☁️ MissionDeck 云服务** | 5 分钟 | [missiondeck.ai](https://missiondeck.ai) |
| **🖥️ 自托管** | 10 分钟 | [GitHub](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw) |

---

## 快速入门  

服务器在启动时会自动检测所有正在运行的 OpenClaw 智能体，无需手动注册——智能体会在 30 秒内显示在控制面板上。  

---

## 功能介绍  

### 看板  
- 支持全屏显示的五列工作流程  
  - 支持拖放任务卡片  
  - 任务优先级通过左侧边框的颜色进行区分  
  - 智能体头像可显示任务分配者信息  
  - 卡片上会显示任务数量（超出限制时会有提示）  
  - 实时 WebSocket 同步：所有连接客户端的数据会立即更新  

### 智能面板（v2.0.3）  
通过顶部按钮可访问三个自定义面板：  
| 按钮 | 功能 |  
|--------|--------------|  
| 💬 聊天 | 实时团队聊天（WebSocket 传输，消息带有智能体表情符号，未读消息会有提示）  
| 📋 报告 | 智能体保存的文件位于 `.mission-control/reports/` 目录下，包含报告、日志和存档等标签  
| ⏰ 日程安排 | 所有智能体的定时任务信息（包括调度间隔、是否启用、上次执行时间）  

### 智能体功能  
- **Claude 代码会话**：每 60 秒自动检测 `~/.claude/projects/` 目录下的 JSONL 文件，显示相关信息（如令牌、模型、Git 分支）  
- **CLI 控制台**：可直接在浏览器中运行允许的 OpenClaw 命令  
- **GitHub 问题同步**：自动将未解决的问题转换为任务卡片（按问题编号唯一标识）  
- **智能体配置文件编辑**：可直接在控制面板中读取和编辑 `SOUL.md`、`MEMORY.md`、`IDENTITY.md` 文件  
- **智能体信息**：每个智能体都有独立的信息面板，显示技能、角色、活动时间线及消息记录  

### 可靠性  
- **SQLite Webhook 传输机制**（使用 `better-sqlite3` 和 WAL 模式），重启后数据仍可保留  
  - 重试策略：0 秒 → 1 秒 → 2 秒 → 4 秒 → 8 秒（最多尝试 5 次）  
  - 故障保护机制：连续 5 次失败后自动切断连接，60 秒后自动重试  
  - 可通过控制面板手动重试或重置连接  
- **结构化日志记录**：生产环境使用 JSON 格式记录日志，开发环境提供美观的可视化展示  
- **Jest 测试**：包含 51 个测试用例（执行 `npm test`）  
- **版本更新通知**：新版本发布时会在控制面板上显示提示  

### 安全性（生产环境强化版）  
- **CSRF 防护**：使用令牌中间件和 `HttpOnly` cookie  
- **速率限制**：普通请求每分钟 100 次；需要认证的请求每分钟 10 次  
- **代码清洗**：使用 `DOMPurify`、`sanitizeInput()` 和 `sanitizeId()` 进行输入内容过滤  
- **SSRF 防护**：通过 `validateWebhookUrl()` 阻止恶意请求（如私设 IP、本地地址、云服务元数据）  
- **当前安全状态**：0 个严重问题（CRITICAL），0 个高风险问题（HIGH）  

---

## `mc` CLI  
智能体可通过终端管理任务：  

---

## 数据存储  
所有数据均保存在 `.mission-control/` 目录下的 JSON 文件中，采用 Git 版本控制，无需外部数据库。  

---

## 版本历史  
| 版本 | 主要更新内容 |  
|---------|-----------|  
| 2.0.3 | 新增智能面板（聊天、报告、日程安排功能，支持 14 个定时任务）  
| 2.0.2 | 默认采用深色主题，修复模态框问题，修复文件 API 错误  
| 2.0.0 | 采用新的矩阵式界面设计（霓虹绿/青色背景，界面元素带有动态效果）  
| 1.19.0 | 重新设计面板标题栏  
| 1.18.0 | 侧边栏可折叠（分为“团队”、“系统”和“集成”三个部分）  
| 1.17.0 | 优化任务卡片显示效果（添加颜色边框、智能体头像等）  
| 1.16.0 | 控制面板新增功能卡片  
| 1.15.0 | 顶部显示综合指标（Claude、CLI、GitHub、Webhook 等信息）  
| 1.14.0 | 引入 SQLite Webhook 传输机制及故障保护机制  
| 1.12.0 | 新增 51 个 Jest 测试用例  
| 1.9.0 | 采用 Pino 结构化日志记录方式  
| 1.7.0 | 实施速率限制功能  
| 1.6.0 | 加强 CSRF 防护  
| 1.5.0 | 支持智能体配置文件同步  
| 1.4.0 | 实现与 GitHub 问题的自动同步  
| 1.3.0 | 直接集成 CLI 命令行工具  
| 1.2.0 | 支持 Claude 代码会话跟踪  
| 1.1.0 | 全面强化安全性（0 个严重问题，0 个高风险问题）  

---

## Asif2BD 的其他产品/服务  
---

## 许可证  
本项目采用 Apache 2.0 许可协议：[github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)  

---

[MissionDeck.ai](https://missiondeck.ai)  
提供免费试用版本，无需使用信用卡。