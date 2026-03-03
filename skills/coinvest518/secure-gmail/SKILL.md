---
name: secure-gmail
description: **使用 Composio 中介的 OAuth 保护 Gmail 功能**：本地不存储原始访问令牌。该功能支持读取、搜索和创建邮件草稿，并严格遵循最小权限原则（即仅允许用户执行其工作所需的最小权限）。发送和删除操作会在 Composio API 网关层面被拦截，而不仅仅是在代码层面。适用于用户需要查看收件箱、按发件人或主题查找特定邮件、汇总未读邮件或创建回复草稿（但暂不发送）的场景。请确保在 `.env` 文件中配置 `COMPOSIO_API_KEY`，并且 Gmail 已在 `app.composio.dev` 上进行配置。**请勿使用此功能发送邮件**——应改用需要人工确认的发送流程。
metadata:
  moltbot:
    requires:
      bins: ["python3"]
      env: ["COMPOSIO_API_KEY"]
---
# 安全Gmail技能（基于Composio的认证）

该技能通过Composio的托管认证层提供只读和草稿功能的Gmail访问权限。OAuth令牌永远不会被存储在您的本地文件系统或代理程序的内存中——所有API调用都由Composio进行中转。

## 何时使用此技能

当用户说出以下任何语句时，激活此技能：

- “查看我的邮件” / “我的收件箱里有什么？”
- “[某人]回复了吗？” / “查找来自[发件人]的邮件”
- “汇总今天/这周未读的邮件”
- “为[邮件地址]创建回复草稿”——仅创建草稿，不会发送
- “[某人]就[主题]给我发了什么？”
- “搜索关于[主题]的邮件”

**请勿在以下情况下激活此技能**：
- “发送邮件” → 使用需要人工审核的发送技能
- “删除邮件” → 在API层面被禁止，会优雅地失败
- “访问Google Drive或Calendar” → 使用/gog或/google-drive技能

## 先决条件（首次使用前必须完成）

1. 在app.composio.dev上拥有Composio账户（免费 tier即可）
2. 在Composio控制台中将Gmail添加为已连接账户
3. 在`~/clawd/skills/secure-gmail/.env`文件中设置COMPOSIO_API_KEY
4. 安装以下Python包：`pip install python-dotenv composio`

如果缺少COMPOSIO_API_KEY，技能将显示错误信息：
`Error: COMPOSIO_API_KEY not found in environment`
请引导用户将密钥添加到.env文件中，然后重试。

## 具体命令

### 获取最近收到的邮件
```bash
cd ~/clawd/skills/secure-gmail && python3 agent.py "fetch last 10 emails"
```

### 按发件人搜索邮件
```bash
python3 agent.py "find emails from sarah@example.com this week"
```

### 按主题关键词搜索邮件
```bash
python3 agent.py "find emails about quarterly budget"
```

### 阅读特定邮件
```bash
python3 agent.py "read email with id MESSAGE_ID_HERE"
```

### 创建回复草稿
```bash
python3 agent.py "draft a reply to the last email from John saying I will review by Friday"
```

## 每个操作的内部处理流程

| 用户请求 | Composio调用的操作 | 结果 |
|---|---|---|
| 查看收件箱 | GMAIL_FETCH_EMAILS | 返回最近N封包含发件人、主题和日期的邮件 |
| 查找邮件 | GMAIL_SEARCH_MESSAGES | 返回匹配的邮件线程 |
| 阅读邮件 | GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID | 返回完整的邮件内容 |
| 创建回复草稿 | GMAIL_CREATE_EMAIL_DRAFT | 创建草稿，确认已保存但不会发送 |
| 查看用户信息 | GMAIL_GET_PROFILE | 返回已认证的电子邮件地址 |

## 被禁止的操作（Composio在网关阶段会拒绝这些操作）

以下操作不在允许的列表中，即使代理程序因误解或指令模糊而尝试执行，也会被立即拒绝：

- GMAIL_SEND_EMAIL
- GMAIL_DELETE_MESSAGE
- GMAIL_MODIFY_LABELS
- GMAIL_EMPTY_TRASH

如果用户请求发送或删除邮件，请回复：
“此技能仅支持读取和创建草稿功能。如需发送邮件，请在Gmail中查看草稿并自行发送，或安装需要人工审核的发送技能。”

## 输出格式

代理程序返回JSON格式的数据。解析并展示如下：

- 对于邮件列表：
```
📬 Found 5 emails:
1. From: sarah@co.com | Subject: Q4 Budget | Date: Mar 1
2. From: mike@co.com  | Subject: Meeting Notes | Date: Feb 28
...
```

- 对于草稿：
```
✅ Draft saved (not sent):
To: john@example.com
Subject: Re: Project Update
Preview: "Hi John, I'll review this by Friday..."
Review it at: mail.google.com/mail/#drafts
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|---|---|---|
| `COMPOSIO_API_KEY未找到` | .env文件中缺少密钥 | 将密钥添加到.env文件中 |
| “Gmail未连接” | OAuth认证未完成 | 访问app.composio.dev → 确保Gmail已连接 |
| 令牌过期 | 需要刷新令牌 | 在Composio控制台中重新连接Gmail |
| 操作不被允许 | 尝试了被禁止的操作 | 通知用户此技能仅支持读取和创建草稿 |
| 超过请求频率限制 | 请求过多 | 等待60秒后重试 |

## 安全架构

该技能采用Composio的代理认证模型：

1. 用户通过app.composio.dev使用OAuth连接到Gmail
2. Composio将access_token和refresh_token存储在加密的保管库中
3. OpenClaw仅接收connected_account_id作为识别信息
4. 所有API调用流程为：OpenClaw → Composio → Gmail
5. 原始凭证永远不会进入代理程序的内存或本地文件系统
6. 每次调用都会在Composio控制台中记录时间戳和操作内容
7. 可通过Composio控制台随时取消权限

这种架构可以防范三种攻击方式：
- 通过提示注入窃取.env文件中的凭证（令牌不在本地存储）
- 通过上下文窗口泄露OAuth令牌（令牌不会存储在内存中）
- 恶意技能尝试读取凭证文件（由于没有凭证可读）

## 审查代理程序的日志

运行技能后，请查看app.composio.dev上的日志：
- 每次Gmail操作的具体时间戳
- 调用了哪些操作（获取、搜索、创建草稿）
- 操作是否成功或被拒绝
- 没有任何操作会被遗漏记录

---
name: secure-gmail
description: 使用Composio的认证机制来读取邮件、搜索收件箱和创建草稿。适用于用户请求查看邮件、阅读邮件、搜索收件箱或创建回复草稿的场景。该技能不允许发送或删除邮件（遵循最小权限原则）。
metadata:
  moltbot:
    requires:
      bins: ["python3"]
      env: ["COMPOSIO_API_KEY"]
---

# 安全Gmail技能

通过Composio的代理认证机制访问Gmail。
代理程序永远不会接触到您的原始OAuth令牌。