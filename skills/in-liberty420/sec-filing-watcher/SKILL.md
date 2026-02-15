---
name: sec-filing-watcher
description: 监控 SEC 的 EDGAR 系统以获取新的文件提交信息，并通过 Clawdbot 接收 Telegram 或 Slack 的通知摘要。该功能适用于设置 SEC 文件提交提醒、添加/删除需要监控的证券代码、配置文件类型、启动/停止监控任务，以及排查文件提交通知相关的问题。
---

# SEC 文件提交监控器

该工具会监控 SEC 的 EDGAR 系统，以检测监视列表中的股票代码是否有新的文件提交。一旦发现新文件提交，它会通知 Clawdbot，后者会下载这些文件、对其进行汇总，并通过 Telegram 将结果发送给用户。

## 快速设置

### 1. 创建监视列表

```bash
cp assets/watchlist.example.json watchlist.json
# Edit watchlist.json with your tickers
```

### 2. 配置 Webhook

编辑 `scripts/watcher.js` 文件中的 `CONFIG` 部分：
- `webhookUrl`：Clawdbot 的 webhook 地址（默认：`http://localhost:18789/hooks/agent`）
- `webhookToken`：你的 webhook 令牌（在 `clawdbot.json` 文件的 `hooks.token` 部分可以找到）

### 3. 测试运行

**第一次运行**：会加载现有的文件提交记录（不会发送通知）。**第二次运行**：会检查是否有新的文件提交。

### 4. 定时执行（每 15 分钟一次）

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

你可以在 `watchlist.json` 文件中添加或删除股票代码：

```json
{
  "tickers": ["AAPL", "MSFT", "TSLA"],
  "formTypes": ["10-K", "10-Q", "8-K", "4"]
}
```

新添加的股票代码会自动被加载到系统中（现有的文件提交记录不会重复发送通知）。

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

| 文件 | 用途 |
|------|---------|
| `scripts/watcher.js` | 主监控脚本 |
| `watchlist.json` | 要监控的股票代码列表及文件提交类型 |
| `state.json` | 记录已处理的文件提交信息（自动生成） |
| `watcher.log` | 日志输出文件（如果已启用） |

## 故障排除

**没有收到通知：**
- 确保 `state.json` 文件存在（第一次运行时会加载文件提交记录，第二次运行时才会发送通知）
- 检查 `watcher.js` 文件中配置的 webhook 地址和令牌是否正确
- 确认 Clawdbot 是否正在运行：`clawdbot status`

**SEC 系统阻止请求：**
- 脚本使用了正确的 User-Agent 头信息
- 如果被阻止，请等待 10 分钟（SEC 系统的请求限制机制）

**收到重复通知：**
- 确保 `state.json` 文件没有损坏
- 删除 `state.json` 文件后重新运行脚本（系统会重新加载所有文件提交记录）