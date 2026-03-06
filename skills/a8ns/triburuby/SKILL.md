---
description: 帮助用户在TribuRuby平台上检查仪式的完成情况、追踪连续完成的记录（即“streaks”），以及查看部落的各类活动。
display_name: TribuRuby Training Agent
env:
- description: TribuRuby Agent API key
  name: TRIBURUBY_API_KEY
  required: true
  secret: true
homepage: "https://triburuby.app"
name: triburuby
primaryEnv: TRIBURUBY_API_KEY
tags:
- fitness
- habits
- training
- community
version: 1.0.1
---
## TribuRuby 技能

该技能与 TribuRuby 平台相连，可帮助用户：

- 完成每日例行签到
- 跟踪训练连续性（即连续完成训练的天数）
- 查看部落活动
- 监控训练计划的进展

官方网站：https://triburuby.app

------------------------------------------------------------------------

## 认证

所有 API 调用均需提供以下授权信息：

Authorization: Bearer \${TRIBURUBY_API_KEY}

API 密钥需在 TribuRuby 的以下设置中创建：

**设置 → 代理 API 密钥**

------------------------------------------------------------------------

## API 基址

API 基址：https://triburuby.app/api/agent

------------------------------------------------------------------------

## 初始化

在使用任何 API 功能之前，务必先进行身份验证：

执行请求：`GET /api/agent`

如果响应内容为：

{"error":"Unauthorized"}

则说明用户的 API 密钥无效或已过期，请重新生成或更换密钥。

------------------------------------------------------------------------

## 可用的 API 功能

### 发现部落

执行请求：`GET /api/agent?action=my-tribes`

返回所有部落及其对应的协议 ID。在调用特定部落的 API 功能之前，请先使用此接口获取信息。

------------------------------------------------------------------------

### 获取训练详情

执行请求：`GET /api/agent?action=context&tribeId=`<id>`{=html}&protocolId=`<id>`{=html}`

返回以下信息：

- 例行签到列表
- 完成状态
- 连续训练的天数
- 训练的数量及单位

------------------------------------------------------------------------

### 查看部落活动

执行请求：`GET /api/agent?action=tribe-activity&tribeId=`<id>`{=html}&protocolId=`<id>`{=html}`

可选参数：`&date=YYYY-MM-DD`

返回以下信息：

- 部落成员名单
- 每周活动记录
- 当前的连续训练天数
- 当天的签到记录

------------------------------------------------------------------------

### 完成例行签到

执行请求：`POST /api/agent`

请求体内容如下：

```json
{
  "action": "check-in",
  "ritualId": "`<id>`{=html}",
  "protocolId": "`<id>`{=html}",
  "quantity": 45,
  "date": "YYYY-MM-DD"
}
```

------------------------------------------------------------------------

## 工作流程

在帮助用户时，请按照以下步骤操作：

1. 使用 `my-tribes` 获取用户的所属部落信息。
2. 确定相关的 `tribeId` 和 `protocolId`。
3. 获取用户的训练详情。
4. 显示部落活动信息。
5. 提供帮助用户完成未完成的例行签到任务的选项。

------------------------------------------------------------------------

## 响应格式

响应内容应保持简洁、积极向上，并重点突出用户的连续训练天数（即“连续性”）。

运动员最关心的是自己的连续训练天数、训练进展以及自己的责任履行情况。