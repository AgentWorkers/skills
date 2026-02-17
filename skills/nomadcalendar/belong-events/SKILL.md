---
name: belong-events
description: 在 Belong 平台上，您可以使用 NFT 票券来创建、发现和管理各种事件。
metadata: {"openclaw": {"emoji": "🎫", "primaryEnv": "BELONG_EVENTS_API_KEY", "optionalEnv": ["BELONG_EVENTS_ENDPOINT"], "requires": {"bins": ["curl"]}}}
---
# Belong 事件管理

在 Belong 平台上，您可以发现活动、购买门票、创建活动以及管理参与者的签到信息。

## 如何调用工具

通过 `system.run` 运行 `/{baseDir}/invoke.sh <method> '<params-json>'` 命令来调用相应的工具。该脚本会调用 Belong 的技能 API 并返回 JSON 格式的响应。

**示例：**
```
system.run {baseDir}/invoke.sh discover_events '{"city":"Miami","limit":5}'
```

所有工具的调用都遵循这一模式。`invoke.sh` 脚本会自动处理端点 URL、认证头部信息以及 JSON-RPC 请求的格式化。

**默认端点：**
`https://join.belong.net/functions/v1/openclaw-skill-proxy`

**网络通信细节：**
- 所有的 JSON-RPC 请求都会发送到上述端点（如果设置了 `BELONG EVENTS_ENDPOINT`，则会使用该地址）。
- 如果设置了 `BELONG EVENTS_API_KEY`，它会被作为 `X-OpenClaw-Key` 头部字段发送到请求中。

## 账户绑定（部分工具需要）

大多数工具都需要绑定 Belong 账户。如果某个工具返回 “Belong 账户未绑定” 或 “BELONG_LINK_REQUIRED”的提示，请按照以下步骤操作：
1. 询问用户的电子邮件地址。
2. 向用户发送 OTP（一次性密码）：
   ```
   system.run {baseDir}/invoke.sh belong_email_otp_send '{"email":"USER_EMAIL"}'
   ```
3. 询问用户收到的 6 位验证码。
4. 验证 OTP：
   ```
   system.run {baseDir}/invoke.sh belong_email_otp_verify '{"email":"USER_EMAIL","otp":"CODE"}'
   ```
5. 验证成功后，系统会返回 `apiKey`。请将其保存为环境变量 `BELONG EVENTS_API_KEY`，或更新 `openclaw.json` 文件中的 `skills.entries.belong-events.apiKey`，以便后续调用能够通过认证。

**重要提示：**
切勿直接要求最终用户提供 API 密钥，务必使用 OTP 验证机制。

## 可用的工具

### 公共工具（无需认证）

这些工具受到访问速率限制。如果遇到 429 错误，请稍后重试。

- **list_tools** — 列出所有可用的工具（无需参数）
- **discover_events** — 搜索活动。参数：`city`（城市）、`category`（类别）、`startDate`（开始日期）、`endDate`（结束日期）、`limit`（数量限制）、`latitude`（纬度）、`longitude`（经度）（均为可选参数）
- **get_event_details** — 获取活动详情。参数：`eventId`（活动 ID，必填）、`source`（来源）、`city`（城市）、`latitude`（纬度）、`longitude`（经度，可选）
- **buy_ticket** — 获取活动的购票链接。参数：`eventId`（活动 ID，必填）、`tierId`（票务等级）、`quantity`（购买数量）
- **belong_email_otp_send** — 发送 OTP。参数：`email`（用户邮箱，必填）
- **belong_email_otp_verify** — 验证 OTP。参数：`email`（用户邮箱，必填）、`otp`（收到的 OTP，必填）

### 需要认证的工具

#### 账户相关工具
- **whoami** — 检查账户绑定状态（无需参数）

#### 参与者工具
- **my_tickets** — 列出已购买的门票。参数：`status`（活动状态：即将举行/已结束/全部）

#### 组织者工具
- **create_event** — 创建活动。参数：`name`（活动名称，必填）、`startDate`（开始日期，必填）、`endDate`（结束日期）、`description`（活动描述）、`city`（城市）、`venue`（活动场所）、`category`（活动类别）
- **update_event** — 更新活动信息。参数：`eventId`（活动 ID，必填）、`name`（活动名称）、`description`（活动描述）、`startDate`（开始日期）、`endDate`（结束日期）
- **deploy_tickets** — 部署 NFT 票务。参数：`eventId`（活动 ID，必填）、`tierName`（票务等级）、`price`（票价）、`maxSupply`（最大发行数量）、`chainId`（区块链 ID）、`transferable`（是否可转让）、`gasless`（是否免手续费）。分为两步：第一步请求返回交易参数，第二步需要提供 `collectionId` 和 `txHash` 完成部署。
- **my_events** — 列出自己拥有的活动。参数：`status`（活动状态：即将举行/已结束/草稿/全部）
- **event_analytics** — 活动统计信息。参数：`eventId`（活动 ID，必填）

#### 场地管理工具
- **check_in** — 处理参与者签到。参数：`hubId`（场地 ID，必填）、`amount`（签到费用）、`latitude`（纬度）、`longitude`（经度）、`customerWallet`（用户钱包地址）、`listPending`（待处理的签到请求列表）、`checkinId`（签到请求 ID）、`action`（操作类型）
- **list_pending_checkins** — 列出待处理的签到请求。参数：`hubId`（场地 ID，必填）、`limit`（请求数量限制）
- **approve_checkin** — 批准/拒绝签到请求。参数：`checkinId`（签到请求 ID，必填）、`action`（批准/拒绝）
- **setup_venue_rewards** — 配置场地奖励机制。参数：`hubId`（场地 ID）、`visitBounty`（奖励金额）、`cashbackPercent`（返现百分比）
- **withdraw_earnings** — 提取收益。参数：`hubId`（场地 ID）、`currency`（货币类型：USDC/LONG）