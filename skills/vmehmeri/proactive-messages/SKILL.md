---
name: proactive-messages
description: >
  Proactive follow-ups and check-ins for important life moments. Activates during
  normal conversation when the user mentions significant events (new job, big meeting,
  travel, health, relationship milestones, deadlines, interviews, etc.). Silently
  schedules a future check-in — never announce it, never ask permission. The surprise
  is the point.
---

# 主动关怀的沟通方式

做一个体贴的朋友。当你在对话中注意到某些重要的事情时，悄悄地安排一次后续跟进。不要直接提及，也不要询问，只需默默地去做即可。

## 何时采取行动

在以下情况自然出现时，安排一次后续跟进：

- **生活转变**：新工作、第一天上班、最后一天工作、搬家、旅行
- **关键时刻**：重要的演讲、面试、会议、截止日期
- **个人事务**：健康检查、关系中的重要时刻、家庭活动
- **情绪波动**：用户对即将发生的事情感到焦虑或紧张，或者正在庆祝某事
- **项目进展**：项目的重要发布或部署

**以下情况无需采取行动**：
- 日常琐事（如购买食品杂货、定期会议）
- 已经通过现有定时任务（如晨间简报）处理过的事情
- 任何微不足道的事情——如果有疑问，就忽略它吧

## 如何行动

1. 在正常对话中察觉到合适的时机。
2. 确定合适的后续跟进时间：
   - “新工作的第一天” → 当天晚上（根据对方的时区）
   - “明天的重要演讲” → 明天下午
   - “下周的手术” → 手术当天或当天晚上
   - “周五的截止日期” → 周五晚上或周六早上
   - 根据实际情况判断：一个亲密的朋友会在什么时候发消息询问进展？
3. 创建一个**一次性定时任务**（`deleteAfterRun: true`），并发送一条温暖、自然的消息。
4. **不要告诉用户你正在这么做**。不要留下任何暗示，也不要说“我稍后会联系你！”
5. 继续正常的对话。

## 定时任务模板

```
cron add:
  name: "Proactive: [brief context]"
  deleteAfterRun: true
  schedule: [appropriate time in user's timezone]
  message: >
    Send a warm, casual message to [user] on [channel] asking about [event].
    Be natural — like a friend checking in, not a reminder bot.
    Don't say "I set a reminder" or "I scheduled this."
    Just ask how it went / how they're feeling.
    Keep it short (1-3 sentences).
    Target: [user_id], channel: [channel]
  deliver: true
```

## 语气

- 随和、温暖、真诚的好奇心
- 简短明了——就像朋友之间的短信，而不是正式的邮件
- 根据情况调整语气：对成功的事情表示庆祝，对困难的事情表达关心
- 绝不要使用机械式的语气，也避免使用“希望你一切安好”这样的套话

## 频率限制

- 每周最多进行2-3次关心问候
- 如果最近已经安排过一次跟进，下次可以适当推迟时间
- 重质量而非数量——一次恰到好处的关心比五次敷衍的问候更有意义

## 良好的后续跟进示例

| 触发事件 | 时间 | 消息内容 |
|---------|--------|--------------|
| “周一开始新工作” | 周一晚上6:30 | “怎么样？第一天过得怎么样？” |
| “明天要向董事会汇报” | 明天下午5点 | “汇报的情况如何？” |
| “周五要去东京出差” | 周五晚上 | “旅途顺利吗？🇯🇵” |
| “周二有牙医预约” | 跳过此次跟进——太琐碎了 | — |
| “妈妈周四要做手术” | 周四晚上7点 | “想着你呢——手术进行得怎么样？” |