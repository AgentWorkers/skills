---
name: command-center
version: 1.1.0
description: OpenClaw的任务控制面板：提供实时会话监控、大型语言模型（LLM）使用情况跟踪、成本分析以及系统运行状态信息。您可以在此处集中查看所有的AI代理。
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

这是您的人工智能团队的任务控制中心。

## 快速入门

```bash
npx clawhub@latest install command-center
cd skills/command-center
node lib/server.js
```

仪表板运行地址：**http://localhost:3333**

## 主要功能

- **会话监控** — 实时查看所有 AI 会话，并提供实时更新
- **大语言模型使用情况统计** — 监控 Claude、Codex 等模型的使用情况
- **系统状态** — 显示 CPU、内存、磁盘和温度等系统指标
- **定时任务** — 查看和管理已安排的任务
- **对话内容整理** — 自动整理对话内容
- **成本跟踪** — 计算每次会话的成本、预测成本及节省金额
- **隐私设置** — 可隐藏演示中的敏感内容

## 配置

仪表板会自动检测您的 OpenClaw 工作空间。如需自定义工作空间路径，请设置 `OPENCLAW_WORKSPACE` 环境变量。

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

| API 端点            | 功能描述                          |
| ----------------------------- | -------------------------------------- |
| `GET /api/state`     | 获取所有仪表板数据（统一格式）            |
| `GET /api/events`     | 提供实时更新的 SSE 数据流                |
| `GET /api/health`     | 系统健康检查                    |

## 链接

- [GitHub](https://github.com/jontsai/openclaw-command-center)  
- [ClawHub](https://www.clawhub.ai/jontsai/command-center)  
- [文档](https://github.com/jontsai/openclaw-command-center#readme)