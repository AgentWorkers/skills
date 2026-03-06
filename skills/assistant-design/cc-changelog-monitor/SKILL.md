---
name: cc-changelog-monitor
description: 监控 Claude 的代码发布情况，并在新版本发布时接收 Telegram 警报。完全不需要使用任何 AI 工具，仅使用纯 Bash 脚本进行监控。
---
# cc-changelog-monitor

该脚本用于监控 `@anthropic-ai/claude-code` 在 npm 上的版本更新，并在检测到新版本时通过 Telegram 发送警报，同时提供版本间的变更摘要。

**监控过程中不使用任何 AI 服务**——完全依赖 bash、curl 和 jq 工具实现。

## 快速入门

### 1. 设置（一次性操作）

```bash
bash ~/clawd/skills/cc-changelog-monitor/scripts/setup.sh
```

此操作将：
- 从 OpenClaw 配置文件中自动获取您的 Telegram 机器人令牌
- 请求您的 Telegram 聊天 ID（默认为您的个人 ID）
- 根据当前的 Claude Code 版本初始化版本跟踪系统
- 使相关脚本可执行

### 2. 手动运行

```bash
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh
```

**未检测到新版本时的输出：**
```
✓ Claude Code is at v2.1.69 — no change.
```

**检测到新版本时的输出：**
```
🔔 New version detected: v2.1.69 → v2.1.70
📦 Downloading @anthropic-ai/claude-code@2.1.70...
✅ Telegram alert sent!
✅ Saved v2.1.70 as current version.
```

### 3. 将脚本添加到 OpenClaw 的 Cron 任务中**

请参考 `cron-payload.md` 文件，了解如何设置每 2 小时自动执行一次监控任务的详细信息。

## 工作原理

1. **查询 npm 注册表**：`curl https://registry.npmjs.org/@anthropic-ai/claude-code/latest`
2. **与 `~/.cc-changelog-version`（存储的当前版本信息）进行比较**
3. **如果发现新版本**：下载新版本的 tarball 文件，解压后与之前的版本进行差异对比
4. **通过 Telegram 发送包含版本信息和差异摘要的警报**
5. **将新版本信息保存到磁盘**

## 配置信息

配置文件存储在 `~/.cc-changelog-config` 中：

```bash
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_CHAT_ID="your-chat-id"
```

## 脚本生成的文件

- `~/.cc-changelog-version`：记录最后一次看到的版本信息
- `~/.cc-changelog-config`：存储 Telegram 机器人所需的凭据
- `~/clawd/projects/cc-changelog/{version}/`：存放用于差异对比的 npm 包文件

## 强制触发警报测试

```bash
# Reset version to trigger an alert
echo "0.0.0" > ~/.cc-changelog-version
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh
```

## 从 OpenClaw 聊天界面调用该脚本

您可以通过 OpenClaw 聊天界面请求运行该监控脚本：

> “检查是否有新的 Claude Code 版本”

OpenClaw 会自动执行 `monitor.sh` 脚本并返回结果。