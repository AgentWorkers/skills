---
name: clawkey
version: 1.0.0
description: OpenClaw代理具有可验证的人类所有者身份。您可以通过VeryAI的掌纹验证功能，将您的代理注册到您本人名下。
homepage: https://clawkey.ai
metadata: { "category": "identity", "api_base": "https://api.clawkey.ai/v1" }
---

# ClawKey — 可验证的人类所有权

通过 VeryAI 的手掌识别技术，将您的代理注册到相应的人类所有者名下。代理在开始注册时会生成一个签名过的挑战信息，以证明其对该密钥的控制权；随后人类需要访问一个 URL 并完成 VeryAI 的手掌识别验证。验证完成后，代理便正式归属于该人类所有者，并可接受第三方的验证。

> **重要提示：** **切勿打开浏览器**  
> **禁止** 使用 `open`、`xdg-open`、`start` 或任何能够打开浏览器的命令。请始终以文本或 Markdown 链接的形式提供 **注册 URL**，供人类用户点击进行验证。  
> - **错误示例：`open "https://api.very.org/oauth2/..."`  
> - **正确示例：** “点击此链接完成验证：https://api.very.org/oauth2/...”  

## 关键文件  

| 文件名          | 用途                                                                                   |
| ------------ | ----------------------------------------------------------------------------------------- |
| SKILL.md     | https://clawkey.ai/skill.md — 注册流程、挑战生成、验证、API  |
| HEARTBEAT.md | https://clawkey.ai/heartbeat.md — 定期检查清单：注册状态等            |
| Identity     | `~/.openclaw/identity/device.json` — OpenClaw 设备 ID 和密钥（切勿发送私钥） |

## 安全性  

- **私钥**：用于生成签名。切勿将私钥发送给 ClawKey 或任何服务器；只需发送 `PublicKey`、`message` 和 `signature`。  
- **注册 URL**：仅限一次性使用且具有较短的有效期。仅将 URL 提供给完成 VeryAI 验证的人类所有者。  
- **deviceId**：使用一个稳定的标识符（例如来自您的身份验证系统或公钥的哈希值）。该标识符用于将代理与注册信息关联起来，并用于后续的查询和验证。  

## 生成 AgentChallenge  

`AgentChallenge` 是一个签名过的数据包，用于证明您控制着一把 Ed25519 密钥。其结构遵循 OpenClaw 的标准身份验证流程：`deviceId`、`publicKey`、`message`、`signature`、`timestamp`。生成一次后，将其发送到 `/agent/register/init` 或 `/agent/verify/signature`。  

### 身份信息的来源（OpenClaw）  

如果您使用 OpenClaw，设备身份信息存储在：  
- **路径：`~/.openclaw/identity/device.json`  

该文件包含以下内容（切勿将 `privateKeyPem` 发送到任何服务器）：  
| 字段           | 用途                                                                      |
| --------------- | ------------------------------------------------------------------------ |
| `deviceId`      | 作为挑战信息中的 `deviceId` 使用。表示代理/设备的唯一标识符。     |
| `publicKeyPem`  | 用于生成 `publicKey`（详见下文）。                                   |
| `privateKeyPem` | 仅用于本地签名操作。**切勿包含在 API 请求中。**  

如果您不使用 OpenClaw，请使用您自己的身份验证系统；确保您拥有一个稳定的 `deviceId`、一对 Ed25519 密钥，并确保您发送的 `message` 是经过签名的。  

### 生成挑战信息的步骤  

1. **选择要签名的消息**  
   注册时，使用一次性生成的挑战信息以防止重放，例如：`clawkey-register-<unix_timestamp_ms>`  
   示例：`clawkey-register-1738500000000`  
   在验证签名时，`message` 可以是您需要证明的内容（例如来自第三方的随机数）。  

2. **使用您的 Ed25519 私钥对消息进行签名**。签名必须覆盖 `message` 的所有 UTF-8 字节（不得添加前缀或后缀）。  

3. **编码以适应 API 格式**：  
   - `publicKey`：以 SPKI DER 格式表示的 Ed25519 公钥，然后使用 Base64 编码。  
   - `signature`：原始的 Ed25519 签名字节，同样使用 Base64 编码。  
   - `timestamp`：挑战信息创建时的 Unix 时间（单位：毫秒，例如 `Date.now()`）。  

4. **构建 JSON 数据包（AgentChallenge）**：  
   - `deviceId`：来自您的身份验证系统（例如 `device.json`）。  
   - `publicKey`：Base64 DER 格式的 Ed25519 公钥。  
   - `message`：需要签名的原始字符串。  
   - `signature`：Ed25519 签名的 Base64 表示形式。  
   - `timestamp`：挑战信息创建时的 Unix 时间（单位：毫秒）。  

### 示例（Node.js 代码）  

```javascript
const crypto = require("crypto");
const fs = require("fs");

const identityPath = `${process.env.HOME}/.openclaw/identity/device.json`;
const identity = JSON.parse(fs.readFileSync(identityPath, "utf8"));

const message = `clawkey-register-${Date.now()}`;
const privateKey = crypto.createPrivateKey(identity.privateKeyPem);
const signature = crypto.sign(null, Buffer.from(message, "utf8"), privateKey);

const publicKeyDer = crypto
  .createPublicKey(identity.publicKeyPem)
  .export({ type: "spki", format: "der" });

const challenge = {
  deviceId: identity.deviceId,
  publicKey: publicKeyDer.toString("base64"),
  message,
  signature: signature.toString("base64"),
  timestamp: Date.now(),
};
// POST challenge to https://api.clawkey.ai/v1/agent/register/init
```  

### 使用脚本  

