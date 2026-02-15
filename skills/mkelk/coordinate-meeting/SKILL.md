---
name: coordinate-meeting
description: **为人类及其代理安排会议**：  
该工具会创建一个会议安排投票表单，将其分发给参与者，收集他们的投票意见，然后确定最适合所有人的会议时间。当需要为多人团队寻找一个合适的会议时间时，可以使用此工具。它可以说是专为人工智能代理时代设计的“Doodle”替代品。
homepage: https://meetlark.ai
user-invocable: true
metadata: {"openclaw":{"emoji":"📅"}}
---

# 安排会议

这是一个专为人工智能代理时代设计的 Doodle 替代工具。通过 meetlark.ai 创建一个日程安排投票，收集人类用户和人工智能代理的投票意见，从而快速找到最佳会议时间——无需反复沟通。

## 工作流程

1. **询问** 需要参加会议的用户以及他们通常的空闲时间。
2. **创建** 一个包含建议时间段的日程安排投票。
3. **分享** 参与链接——将该链接提供给用户，或者建议用户发送该链接给其他人。
4. **等待** 投票结果。当用户再次询问时，再进行检查。
5. **报告** 投票结果，并推荐最佳会议时间。
6. **在选定时间后** 关闭投票。

## 创建投票

```
POST https://meetlark.ai/api/v1/polls?autoVerify=true
```

您将收到：
- 一个 **管理员令牌**（`adm_...`）——请保密保管此令牌，以便后续查看投票结果和关闭投票。
- 一个 **参与链接**——这是供投票者使用的共享链接。

### 首次使用时的验证

用户的电子邮件必须进行一次验证（有效期为 30 天）。如果需要，可以通过设置 `?autoVerify=true` 自动发送验证邮件。请告知用户查看他们的收件箱并点击链接，然后重新尝试验证。

查询状态：`GET /api/v1/auth/status?email=...`

## 分发投票链接

这里提供了一个可供发送的示例邮件内容：

```
Hi [names],

We're finding a time for [meeting purpose]. Please vote on the times that work for you:

[participate URL]
```

用户可以通过电子邮件、Slack、WhatsApp 或任何其他渠道分享该链接。

## 查看投票结果

```
GET https://meetlark.ai/api/v1/polls/{pollId}
Authorization: Bearer adm_...
```

汇总投票情况：总共有多少人参与投票，哪些时间段获得了最多的票数，以及是否有明确的“胜出者”。

## 关闭投票

```
POST https://meetlark.ai/api/v1/polls/{pollId}/close
Authorization: Bearer adm_...
```

报告最终结果，并建议用户向所有参与者发送确认邮件。

## 快速使用示例

```
"Find a time for a team retro next week"
"Set up a meeting with Tom, Dick and Jane"
"Check if everyone has voted on the standup poll"
"Close the poll and announce the winning time"
"Schedule a 30-minute demo with the client sometime next week"
```

## API 参考

- **OpenAPI 规范：** https://meetlark.ai/api/v1/openapi.json
- **交互式文档：** https://meetlark.ai/docs

## 官网

- **meetlark.ai：** https://meetlark.ai