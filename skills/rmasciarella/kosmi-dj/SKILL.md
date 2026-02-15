---
name: kosmi-dj
description: 当用户请求在 Kosmi 中“播放视频”、“将视频加入队列”、“在 Kosmi 中担任 DJ”、“开始视频播放”、“在 Kosmi 中循环播放视频”、“连接到 Kosmi 房间”、“在 Kosmi 中播放 YouTube 视频”、“停止视频循环播放”、“将视频添加到队列中”、“成为我的视频 DJ”，或者需要关于通过代理浏览器自动化来控制 Kosmi 观看派对房间的指导时，应使用此技能。
---

# Kosmi 视频 DJ — 代理-浏览器自动化技能

该技能可将代理程序转换为 Kosmi 观看派对房间的视频 DJ。它利用 `agent-browser`（通过 accessibility-tree 快照实现 Chromium 自动化）来导航到 Kosmi 房间，按 URL 队列播放视频，并实现自动循环播放功能。

## 先决条件

- 已安装 `agent-browser` CLI 并将其添加到 PATH 中（`npm install -g agent-browser` 或确保其在环境中可用）
- 在 `${CLAUDE_PLUGIN_ROOT}/.env` 文件中配置房间 URL 和凭据
- 通过 `AGENT-browser_SESSION_NAME` 环境变量支持会话持久化（在多次运行之间保留 cookie/localStorage）

## 环境变量

在调用 `agent-browser` 之前，从 `${CLAUDE_PLUGIN_ROOT}/.env` 文件中加载以下环境变量：

| 变量 | 是否必需 | 说明 |
|---|---|---|
| `KOSMI_ROOM_URL` | 是 | Kosmi 房间的完整 URL（例如：`https://app.kosmi.io/room/XXXXX`） |
| `KOSMI_EMAIL` | 否 | 登录邮箱（如果使用会话持久化则可省略） |
| `KOSMI_PASSWORD` | 否 | 登录密码（如果使用会话持久化则可省略） |
| `KOSMI_BOT_NAME` | 否 | 房间中的显示名称（默认：`clawdbot`） |
| `AGENT_BROWSER_SESSION_NAME` | 是 | 会话持久化键（默认：`kosmi-dj-session`） |
| `AGENT_BROWSER_ENCRYPTION_KEY` | 否 | 用于加密存储会话数据的十六进制密钥 |

## 核心工作流程

### 1. 连接到房间

执行 `${CLAUDE_PLUGIN_ROOT}/skills/kosmi-dj/scripts/kosmi-connect.sh`，完成以下操作：
- 在 `agent-browser` 中打开 Kosmi 房间 URL
- 等待页面加载完成（约 800 毫秒）
- 生成一个 accessibility 快照以检测当前的 UI 状态
- 如果出现昵称/名称提示框 → 输入 `KOSMI_BOT_NAME` 并点击“加入”
- 如果出现登录提示框且凭据存在 → 输入邮箱/密码并提交
- 通过确认房间 UI 元素的存在来验证连接是否成功

### 2. 按 URL 播放视频

执行 `${CLAUDE_PLUGIN_ROOT}/skills/kosmi-dj/scripts/kosmi-play.sh <VIDEO_URL>`，完成以下操作：
- 确保已成功连接（该命令可重复执行）
- 在 Kosmi 中打开“应用/媒体”模态框
- 选择“URL/链接”输入模式
- 在 URL 输入框中输入提供的视频 URL
- 点击“播放”按钮（或按 Enter 键）
- 通过检查播放器 UI 元素来确认视频是否开始播放

### 3. 自动循环播放模式

执行 `${CLAUDE_PLUGIN_ROOT}/skills/kosmi-dj/scripts/kosmi-loop.sh`，执行以下操作：
- 连接到房间
- 进入一个循环：获取视频 URL（从提供的列表中获取，或由代理程序自动查找）
- 播放视频
- 定期检查房间状态以检测视频是否结束（生成播放器状态的快照）
- 视频结束后，播放下一个视频
- 该循环会一直持续，直到被中断或收到停止信号

