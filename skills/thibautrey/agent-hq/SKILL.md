---
name: agent-hq
description: 部署 Agent HQ 的任务控制堆栈（Express + React + Telegram 通知器 / Jarvis 总结功能），以便其他 Clawdbot 团队能够快速搭建相同的功能模块，实现高优先级任务监控和自动化警报功能。该部署方案包括设置流程、遥测数据收集以及自动化脚本的集成。
---

# 代理总部（Agent HQ）安装指南

## 概述

- **后端 + 前端**：使用 Express 构建 API，数据存储在 SQLite 数据库中；前端界面由 `frontend-react/dist` 提供，采用 Vite/React 技术实现。
- **自动化组件**：包括 Jarvis 总结功能（`scripts/jarvis-connector.js`）、Telegram 通知功能（`scripts/notify-jarvis-telegram.js` 以及定时任务），此外后端代码 `backend/server.js` 中还包含一个高优先级的任务监控机制。
- **数据存储**：`data/board.json` 文件用于初始化任务、代理和卡片信息；这些数据会持久化存储在 `data/mission.db` 数据库中。
- **通知机制**：通过 `config/telegram.json` 文件（或环境变量 `AGENT_HQ_TELEGRAM_*`）配置，可以将警报信息发送到 Telegram。

## 安装步骤

1. 克隆仓库并安装依赖项：
   ```bash
   git clone https://github.com/thibautrey/agent-hq.git
   cd agent-hq
   npm install
   npm --prefix frontend-react install
   ```
2. 使用你的 `botToken` 和 `chatId` 更新 `config/telegram.json` 文件（或设置环境变量 `AGENT_HQ_TELEGRAM_TOKEN` 和 `AGENT_HQ_TELEGRAMCHAT_ID`）。请确保该文件的安全性。
3. 构建前端界面并启动服务器：
   ```bash
   npm --prefix frontend-react run build
   npm run start:agent-hq
   ```
   前端界面通过 `/` 路径提供访问，API 服务位于 `/api` 路径下（默认端口为 4000）。
4. 配置定时任务（包括 Jarvis 总结和 Telegram 通知）：
   - 执行 `node scripts/jarvis-connector.js` 或 `scripts/notify-jarvis-telegram.js --force` 来更新 Jarvis 总结信息。
   - 使用 `run-telegram-notifier.sh` 脚本来执行 Telegram 通知任务。
5. 通过前端界面创建卡片，或通过 `POST /api/cards`/`/api/cards/quick` 请求来触发相关操作。

## 运行时命令

- **查看任务列表**：`curl http://localhost:4000/api/board`
- **触发 Telegram 通知**：`curl -X POST http://localhost:4000/api/notify-telegram`
- **快速创建卡片**：`curl -X POST http://localhost:4000/api/cards/quick -H "Content-Type: application/json" -d '{"text":"Design review needed"}`
- **执行 Jarvis 总结任务**：`node scripts/jarvis-connector.js`

## 使用提示

- 在首次运行前，可以直接将卡片信息添加到 `data/board.json` 文件中以初始化任务数据。
- SQLite 数据库中的 `high_priority_jobs` 表可防止重复的 Telegram 通知。
- `AGENT_HQ_API_TOKEN` 用于保护 API 接口的安全性，防止未经授权的访问。

## 发布说明

- **2026-02-09**：新增了任务控制（Mission Control）功能，将 README 文件翻译为英文，添加了更新日志，并发布了 Clawdhub 的安装脚本 `agent-hq@1.0.0`（该版本现已与本文档同步）。

希望你能顺利使用这个代理总部系统来管理你的任务！