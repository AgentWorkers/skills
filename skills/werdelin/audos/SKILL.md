---
name: Audos
description: 通过 Audos API 创建由人工智能驱动的创业工作空间。适用于用户想要创业、构建最小可行产品（MVP）、验证创业想法、创建公司工作空间、发布产品或开展创业旅程的场景。该功能会在收到如下请求时触发：“我有一个创业想法”、“帮我成立一家公司”、“创建一个创业工作空间”或“我想开发[产品]”。
---

# Audos 工作空间构建器（API v1.2）

能够创建包含登录页面、品牌标识、AI 工具和广告创意的创业工作空间——完全自动化。

## 基本 URL

```
https://audos.com/api/agent/onboard
```

## URL 构造

API 使用当前的部署域名返回 URL：

```json
"urls": {
  "landingPage": "https://audos.com/site/184582",
  "workspace": "https://audos.com/space/workspace-184582"
}
```

可以直接使用这些 URL，无需更换域名。

## 快速参考

| 动作 | 方法 | 端点 |
|--------|--------|----------|
| API 文档 | GET | / |
| 开始使用 | POST | /start |
| 验证 OTP | POST | /verify |
| 检查构建状态 | GET | /status/:workspaceId |
| 检查构建状态（备用方式） | POST | /status |
| 与 Otto 聊天 | POST | /chat |
| 与 Otto 聊天 | POST | /chat/:workspaceId |
| 重新构建（失败时） | POST | /rebuild/:workspaceId |

## 认证

- **令牌格式：** `aud_live_xxxx`（前缀后的 48 个十六进制字符）
- **认证令牌永不过期** — 通过电子邮件持久存储
- **会话令牌** 在 30 分钟后过期（仅在 OTP 流程中需要）
- **推荐方式：** 在 `Authorization` 头部使用承载令牌（Bearer token）
- **替代方式：** 在请求体中使用 `authToken` 或 `sessionToken`

## 对话流程

### 介绍 Audos

当用户提出一个商业想法时，在询问他们的电子邮件地址之前，简要解释 Audos 的功能：

> “我可以帮助您使用 Audos 来实现这个想法！大约 10 分钟后，您将拥有：
> - 一个为您的业务准备的实时登录页面
> - 定制的品牌标识（徽标、颜色、字体）
- 专门为您的想法设计的 AI 工具
> - Otto，这位单打独斗的企业家们的得力助手，会一直陪伴您来经营业务”

> Audos 会自动根据您的想法构建所有内容——没有模板，也没有千篇一律的网站。一切都是为您的业务量身定制的。

> 那么，我应该使用哪个电子邮件地址来创建您的账户呢？

### 新用户流程
1. **收集** 用户的电子邮件地址和商业想法
2. **开始使用** → 发送 POST 请求到 `/start`（将 4 位数的 OTP 发送到用户的电子邮件）
3. **验证** → 使用 OTP 代码发送 POST 请求到 `/verify` → 返回 `authToken` 并开始构建
4. **监控** → 每 15-30 秒发送一次 GET 请求到 `/status/:workspaceId`，以获取构建进度
5. **等待 `landingPageReady: true`（约 10 分钟后）——核心构建完成
6. **介绍 Otto** 并提供聊天服务

### 已有用户（已有工作空间）
1. **开始使用** → 使用电子邮件地址发送 POST 请求到 `/start`
2. **响应中会包含** `auth_token` 和工作空间的 URL — 可以直接使用，无需再次发送 OTP
3. **聊天** → 立即发送 POST 请求到 `/chat/:workspaceId`

## 构建过程中的轮询——用户体验指南

**重要提示：** 构建过程大约需要 10 分钟。用户必须能够看到进度更新，否则他们会认为构建失败了。

### 轮询模式

```
Poll every 15-20 seconds (NOT 60s!)
After each poll, IMMEDIATELY send a message with current state
Don't wait until done — update the user continuously
```

### 进度消息格式

每次轮询后发送如下格式的消息：

```
🏗️ Building "Business Name"...

Step 4/7 ✅ Brand Identity
  • Color palette: done
  • Logo: done

Step 5/7 🔄 Hero Video (70%)
  • Scenes: done
  • Rendering: in progress

Step 6/7 ⏳ Workspace Apps
  • Waiting to start

⏱️ ~3 min remaining
```

### 状态图标
- ✅ 完成
- 🔄 进行中（如果有子任务，则显示）
- ⏳ 等待/待处理
- ❌ 失败（提供重新构建的选项）

