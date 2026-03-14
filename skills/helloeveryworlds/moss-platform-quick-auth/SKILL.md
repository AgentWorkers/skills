---
name: moss-platform-quick-auth
description: 通过 Quick Auth 终端处理 Moss 平台的认证，并返回可用的凭据。当用户提供电子邮件地址并请求注册/登录、接收验证码、完成基于代码的认证，或使用 API（api-register/api-login）获取 access_token/refresh_token/api_key 时，应使用此方法。
---
# Moss平台快速认证（Quick Auth）

执行认证操作的URL为：  
- 基本URL：`https://<host>/studio-api/v1/auth/quick/*`  

请通过shell使用`curl`命令来发起API请求。  

## 需要收集的输入信息  
在调用API端点之前，需要收集以下信息：  
- `host`（示例：`sotatts.online`）  
- `email`  
- 可选：`code`（用于基于代码的认证流程）  
- 可选：用户操作意图（`new user` / `existing user` / `auto`）  

## 认证流程A：基于代码的快速认证  
### 第1步：发送验证码  
```bash
curl -sS -X POST "https://<host>/studio-api/v1/auth/quick/send-code" \
  -H 'Content-Type: application/json' \
  --data '{"email":"<email>"}'
```  

预期的成功响应字段包括：  
- `message`  
- `expires_in`  
- `cooldown_in`  

如果返回`IN_COOLDOWN`，请等待指定的冷却时间后再重试。  

### 第2步：登录或注册  
当用户状态未知时，优先尝试访问`/quick/login`；  
如果用户不存在（`USER_NOT_EXIST`），则调用`/quick/register`：  
- **登录操作**：  
```bash
curl -sS -X POST "https://<host>/studio-api/v1/auth/quick/login" \
  -H 'Content-Type: application/json' \
  --data '{"email":"<email>","code":"<code>"}'
```  
- **注册操作**：  
```bash
curl -sS -X POST "https://<host>/studio-api/v1/auth/quick/register" \
  -H 'Content-Type: application/json' \
  --data '{"email":"<email>","code":"<code>"}'
```  

注册成功后，立即保存用户临时密码（`temp_password`，该密码仅会在注册时返回一次）。  

## 认证流程B：无需验证码的API认证  
适用于服务器间通信或用户主动选择的无需交互的登录方式。  
**首先尝试登录**：  
```bash
curl -sS -X POST "https://<host>/studio-api/v1/auth/quick/api-login" \
  -H 'Content-Type: application/json' \
  --data '{"email":"<email>"}'
```  
如果用户不存在（`USER_NOT_EXIST`），则调用注册接口：  
```bash
curl -sS -X POST "https://<host>/studio-api/v1/auth/quick/api-register" \
  -H 'Content-Type: application/json' \
  --data '{"email":"<email>"}'
```  

预期的响应字段包括：  
- `user_id`  
- `access_token`  
- `refresh_token`  
- `expires_in`  
- `api_key`（必须包含）  
- `temp_password`（仅用于注册，保存一次）  

## 返回给用户的响应信息  
返回给用户的详细信息包括：  
- 使用的API端点  
- 认证结果状态（`login success` / `register success` / `error code`）  
- `user_id`  
- `expires_in`  
- 凭据信息（`access_token`、`refresh_token`、`api_key`、`temp_password`，如果存在的话）  

如果基于令牌的认证接口出现意外错误（例如在认证成功后返回`UNAUTHORIZED`），应将其视为后端异常，并记录相关端点和响应内容以协助调试。  

## 错误处理规则：  
- `USER_NOT_EXIST` → 切换到登录流程  
- `EMAIL_EXISTS` → 切换到注册流程  
- `INVALID_CODE` → 要求用户重新输入正确的验证码  
- `CODE_EXPIRED` / `CODE_NOT_FOUND` → 重新发送验证码后重试  
- `IN_COOLDOWN` → 等待指定的冷却时间（`cooldown_in`秒）  
- `ACCOUNT_BANNED` → 停止操作并通知用户  

## 安全性与用户体验规则：  
- 未经明确授权，严禁访问用户的邮箱。  
- 默认情况下，应屏蔽凭据信息；除非用户明确要求显示原始数据。  
- 提醒用户：`temp_password`仅为一次性使用的临时密码，必须妥善保存。  
- 尽可能确保API请求具有幂等性（idempotent），避免不必要的重复请求。