循环脚本会在 `/tmp/kosmi-dj-loop.pid` 文件中记录循环的进程 ID（PID），以便后续执行停止或状态查询操作。

## `agent-browser` CLI 参考（简要说明）

所有浏览器自动化操作都通过 `agent-browser` CLI 完成。主要命令如下：

| 命令 | 用法 | 功能 |
|---|---|---|
| `open <url>` | `agent-browser open "$URL"` | 导航到指定 URL |
| `snapshot` | `agent-browser snapshot -i -C --json` | 以 JSON 格式获取交互式元素 |
| `click <ref>` | `agent-browser click @ref123` | 根据 ref ID 点击元素 |
| `fill <ref> <text>` | `agent-browser fill @ref123 "text"` | 向文本框中输入内容 |
| `press <key>` | `agent-browser press Enter` | 按下指定的键盘键 |
| `wait <ms>` | `agent-browser wait 1000` | 等待指定时间（毫秒） |

快照的输出为 JSON 格式，其中 `data.refs` 是一个映射，键值为 `refId`，值为 `{ role, name }`。可以使用 `role` 和 `name` 来匹配 UI 元素。建议始终使用 `-i`（仅获取交互式元素）和 `-C`（包含光标的交互式元素）标志，以获得更清晰的快照结果。

详细命令参考请参见 `references/agent-browser-commands.md`。

## 基于快照的元素检测

Kosmi 的 UI 是动态变化的。正确的操作步骤如下：
1. 生成快照：`agent-browser snapshot -i -C --json`
2. 从 `data.refs` 中解析元素引用
3. 根据 `role`（按钮、文本框、链接）和 `name`（不区分大小写的子字符串匹配）来查找目标元素
4. 使用带有前缀 `@` 的 ref ID 来执行点击或输入操作

有关 Kosmi 特定的 UI 元素映射（按钮名称、模态框流程）信息，请参阅 `references/kosmi-ui-map.md`。

## 调试/检查

运行 `${CLAUDE_PLUGIN_ROOT}/skills/kosmi-dj/scripts/kosmi-snapshot-debug.sh`，以生成当前可见的所有交互式元素的可视化快照。这有助于确定 Kosmi 房间中的按钮名称和文本框标签。

## 错误处理

- 如果未安装 `agent-browser`，请安装它：`npm install -g agent-browser`
- 如果快照中没有返回任何元素引用，可能是因为页面仍在加载中——请添加 `wait 1500` 并重试
- 如果打开模态框后找不到 URL 输入框，可能是 Kosmi 更新了其 UI——请运行调试快照脚本并更新 `references/kosmi-ui-map.md`
- 如果登录失败，请检查 `.env` 文件中的凭据，或删除会话以强制重新登录：`agent-browser session delete kosmi-dj-session`

## 令牌使用效率

为了降低长时间循环播放时的令牌消耗：
- 使用 cron 风格的调度任务（如 `crontab` 或 `watch`）代替代理程序的轮询
- 循环脚本在每次检查之间会进行休眠（可配置间隔，默认为 30 秒）
- 代理程序仅在以下情况下唤醒：检查视频是否结束 → 添加下一个视频到队列 → 继续休眠
- 对于完全自动化的操作，可以使用 `/dj-start` 命令将循环作为后台进程启动

## 额外资源

### 参考文件

- **`references/agent-browser-commands.md`** — 完整的 `agent-browser` CLI 参考及示例
- **`references/kosmi-ui-map.md`** — Kosmi 房间 UI 元素名称、模态框流程和快照模式

### 脚本

- **`scripts/kosmi-connect.sh`** — 连接到 Kosmi 房间
- **`scripts/kosmi-play.sh`** — 按 URL 播放单个视频
- **`scripts/kosmi-loop.sh`** — 自动循环播放模式（后台进程）
- **`scripts/kosmi-snapshot-debug.sh`** — 生成交互式元素的调试快照