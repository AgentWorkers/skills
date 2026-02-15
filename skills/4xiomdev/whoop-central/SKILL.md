---
name: whoop
description: **WHOOP Central - OAuth集成及用于获取WHOOP数据的脚本（包括睡眠、恢复状态、身体压力及锻炼数据）**  
当用户询问自己的睡眠状况、恢复评分、心率变异性（HRV）、身体压力或锻炼数据时，可使用该工具。  

**功能说明：**  
- **OAuth集成**：支持使用OAuth协议进行安全登录，确保用户数据的安全性。  
- **数据获取脚本**：内置脚本用于从WHOOP设备获取以下数据：  
  - 睡眠质量（sleep）  
  - 恢复状态（recovery）  
  - 身体压力（strain）  
  - 锻炼记录（workouts）  

**使用场景：**  
- 用户界面：通过WHOOP Central的Web界面或移动应用程序，用户可以方便地查看和查询这些数据。  
- 数据分析：开发人员可以利用这些数据为用户提供个性化的健康建议或训练计划。  

**注意事项：**  
- 请确保已正确配置WHOOP设备的API密钥和OAuth认证信息。  
- 该工具适用于支持WHOOP设备数据导出的所有平台（如Web界面、移动应用程序等）。
version: 1.0.2
metadata:
  clawdbot:
    emoji: "🏋️"
    requires:
      bins: ["node", "openssl"]
---

# WHOOP Central

通过v2 API访问WHOOP的睡眠、恢复、压力和锻炼数据。

## 快速命令

```bash
# 1) One-time setup (writes ~/.clawdbot/whoop/credentials.json)
node src/setup.js

# 2) Recommended: Get tokens via Postman (see Auth section), then verify
node src/verify.js
node src/verify.js --refresh

# Prompt-friendly snapshot (includes last workout)
node src/today.js

# Daily summary (all metrics)
node src/summary.js

# Individual metrics
node src/recovery.js
node src/sleep.js
node src/strain.js
node src/workouts.js

# Bulk import to ~/clawd/health/logs/whoop/*
node src/import-historical.js
```

## 可用的数据

| 指标 | 数据点 |
|--------|-------------|
| **恢复** | 评分（0-100%）、心率变异性（HRV）、静息心率、血氧饱和度（SpO2）、皮肤温度 |
| **睡眠** | 睡眠时长、睡眠阶段（REM/深度/浅度）、睡眠效率、睡眠质量 |
| **压力** | 每日压力水平（0-21）、消耗的卡路里、平均/最高心率 |
| **锻炼** | 锻炼类型、锻炼时长、锻炼强度、消耗的卡路里、心率 |

## 恢复评分指南

- 💚 **67-100%** 绿色 - 可以正常工作 |
- 💛 **34-66%** 黄色 - 需要适当休息 |
- ❤️ **0-33%** 红色 - 需要重点恢复 |

## 设置

### 0. 系统要求

- Node.js 18及以上版本（此仓库使用ESM）
- `openssl`（仅在通过`https://localhost`使用`auth.js`时需要；Postman认证不需要）

### 1. 创建WHOOP开发者应用

1. 访问 https://developer.whoop.com/
2. 用您的WHOOP账户登录
3. 创建一个新的应用
4. 添加以下重定向URL（必须完全匹配，不要在末尾添加斜杠）：
   - Postman浏览器回调（推荐认证路径）：
     ```
     https://oauth.pstmn.io/v1/browser-callback
     ```
   - 可选的本地回调（仅由`auth.js`使用）：
     ```
     https://localhost:3000/callback
     ```
   您可以同时注册这两个回调。
5. 复制客户端ID（Client ID）和客户端密钥（Client Secret）。

团队说明：此技能不会发送任何客户端凭据。每个用户都可以创建自己的WHOOP应用，或者（如果彼此信任的话），团队可以共享一个应用的`client_id`/`client_secret`，并让多个WHOOP账户使用该应用进行认证。

### 2. 保存凭据（推荐方式：交互式）

运行：
```bash
node src/setup.js
```
这会将凭据保存到`~/.clawdbot/whoop/credentials.json`文件中（如果需要，也可以保存到`token.json`文件中）。

### 3. 进行认证（推荐方式：使用Postman）

Postman是许多账户认证的首选方式，因为WHOOP可能会阻止类似浏览器的请求访问OAuth端点（或者根据请求头部的信息有不同的行为）。

Postman设置步骤（请务必完成）：
- WHOOP仪表板上的重定向URL包括：
  - `https://oauth.pstmn.io/v1/browser-callback`
- Postman OAuth设置：
  - 选择`offline`权限范围（否则无法获取`refresh_token`）
  - 客户端认证方式设置为“在请求体中发送客户端凭据”（`client_secret_post`）

1) 在WHOOP仪表板中，确保您已注册Postman回调URL：
```text
https://oauth.pstmn.io/v1/browser-callback
```

2) 在Postman中：
- 创建一个环境并设置变量：
  - `ClientId` = 您的WHOOP客户端ID
  - `ClientSecret` = 您的WHOOP客户端密钥
- 打开WHOOP API集合（或任何请求），然后打开“授权”（Authorization）选项卡：
  - 选择认证类型：OAuth 2.0
  - 将认证信息添加到“请求头”（Request Headers）中
  - 选择授权方式：授权码（Authorization Code）
  - 回调URL：选择“使用浏览器进行授权”（Authorize using browser）
  - 认证URL：
    ```
    https://api.prod.whoop.com/oauth/oauth2/auth
    ```
  - 访问令牌URL：
    ```
    https://api.prod.whoop.com/oauth/oauth2/token
    ```
  - 客户端ID：`{{ClientId}}`
  - 客户端密钥：`{{ClientSecret}}`
  - 权限范围（用空格分隔）：包括`offline`以及您需要的其他读取权限范围，例如：
    ```
    offline read:profile read:sleep read:recovery read:workout read:cycles read:body_measurement
    ```
  - 状态码：至少8个字符（例如`loomingState`
  - 客户端认证方式：选择“在请求体中发送客户端凭据”

3) 点击“获取新访问令牌”（Get New Access Token），登录WHOOP，然后点击“授权”（Grant）。

4) 在Postman的“管理访问令牌”（Manage Access Tokens）窗口中：
- 点击“使用令牌”（Use Token），以便请求能够正常发送
- 重要提示：请复制并保存以下两个令牌：
  - `access_token`
  - `refresh_token`
  注意：Postman通常不会自动保存`refresh_token`。

5) 将令牌保存到`~/.clawdbot/whoop/token.json`文件中：
- 使用`token.example.json`作为模板
  - 设置：
    - `obtained_at`为当前时间（以毫秒为单位）
    - `redirect_uri`为：
    ```
    https://oauth.pstmn.io/v1/browser-callback
    ```

6) 验证令牌是否有效（并测试刷新功能）：
```bash
node src/verify.js
node src/verify.js --refresh
```

### 4. 可选：通过`auth.js`进行认证（某些账户可能无法使用）

如果您希望完全在本地完成OAuth认证流程（且WHOOP允许的话），可以使用`auth.js`。

**前提条件**：在WHOOP仪表板中添加以下重定向URL：
```text
https://localhost:3000/callback
```

运行：
```bash
WHOOP_REDIRECT_URI='https://localhost:3000/callback' node src/auth.js
```

如果您需要在手机或远程设备上进行认证：
```bash
WHOOP_REDIRECT_URI='https://localhost:3000/callback' node src/auth.js --manual
```

注意：对于使用`https://localhost`的情况，脚本会生成一个自签名证书，您的浏览器可能会显示TLS警告。请忽略警告并继续操作，以便完成重定向。

### 4. 验证功能是否正常

```bash
node src/verify.js
node src/summary.js
```

## 故障排除

### 浏览器在登录页面前显示“NotAuthorizedException”

