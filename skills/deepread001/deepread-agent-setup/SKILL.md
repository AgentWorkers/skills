---
name: deepread-agent-setup
title: DeepRead Agent Setup
description: 使用 OAuth 设备流程，通过 DeepRead OCR API 对 AI 代理进行身份验证。代理会显示一个验证码，用户在浏览器中批准该验证码，随后代理会收到一个存储为环境变量的 DEEPREAD_API_KEY。
disable-model-invocation: true
metadata:
  {"openclaw":{"produces":{"env":["DEEPREAD_API_KEY"]},"homepage":"https://www.deepread.tech"}}
---
# DeepRead 代理设置

使用 **OAuth 2.0 设备授权流程**（RFC 8628）通过 DeepRead OCR API 对 AI 代理进行身份验证。设置完成后，代理将拥有一个名为 `DEEPREAD_API_KEY` 的环境变量，并可以使用 [DeepRead OCR 技能](https://clawhub.ai/deepread-tech/deepread)。

## 工作原理

该设备授权流程允许无浏览器功能的代理（headless agents）安全地进行身份验证：

```
Agent requests device code  →  User opens URL in browser  →  User approves  →  Agent receives API key
```

1. 代理调用 `POST https://api.deepread.tech/v1/agent/device/code` 以获取 `device_code` 和 `user_code`。
2. 代理向用户显示 `user_code` 以及一个验证链接。
3. 用户在浏览器中打开该链接，登录并输入代码。
4. 代理持续调用 `POST https://api.deepread.tech/v1/agent/device/token`，直到用户批准。
5. 代理收到一个以 `sk_live_` 为前缀的 `api_key`，并将其存储为 `DEEPREAD_API_KEY` 环境变量。

**仅连接的域名：** `api.deepread.tech`

## 先决条件

- 一个 DeepRead 账户（在 https://www.deepread.tech/dashboard/?utm_source=clawdhub 上可免费注册）。
- 可以访问 `api.deepread.tech` 的网络环境。

## 设置说明

### 第一步：请求设备代码

```bash
curl -s -X POST https://api.deepread.tech/v1/agent/device/code \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-ai-agent"}'
```

`agent_name` 字段是可选的——它会在批准页面上显示，以便用户知道是哪个代理请求访问权限。

**响应：**
```json
{
  "device_code": "GmRhmhcxhZAzk...EeNu5OfKhL79MQgN",
  "user_code": "WDJB-MJHT",
  "verification_uri": "https://www.deepread.tech/activate",
  "verification_uri_complete": "https://www.deepread.tech/activate?code=WDJB-MJHT",
  "expires_in": 900,
  "interval": 5
}
```

**告知用户**（使用响应中的信息——这些信息每次都会变化）：
> 打开 **{verification_uri}** 并输入代码 **{user_code}**。
>
> 或者直接点击此链接：**{verification_uri_complete}**

### 第二步：等待用户批准

以每 `interval` 秒的间隔（默认值为 5 秒）持续请求批准：

```bash
curl -s -X POST https://api.deepread.tech/v1/agent/device/token \
  -H "Content-Type: application/json" \
  -d '{"device_code": "GmRhmhcxhZAzk...EeNu5OfKhL79MQgN"}'
```

**在等待期间（用户尚未批准）：**
```json
{
  "error": "authorization_pending",
  "api_key": null,
  "key_prefix": null
}
```

**用户批准后：**
```json
{
  "error": null,
  "api_key": "sk_live_abc123def456...",
  "key_prefix": "sk_live_abc123de"
}
```

**`api_key` 仅会返回一次**。下一次请求时会返回 `expired_token`。收到后请立即保存它。

**如果用户拒绝：**
```json
{
  "error": "access_denied",
  "api_key": null,
  "key_prefix": null
}
```

**如果代码过期（15 分钟后）：**
```json
{
  "error": "expired_token",
  "api_key": null,
  "key_prefix": null
}
```

### 第三步：存储 API 密钥

收到 `api_key` 后，将其设置为当前会话的变量：

```bash
export DEEPREAD_API_KEY="<api_key from response>"
```

**为了在会话之间保持密钥的持久性，用户可以选择以下方法之一：**

| 方法 | 命令 | 安全性 |
|---|---|---|
| **密钥管理器（推荐）** | 使用操作系统的密钥链、1Password CLI 或 `pass` | 密钥在存储时被加密 |
| **Shell 配置文件** | 用户手动将 `export DEEPREAD_API_KEY="..."` 添加到 `~/.zshrc` | 密钥以明文形式保存在配置文件中——可供本地进程读取 |

**重要提示：**
- 代理应仅将密钥设置为当前会话的变量（使用 `export` 命令）。
- 密钥的持久性由用户自行决定——切勿自动将密钥写入 Shell 配置文件。
- 绝不要将密钥提交到版本控制系统中或写入项目文件中。
- 密钥前缀 `sk_live_` 表明这是一个有效的 DeepRead 生产密钥。

### 第四步：验证密钥的有效性

提交一份测试文档以确认密钥是否有效：

```bash
curl -s -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@test.pdf"
```

如果验证成功，系统会返回一个作业 ID，证明密钥有效：
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}
```

如果密钥无效，系统会返回 `401 Unauthorized` 的错误响应。

## 完整流程（所有步骤）

```bash
#!/bin/bash
# DeepRead Device Flow — complete example

