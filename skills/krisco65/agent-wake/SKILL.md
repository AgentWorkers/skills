---
name: agent-wake
version: 1.0.1
description: 通过外部脚本或进程唤醒 OpenClaw 代理会话。当后台任务（如 Claude Code CLI、cron 作业、Webhook、价格警报或任何脚本）完成时，使用此方法可以确保代理自动收到通知，并在正确的 Discord 频道中作出响应，而无需人工干预。这解决了代理无法知晓异步任务何时完成的问题。
credentials:
  - name: GATEWAY_TOKEN
    description: OpenClaw gateway auth token. Read from GATEWAY_TOKEN env var, a local .env file next to the script, or auto-detected from ~/.openclaw/gateway.cmd.
    required: true
---
# agent-wake

使用网关HTTP API从任何外部进程唤醒您的OpenClaw代理。

## 工作原理

`scripts/agent-wake.py`通过`cron`工具调用`POST /tools/invoke`接口，向代理的会话中触发一个“wake”事件。代理会以系统消息的形式接收该事件文本，并立即在正确的频道中作出响应。

## 快速入门

```bash
python agent-wake.py "Task finished -- brief summary" "YOUR_DISCORD_CHANNEL_ID"
```

## 设置（一次性操作）

请参阅`references/setup.md`以了解以下内容：
- 通过HTTP启用`cron`工具（必需——默认情况下是被禁用的）
- 设置`GATEWAY_TOKEN`
- 查找您的Discord频道ID

## 使用方式

### Claude Code CLI任务结束时
在任务提示中添加以下代码：
```
When done, run: python "/path/to/agent-wake.py" "Task done -- summary here" "CHANNEL_ID"
```

### 从任何Python脚本中调用
```python
import subprocess
subprocess.run([
    "python", "/path/to/agent-wake.py",
    "Price alert triggered -- AAPL crossed $200",
    "1475232925724315740"
])
```

### 独立运行（唤醒主会话）
```bash
python agent-wake.py "Backup completed successfully"
```
省略频道ID即可唤醒主会话（响应将发送到默认频道）。

## 代理的接收方式

事件文本会以系统消息的形式传递给代理。请确保信息具体明确——代理会根据您提供的内容执行相应的操作：

```
Build finished -- 3 errors fixed, tests passing. Send your response to Discord channel 1475232925724315740...
```

## 脚本位置

`scripts/agent-wake.py`——请将此脚本复制到运行任务的任何位置。该脚本仅依赖于Python标准库。