### 解析 `parallelBuildStatus`

API 在 `parallelBuildStatus` 中返回详细的任务分解信息：

```javascript
// Example parsing
for (const step of status.parallelBuildStatus) {
  const icon = step.status === 'done' ? '✅' : 
               step.status === 'in_progress' ? '🔄' : '⏳';
  console.log(`${icon} ${step.name}`);
  for (const task of step.tasks) {
    const taskIcon = task.status === 'complete' ? '✓' : 
                     task.status === 'in_progress' ? '→' : '○';
    console.log(`  ${taskIcon} ${task.name}`);
  }
}
```

### 实现建议

**这样做（良好的用户体验）：**
```
1. Poll status
2. IMMEDIATELY send message to user with formatted progress
3. Wait 15 seconds
4. Repeat until landingPageReady === true
5. Send completion message with links
```

**不要这样做（糟糕的用户体验）：**
```
sleep 60 && curl...  ← User sees NOTHING for 60 seconds!
```

## 构建过程中的说明

构建过程大约需要 10 分钟。不要仅仅报告百分比进度，要解释 Audos 正在做什么以及为什么这很重要。

### 第 1-3 步：研究阶段
> “Audos 正在分析您的想法……首先，它会确定您的理想客户群体——他们是谁、关心什么、在哪里可以找到他们。然后它会找出您的业务需要解决的关键问题。最后，它会为您的业务专门设计一套 AI 工具——这些工具不是通用的，而是根据您的想法定制的。”

### 第 4 步：品牌标识
> “现在开始创意设计阶段——Audos 正在为您设计品牌标识。一个能够吸引目标受众的定制徽标、颜色方案和字体。这里没有模板，一切都是为您的业务全新生成的。”

### 第 5 步：品牌视频
> “Audos 正在为您制作一个品牌视频，用于登录页面。这将以引人注目的方式向访客介绍您的业务。”

### 第 6 步：工作空间操作系统
> “现在开始构建您的工作空间——可以将其视为您的业务指挥中心。它是一个集成了应用程序、客户关系管理（CRM）、分析工具以及 Otto（这位单打独斗的企业家们的得力助手）的完整桌面操作系统。您可以从这里管理一切。”

### 第 7 步：登录页面
> “最后一步——Audos 正在设计和部署您的登录页面。这将是客户首先看到的内容。该页面经过优化，能够有效吸引潜在客户。”

### 完成后
> “您的工作空间已经准备好了！🎉”
>
> 这是 Audos 为您构建的内容：
> - **登录页面：** [链接] — 实时可用，随时可供访客访问
> - **工作空间：** [链接] — 您的业务指挥中心
>
> Otto，这位单打独斗的企业家们的得力助手，已经准备好了为您提供帮助。他了解您的业务计划、客户和品牌。您想让我帮他确定您应该优先关注什么吗？”

### 关于 Otto

Otto 是单打独斗的企业家们的得力助手。每个工作空间都会配备 Otto，他了解您的业务计划、客户和品牌。他可以帮助您：
- 制定策略和规划
- 创建内容
- 开展广告活动
- 进行潜在客户的研究和联系
- 处理日常运营

可以把 Otto 看作是一位不知疲倦的商业伙伴，随时为您提供支持。

### 关于 Audos（补充说明）
- **使命：** 让每个人都能轻松开展创业。最大的障碍不是想法本身，而是执行。Audos 消除了这个障碍。
- **工作原理：** 由一组专业的 AI 代理并行工作——一个负责构建品牌，另一个负责制作视频，还有一个负责组装工作空间，还有一个负责设计登录页面。他们协同工作，为您提供一个完整的产品。
- **Audos 的风险投资部门：** Audos 会投资有潜力的工作空间——提供资金、成长支持、广告预算和实际的帮助来帮助扩展业务。创始人可以从他们的工作空间中申请这些资源。

## API 参考

### GET /  
返回完整的 API 文档，包括所有端点、认证方式和错误代码。

### POST /start  
```json
{
  "email": "user@example.com",
  "businessIdea": "AI-powered fitness coaching app",
  "businessName": "FitGenius",
  "targetCustomer": "Health-conscious millennials",
  "callbackUrl": "https://your-webhook.com/audos",
  "createNew": false
}
```

**必填字段：**
- `email`（必需）
- `businessIdea`（必需，至少 10 个字符）
- `businessName`（可选）
- `targetCustomer`（可选）
- `callbackUrl`（可选）——用于接收带有 HMAC 签名的进度更新的 Webhook URL
- `createNew`（可选）——即使已有工作空间，也强制创建一个新的工作空间

