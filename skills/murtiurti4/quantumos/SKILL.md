---
name: quantumos
description: 安装并管理 QuantumOS——这是一个专为 OpenClaw 设计的人工智能命令中心仪表板。用户可以通过该工具来设置 QuantumOS、启动/停止仪表板、进行故障排查或进行更新。QuantumOS 提供实时聊天界面、任务管理功能（基于 AI 的看板式任务管理）以及信息更新功能（涵盖 Reddit、Hacker News、X 社交媒体和新闻来源）。
---
# QuantumOS

这是一个专为 OpenClaw 设计的 AI 命令中心仪表盘，采用 Next.js 构建，通过 WebSocket 与 OpenClaw 门户进行连接。

## 安装

首先运行设置脚本，然后配置代理集成。这两个步骤都是必需的。

### 步骤 1：运行设置脚本

```bash
bash "SKILL_DIR/scripts/setup.sh"
```

该脚本会克隆仓库、安装依赖项、自动检测门户令牌，并创建数据目录。

如果用户尚未安装 Node.js 20 及更高版本，请先安装：https://nodejs.org

### 步骤 2：配置代理集成

设置完成后，您需要将任务分类功能（Mission Control）添加到工作空间的 `HEARTBEAT.md` 文件中。在文件末尾添加以下内容（不要覆盖原有内容）：

```
## Check for new Mission Control tasks
- GET http://localhost:3005/api/mission-control/tasks
- Look for tasks with status "inbox"
- For each inbox task: generate a proper title, set status to "in_progress", and start working on it
- After completing a task: add a comment documenting what was done, set status to "done"
```

这样用户在仪表板上创建任务时，系统就能自动对任务进行分类。

## 启动

```bash
cd ~/Projects/quantumos && npm run dev
```

仪表盘的访问地址为 **http://localhost:3005**

首次打开仪表盘时，用户需要在设置面板中输入他们的 OpenClaw 门户令牌。该令牌可以在 `~/.openclaw/openclaw.json` 文件的 `gateway.token` 配置项中找到。

## 停止运行

通过终端（运行该脚本的终端）执行 `Ctrl+C` 来终止开发服务器进程。

若需让应用程序在后台持续运行：

```bash
cd ~/Projects/quantumos && nohup npm run dev > /tmp/quantumos.log 2>&1 &
```

## 更新

```bash
cd ~/Projects/quantumos && git pull && npm install
```

完成后重新启动开发服务器。

## 故障排除

- **页面为空/无法连接**：检查 OpenClaw 门户是否正在运行（使用 `openclaw gateway status` 命令）。确认仪表板设置中的门户令牌与 `~/.openclaw/openclaw.json` 文件中的令牌一致。
- **端口冲突**：修改 `package.json` 文件中 `scripts.dev` 部分的 `--port` 参数（例如改为 `--port 3005`）。
- **数据源无法加载**：在 `quantumos` 目录下运行 `python3 scripts/fetch-dashboard-feeds.py` 命令。此操作需要 Python 3.8 及更高版本的支持。

## API 密钥

- **X/Twitter 数据源** 需要 xAI API 密钥。请在 [console.x.ai](https://console.x.ai) 获取密钥，并将其添加到 `.env.local` 文件中，或设置为环境变量。如果没有该密钥，X 和 Twitter 的数据源将不会被显示。

## 功能概述

- **聊天**：与 OpenClaw 门户进行实时 WebSocket 聊天，支持响应流、思维过程展示以及工具调用功能。
- **任务管理**：提供看板界面，支持任务创建、代理分配、评论添加和状态跟踪。
- **仪表盘**：汇总来自 Reddit、Hacker News、X 和其他新闻源的数据，并提供数据归档功能。
- **代理设置**：用户可以直接通过用户界面配置代理、模型和工具的相关参数。