---
name: jarvis-mission-control
description: "**搭建 JARVIS Mission Control v2.0.4 — 一个免费的开源 AI 代理协调平台**  
JARVIS Mission Control v2.0.4 是一个开源的 AI 代理协调工具，提供以下核心功能：  
- **看板（Kanban）**：用于任务管理和进度跟踪  
- **实时 WebSocket 更新**：确保团队成员能够实时获取任务状态  
- **团队聊天**：支持实时沟通  
- **任务调度与监控**：可查看任务的执行计划和进度  
- **代理配置编辑器（Agent SOUL Editor）**：用于自定义代理的行为和设置  
- **Claude 代码会话跟踪**：记录代理执行的代码操作  
- **GitHub Issues 同步**：与 GitHub 问题库集成，便于问题追踪  
- **基于 SQLite 的 Webhook 通知系统**：支持错误报告和通知功能，并具备断路器（circuit breaker）保护机制  
- **CSRF 防护与速率限制**：保障系统安全  
**使用步骤：**  
1. **克隆仓库（Fork the repo）**：从 GitHub 上克隆 JARVIS 的源代码仓库。  
2. **启动服务器（Start the server）**：根据文档中的说明配置并运行服务器。  
3. **打开控制面板（Open the dashboard）**：通过浏览器访问服务器提供的 Web 界面。  
**无需云账户（No cloud account required）**：JARVIS 完全基于本地部署，无需依赖云服务。  
**适用场景：**  
- **多代理任务管理**：适用于需要管理多个 AI 代理的任务场景。  
- **人机协作**：帮助团队成员与 AI 代理协同完成工作。  
- **自定义监控**：需要自定义监控工具来追踪代理的运行状态和性能。  
JARVIS 是一个理想的工具，适用于那些希望实现高效、安全的 AI 代理协调系统的开发者和企业。"
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node", "npm", "git"] },
        "network": "optional",
        "env":
          [
            { "name": "PORT", "description": "Server port (default: 3000)" },
            { "name": "MISSION_CONTROL_DIR", "description": "Path to .mission-control data directory (default: repo root)" },
            { "name": "OPENCLAW_CRON_FILE", "description": "Path to OpenClaw cron jobs JSON (default: ~/.openclaw/cron/jobs.json — auto-detected)" }
          ]
      }
  }
---
# JARVIS 任务控制中心

**v2.0.4** — 一个免费的开源多智能体协调平台，专为 OpenClaw 设计。

**使用步骤：**  
 fork 该仓库 → 启动服务器 → 您的 AI 智能体团队和人类团队即可立即使用共享的看板、实时聊天功能以及完整的历史任务记录。

