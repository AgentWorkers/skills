---
name: overkill-mission-control
description: OpenClaw 的全面任务控制仪表板：用于监控代理、自动化流程、团队成员、文档、消息以及系统指标。该仪表板具备实时数据显示功能，支持代理间的消息传递、任务执行管理，并提供企业级监控服务。
homepage: https://github.com/your-repo/overkill-mission-control
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "requires": { "ports": [3000], "services": ["openclaw-gateway"] },
        "install":
          [
            {
              "id": "npm-install",
              "kind": "npm",
              "package": "next",
              "label": "Install Next.js dependencies",
              "command": "npm install",
              "workdir": "mission-control"
            },
            {
              "id": "service",
              "kind": "systemd",
              "label": "Create Mission Control systemd service",
              "path": "/etc/systemd/system/mission-control.service"
            },
            {
              "id": "tailscale",
              "kind": "systemd",
              "label": "Create Tailscale proxy service",
              "path": "/etc/systemd/system/tailscale-serve.service"
            }
          ],
      },
  }
---
# Overkill Mission Control

这是一个为企业级OpenClaw自主代理设计的操作控制面板。

## 概述

Mission Control为OpenClaw代理提供了全面的监控和控制功能，包括：
- 实时仪表板，显示实时指标
- 基于大型语言模型（LLM）的代理间消息传递功能
- 任务执行框架
- 自动化工作流程
- 文档管理
- 团队协作
- 系统警报和SLA（服务水平协议）跟踪

## 快速入门

1. **启动仪表板：**
   ```bash
   cd ~/.openclaw/workspace-mission-control
   npm run dev
   ```

2. **本地访问：** http://localhost:3000

3. **通过Tailscale访问：** https://ubuntu-openclaw.taila0448b.ts.net

## 页面结构

| 页面 | 描述 |
|------|-------------|
| `/` | 主仪表板，显示实时指标 |
| `/tasks` | 任务队列和任务管理 |
| `/workshop` | 代理工作坊（使用Kanban工具） |
| `/teams` | 团队管理 |
| `/messages` | 代理间消息传递 |
| `/documents` | 文档存储和管理 |
| `/automation` | 自动化工作流程 |
| `/intelligence` | 系统智能分析 |
| `/alerts` | 警报管理 |
| `/slo` | SLA/错误预算跟踪 |
| `/runbooks` | 运行手册自动化 |
| `/feature-flags` | 特性开关管理 |
| `/environments` | 环境配置比较 |
| `/webhooks` | Webhook管理 |
| `/stats` | 统计数据和分析 |
| `/settings` | 系统设置 |

## 主要功能

### 实时仪表板
- 实时会话数量
- 活动中的代理数量
- 资源使用情况（CPU、内存、磁盘）
- 系统健康状况
- 任务分配情况
- 活动时间线

### 代理间消息传递
- 代理之间可以发送消息
- 使用LLM（MiniMax M2.5）生成响应
- 支持任务执行
- 自动确认和回复
- 每60秒进行一次轮询

### 任务执行
代理可以根据接收到的消息内容执行相应任务：
- `researcher`：进行研究、网络搜索、总结信息
- `seo`：关键词研究、竞争对手分析
- `contentwriter`：撰写文章、修改文章内容
- `data-analyst`：数据分析、生成报告
- `designer`：生成图片、创建原型
- `orchestrator`：协调任务、分配工作

### 文档管理
- 可上传PDF、图片、文件
- 使用SQLite数据库进行存储，支持FTS5搜索算法
- 支持文件分类和标签管理
- 提供版本历史记录
- 具有访问控制功能（私有/代理/团队/公共）

### 自动化
- 提供可视化的工作流程构建工具
- 触发条件：定时任务、Webhook事件、手动触发、条件触发
- 可执行的操作：发送消息、发起HTTP请求、执行任务、通知相关人员、根据条件执行操作
- 提供分析仪表板

## API接口

| 接口 | 描述 |
|--------|-------------|
| `/api/status` | 系统状态和指标信息 |
| `/api/mission-control/agents` | 列出所有代理信息 |
| `/api/mission-control/sessions` | 会话数据管理 |
| `/api/messages` | 代理间消息传递功能 |
| `/api/messages/polling` | 消息轮询和执行机制 |
| `/api/documents` | 文档管理接口 |
| `/api/automation` | 自动化工作流程接口 |
| `/api/alerts` | 警报管理接口 |
| `/api/slo` | SLA/错误预算跟踪接口 |
| `/api/runbooks` | 运行手册管理接口 |

## 配置信息

### systemd服务配置

**mission-control.service:**
```ini
[Unit]
Description=Mission Control Dashboard
After=network.target

[Service]
Type=simple
User=broedkrummen
WorkingDirectory=/home/broedkrummen/.openclaw/workspace-mission-control
ExecStart=/usr/bin/npm run dev
Restart=always

[Install]
WantedBy=multi-user.target
```

**tailscale-serve.service:**
```ini
[Unit]
Description=Tailscale Serve for Mission Control
After=network.target tailscaled.service

[Service]
Type=simple
User=root
ExecStart=/usr/bin/sudo /usr/bin/tailscale serve 3000
Restart=always

[Install]
WantedBy=multi-user.target
```

## 数据库配置

- **消息数据存储：** `/mnt/openclaw/state/messages.db`
- **文档数据存储：** `/mnt/openclaw/state/documents.db`
- **系统状态数据存储：** `/mnt/openclaw/state/`

## 系统要求

- Node.js 22及以上版本
- Next.js 16版本
- 使用SQLite数据库（推荐使用sqlite3版本）
- 使用Tailwind CSS进行前端界面设计

## 常见问题解决方法

- **仪表板无法加载？** 请检查网络连接和服务器配置。
- **Tailscale无法正常使用？** 请检查Tailscale服务是否正在运行。
- **消息无法被处理？** 请检查系统日志和数据库连接状态。

## 文件结构

```
mission-control/
├── src/
│   ├── app/           # Next.js pages
│   ├── components/    # React components
│   ├── lib/          # Utilities and APIs
│   └── hooks/        # Custom React hooks
├── public/            # Static assets
├── package.json
└── next.config.js
```

## 开发工具与技术栈

本项目使用Next.js、Tailwind CSS和SQLite技术进行开发。