这是WHOOP方面对尝试访问`api.prod.whoop.com` OAuth端点的浏览器用户代理（User-Agent）的限制。

- 使用更新后的`node src/auth.js`脚本，该脚本会自动处理登录流程，并将浏览器直接重定向到`id.whoop.com`。
- 如果问题仍然存在，尝试运行`node src/auth.js --manual`，然后打开生成的URL。

### “redirect_uri未被允许”

1. 访问 https://developer.whoop.com/
2. 编辑您的应用设置
3. 确保您的应用配置中包含以下URL：
   ```
   https://oauth.pstmn.io/v1/browser-callback
   ```
   如果您在本地使用`auth.js`，还需要添加以下配置：
   ```
   https://localhost:3000/callback
   ```
4. 保存设置后再次尝试。

### 令牌过期

令牌会自动刷新（无需手动设置定时任务）。如果问题仍然存在：
```bash
rm ~/.clawdbot/whoop/token.json
node src/auth.js
```

### “Authorization was not valid”

这通常表示您的访问令牌已过期或无效（尤其是在您在其他地方重新认证或刷新令牌后）。解决方法：
- 重新运行`node src/auth.js`脚本，
- 或者将Postman中的最新`access_token`和`refresh_token`复制到`~/.clawdbot/whoop/token.json`文件中，并更新`obtained_at`字段。

### 通过手机/远程设备进行认证

使用手动认证模式：
```bash
node src/auth.js --manual
```
在任何设备上打开相应的URL，完成认证后，复制回调URL中的代码。

### 出现“error=request_forbidden”或“The request is not allowed”错误

这可能是WHOOP在登录/授权后拒绝了请求。常见原因包括：
- 重定向URL策略（WHOOP文档中仅允许使用`https://`或`whoop://`作为重定向URL）
- 应用/账户限制（例如会员资格、审批或测试用户限制）
- 权限范围限制（尝试请求较少的权限范围）

如果您怀疑是重定向URL问题，可以使用HTTPS隧道进行连接：
```bash
# 1) Get a public HTTPS URL that forwards to localhost:3000 (example)
ngrok http 3000

# 2) Add the ngrok HTTPS URL + /callback to WHOOP dashboard Redirect URIs, then run:
WHOOP_REDIRECT_URI=https://YOUR-NGROK-DOMAIN.ngrok-free.app/callback node src/auth.js
```

如果您怀疑是权限范围问题，可以尝试请求较少的权限范围：
```bash
WHOOP_SCOPES="read:profile" node src/auth.js
```

### 如果您的WHOOP重定向URL是`https://localhost:3000/callback`

在这种情况下，本地回调服务器必须使用HTTPS协议（而不是HTTP）。运行以下脚本：
```bash
WHOOP_REDIRECT_URI=https://localhost:3000/callback node src/auth.js
```
该脚本会生成一个自签名证书，您的浏览器可能会显示TLS警告。请忽略警告并继续操作，以便完成重定向。

## JSON输出格式

这些命令支持以下输出格式：
- `--json`（生成一个JSON字符串）
- `--jsonl`（每行生成一个JSON对象；适用于管道传输）
- `--limit N`（在支持的情况下限制输出数量）
- 时间过滤选项：`--days N`、`--since 7d` / `12h`、`--start ISO`、`--end ISO`

```bash
node src/summary.js --json
node src/recovery.js --json --limit 1
node src/sleep.js --json --limit 1
node src/strain.js --json --limit 1
node src/workouts.js --json --limit 1

# Examples with filters
node src/sleep.js --json --days 7
node src/workouts.js --jsonl --since 30d
node src/recovery.js --json --start 2026-01-01T00:00:00Z --end 2026-02-01T00:00:00Z
```

## API说明

- 使用WHOOP开发者API v2
- 支持OAuth 2.0认证和令牌自动刷新机制
- 支持的权限范围包括：`offline`、`read:recovery`、`read:sleep`、`read:workout`、`read:cycles`、`read:profile`
- 令牌会在过期后自动刷新