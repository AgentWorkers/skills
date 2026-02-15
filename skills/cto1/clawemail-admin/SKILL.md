---
name: claw-admin
description: "配置和管理 @clawemail.com 的 Google Workspace 邮箱账户。当用户需要为他们的 AI 代理创建邮箱、检查邮箱是否可用或管理现有的 ClawEmail 账户时，请使用此功能。"
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["CLAWEMAIL_API_KEY"]},"primaryEnv":"CLAWEMAIL_API_KEY","emoji":"🦞"}}
---

# ClawEmail

用于为AI代理提供并管理**@clawemail.com**的Google Workspace电子邮件账户。每个账户都具备Gmail、Docs、Sheets、Calendar和Drive的完整访问权限，同时提供用于程序化操作的OAuth凭证。

## 设置

将您的API密钥设置为环境变量：

```
export CLAWEMAIL_API_KEY=your_api_key_here
```

**基础URL：** `https://clawemail.com`

所有管理员端点都需要添加以下头部信息：`-H "X-API-Key: $CLAWEMAIL_API_KEY"`

## 检查电子邮件地址的可用性（公开查询——无需API密钥）

在创建账户之前，请务必先检查所需的前缀是否可用：

```bash
curl -s https://clawemail.com/check/DESIRED_PREFIX
```

**可用时的响应：**
```json
{"prefix":"tom","email":"tom@clawemail.com","available":true}
```

**已被占用或预留时的响应：**
```json
{"available":false,"errors":["This email is reserved"]}
```

## 创建电子邮件账户

创建一个新的@clawemail.com Google Workspace用户账户。系统会返回一个临时密码以及一个用于OAuth连接的URL。

```bash
curl -s -X POST https://clawemail.com/api/emails \
  -H "X-API-Key: $CLAWEMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prefix":"DESIRED_PREFIX"}'
```

**响应：**
```json
{
  "success": true,
  "email": "tom@clawemail.com",
  "password": "aB3$xYz...",
  "connect_url": "https://clawemail.com/connect/tom",
  "instructions": "1. User logs into Gmail with the email/password above. 2. User visits connect_url to authorize OAuth. 3. User receives their OpenClaw credentials."
}
```

**重要提示：** 请立即保存密码——该密码仅显示一次。

创建账户后，用户需要：
1. 使用新邮箱和密码登录Gmail（网址：https://mail.google.com）
2. 访问`connect_url`以完成OAuth授权并获取他们的认证信息（JSON格式）。

## 列出所有电子邮件地址

```bash
curl -s https://clawemail.com/api/emails \
  -H "X-API-Key: $CLAWEMAIL_API_KEY"
```

支持分页查询，格式为`?limit=100&offset=0`。

## 获取电子邮件详细信息

```bash
curl -s https://clawemail.com/api/emails/PREFIX \
  -H "X-API-Key: $CLAWEMAIL_API_KEY"
```

返回电子邮件的状态、创建日期、OAuth连接日期以及Workspace用户的详细信息。

## 暂停电子邮件账户

暂时禁用Google Workspace账户（数据保持不变）：

```bash
curl -s -X POST https://clawemail.com/api/emails/PREFIX/suspend \
  -H "X-API-Key: $CLAWEMAIL_API_KEY"
```

## 恢复电子邮件账户

重新启用之前被暂停的账户：

```bash
curl -s -X POST https://clawemail.com/api/emails/PREFIX/unsuspend \
  -H "X-API-Key: $CLAWEMAIL_API_KEY"
```

## 删除电子邮件账户

永久删除Google Workspace账户及其所有关联数据：

```bash
curl -s -X DELETE https://clawemail.com/api/emails/PREFIX \
  -H "X-API-Key: $CLAWEMAIL_API_KEY"
```

## 自助注册（无需API密钥）

对于希望通过Stripe支付系统自行注册的用户：
1. 将他们引导至：`https://clawemail.com/signup?prefix=DESIRED_PREFIX`
2. 用户可以选择月度（16美元/月）或年度（160美元/年）订阅计划，输入账单邮箱地址，然后通过Stripe完成支付
3. 支付完成后，用户将收到密码和OAuth连接链接。

## 典型工作流程：
1. **检查可用性：** `curl -s https://clawemail.com/check/myagent`
2. **创建账户：** 向`/api/emails`发送POST请求，并提供所需的前缀
3. **保存凭证：** 安全地存储密码
4. **完成OAuth授权：** 将用户引导至响应中提供的`connect_url`
5. **使用账户：** 代理现在拥有了一个具有完整Google Workspace访问权限的Gmail地址。

## 前缀规则：
- 前缀长度必须在3到30个字符之间
- 必须以字母开头
- 可以包含字母、数字、点（.）、下划线（_）或连字符（-）
- 许多常见的名称、品牌和词汇已被预留。

## 使用场景：
- 用户需要为他们的AI代理创建电子邮件账户
- 用户需要一个具有OAuth访问权限的Google Workspace账户
- 用户想要检查特定电子邮件地址是否可用
- 用户需要管理（暂停/恢复/删除）现有账户