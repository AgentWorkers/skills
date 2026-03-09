---
name: overkill-mission-control
description: OpenClaw 的综合任务控制仪表板：用于监控代理节点、自动化流程、团队成员、文档、消息以及系统指标。该仪表板具备实时数据显示功能，支持代理节点之间的消息传递、任务执行监控，并提供企业级管理视图。
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

Mission Control提供了对OpenClaw代理的全面监控和控制功能，包括：
- 实时仪表板，显示实时指标
- 基于大型语言模型（LLM）的代理间通信功能
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

3. **通过Tailscale访问：** https://<your-host>.taila0448b.ts.net （运行 `tailscale serve 3000` 以启用）

## 页面

| 页面 | 描述 |
|------|-------------|
| `/` | 主仪表板，显示实时指标 |
| `/tasks` | 任务队列和管理 |
| `/workshop` | 代理工作坊（使用Kanban管理） |
| `/teams` | 团队管理 |
| `/messages` | 代理间通信 |
| `/documents` | 文档存储和管理 |
| `/automation` | 自动化工作流程 |
| `/intelligence` | 系统智能分析 |
| `/alerts` | 警报管理 |
| `/slo` | SLA/错误预算跟踪 |
| `/runbooks` | 运行手册自动化 |
| `/feature-flags` | 特性开关管理 |
| `/environments` | 环境配置比较 |
| `/webhooks` | Webhook管理 |
| `/stats` | 统计和分析 |
| `/settings` | 系统设置 |

## 功能

### 实时仪表板
- 实时会话数量
- 活跃代理数量
- 资源使用情况（CPU、内存、磁盘）
- 系统健康状况
- 任务分配情况
- 活动时间线

### 代理间通信
- 代理之间发送消息
- 基于LLM的响应（使用MiniMax M2.5模型）
- 任务执行框架
- 自动确认和回复
- 每60秒进行一次轮询

### 任务执行
代理可以根据消息内容执行任务：
- `researcher`：进行研究、网络搜索、总结
- `seo`：关键词研究、审计、分析竞争对手
- `contentwriter`：撰写文章、修改文章
- `data-analyst`：分析数据、生成报告
- `designer`：生成图片、创建原型
- `orchestrator`：分配任务、协调工作

### 文档
- 上传PDF、图片、文件
- 使用SQLite数据库进行存储，支持FTS5搜索
- 支持文档分类和标签管理
- 提供版本历史记录
- 具有访问控制权限（私有/代理/团队/公共）

### 自动化
- 可视化工作流程构建器
- 触发条件：定时、Webhook、事件、手动触发
- 可执行的操作：发送消息、发送HTTP请求、执行任务、通知、根据条件执行操作
- 提供分析仪表板

## API接口

| 接口 | 描述 |
|----------|-------------|
| `/api/status` | 系统状态和指标 |
| `/api/mission-control/agents` | 列出所有代理 |
| `/api/mission-control/sessions` | 会话数据 |
| `/api/messages` | 代理间通信记录 |
| `/api/messages/polling` | 消息轮询与执行 |
| `/api/documents` | 文档管理 |
| `/api/automation` | 自动化工作流程 |
| `/api/alerts` | 警报管理 |
| `/api/slo` | SLA/错误预算跟踪 |
| `/api/runbooks` | 运行手册管理 |

## 配置

### systemd服务

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

## 数据库

- **消息数据：** `/mnt/openclaw/state/messages.db`
- **文档数据：** `/mnt/openclaw/state/documents.db`
- **系统状态数据：** `/mnt/openclaw/state/`

## 系统要求

- Node.js 22及以上版本
- Next.js 16版本
- 使用SQLite数据库（推荐使用sqlite3）
- 使用Tailwind CSS进行界面设计

## 故障排除

### 仪表板无法加载
```bash
# Check if server is running
curl http://localhost:3000

# Restart server
sudo systemctl restart mission-control
```

### Tailscale无法正常工作
```bash
# Check Tailscale status
tailscale status

# Restart Tailscale serve
sudo systemctl restart tailscale-serve
```

### 消息无法被处理
```bash
# Check cron job
cron list

# Manually trigger polling
curl -s http://localhost:3000/api/messages/polling?action=check-all
curl -s -X POST http://localhost:3000/api/messages/polling -H 'Content-Type: application/json' -d '{"action":"execute"}'
```

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

## 致谢

该项目使用Next.js、Tailwind CSS和SQLite技术构建。