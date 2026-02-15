---
name: mission-control
description: 专为 macOS 设计的 Web 仪表板，用于监控和控制您的 OpenClaw 代理。支持实时聊天、Cron 任务管理、任务调度、资源调度（Scout Engine）、成本跟踪等功能。
homepage: https://github.com/Jzineldin/mission-control
metadata: { "openclaw": { "emoji": "🖥️", "requires": { "bins": ["node", "npm"] } } }
---

# Mission Control — OpenClaw 的仪表盘

这是一个专为 OpenClaw 代理设计的、外观简洁且具有 macOS 原生风格的 Web 仪表盘。您可以通过这个仪表盘监控会话、管理定时任务（cron jobs）、实时聊天、将任务分配给子代理、发现新的机会以及跟踪成本——所有这些功能都集中在一个美观的界面中。

## 快速安装

```bash
# Clone the repo into your workspace
cd "$CLAWD_WORKSPACE" 2>/dev/null || cd ~/clawd
git clone https://github.com/Jzineldin/mission-control.git
cd mission-control

# Install dependencies + build frontend
npm install
cd frontend && npm install && npm run build && cd ..

# Create your config
cp mc-config.default.json mc-config.json

# Start (dev)
node server.js

# Or use systemd for production:
sudo cp mission-control.service /etc/systemd/system/
# Edit paths in the service file, then:
sudo systemctl enable --now mission-control
```

访问 `http://localhost:3333`，设置向导会自动检测您的 OpenClaw 配置。

## 功能介绍

| 页面 | 功能描述 |
|------|-------------|
| **仪表盘** | 代理状态、快速操作（发送邮件/日历通知/心跳检测）、活动动态、频道信息 |
| **聊天记录** | 浏览所有会话记录、查看聊天历史、继续对话 |
| **工作台** | Kanban 任务板：安排任务、让子代理进行研究、您可审阅报告 |
| **成本追踪** | 每个模型的代币使用情况、每日图表、预算警报 |
| **定时任务管理** | 可视化地切换、运行或删除定时任务 |
| **机会发现** | 自动发现新的机会：工作项目、技能需求、资助信息、悬赏任务、新闻动态 |
| **代理中心** | 显示所有代理/会话的代币数量及管理信息 |
| **设置** | 模型路由设置（主代理/子代理/心跳检测机制）、配置文件导出/导入 |
| **技能管理** | 浏览已安装的技能及可用技能 |
| **AWS** | （可选）实际使用成本信息、Bedrock 模型、图像生成功能 |

## 系统要求

- OpenClaw 已启用网关（gateway）功能
- Node.js 18 及更高版本
- Brave Search API 密钥（用于 “机会发现” 功能——[免费 tier](https://brave.com/search/api/)

## 配置信息

系统会自动从您的 OpenClaw 配置中读取以下信息：
- 来自 `~/.openclaw/openclaw.json` 的网关令牌（gateway token）
- 来自 `IDENTITY.md` 的代理名称（agent name）
- 来自 OpenClaw 配置文件的模型信息（model）和频道设置（channels）

您可以通过 `mc-config.json` 文件或应用程序内的设置页面进行进一步微调。

## 链接

- **GitHub:** https://github.com/Jzineldin/mission-control
- **支持:** https://ko-fi.com/kevinelzarka
- **许可证:** BSL 1.1（可转换为 MIT 2030 许可证）