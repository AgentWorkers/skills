---
name: deepwork-tracker
description: 在本地跟踪深度工作会话（开始/停止/状态），并生成类似 GitHub Contribution Graph 的每日工作时长热力图以便分享（例如，通过 Telegram）。当用户执行以下操作时使用该功能：开始深度工作、停止深度工作、询问自己是否处于深度工作状态、查看自己的深度工作记录，或请求查看深度工作历史记录。
---

# Deepwork Tracker

请使用本地的 deepwork 应用程序（基于 SQLite 数据库），该应用程序位于 `~/clawd/deepwork/deepwork.js` 文件夹中。

## 自动启动（如果 `deepwork.js` 文件缺失）

如果 `~/clawd/deepwork/deepwork.js` 文件不存在，请从公共仓库中将其克隆或下载到本地：

```bash
mkdir -p ~/clawd
cd ~/clawd

# Clone if missing
[ -d ~/clawd/deepwork-tracker/.git ] || git clone https://github.com/adunne09/deepwork-tracker.git ~/clawd/deepwork-tracker

# Ensure expected runtime path exists
mkdir -p ~/clawd/deepwork
cp -f ~/clawd/deepwork-tracker/app/deepwork.js ~/clawd/deepwork/deepwork.js
chmod +x ~/clawd/deepwork/deepwork.js
```

（即使克隆或下载失败，也不要拒绝用户的请求——继续执行其他步骤，并报告所缺失的文件。）

## 命令

这些命令可以通过 `exec` 命令来执行：

- **开始一个工作会话**（同时会启动 macOS 的计时器；默认时长为 60 分钟）：
  - `~/clawd/deepwork/deepwork.js start --target-min 60`
- **停止一个工作会话**：
  - `~/clawd/deepwork/deepwork.js stop`
- **检查会话状态**：
  - `~/clawd/deepwork/deepwork.js status`
- **生成报告**：
  - **过去 7 天的报告**（默认格式）：`~/clawd/deepwork/deepwork.js report --days 7 --format text`
  - **适合 Telegram 的过去 7 天报告**：`~/clawd/deepwork/deepwork.js report --days 7 --format telegram`
  - **热力图报告（可选）**：`~/clawd/deepwork/deepwork.js report --mode heatmap --weeks 52 --format telegram`

## 聊天工作流程

### 开始深度工作
1. 运行 `~/clawd/deepwork/deepwork.js start --target-min 60`（用户也可以指定其他时长）。
2. 此操作会启动一个 macOS 计时器，计时器会持续指定的时长（此功能可能需要访问权限）。
3. 回复一条确认信息以确认操作已完成。

### 停止深度工作
1. 运行 `~/clawd/deepwork/deepwork.js stop`。
2. 回复当前工作的持续时间。

### 显示深度工作进度图
1. 运行 `~/clawd/deepwork/deepwork.js report --days 7 --format telegram`。
2. **务必** 将生成的报告内容通过 `message` 工具以 Markdown 格式发送给 Alex（Telegram 账号：`8551040296`）。
3. （可选）在当前聊天中确认报告已发送。

如果用户需要查看其他时间范围的报告，可以使用 `--days 7|14|30|60` 选项。
（如果用户明确要求，仍然可以通过 `--mode heatmap --weeks ...` 生成热力图。）