如果您已有生成 AgentChallenge 的脚本（例如能够签名消息并输出包含 `deviceId`、`publicKey`、`message`、`signature`、`timestamp` 的 JSON 数据），可以将其直接用于 ClawKey：  
1. 生成挑战信息字符串，例如 `clawkey-register-$(date +%s)000`（其中 `date +%s` 表示当前时间戳，`000` 表示毫秒）。  
2. 运行脚本对消息进行签名并获取生成的 JSON 数据。  
3. 将该 JSON 数据发送到 `https://api.clawkey.ai/v1/agent/register/init`。  

同样的挑战格式也适用于远程验证签名的请求（`POST /agent/verify/signature`）。  

## 快速入门  

### 1. 开始注册（代理主动发起）  
按照上述步骤生成 `AgentChallenge`，然后发送给 ClawKey 以创建会话并获取注册 URL。  

**响应（201 状态码）：**  
- `sessionId`：用于查询注册状态。  
- `registrationUrl`：以链接形式提供给人类用户；**切勿在浏览器中打开该链接**。  
- `expiresAt`：会话的有效期限（格式：ISO 8601）。  

如果代理已经注册（`deviceId` 存在），API 会返回 **409 Conflict** 状态码。  

### 2. 人类完成验证  
要求人类用户在其浏览器中打开 `registrationUrl`，完成 VeryAI 的手掌识别验证。验证通过后，代理便归属于该用户。  

### 3. 查询注册状态  
持续查询，直到人类完成验证或会话过期：  

**响应状态码：** `pending` | `completed` | `expired` | `failed`  
当状态为 `completed` 时，响应中会包含 `deviceId` 和注册信息（例如 `publicKey`、`registeredAt`）。  

### 4. 验证签名或查询代理信息  

- **验证签名**：检查消息是否由指定密钥签名，以及该代理是否归属于已验证的人类。  

**响应示例：** `verified`（签名有效）；`registered`（代理已注册）。  

- **按设备 ID 查询代理信息**：获取代理的注册和验证状态。  

**响应示例：** `registered`、`verified`（代理已注册），可选字段 `registeredAt`。  

## API 参考  

**基础 URL：** `https://api.clawkey.ai/v1`  
**本地访问地址：** `http://localhost:3000/v1`  

### API 端点  

| 方法        | 端点                          | 认证方式 | 说明                                                                                   |
|------------|------------------|---------|-----------------------------------------------------------------------------------------|
| POST       | `/agent/register/init`       | 无       | 开始注册会话；返回 `sessionId`、`registrationUrl`、`expiresAt`。 |
| GET        | `/agent/register/{sessionId}/status`    | 无       | 查询注册状态（`pending` / `completed` / `expired` / `failed`）。 |
| POST       | `/agent/verify/signature`      | 无       | 验证签名以及代理的注册状态。            |
| GET        | `/agent/verify/device/{deviceId}`     | 无       | 根据设备 ID 查询代理的注册和验证状态。           |

### 请求/响应格式  

**AgentChallenge**（用于 `register/init` 和 `verify/signature`）：  
| 字段        | 类型         | 是否必填 | 说明                                                                                   |
|---------------|-------------|---------|--------------------------------------------------------|
| deviceId      | string       | 是        | 设备 ID（例如公钥哈希值或应用 ID）。                          |
| publicKey     | string       | 是        | Ed25519 公钥（Base64 DER SPKI 格式）。                     |
| message     | string       | 是        | 需要签名的原始字符串。                          |
| signature    | string       | 是        | 对消息的 Ed25519 签名（Base64 编码）。                   |
| timestamp    | int64        | 是        | 挑战信息创建时的 Unix 时间（单位：毫秒）。                     |

**注册响应（201 状态码）：**  
```json
{
  "sessionId": "uuid",
  "registrationUrl": "https://clawkey.ai/register/...",
  "expiresAt": "2026-02-02T12:00:00Z"
}
```  

**注册状态响应（200 状态码）：**  
```json
{
  "status": "completed",
  "deviceId": "my-agent-device-id",
  "registration": {
    "publicKey": "...",
    "registeredAt": "2026-02-02T12:00:00Z"
  }
}
```  

**签名验证响应（200 状态码）：**  
```json
{
  "verified": true,
  "registered": true
}
```  

**设备状态响应（200 状态码）：**  
```json
{
  "registered": true,
  "verified": true,
  "registeredAt": "2026-02-02T12:00:00Z"
}
```  

**错误代码（4xx/5xx）：**  
```json
{
  "error": "Human-readable message",
  "code": "optional_code",
  "details": {}
}
```  

### 错误代码说明：  
| 代码        | 含义                                                         |                                                                                   |
|-------------|---------------------------------------------------------|                                                                                   |
| 400         | 请求无效或缺少必要字段。                                      |                                                                                   |
| 404         | 会话或设备未找到。                                      |                                                                                   |
| 409         | 代理已注册（设备 ID 已存在）。                                   |                                                                                   |
| 500         | 服务器错误。                                        |                                                                                   |  

## 功能说明：**  
注册完成后并通过 VeryAI 验证后：  
- **人类所有权**：代理与通过验证的人类用户关联。  
- **密钥绑定**：Ed25519 签名证明代理对该密钥的控制权；ClawKey 将该密钥与已验证的用户关联起来。  
- **公开验证**：第三方可以通过 `/agent/verify/signature` 或 `/agent/verify/device/{deviceId}` 验证代理的注册状态。  

## 使用场景：**  
- 将 OpenClaw（或其他类型）代理注册到人类所有者名下。  
- 向第三方证明代理确实由已验证的人类用户拥有。  
- 检查特定密钥或设备是否已注册并经过验证。  

## 需要帮助？  
- API 基础文档：https://api.clawkey.ai/v1  
- 官网：https://clawkey.ai