**GitHub 仓库：** [Asif2BD/JARVIS-Mission-Control-OpenClaw](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)  
**在线演示：** [missiondeck.ai/mission-control/demo](https://missiondeck.ai/mission-control/demo) （无需注册）

---

## 快速入门

**服务器自动发现所有运行的 OpenClaw 智能体**  
无需手动注册——智能体会在 30 秒内显示在仪表板上。

---

## 主要功能

### 看板  
- 支持全屏显示的五列工作流程  
  - 可拖放任务卡片  
  - 任务优先级通过左侧边框的颜色进行区分  
  - 智能体头像显示任务负责人  
  - 卡片上可显示任务剩余数量  
  - 实时 WebSocket 同步——所有连接的客户端都会立即更新信息  

### 智能面板（v2.0.3）  
通过顶部按钮可访问三个自定义面板：  
| 按钮 | 功能 |  
|--------|--------------|  
| 💬 聊天 | 实时团队聊天（WebSocket 传输，带智能体表情符号的消息气泡，未读消息标记） |  
| 📋 报告 | 智能体保存的文件（位于 `.mission-control/reports/` 目录下，包含报告、日志和存档选项） |  
| ⏰ 日程安排 | 所有智能体的 Cron 任务信息（包括调度间隔、是否启用、上次执行时间） |

### 智能体管理功能  
- **Claude 代码会话**：每 60 秒自动检测 `~/.claude/projects/` 目录下的 JSONL 文件；显示会话信息、成本、模型和 Git 分支  
- **CLI 控制台**：可直接在浏览器中执行允许的 OpenClaw 命令  
- **GitHub 问题同步**：从未解决的问题自动生成任务卡片（按问题编号唯一）  
- **智能体配置文件编辑**：可直接在仪表板上读取和修改 `SOUL.md`、`MEMORY.md`、`IDENTITY.md` 文件  
- **智能体信息**：每个智能体都有可滑出的信息面板，显示技能、角色和活动时间线  

### 可靠性  
- **SQLite Webhook 传输**（使用 `better-sqlite3` 和 WAL 模式）：重启后数据仍可保留  
  - 重试机制：0 秒 → 1 秒 → 2 秒 → 4 秒 → 8 秒（最多尝试 5 次）  
  - 故障保护机制：连续失败 3 次后自动关闭服务，60 秒后自动重试  
  - 可通过仪表板手动重试或重置服务  
- **结构化日志记录**：生产环境使用 JSON 格式记录日志，开发环境提供美观的可视化展示  
- **Jest 测试**：包含 51 个测试用例（`npm test` 命令执行）  
- **版本更新通知**：新版本发布时会在仪表板上显示通知  

### 安全性（生产环境强化版）  
- **CSRF 防护**：使用 token 中间件和 HttpOnly cookie  
- **速率限制**：普通请求限制为每分钟 100 次，需要认证的请求限制为每分钟 10 次  
- **代码清洗**：使用 `DOMPurify`、`sanitizeInput()` 和 `sanitizeId()` 进行输入安全处理  
- **SSRF 防护**：通过 `validateWebhookUrl()` 阻止恶意请求  
- **当前安全状态**：0（严重问题）· 0（高风险）

---

## `mc` CLI  
智能体可通过终端管理任务：

---

## 数据存储  
所有数据均存储在 `.mission-control/` 目录下的 JSON 文件中，支持 Git 版本控制，无需外部数据库。

---

## 版本历史  
| 版本 | 主要更新内容 |  
|---------|-----------|  
| 2.0.3 | 新增智能面板（聊天、报告、日程安排功能；支持 14 个 Cron 任务） |  
| 2.0.2 | 默认启用暗黑模式，修复模态框问题，修复文件 API 错误 |  
| 2.0.0 | 新界面设计（矩阵主题，采用霓虹绿/青色背景，文字效果优化） |  
| 1.19.0 | 重新设计面板标题栏的渐变效果 |  
| 1.18.0 | 侧边栏可折叠（分为团队、系统和集成选项） |  
| 1.17.0 | 优化任务卡片显示效果（添加颜色边框和智能体头像） |  
| 1.16.0 | 仪表板新增功能卡片展示 |  
| 1.15.0 | 仪表板整合综合指标（Claude、CLI、GitHub 和 Webhook 数据） |  
| 1.14.0 | 引入 SQLite Webhook 传输机制及故障保护机制 |  
| 1.12.0 | 添加 51 个 Jest 测试用例 |  
| 1.9.0 | 采用 Pino 结构化日志记录方式 |  
| 1.7.0 | 实施速率限制功能 |  
| 1.6.0 | 加强 CSRF 防护 |  
| 1.5.0 | 实现智能体配置文件的实时同步 |  
| 1.4.0 | 开启 GitHub 问题的同步功能 |  
| 1.3.0 | 直接集成 CLI 命令行工具 |  
| 1.2.0 | 优化 Claude 代码会话的跟踪功能 |  
| 1.1.0 | 完整提升系统安全性（0 高风险等级） |

---

## 许可证  
Apache 2.0 许可协议  
[GitHub 仓库：](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw)