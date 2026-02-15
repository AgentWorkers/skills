---
name: quantumos
description: 安装并管理 QuantumOS——这是一个专为 OpenClaw 设计的人工智能命令中心仪表板。用户可以通过该工具来设置 QuantumOS、启动/停止仪表板、进行故障排查或更新系统。QuantumOS 提供实时聊天界面、任务管理功能（基于 AI 的看板式任务管理），以及新闻信息展示（涵盖 Reddit、Hacker News、X 等平台）。
---
# QuantumOS

这是一个专为 OpenClaw 设计的 AI 命令中心仪表板，采用 Next.js 构建，通过 WebSocket 与 OpenClaw 服务器进行连接。

## 安装

运行设置脚本。该脚本会完成所有必要的操作：克隆代码仓库、安装依赖项、配置环境变量以及创建数据目录。

```bash
bash "SKILL_DIR/scripts/setup.sh"
```

脚本将执行以下步骤：
1. 将代码仓库克隆到 `~/Projects/quantumos` 目录（或使用已存在的目录）。
2. 安装 Node.js 及其相关依赖项。
3. 自动从 OpenClaw 的配置文件中提取网关令牌，并将其保存到 `.env.local` 文件中。
4. 创建数据目录（`~/.openclaw/mission-control/` 和 `~/.openclaw/dashboard-data/`）。
5. 显示可访问的仪表板 URL。

如果用户尚未安装 Node.js 20 及更高版本，请先安装它：https://nodejs.org

## 启动

仪表板的访问地址为 **http://localhost:3005**。

首次打开仪表板时，用户需要在设置面板中输入他们的 OpenClaw 网关令牌。该令牌可以在 `~/.openclaw/openclaw.json` 文件的 `gateway.token` 配置项中找到。

## 停止

通过终端（运行该脚本的窗口）执行 `Ctrl+C` 来终止开发服务器进程。

若需要让仪表板在后台持续运行，可以采取相应的措施（具体方法请参考后续说明）。

## 更新

```bash
cd ~/Projects/quantumos && git pull && npm install
```

更新完成后，重新启动开发服务器。

## 故障排除

- **页面为空/无法连接**：请确认 OpenClaw 服务器正在运行（使用 `openclaw gateway status` 命令检查）。同时，请验证仪表板设置中的网关令牌是否与 `~/.openclaw/openclaw.json` 文件中的内容一致。
- **端口冲突**：请修改 `package.json` 文件中的 `scripts.dev` 配置项（将 `--port` 参数设置为其他可用端口，例如 `--port 3005`）。
- **数据源无法加载**：在 `quantumos` 目录下运行 `python3 scripts/fetch-dashboard-feeds.py` 命令。该命令需要 Python 3.8 及更高版本的支持。

## 功能概述

- **聊天**：支持与 OpenClaw 服务器的实时 WebSocket 聊天功能，可查看响应内容、思考过程以及工具调用信息。
- **任务管理**：提供看板式界面，支持任务创建、代理分配、添加评论以及跟踪任务状态。
- **仪表板**：汇总来自 Reddit、Hacker News、X 等平台的新闻内容，并支持数据归档。
- **代理配置**：用户可以直接通过用户界面配置代理、模型及使用的工具。