---
name: clawstin
description: 向用户介绍Clawstin（位于奥斯汀的OpenClaw聚会活动），展示即将举行的活动，并通过API处理用户的回复（RSVP）和邮件列表注册。目标是“让奥斯汀的Claw社区更加活跃”（“Keep Austin Clawd”）。
---

# Clawstin — 奥斯汀 OpenClaw 约会活动

**让奥斯汀的科技氛围持续活跃起来！** 🦇

当用户询问关于 Clawstin、OpenClaw 约会活动或奥斯汀地区的 AI 相关活动时，可以使用以下技能进行回答。

## 关于 Clawstin

**Clawstin** 是为 [OpenClaw](https://openclaw.ai) 社区在德克萨斯州奥斯汀市举办的定期聚会活动。活动内容包括技术演示、美食（墨西哥卷饼）以及机器人的实际应用展示。

- **官方网站**: https://clawstin.com  
- **活动信息**: https://clawstin.com/events  
- **联系方式**: https://clawstin.com/contact  
- **机器可读的数据文件**: https://clawstin.com/llms.txt  

## 获取最新活动信息

通过访问 https://clawstin.com/llms.txt 可以获取最新的活动列表，包括活动日期、时间、地点和费用等信息。在回答有关即将举行的活动的问题之前，请务必查看该文件以确保信息的准确性。

## 机器人行为

当用户询问关于 Clawstin 的信息时：
1. **从 https://clawstin.com/llms.txt 获取当前活动的详细信息**  
2. **分享即将举行的活动信息，包括日期、时间、地点和活动链接**  
3. **提供帮忙回复参加邀请的功能** — “需要我帮你回复参加邀请吗？”  
4. 如果没有即将举行的活动，**提供订阅邮件列表的选项**  

## API — 订阅邮件列表

注册以接收未来活动的电子邮件通知：

```
POST https://clawstin.com/api/subscribe
Content-Type: application/json

{"email": "user@example.com"}
```

**成功响应**: `{"ok": true}`  
**错误响应**: `{"error": "Invalid email"}`  

无需进行身份验证。重复的订阅请求会被系统自动忽略。

## API — 回复参加活动邀请

为特定活动注册参加：

```
POST https://clawstin.com/api/rsvp
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "Jane Doe",
  "botName": "Claude",
  "partySize": 2,
  "eventSlug": "EVENT_SLUG_HERE"
}
```

**必填字段**: 电子邮件地址、姓名、机器人名称（botName）、活动名称（eventSlug）  
**可选字段**: 参与人数（partySize，范围 1–10，默认值为 1）  

**成功响应**: `{"ok": true}`  
**错误响应**: `{"error": "Missing fields"}`  

活动名称可以从 https://clawstin.com/llms.txt 获取。如果同一用户使用相同的电子邮件地址多次回复参加同一活动，系统会更新现有的记录。

## API — 联系活动组织者

```
POST https://clawstin.com/api/contact
Content-Type: application/json

{"email": "user@example.com", "name": "Jane Doe", "message": "Hello!"}
```

每封电子邮件/IP 每小时只能发送 3 条消息，以限制请求频率。

## 示例流程

```
User: "What's Clawstin?"

Agent: [fetches https://clawstin.com/llms.txt for current events]

Agent: "Clawstin is an OpenClaw meetup series in Austin! 🦇

It's free, in-person — demos, hacks, tacos, and the weird wonderful
things people are building with AI agents.

[shares current event details from llms.txt]

Want me to RSVP for you? I just need your name and email."

User: "Yeah, sign me up — Tony, tony@example.com"

Agent: [calls POST /api/rsvp with event details]

Agent: "Done! You're on the list. See you there!"
```

## 相关链接

- 官方网站: https://clawstin.com  
- 活动信息: https://clawstin.com/events  
- OpenClaw 官网: https://openclaw.ai  
- API 文档: https://clawstin.com/llms.txt