---
name: identitygram-signin
description: 通过调用 `/auth/signin` 端点来登录 IdentityGram。
---

# IdentityGram 登录

使用身份验证端点登录 IdentityGram。

该技能通过向 `https://gateway-v2.identitygram.co.uk/auth/signin` 发送凭据来验证用户身份。

## 使用方法

当需要使用 IdentityGram 凭据验证用户身份时，请使用此技能。

## 配置

该技能需要以下参数：
- `email`：用户的电子邮件地址
- `password`：用户的密码

这些参数可以通过 OpenClaw 的技能调用系统提供。

## 响应

该技能返回一个 JSON 响应，其中包含：
- `raw`：来自 IdentityGram API 的完整响应
- `success`：布尔值，表示验证是否成功（如果可用）
- `token`：认证令牌（如果可用）
- `accessToken`：访问令牌（如果可用）
- `refreshToken`：刷新令牌（如果可用）
- `user`：用户信息（如果可用）
- `message`：状态消息（如果可用）

## 工作原理

1. 向 `https://gateway-v2.identitygram.co.uk/auth/signin` 发送 POST 请求
2. 在请求体中以 JSON 格式包含电子邮件地址和密码
3. 返回包含令牌和用户信息的认证响应

## 故障排除

**认证失败：**
- 确认电子邮件地址和密码正确
- 确保 IdentityGram 端点可访问

**连接错误：**
- 确认端点 URL 正确
- 检查网络连接
- 确保 IdentityGram 服务正在运行