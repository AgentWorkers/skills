---
name: browserbase-auth
description: 使用 stagehand CLI 指导 Claude 完成交互式身份验证流程
---

# 认证技能

使用 `stagehand` CLI 指导 Claude 完成交互式认证流程。

## 使用场景

在以下情况下使用此技能：
- 网站需要登录才能访问内容
- 遇到登录页面或认证障碍
- 用户需要认证才能完成任务
- 会话 cookie 已过期

## 认证流程

### 1. 检测登录页面

导航到某个 URL 后，判断是否需要认证：

```bash
stagehand snapshot
```

查找以下提示：
- 类型为 `type="password"` 或 `type="email"` 的表单元素
- 包含 “sign in”（登录）、“log in”（登录）、“username”（用户名）、“password”（密码）等文字的元素
- OAuth 按钮（如 Google、GitHub、Microsoft 等）

### 2. 请求用户提供凭证

**务必请求用户提供凭证——切勿自行猜测或存储用户的凭证。**

示例提示：
```
I've detected a login page. To continue, I'll need your credentials:

1. What is your email/username?
2. What is your password?

Note: Your credentials will only be used to fill the login form and won't be stored.
```

### 3. 填写登录表单

使用快照引用（snapshot refs）来识别表单字段：

```bash
# Get the current page state
stagehand snapshot

# Fill the email/username field
stagehand fill @0-5 "user@example.com"

# Fill the password field  
stagehand fill @0-8 "their-password"

# Click the submit button
stagehand click @0-12
```

### 4. 处理双重身份验证（2FA/MFA）

如果登录后出现双重身份验证（2FA）提示：

```bash
stagehand snapshot
```

提示用户：
```
Two-factor authentication is required. Please provide:
- The code from your authenticator app, OR
- The code sent to your phone/email

What is your 2FA code?
```

然后填写并提交凭证：
```bash
stagehand fill @0-3 "123456"
stagehand click @0-5
```

### 5. 验证登录是否成功

提交凭证后：

```bash
stagehand wait networkidle
stagehand snapshot
```

检查以下情况：
- 是否已从登录页面跳转到其他页面
- 是否显示了用户个人资料/头像
- 是否显示了仪表板或首页内容
- 是否没有错误信息

如果登录失败：
```
The login attempt was unsuccessful. I see an error message: "[error text]"

Would you like to:
1. Try again with different credentials
2. Use a different login method (OAuth, SSO)
3. Reset your password
```

## OAuth/单点登录（SSO）流程

对于 OAuth 按钮（如 Google、GitHub 等）：
1. 点击 OAuth 按钮
2. 将出现弹窗或页面重定向
3. 用户在 OAuth 提供商处完成认证
4. 等待系统重定向回原始网站

```bash
# Click OAuth button
stagehand click @0-15

# Wait for OAuth flow to complete
stagehand wait networkidle

# Verify authentication succeeded
stagehand snapshot
```

## 常见认证方式

### 用户名 + 密码表单
```html
<form>
  <input type="email" name="email">
  <input type="password" name="password">
  <button type="submit">Sign In</button>
</form>
```

### 魔法链接（Magic Link）/ 无密码登录
```
I see this site uses passwordless authentication (magic link).

1. Enter your email address
2. Check your email for the login link
3. Let me know when you've clicked the link

What email should I use?
```

### 图形验证码（CAPTCHA）
```
This login page has a CAPTCHA. I cannot solve CAPTCHAs automatically.

Options:
1. Use `stagehand session live` to open the browser and solve it manually
2. Try a different authentication method
3. Contact the site administrator
```

## 安全提示

- **切勿存储或记录用户的凭证**
- 凭证仅用于填充表单字段
- 建议用户使用密码管理工具
- 如果支持双重身份验证，请建议用户启用该功能
- 使用后及时清除对话记录中的敏感信息

## 故障排除

### 登录按钮无法使用
```bash
# Try waiting for page to be fully loaded
stagehand wait networkidle

# Check if button is actually clickable
stagehand snapshot

# Try clicking by coordinates if ref doesn't work
stagehand click 450,320
```

### 无法找到表单字段
```bash
# Get full snapshot to find correct refs
stagehand snapshot

# Try using evaluate to find elements
stagehand eval "document.querySelector('input[type=password]')?.id"
```

### 会话过期过快
- 一些网站的会话超时时间较短
- 可以考虑使用 `stagehand session create` 与 Browserbase 结合来实现持久化会话
- 检查是否提供了 “记住我”（Remember me）选项