# 1. Request device code
RESPONSE=$(curl -s -X POST https://api.deepread.tech/v1/agent/device/code \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-ai-agent"}')

DEVICE_CODE=$(echo "$RESPONSE" | jq -r '.device_code')
USER_CODE=$(echo "$RESPONSE" | jq -r '.user_code')
VERIFY_URI=$(echo "$RESPONSE" | jq -r '.verification_uri')
VERIFY_URI_COMPLETE=$(echo "$RESPONSE" | jq -r '.verification_uri_complete')
INTERVAL=$(echo "$RESPONSE" | jq -r '.interval')

echo "Open $VERIFY_URI and enter code: $USER_CODE"
echo "Or open directly: $VERIFY_URI_COMPLETE"

# 2. Poll for token
while true; do
  TOKEN_RESPONSE=$(curl -s -X POST https://api.deepread.tech/v1/agent/device/token \
    -H "Content-Type: application/json" \
    -d "{\"device_code\": \"$DEVICE_CODE\"}")

  ERROR=$(echo "$TOKEN_RESPONSE" | jq -r '.error // empty')

  if [ -z "$ERROR" ]; then
    export DEEPREAD_API_KEY=$(echo "$TOKEN_RESPONSE" | jq -r '.api_key')
    echo "Authenticated. DEEPREAD_API_KEY is set for this session."
    break
  elif [ "$ERROR" = "authorization_pending" ]; then
    sleep "$INTERVAL"
  elif [ "$ERROR" = "slow_down" ]; then
    INTERVAL=$((INTERVAL + 5))
    sleep "$INTERVAL"
  else
    echo "Error: $ERROR"
    exit 1
  fi
done
```

## 使用的端点

| 端点 | 方法 | 认证方式 | 用途 |
|---|---|---|---|
| `https://api.deepread.tech/v1/agent/device/code` | POST | 无 | 请求设备代码和用户代码 |
| `https://api.deepread.tech/v1/agent/device/token` | POST | 无 | 在用户批准后请求 API 密钥 |
| `https://www.deepread.tech/activate` | — | 浏览器 | 用户通过此链接输入代码并批准 |

**此技能不会访问其他端点。**

## 故障排除

### “authorization_pending” 持续显示
用户尚未批准。请继续等待。代码会在 15 分钟后过期（`expires_in: 900`）。

### “expired_token”
设备代码在用户批准之前已过期，或者 API 密钥已被获取（密钥仅获取一次）。请从第一步重新开始。

### “slow_down”
请求频率过高。将请求间隔增加 5 秒。

### “access_denied”
用户在批准页面上选择了“拒绝”。如果用户希望重试，请从第一步开始。

### 密钥导入后无法使用
确保 Shell 会话没有重新启动。如果将密钥保存到 `~/.zshrc` 中，请运行 `source ~/.zshrc` 以重新加载配置文件。

### “DEEPREAD_API_KEY 未设置”
环境变量未正确设置。请重新执行设备授权流程或手动设置密钥：
```bash
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## 安全注意事项

- 该设备授权流程遵循 [RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628) 标准。
- `user_code` 的有效期为 15 分钟，且仅限一次性使用。
- `api_key` 仅返回一次——后续请求会返回 `expired_token`。
- 所有通信均通过 HTTPS 进行。
- 代理仅将 `DEEPREAD_API_KEY` 设置为当前会话的变量——不会将其保存到磁盘上。
- 对于长期存储，建议使用密钥管理器（如操作系统的密钥链、1Password CLI 或 `pass`）而非明文的 Shell 配置文件。
- 绝不要将密钥提交到版本控制系统中或写入项目文件中。
- 代理无法获取用户的密码。

## 支持方式

- **控制台**：https://www.deepread.tech/dashboard
- **问题反馈**：https://github.com/deepread-tech/deep-read-service/issues
- **电子邮件**：hello@deepread.tech