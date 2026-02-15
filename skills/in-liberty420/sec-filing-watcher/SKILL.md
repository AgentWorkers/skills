---
name: sec-filing-watcher
description: 监控 SEC EDGAR 系统中的新文件提交情况，并通过 Clawdbot 接收 Telegram 或 Slack 的通知摘要。该功能适用于设置 SEC 文件提交提醒、添加/删除需要监控的股票代码、配置文件类型、启动/停止文件提交监控，以及解决相关通知问题时使用。
---
# SEC 文件提交监控器

该工具会监控 SEC 的 EDGAR 系统，以检测监视列表中的股票代码是否有新的文件提交。一旦发现新文件提交，它会通知 Clawdbot，后者会下载这些文件、对其进行汇总，并通过 Telegram 将结果发送给指定的接收者。

## 快速设置

### 1. 创建监视列表

```bash
cp assets/watchlist.example.json watchlist.json
# Edit watchlist.json with your tickers
```

### 2. 配置环境变量

请设置以下环境变量（例如，在您的 shell 配置文件或 OpenClaw 技能配置中）：

| 变量 | 是否必需 | 说明 |
|---------|---------|-------------------|
| `OPENCLAWHOOKS_TOKEN` | 是 | 用于 OpenClaw 的挂钩令牌 |
| `SECWATCHER_RECIPIENT` | 是 | 接收通知的聊天频道/用户 ID |
| `SECWATCHER_CHANNEL` | 可选 | 用于发送通知的渠道插件（默认：Telegram） |
| `SECWATCHER_USER_AGENT` | 可选 | SEC API 的用户代理字符串（SEC 要求提供此信息） |

### 3. 测试运行

**首次运行**：会下载现有的文件提交数据（不会发送通知）。**第二次运行**：会检查是否有新的文件提交。

### 4. 定时运行（每 15 分钟一次）

**macOS:**
```bash
cp assets/com.sec-watcher.plist ~/Library/LaunchAgents/
# Edit the plist to set correct paths
launchctl load ~/Library/LaunchAgents/com.sec-watcher.plist
```

**Linux:**
```bash
crontab -e
# Add: */15 * * * * /usr/bin/node /path/to/scripts/watcher.js >> /path/to/watcher.log 2>&1
```

## 管理股票代码

您可以在 `watchlist.json` 文件中添加或删除股票代码：

```json
{
  "tickers": ["AAPL", "MSFT", "TSLA"],
  "formTypes": ["10-K", "10-Q", "8-K", "4"]
}
```

新添加的股票代码会自动被纳入监控列表；现有的文件提交数据不会重复发送通知。

有关常见的 SEC 文件提交类型，请参阅 `references/form-types.md`。

## 命令

**检查状态：**
```bash
launchctl list | grep sec-watcher
```

**查看日志：**
```bash
cat ~/clawd/sec-filing-watcher/watcher.log
```

**停止运行：**
```bash
launchctl unload ~/Library/LaunchAgents/com.sec-watcher.plist
```

**启动运行：**
```bash
launchctl load ~/Library/LaunchAgents/com.sec-watcher.plist
```

**手动运行：**
```bash
node scripts/watcher.js
```

## 文件说明

| 文件名 | 用途 |
|--------|---------|
| `scripts/watcher.js` | 主监控脚本 |
| `watchlist.json` | 监视列表中的股票代码及文件提交类型 |
| `state.json` | 记录已处理的文件提交信息（自动生成） |
| `watcher.log` | 日志输出文件（如果已启用） |

## 故障排除

**未收到通知：**
- 确保 `state.json` 文件存在（首次运行时会下载数据，第二次运行时会发送通知）。
- 检查 `watcher.js` 中的 Webhook URL 和令牌是否正确配置。
- 确保 Clawdbot 正在运行：使用 `clawdbot status` 命令查看其状态。

**SEC 系统阻止请求：**
- 脚本使用了正确的用户代理（User-Agent）头信息。
- 如果被阻止，请等待 10 分钟（SEC 系统有请求频率限制）。

**收到重复通知：**
- 确保 `state.json` 文件没有损坏。
- 删除 `state.json` 文件后重新运行脚本（这将重新下载所有现有的文件提交数据）。