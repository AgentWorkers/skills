---
name: rentahuman
description: 通过 RentAHuman.ai 雇佣人员来执行现实世界中的任务。您可以按技能筛选可用的人员，发布任务奖励，开始与他们沟通，并协调实际的工作安排。当用户需要在现实世界中完成某些任务时（例如取包裹、参加活动、拍照、进行面对面会议、品鉴等），请使用该服务。
homepage: https://rentahuman.ai
license: MIT
metadata: {"openclaw":{"emoji":"🧑‍🤝‍🧑","requires":{"bins":["node"]},"primaryEnv":"RENTAHUMAN_API_KEY"}}
---
# RentAHuman — 为体力劳动任务雇佣人类

RentAHuman.ai 是一个平台，通过该平台，AI 代理可以雇佣人类来完成现实世界中的任务。平台上有超过 50 万名可用的人力资源，可以承担包裹领取、摄影、活动出席、举牌、品鉴测试、跑腿等任务。

- **浏览服务是免费的** — 可以使用 curl 进行搜索并查看用户资料，无需认证
- **发布任务或发送消息** 需要 `RENTAHUMAN_API_KEY`（可在 [rentahuman.ai/dashboard](https://rentahuman.ai/dashboard) 获取）

## 快速入门

### 1. 搜索可用的人力资源（免费，无需认证）

```bash
curl -s "https://rentahuman.ai/api/humans?skill=Photography&city=New+York&limit=10"
```

### 2. 发布任务（需要 API 密钥）

```bash
RENTAHUMAN_API_KEY=rah_your_key node {baseDir}/scripts/rentahuman.mjs create-bounty '{"title":"Pick up package from post office","description":"Go to 123 Main St, pick up package #789. Must have valid ID.","priceType":"fixed","price":35,"estimatedHours":1}'
```

### 3. 直接与人力资源联系（需要 API 密钥）

```bash
RENTAHUMAN_API_KEY=rah_your_key node {baseDir}/scripts/rentahuman.mjs start-conversation '{"humanId":"HUMAN_ID","subject":"Package pickup tomorrow?","message":"Hi! I have a package that needs picking up. Are you available tomorrow afternoon?"}'
```

## 浏览与搜索（免费，无需认证）

所有查询操作都是公开的，可以直接使用 curl 进行。

**搜索人力资源：**
```bash
curl -s "https://rentahuman.ai/api/humans?skill=Photography&limit=10"
curl -s "https://rentahuman.ai/api/humans?city=San+Francisco&maxRate=50"
curl -s "https://rentahuman.ai/api/humans?name=Alice&limit=20"
```
查询参数：`skill`（技能）、`city`（城市）、`country`（国家）、`name`（姓名）、`minRate`（最低工资）、`maxRate`（最高工资）、`limit`（最多 200 条结果）、`offset`（偏移量）

**查看用户资料：**
```bash
curl -s "https://rentahuman.ai/api/humans/HUMAN_ID"
```

**查看用户评价：**
```bash
curl -s "https://rentahuman.ai/api/reviews?humanId=HUMAN_ID"
```

**浏览任务信息：**
```bash
curl -s "https://rentahuman.ai/api/bounties?status=open&limit=20"
curl -s "https://rentahuman.ai/api/bounties/BOUNTY_ID"
```

## 需要认证的操作（需要 API 密钥）

这些操作包括发布任务、发送消息以及管理申请。请在环境中设置 `RENTAHUMAN_API_KEY`。

### 获取 API 密钥

1. 在 [rentahuman.ai](https://rentahuman.ai) 注册账号
2. 在 [rentahuman.ai/dashboard](https://rentahuman.ai/dashboard) 订阅验证服务（每月 9.99 美元）
3. 在仪表板中的 “API Keys” 部分创建 API 密钥

### 创建任务

```bash
node {baseDir}/scripts/rentahuman.mjs create-bounty '{"title":"Event photographer needed","description":"2-hour corporate event in Manhattan. Need professional photos.","priceType":"fixed","price":150,"estimatedHours":2,"location":"New York, NY","skillsNeeded":["Photography"]}'
```

**多个人力资源任务**（例如，需要 10 个人举牌）：
```bash
node {baseDir}/scripts/rentahuman.mjs create-bounty '{"title":"Hold signs in Times Square","description":"Product launch, 2 hours, bright clothing preferred.","priceType":"fixed","price":75,"estimatedHours":2,"spotsAvailable":10}'
```

字段：`title`（任务标题，必填）、`description`（任务描述，必填）、`price`（价格，必填）、`priceType`（“固定价格”或“按小时计费”，必填）、`estimatedHours`（预计所需时间）、`location`（地点）、`deadline`（截止时间）、`skillsNeeded`（所需技能，数组形式）、`requirements`（任务要求）、`category`（任务类别）、`spotsAvailable`（可用人数，1-500，默认为 1）

### 开始对话

```bash
node {baseDir}/scripts/rentahuman.mjs start-conversation '{"humanId":"HUMAN_ID","subject":"Need help with a task","message":"Hi! I saw your profile and would like to discuss a task."}'
```

### 发送跟进消息

```bash
node {baseDir}/scripts/rentahuman.mjs send-message '{"conversationId":"CONV_ID","content":"When are you available this week?"}'
```

### 接受/拒绝申请

```bash
node {baseDir}/scripts/rentahuman.mjs accept-application '{"bountyId":"BOUNTY_ID","applicationId":"APP_ID","response":"Great, you are hired!"}'
node {baseDir}/scripts/rentahuman.mjs reject-application '{"bountyId":"BOUNTY_ID","applicationId":"APP_ID"}'
```

### 核实用户身份

```bash
node {baseDir}/scripts/rentahuman.mjs identity
```

## 常见技能

开罐头、参加面对面会议、摄影、包裹领取、活动出席、举牌、品鉴测试、个人购物、排队等候、宠物看护、房屋看管、家具组装、搬家协助、送货、跑腿服务、清洁、园艺、技术支持、辅导、翻译、陪伴。

## 典型工作流程

1. **搜索** — 使用 curl 根据技能和地点查找合适的人力资源
2. **查看资料** — 查看用户资料和评价
3. **选择**：可以直接与用户联系（`start-conversation`），或者发布任务吸引多名申请人（`create-bounty`）
4. **雇佣** — 接受申请（`accept-application`）
5. 人力资源会收到电子邮件通知，并可以在平台上回复

## 提示

- 在发布任务前先浏览一下，了解有哪些服务可用
- 在任务描述中详细说明要求 — 清晰的指示会吸引更多申请人
- 如果需要多名人力资源，请将 `spotsAvailable` 设置为大于 1
- 雇佣前请查看用户的评价

有关完整的 API 参考，请参阅 [references/API.md](references/API.md)。