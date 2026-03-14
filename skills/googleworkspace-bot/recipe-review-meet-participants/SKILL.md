---
name: recipe-review-meet-participants
version: 1.0.0
description: "查看哪些人参加了 Google Meet 会议以及他们参加了多长时间。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-meet"]
---
# 查看 Google Meet 的出席情况

> **先决条件：** 需要安装并使用以下工具来执行此操作：`gws-meet`

查看谁参加了 Google Meet 会议以及他们的参会时长。

## 步骤

1. 列出最近的会议记录：`gws meet conferenceRecords list --format table`
2. 列出会议参与者：`gws meet conferenceRecords participants list --params '{"parent": "conferenceRecords/CONFERENCE_ID"}' --format table`
3. 获取会议会话详情：`gws meet conferenceRecords participants participantSessions list --params '{"parent": "conferenceRecords/CONFERENCE_ID/participants/PARTICIPANT_ID"}' --format table`