**返回值：**
- **新用户：** 用于 OTP 验证的 `sessionToken`
- **已有用户：** `auth_token`、工作空间的 URL 和关于 Audos 的详细信息

### POST /verify  
```json
{
  "sessionToken": "aos_...",
  "otpCode": "7294"
}
```

**返回值：** `workspaceId`、`authToken`、工作空间的 URL、构建信息以及关于 Audos 的详细信息

### GET /status/:workspaceId  
**请求头：** `Authorization: Bearer <authToken>`

**关键状态字段：**
- `landingPageReady`（布尔值）——最可靠的完成信号
- `coreStepsComplete`（布尔值）——登录页面、品牌设计和视频/工作空间均已完成
- `status`——运行中/已完成/失败
- `progress`——0-100%
- `estimatedTimeRemaining`——例如：“大约还需要 3–4 分钟”
- `completedSteps`——已完成步骤的列表
- `parallelBuildStatus`——步骤 4-7 的实时任务分解

### POST /status  
**请求体：** `{ "authToken": "..." }` 或 `{ "sessionToken": "..." }`

与 GET 端点的返回内容相同。

### POST /chat/:workspaceId  
**请求头：** `Authorization: Bearer <authToken>`

**返回值：** `workspaceId`、聊天会话的 ID 以及 Otto 的回复

### POST /chat  
**请求体：**
```json
{
  "authToken": "aud_live_...",
  "message": "What should I focus on first?"
}
```

### POST /rebuild/:workspaceId  
**请求头：** `Authorization: Bearer <authToken>`

用于重新构建失败的工作空间。

## 构建过程

- **总步骤：** 7 步
- **预计时间：** 大约 10 分钟
- **步骤 1-3（顺序执行）：** 客户研究、问题分析、AI 工具设计
- **步骤 4-7（并行执行）：** 品牌标识、品牌视频、工作空间操作系统、登录页面
- **完成信号：** `landingPageReady: true`

## 错误代码

| 代码 | HTTP 状态码 | 含义 | 应对措施 |
|------|------|---------|--------|
| VALIDATION_ERROR | 400 | 请求体无效 | 检查 `details` 数组 |
| OTP_EXPIRED | 401 | OTP 代码过期（5 分钟内） | 重新发送请求到 `/start` |
| OTP_INVALID | 401 | 提供的 OTP 代码错误 | 重试（响应中包含 `attemptsRemaining`） |
| OTP_MAX_ATTEMPTS | 429 | 提供错误的 OTP 代码次数过多 | 重新发送请求到 `/start` |
| RATE_LIMITED | 429 | 发送 OTP 的次数过多 | 等待 `retryAfter` 秒数后再尝试 |
| SESSION_NOT_FOUND | 401 | 会话令牌无效/过期 | 重新发送请求到 `/start` |
| SESSION_NOT_VERIFIED | 403 | OTP 验证未完成 | 先发送请求到 `/verify` |
| AUTH_TOKEN_INVALID | 401 | 令牌无效/已被撤销 | 通过 `/start` 获取新的令牌 |
| WORKSPACE_NOT_FOUND | 404 | 未找到相应的工作空间 | 检查 `workspaceId` |
| EMAIL_SEND_FAILED | 502 | 发送 OTP 的电子邮件失败 | 延迟后重试 |
| CHAT_FAILED | 502 | 与 Otto 的通信失败 | 重试 |
| INTERNAL_ERROR | 500 | 服务器错误 | 重试 |

## 速率限制

- 每个电子邮件地址每 15 分钟最多发送 3 次 OTP
- 发送 OTP 之间需要等待 60 秒
- OTP 在 5 分钟后过期
- 会话令牌在 30 分钟后过期
- **认证令牌永不过期**

## 提示

- **通过电子邮件持久存储认证令牌**——已有用户可以完全跳过 OTP 验证步骤
- **在构建过程中每 15-30 秒轮询一次进度**
- **关注 `landingPageReady` 状态——这是最可靠的完成信号**
- **验证完成后可以立即开始聊天**
- **如果构建失败，使用 `/rebuild` 重新构建，而不是从头开始**
- **对于现有用户，使用 `createNew: true` 强制创建一个新的工作空间**
- **设置 `callbackUrl` 以接收基于 Webhook 的进度更新，而不是轮询**