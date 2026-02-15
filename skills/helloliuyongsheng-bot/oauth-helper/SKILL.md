---
name: oauth-helper
description: |
  Automate OAuth login flows with user confirmation via Telegram.
  Supports 7 providers: Google, Apple, Microsoft, GitHub, Discord, WeChat, QQ.
  
  Features:
  - Auto-detect available OAuth options on login pages
  - Ask user to choose via Telegram when multiple options exist
  - Confirm before authorizing
  - Handle account selection and consent pages automatically
---

# OAuth辅助工具

该工具支持通过Telegram进行OAuth登录自动化处理，目前支持7种主要的OAuth提供商。

## 支持的提供商

| 提供商 | 状态 | 检测域名 |
|----------|--------|------------------|
| Google | ✅ | accounts.google.com |
| Apple | ✅ | appleid.apple.com |
| Microsoft | ✅ | login.microsoftonline.com, login.live.com |
| GitHub | ✅ | github.com/login/oauth |
| Discord | ✅ | discord.com/oauth2 |
| WeChat | ✅ | open.weixin.qq.com |
| QQ | ✅ | graph.qq.com |

## 先决条件

1. 已在Clawd浏览器中登录相应的OAuth提供商（需完成一次设置）。
2. 已配置Telegram频道。

## 核心工作流程

### 流程A：包含多种OAuth选项的登录页面

当用户请求登录网站时：

```
1. Open website login page
2. Scan page for available OAuth buttons
3. Send Telegram message:
   "🔐 [Site] supports these login methods:
    1️⃣ Google
    2️⃣ Apple  
    3️⃣ GitHub
    Reply with number to choose"
4. Wait for user reply (60s timeout)
5. Click the selected OAuth button
6. Enter Flow B
```

### 流程B：OAuth授权页面

当用户进入OAuth提供商的页面时：

```
1. Detect OAuth page type (by URL)
2. Extract target site info
3. Send Telegram: "🔐 [Site] requests [Provider] login. Confirm? Reply yes"
4. Wait for "yes" (60s timeout)
5. Execute provider-specific click sequence
6. Wait for redirect back to original site
7. Send: "✅ Login successful!"
```

## 检测规则

### Google
```
URL patterns:
- accounts.google.com/o/oauth2
- accounts.google.com/signin/oauth
- accounts.google.com/v3/signin
```

### Apple
```
URL patterns:
- appleid.apple.com/auth/authorize
- appleid.apple.com/auth/oauth2
```

### Microsoft
```
URL patterns:
- login.microsoftonline.com/common/oauth2
- login.microsoftonline.com/consumers
- login.live.com/oauth20
```

### GitHub
```
URL patterns:
- github.com/login/oauth/authorize
- github.com/login
- github.com/sessions/two-factor
```

### Discord
```
URL patterns:
- discord.com/oauth2/authorize
- discord.com/login
- discord.com/api/oauth2
```

### WeChat
```
URL patterns:
- open.weixin.qq.com/connect/qrconnect
- open.weixin.qq.com/connect/oauth2
```

### QQ
```
URL patterns:
- graph.qq.com/oauth2.0/authorize
- ssl.xui.ptlogin2.qq.com
- ui.ptlogin2.qq.com
```

## 不同提供商的点击顺序

### Google
```
Account selector: [data-identifier], .JDAKTe
Auth buttons: button:has-text("Allow"), button:has-text("Continue")
```

### Apple
```
Email input: input[type="email"], #account_name_text_field
Password: input[type="password"], #password_text_field  
Continue: button#sign-in, button:has-text("Continue")
Trust device: button:has-text("Trust")
```

### Microsoft
```
Account selector: .table-row[data-test-id]
Email input: input[name="loginfmt"]
Password: input[name="passwd"]
Next: button#idSIButton9
Accept: button#idBtn_Accept
```

### GitHub
```
Email: input#login_field
Password: input#password
Sign in: input[type="submit"]
Authorize: button[name="authorize"]
2FA: input#app_totp
```

### Discord
```
Email: input[name="email"]
Password: input[name="password"]
Login: button[type="submit"]
Authorize: button:has-text("Authorize")
```

### WeChat
```
Method: QR code scan
- Screenshot QR code to user
- Wait for mobile scan confirmation
- Detect page redirect
```

### QQ
```
Method: QR code or password login
QR: Screenshot to user
Password mode:
  - Switch: a:has-text("密码登录")
  - Username: input#u
  - Password: input#p
  - Login: input#login_button
```

## OAuth按钮的识别方法

在登录页面中查找以下元素：

| 提供商 | 识别元素 | 常见文本 |
|----------|-----------|-------------|
| Google | `[data-provider="google"]`, `.google-btn` | “使用Google登录” |
| Apple | `[data-provider="apple"]`, `.apple-btn` | “使用Apple登录” |
| Microsoft | `[data-provider="microsoft"]` | “使用Microsoft登录” |
| GitHub | `[data-provider="github"]` | “使用GitHub登录” |
| Discord | `[data-provider="discord"]` | “使用Discord登录” |
| WeChat | `.wechat-btn`, `img[src*="wechat"]` | “微信登录” |
| QQ | `.qq-btn`, `img[src*="qq"]` | “QQ登录” |

## 一次设置流程

在Clawd浏览器中登录每个提供商：

```bash
# Google
browser action=navigate profile=clawd url=https://accounts.google.com

# Apple
browser action=navigate profile=clawd url=https://appleid.apple.com

# Microsoft  
browser action=navigate profile=clawd url=https://login.live.com

# GitHub
browser action=navigate profile=clawd url=https://github.com/login

# Discord
browser action=navigate profile=clawd url=https://discord.com/login

# WeChat/QQ - Use QR scan, no pre-login needed
```

## 错误处理

- 如果用户没有给出“同意”回复 → 取消操作并通知用户。
- 如果需要两步验证（2FA） → 提示用户手动输入验证码。
- 如果二维码无法识别 → 重新扫描二维码。
- 如果登录失败 → 生成截图并发送给用户以协助调试。

## 使用示例

```
User: Login to Kaggle for me

Agent:
1. Navigate to kaggle.com/account/login
2. Detect Google/Facebook/Yahoo options
3. Send: "🔐 Kaggle supports:
   1️⃣ Google
   2️⃣ Facebook
   3️⃣ Yahoo
   Reply number to choose"
4. User replies: 1
5. Click Google login
6. Detect Google OAuth page
7. Send: "🔐 Kaggle requests Google login. Confirm? Reply yes"
8. User replies: yes
9. Select account, click Continue
10. Send: "✅ Logged into Kaggle!"
```

## 版本历史

- v1.0.0 - 首次发布，支持7种OAuth提供商。