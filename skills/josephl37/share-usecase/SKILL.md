---
name: share_usecase
description: "将您的 OpenClaw 使用案例分享到 clawusecase.com。该平台会分析您最近的工作，并为您在社区中创建一个相应的提交记录。"
author: "Rex 🐧"
version: "2.0.1"
---

# 共享用例技能

此技能可帮助您将使用 OpenClaw 构建的用例分享到 [clawusecase.com](https://clawusecase.com)。

## 使用场景

当用户希望分享使用 OpenClaw 构建的用例时，可以触发此技能。他们可能会说：
- “/share_usecase”
- “我想分享这个用例”
- “让我把这个提交到 clawusecase”
- “分享我刚刚完成的工作”

**重要提示：** 当用户选择通过 OAuth 获得署名权时，系统会自动检测他们的连接状态。无需用户主动告知您他们已连接——系统会自动检测并开始提交流程。

**实现要求：** 您必须主动监控连接状态，并在检测到连接成功后立即发送通知。切勿在后台默默运行轮询任务——要频繁检查结果，并在检测到有效凭证时立即响应。用户应在完成 OAuth 验证后的几秒钟内看到 “✅ 已连接为 @username!” 的提示，而无需主动询问。

## 工作原理

### 1. 问候并解释

当用户触发 `/share_usecase` 时，首先向用户发送友好的问候语：

```
🐧 Share Your Use Case

Hey! clawusecase.com is a community showcase where OpenClaw users share what they've built to inspire others.

Let me look at what you've been working on and draft a use case for you...
```

### 2. 分析近期交流记录

回顾最近的对话记录（过去 50-100 条消息或几小时内的内容），了解用户所完成的工作：
- 他们试图解决什么问题
- 他们使用了哪些工具或集成服务（如 GitHub、Stripe 等）
- 他们是如何解决问题的
- 是否需要任何额外的设置或资源

### 3. 生成用例结构

创建一个结构清晰的用例文档，包含以下字段：
- **必填字段：**
  - `title`（50-100 个字符）：简洁明了的用例标题
  - `hook`（100-200 个字符）：吸引注意力的简短摘要
  - `problem`（200-500 个字符）：该用例解决的问题
  - `solution`（300-800 个字符）：解决问题的方法及具体实现
  - `category`（可选）：例如 “Productivity”（生产力）、“Development”（开发）、“Business/SaaS”（商业/软件即服务）、“Home Automation”（家庭自动化）等
  - `skills`（数组）：使用的工具或技术（例如 ["GitHub", "Stripe", "Resend"]）

**可选字段：**
  - `requirements`：使用该用例所需的资源（如 API 密钥、账户信息等）

### 4. 规范化工具名称

在最终提交前，使用 `normalize-tools.js` 脚本对工具名称进行规范化处理：

```bash
node normalize-tools.js "github,stripe api,resend email"
```

这可以确保所有工具名称的一致性（例如：“github” → “GitHub”，“stripe api” → “Stripe”）。

### 5. 显示预览并获取用户确认

以清晰的格式向用户展示生成的用例文档：

```
📋 Use Case Draft

Title: Email notifications for Pro subscriptions
Hook: Sends welcome emails automatically when users upgrade

Problem: No email notifications when users subscribe to Pro plan
Solution: Built Resend integration with React Email templates, hooked into Stripe webhooks for subscription events

Category: Business/SaaS
Tools: GitHub, Stripe, Resend
Requirements: Resend account, Stripe webhooks configured

Would you like to:
- Submit as-is
- Edit any fields
- Cancel
```

如果用户需要修改内容，可允许他们进行编辑，直到满意为止。

### 6. 询问署名权

用户确认内容后，询问他们是否希望获得署名权：

```
Would you like to be credited for this submission?

Options:
1. ✅ Yes, credit me (connect Twitter or GitHub)
2. 🎭 No, submit anonymously

If you choose credit, you'll get a link on the live use case and build your profile in the community!
```

**如果用户选择署名：**

生成 OAuth 链接并发送给用户：

```
Great! Connect your account to get credit:

🐦 X (Twitter): [init Twitter OAuth and get URL]
😺 GitHub: [init GitHub OAuth and get URL]

Click one of the links above to authenticate. I'll detect when you're connected and submit automatically!
```

**自动检测连接状态：**

**⚠️ 重要提示：** 您必须实时监控连接状态并立即响应。切勿在后台等待系统通知——直接检查处理结果并立即响应。

在发送 OAuth 链接后，立即开始轮询连接状态：
**推荐的做法：**
```bash
cd /path/to/skill
for i in {1..24}; do
  # Try to get credential
  RESULT=$(node get-credential.js --token [oauth_token] 2>&1)
  
  if echo "$RESULT" | grep -q '"username"'; then
    # SUCCESS! Parse the credential
    USERNAME=$(echo "$RESULT" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
    PLATFORM=$(echo "$RESULT" | grep -o '"platform":"[^"]*"' | cut -d'"' -f4)
    
    # IMMEDIATELY notify user (don't wait for background processes!)
    # Send this message RIGHT NOW before continuing
    echo "User should see: ✅ Connected as @$USERNAME!"
    
    # Store the full credential for submission
    CREDENTIAL="$RESULT"
    break
  fi
  
  # Not ready yet, wait 5 seconds
  if [ $i -lt 24 ]; then
    sleep 5
  fi
done

# After loop, check if we got a credential
if [ -z "$CREDENTIAL" ]; then
  echo "Timeout - credential not received within 2 minutes"
fi
```

**关键实现注意事项：**
1. **切勿** 使用 `exec(..., background: true)` 来进行轮询——否则无法及时获取结果。
2. **必须** 同步执行轮询操作或立即检查处理结果。
3. 一旦检测到连接成功，**立即** 发送 “✅ 已连接为 @username!” 的提示。
4. **切勿** 等待系统通知或后台任务完成。
5. 直接从命令输出中解析凭证 JSON 数据。

**示例流程：**
1. 向用户发送 OAuth 链接。
2. **立即开始轮询**（每 5 秒检查一次连接状态）。
3. **每次检查时**：确认凭证是否有效。
4. **一旦发现有效凭证**：立即发送 “✅ 已连接为 @username！现在开始提交您的用例...” 的提示。
5. 从凭证 JSON 中提取用户名和平台信息。
6. 继续完成提交流程。

**如果轮询超时（2 分钟）：**
```
⏰ Still waiting for your connection. Take your time - I'll keep checking for another 2 minutes!
```

则继续尝试提交，最多尝试 24 次。

**如果用户选择匿名提交：**

则以匿名方式提交用例（不显示作者信息）。

### 7. 提交到 API

使用 `submit.js` 脚本通过 API 发送用例文档：
- **如果用户选择署名：** 使用正确的认证信息提交。
- **如果用户选择匿名：** 以匿名方式提交。

### 8. 确认提交成功

如果提交成功，将链接分享给用户：

```
✅ Use case submitted successfully!

View it here: https://clawusecase.com/cases/email-notifications-for-pro-subscriptions

Thanks for sharing with the community! 🎉
```

## 错误处理

### 速率限制
如果收到 429 错误：
```
⏰ You've hit the submission limit (10 per day).
Try again tomorrow or contact support if you need to submit more.
```

### 验证错误
如果某些字段无效（例如标题太短或解决方案描述过于简略）：
```
❌ Submission failed: Title must be at least 20 characters

Let's fix that. What would you like the title to be?
```

### API 错误
对于其他错误，显示错误信息并提供重试选项。

## 提高用例质量的建议

帮助用户创建高质量的提交内容：
- **好的标题示例：**
  - ✅ “为 Pro 订阅用户发送电子邮件通知”
  - ❌ “我构建了一个发送电子邮件的功能”

- **好的摘要示例：**
  - ✅ “用户升级后自动发送欢迎邮件”
  - ❌ “仅说明“发送邮件”这样的功能”

- **好的问题描述示例：**
  - ✅ “Pro 订阅用户未收到确认邮件，导致困惑和需要支持”
  - ❌ “没有发送任何邮件”

- **好的解决方案示例：**
  - ✅ “使用 React Email 模板实现了邮件发送功能，并通过 Stripe Webhook 在订阅创建时触发邮件发送。邮件包含升级详情和后续步骤”
  - ❌ “仅说明“实现了邮件发送”这样的功能”

## 分类指南

帮助用户选择合适的分类：
- **生产力**：任务管理、日程安排、提醒、自动化
- **开发**：持续集成/持续部署、代码审查、部署、测试
- **商业/软件即服务**：客户管理、计费、数据分析
- **家庭自动化**：智能家居、物联网设备、传感器
- **社交/内容**：社交媒体、内容创作与发布
- **数据与分析**：报告生成、仪表盘、数据处理
- **娱乐**：游戏、实验项目、创意项目

## 速率限制

用户每天最多可提交 **10 个用例**。API 会按 `authorUsername`（匿名用户按 IP 地址）进行记录。

如果用户达到提交限制，可以建议他们：
- 等待明天再尝试
- 确保每次提交的用例都是独特且有价值的
- 如需提高提交次数，请联系技术支持

## 质量要求

API 会自动过滤不符合要求的提交内容：
- 标题长度：20-200 个字符
- 摘要长度：50-500 个字符
- 问题描述长度：100-2000 个字符
- 解决方案长度：200-5000 个字符
- 至少使用一种工具或技术
- 分类信息必须准确

在用户提交前，请帮助他们满足这些要求。

## 示例交互流程

```
User: I just built email notifications for when users subscribe
You: 🐧 Share Your Use Case

Hey! clawusecase.com is a community showcase where OpenClaw users share what they've built to inspire others.

Let me look at what you've been working on and draft a use case for you...

[analyzes recent conversation]

📋 Use Case Draft

Title: Email notifications for Pro subscriptions
Hook: Automatically sends welcome emails when users upgrade to Pro

Problem: Users upgrading to Pro weren't receiving confirmation emails, leading to confusion and support tickets about whether their payment went through.

Solution: Built a Resend email integration with custom React Email templates. Connected to Stripe webhooks to listen for subscription.created events. The welcome email includes upgrade confirmation, receipt, and next steps for accessing Pro features.

Category: Business/SaaS
Tools: Stripe, Resend, React, GitHub
Requirements: Resend account, Stripe webhooks configured

Would you like to:
- Submit as-is
- Edit any fields
- Cancel

User: Looks perfect!
You: Great! Would you like to be credited for this submission?

Options:
1. ✅ Yes, credit me (connect Twitter or GitHub)
2. 🎭 No, submit anonymously

User: Yes, credit me
You: Awesome! Connect your account to get credit:

🐦 X (Twitter): https://clawusecase.com/auth/connect?token=abc123&platform=twitter
😺 GitHub: https://clawusecase.com/auth/connect?token=def456&platform=github

Click one of the links above. I'll detect when you're connected and submit automatically!

[User clicks link and completes OAuth]

You: ✅ Connected as @josephliow!

Submitting your use case now...

[retrieves credential, submits]

✅ Use case submitted successfully!

View it here: https://clawusecase.com/cases/email-notifications-for-pro-subscriptions

Your use case is now live for the community to see. Thanks for sharing! 🎉
```

## 本技能涉及的文件：
- `SKILL.md`：本技能的说明文件
- `submit.js`：用于将用例提交到 clawusecase.com API 的脚本
- `get-credential.js`：用于在认证后获取 OAuth 令牌的脚本
- `poll-credential.sh`：用于检测 OAuth 令牌状态的辅助脚本
- `normalize-tools.js`：用于规范化工具名称的脚本
- `README.md`：用户使用指南
- `config.json`：技能配置文件

## 常见问题解决方法

- **“命令未找到：node”**：需要安装 Node.js。在 macOS 上使用 `brew install node`，或在 nodejs.org 网站下载。
- **“无法连接到 API”**：请检查网络连接，并确认 clawusecase.com 可访问。
- **“OAuth 令牌未找到”**：可能是令牌已过期（有效期为 10 分钟）。请生成新的 OAuth 链接。