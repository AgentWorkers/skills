---
name: vizclaw
description: **将 OpenClaw 风格的运行任务连接到 VizClaw 实时房间**：这可以通过一个可在 ClawHub 上安装的技能来实现。当您需要快速创建房间、使用 JSONL/Websocket 进行数据传输、触发事件以及查看代理事件流，或者以安全的方式查看可视化数据时，这个技能非常实用。
---

# VizClaw 技能

使用此技能可以创建一个 VizClaw 房间，并以 OpenClaw 的风格流式传输事件。

## 快速命令

从 ClawHub 安装：

```bash
npx clawhub@latest install vizclaw
```

之后正常运行您的代理程序，VizClaw 事件将自动开始流式传输。

直接从 vizclaw.com 运行脚本：

```bash
uv run https://vizclaw.com/skills/vizclaw/scripts/connect.py
```

```bash
openclaw run ... --json | uv run https://vizclaw.com/skills/vizclaw/scripts/connect.py --openclaw-jsonl --mode detailed
```

高级配置（技能、模型、提醒、心跳检测）：

```bash
uv run https://vizclaw.com/skills/vizclaw/scripts/connect.py \
  --skills "ez-google,ez-unifi,claude-code" \
  --available-models "sonnet,haiku,gpt-4o" \
  --heartbeat-interval 30 \
  --reminders-json '[{"title":"Check email","schedule":"every 30min"}]'
```

## 安全性

- 在 `overview`/`hidden` 模式下，查询/工具/报告中的文本会被屏蔽。
- 请勿传输任何您无权分享的秘密信息或敏感数据。