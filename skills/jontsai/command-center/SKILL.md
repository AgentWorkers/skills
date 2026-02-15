---
name: command-center
version: 1.0.4
description: OpenClaw的任务控制面板：提供实时会话监控、大型语言模型（LLM）使用情况跟踪、成本分析以及系统关键指标的展示。您可以在一个地方查看所有的人工智能代理（AI agents）。
metadata:
  openclaw:
    requires:
      node: ">=18"
    install:
      - id: start
        kind: shell
        command: "node lib/server.js"
        label: "Start Command Center (http://localhost:3333)"
---

# OpenClaw 命令中心

您的 AI 工作力的任务控制中心。

## 快速入门

```bash
# Install from ClawHub
clawhub install command-center

# Start the dashboard
cd ~/.openclaw/skills/command-center
node lib/server.js
```

仪表板运行地址：**http://localhost:3333**

## 功能

- **会话监控** — 实时查看所有 AI 会话，并提供实时更新
- **大型语言模型（LLM）使用情况** — 监控 Claude、Codex 等模型的使用情况
- **系统状态** — CPU、内存、磁盘、温度等系统指标
- **定时任务** — 查看和管理已安排的任务
- **对话内容整理** — 自动整理对话内容
- **成本跟踪** — 记录每次会话的成本、预测及节省金额
- **隐私控制** — 可隐藏演示中的敏感内容

## 配置

仪表板会自动检测您的 OpenClaw 工作空间。如需自定义，请设置 `OPENCLAW_WORKSPACE` 环境变量。

### 认证方式

| 认证模式 | 使用场景                |
| -------- | ---------------------- |
| `none`   | 本地开发                |
| `token`   | 远程访问                |
| `tailscale` | 团队 VPN                |
| `cloudflare` | 公开部署                |

```bash
DASHBOARD_AUTH_MODE=tailscale node lib/server.js
```

## API

| API 端点        | 描述                          |
| ------------ | ----------------------------------- |
| `GET /api/state` | 所有仪表板数据（统一格式）         |
| `GET /api/events` | 提供实时更新的 SSE 数据流           |
| `GET /api/health` | 系统健康检查                 |

## 链接

- [GitHub](https://github.com/jontsai/openclaw-command-center)  
- [ClawHub](https://www.clawhub.ai/jontsai/command-center)  
- [文档](https://github.com/jontsai/openclaw-command-center#readme)