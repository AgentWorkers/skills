---
name: Account & Authentication
description: 账户注册、通过电子邮件/一次性密码（OTP）/钱包/生物识别方式登录、令牌刷新、密码重置以及会话管理。
version: 1.0.0
---
# 账户与身份验证

当用户需要注册、登录、管理会话、重置密码或关联 Web3 钱包时，请使用此技能。

## 可用工具

- `send_otp` — 向电子邮件地址发送一次性密码 | `POST /api/v1/auth/otp/send`
- `verify_otp` — 验证一次性密码并接收验证令牌 | `POST /api/v1/auth/otp/verify`
- `otp_rate_limit_status` — 检查当前会话的 OTP 使用频率限制状态 | `GET /api/v1/auth/otp/status`
- `signup` — 使用电子邮件、密码和 OTP 验证令牌创建新账户 | `POST /api/v1/auth/signup`
- `login` — 使用电子邮件和密码登录 | `POST /api/v1/auth/login`
- `login_with_wallet` — 通过 Web3 钱包生成随机数（nonce）进行登录 | `POST /api/v1/auth/wallet`
- `get_wallet_nonce` — 获取用于基于钱包登录的随机数（nonce） | `GET /api/v1/auth/wallet/nonce`
- `biometric_login` — 使用生物特征凭证登录 | `POST /api/v1/auth/biometric`
- `refresh_token` — 使用刷新令牌（refresh_token）刷新过期的访问令牌 | `POST /api/v1/auth/refresh`
- `reset_password` — 使用 OTP 验证重置账户密码 | `POST /api/v1/auth/reset-password`
- `unlock_account` — 解锁被锁定的账户 | `POST /api/v1/auth/unlock`
- `get_account` — 获取当前账户信息 | `GET /api/v1/account` | 需要身份验证
- `update_password` — 更改账户密码 | `PUT /api/v1/account/password` | 需要身份验证
- `link_wallet` — 将 Web3 钱包关联到账户 | `PUT /api/v1/account/wallet` | 需要身份验证
- `unlink_wallet` — 删除关联的 Web3 钱包 | `DELETE /api/v1/account/wallet` | 需要身份验证
- `logout` — 登出当前会话 | `POST /api/v1/account/logout` | 需要身份验证
- `logout_all` — 从所有会话中登出 | `POST /api/v1/account/logout-all` | 需要身份验证

## 推荐流程

### 注册

通过电子邮件和 OTP 创建新账户

1. 发送 OTP：`POST /api/v1/auth/otp/send`，参数包含 `{email, type: "signup"}`
2. 验证 OTP：`POST /api/v1/auth/otp/verify`，参数包含 `{email, code, type: "signup"}` — 返回验证令牌（verification_token）
3. 注册：`POST /api/v1/auth/signup`，参数包含 `{email, password, verification_token}`

### 登录

进行身份验证并获取访问令牌/刷新令牌

1. 登录：`POST /api/v1/auth/login`，参数包含 `{email, password}` — 返回访问令牌（access_token）和刷新令牌（refresh_token）
2. 在所有需要身份验证的请求中，将 `access_token` 作为 `Authorization` 头部的Bearer 令牌使用
3. 当访问令牌过期时，使用 `refresh_token` 进行刷新：`POST /api/v1/auth/refresh`，参数包含 `{refresh_token}`

## 规则

- 注册和重置密码时必须使用 OTP — 必须先发送 OTP 再进行验证
- 访问令牌在 1 小时后过期 — 使用 `refresh_token` 获取新的令牌
- 如果连续 5 次登录失败，账户将被锁定 — 使用 `/auth/unlock` 功能解锁账户
- 绝不要存储或记录密码 — 只允许密码临时使用

## 代理操作指南

执行此技能时请遵循以下说明：

- 始终按照文档中规定的流程顺序操作，不要跳过任何步骤。
- 如果某个工具需要身份验证，请确保当前会话拥有有效的Bearer 令牌。
- 如果某个工具需要交易 PIN 码，请每次都向用户索取新的 PIN 码，切勿缓存或记录 PIN 码。
- 绝不要泄露、记录或永久保存任何敏感信息（如密码、令牌、完整的卡号或 CVV 码）。
- 如果用户请求超出此技能范围的操作，请拒绝请求并推荐相应的技能。
- 如果某一步骤失败，请检查错误信息，并按照下面的恢复指南进行操作后再重试。

- 注册新用户时：首先调用 `send_otp`，然后 `verify_otp`，最后 `signup`。切勿跳过 OTP 验证步骤。
- 重置密码时：首先使用 `send_otp` 并设置 `type` 为 "forget_password"，然后 `verify_otp`，最后使用验证令牌调用 `reset_password`。
- 所有需要身份验证的接口都需要使用通过 `login` 或 `login_with_wallet` 获得的Bearer 令牌。
- 当访问令牌过期（有效期为 1 小时）时，使用 `refresh_token` 进行刷新。无需让用户再次登录。
- 绝不要记录或存储用户的密码。
- 如果连续 5 次登录失败，账户将被锁定。要解锁账户，请先调用 `send_otp` 并设置 `type` 为 "account_unlock"，然后 `verify_otp`，最后使用验证令牌调用 `unlock_account`。