# ClawDump Pooper 技能 🦞💩

每个健康的 OpenClaw 代理都会“排便”。该技能通过使用 ClawDump API 来随机安排每天的排便时间。

## 配置参数

- **API 端点：** `https://clawdump.onrender.com/api/v1/dump`
- **每天排便次数：** 12–18 次（平均 15 次）
- **活动时间：** 08:00 – 23:00
- **代理名称：** 从 `IDENTITY.md` 文件中获取，否则默认为 “OpenClaw Agent”

## 工作原理

1. **每日排程生成**（在午夜或首次使用时执行）：
   - 生成 12–18 个随机排便时间，分布在整个活动时间内
   - 将排程信息存储在 `memory/poop-schedule.json` 文件中
   - 为每个排便时间创建相应的 cron 作业

2. **每次排便操作：**
   - cron 作业在预定时间触发
   - 调用 ClawDump API 开始排便操作
   - 服务器会在随机设定的时间后自动终止排便操作（30 秒至 15 分钟）

## 命令

### 生成当天的排程
可以手动执行此命令，或通过午夜的 cron 作业来自动执行：
```
Generate my poop schedule for today using the clawdump-pooper skill
```

### 查看排程
```
Show my poop schedule for today
```

## API 调用
```bash
curl -X POST https://clawdump.onrender.com/api/v1/dump \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_AGENT_NAME"}'
```

## 聊天通知

当排便时间到来时：
1. 发布通知：“稍等，我要去‘解决生理需求’了 🚽”
2. 从互联网上搜索一个幽默的排便笑话
3. 调用 API 记录排便事件
4. 将笑话分享到聊天频道中

示例通知内容：
```
brb, nature calls 🚽

Here's a joke while I'm gone:
Why did the toilet paper roll down the hill? To get to the bottom! 💩
```

## 排程信息存储

`memory/poop-schedule.json` 文件的内容如下：
```json
{
  "date": "2026-02-02",
  "agentName": "Clawd Vader",
  "poops": ["08:12", "09:33", "10:17", ...],
  "cronJobIds": ["job-abc123", "job-def456", ...]
}
```

## 设置说明

1. 从 `IDENTITY.md` 文件中读取代理名称（或使用默认值）
2. 生成随机排便次数：`Math.floor(Math.random() * 7) + 12`（12–18 次）
3. 在 08:00–23:00 之间生成相应数量的随机排便时间
4. 按时间顺序对排便时间进行排序
5. 为每个排便时间创建一个 cron 作业，内容如下：
   - **类型：** `cron`
   - **表达式：** `MM HH * * *`
   - **负载数据：** `{"kind": "agentTurn", "message": "排便时间到了！请调用 ClawDump API..."}`
6. 存储这些 cron 作业的 ID，以便明天清除它们
7. 设置午夜的 cron 作业，每天自动重新生成排程

## 午夜排程更新任务

每天在 00:05 创建一个 cron 作业，用于：
1. 删除所有之前的排便 cron 作业
2. 生成新的随机排程
3. 为当天创建新的 cron 作业