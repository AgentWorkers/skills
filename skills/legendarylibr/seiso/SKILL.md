---
name: seisoai
description: SeisoAI x402 协议技能，适用于 OpenClaw/Claw 代理。通过 Base 平台，使用 USDC 以按请求计费的方式提供 AI 推理服务。
metadata: {"openclaw":{"homepage":"https://seisoai.com","emoji":":art:"}}
version: 2.0.0
last_synced: 2026-02-13
---

# SeisoAI x402 技能（适用于 OpenClaw）

基础 URL：`https://seisoai.com`

## 概述

SeisoAI 提供了 AI 推理工具（图像、视频、音乐、3D、音频），可通过 x402 支付协议进行使用。外部代理需要通过支付来验证身份——无需 API 密钥或 JWT。

**支付网络**：Base 主网（eip155:8453）
**支付货币**：USDC

## 快速入门

1. 无需认证即可调用任何网关端点。
2. 收到“需要支付（402）”的提示，并显示价格信息。
3. 向 `payTo` 钱包支付费用。
4. 使用 `payment-signature` 头部信息重新尝试请求。
5. 接收结果或作业 ID 以进行后续查询。

## 网关端点

所有支持 x402 的端点都位于 `/api/gateway/` 下：

### 发现（无需认证）

| 端点 | 描述 |
|----------|-------------|
| `GET /api/gateway` | 网关信息、类别、端点列表 |
| `GET /api/gateway/tools` | 列出所有工具 |
| `GET /api/gateway/tools?category=X` | 按类别筛选工具 |
| `GET /api/gateway/tools?q=X` | 搜索工具 |
| `GET /api/gateway/tools/:toolId` | 获取工具详情 |
| `GET /api/gateway/price/:toolId` | 查看工具价格 |
| `GET /api/gateway/schema` | OpenAPI 架构 |
| `GET /api/gateway/mcp-manifest` | MCP 清单 |
| `GET /api/gateway/agents` | 注册代理列表 |

### 调用（需要 x402 支付）

| 端点 | 描述 |
|----------|-------------|
| `POST /api/gateway/invoke/:toolId` | 调用工具 |
| `POST /api/gateway/invoke` | 在请求体中包含 `toolId` 来调用工具 |
| `POST /api/gateway/batch` | 批量调用多个工具 |
| `POST /api/gateway/orchestrate` | 多步骤工作流 |

### 作业（无需认证）

| 端点 | 描述 |
|----------|-------------|
| `GET /api/gateway/jobs/:jobId` | 查询作业状态 |
| `GET /api/gateway/jobs/:jobId/result` | 获取作业结果 |

## 可用的工具类别

- `image-generation` - 文本转图像（FLUX 等）
- `image-editing` - 图像编辑/合成 |
- `image-processing` - 图像缩放、图层提取 |
- `video-generation` - 文本/图像转视频（Veo3、Kling 等）
- `video-editing` - 图像动画处理、视频编辑 |
- `music-generation` - 音乐生成 |
- `audio-generation` - 文本转语音（TTS）、视频转音频 |
- `audio-processing` - 文本转语音、音频分离 |
- `3d-generation` - 图像/文本转 3D |
- `vision` - 图像描述 |
- `training` - 训练 LoRA 模型 |

## x402 支付流程

### 第 1 步：初始请求（无需认证）

```http
POST /api/gateway/invoke/image.generate.flux-2
Host: seisoai.com
Content-Type: application/json

{"prompt": "a cyberpunk cityscape at sunset", "aspect_ratio": "16:9"}
```

### 第 2 步：收到支付提示（402）

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json

{
  "x402Version": 2,
  "error": "Payment required",
  "resource": {
    "url": "https://seisoai.com/api/gateway/invoke/image.generate.flux-2",
    "description": "Invoke any AI tool via the gateway",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "maxAmountRequired": "32500",
      "asset": "USDC",
      "payTo": "0xa0aE05e2766A069923B2a51011F270aCadFf023a",
      "extra": {
        "priceUsd": "$0.0325"
      }
    }
  ]
}
```

### 第 3 步：完成支付

使用 OpenClaw 主机的支付签名器完成 x402 支付：
- 金额：`accepts[0].maxAmountRequired`（以 USDC 为单位，保留 6 位小数）
- 收款人：`accepts[0].payTo`（与提示中指定的收款人地址一致）
- 网络：`eip155:8453`（Base 主网）

### 第 4 步：重新尝试请求

```http
POST /api/gateway/invoke/image.generate.flux-2
Host: seisoai.com
Content-Type: application/json
payment-signature: <signed-x402-payload>

{"prompt": "a cyberpunk cityscape at sunset", "aspect_ratio": "16:9"}
```

### 第 5 步：接收结果

- 对于同步执行的工具，直接接收结果。
- 对于异步/排队执行的工具，等待结果。

## 查询排队中的作业

```http
GET /api/gateway/jobs/{jobId}
Host: seisoai.com
```

响应状态：`QUEUED`、`IN_PROGRESS`、`COMPLETED`、`FAILED`

## 示例工具调用

### 图像生成

```json
POST /api/gateway/invoke/image.generate.flux-2
{
  "prompt": "a serene japanese garden with cherry blossoms",
  "aspect_ratio": "16:9",
  "num_images": 1
}
```

### 视频生成

```json
POST /api/gateway/invoke/video.generate.veo3
{
  "prompt": "a timelapse of clouds moving over mountains",
  "duration": 5
}
```

### 音乐生成

```json
POST /api/gateway/invoke/music.generate
{
  "prompt": "upbeat electronic music for a tech demo",
  "duration": 30
}
```

### 文本转语音

```json
POST /api/gateway/invoke/audio.tts
{
  "text": "Hello, this is a test of the text to speech system.",
  "voice": "alloy"
}
```

### 图像转 3D

```json
POST /api/gateway/invoke/3d.image-to-3d
{
  "image_url": "https://example.com/object.png"
}
```

## 查看价格

在调用工具之前，请先查看价格信息：

```http
GET /api/gateway/price/image.generate.flux-2
```

```json
{
  "success": true,
  "toolId": "image.generate.flux-2",
  "pricing": {
    "usd": 0.0325,
    "usdcUnits": "32500"
  },
  "x402": {
    "network": "eip155:8453",
    "asset": "USDC",
    "amount": "32500"
  }
}
```

## 安全性

### 服务器端防护措施

网关实施了以下安全措施：
- **防止重放**：支付签名是一次性使用的。重复提交已使用的签名会收到 402 错误 “Payment signature already used”。
- **签名去重**：基于 Redis（或内存缓存）的机制防止多次提交相同的签名。
- **钱包验证**：CDP 服务验证支付是否发送到了正确的 `payTo` 地址。
- **金额验证**：支付金额必须等于或超过提示中的 `maxAmountRequired`。
- **网络验证**：支付必须通过 Base 主网（eip155:8453）进行。
- **路由限制**：x402 仅支持 `/api/gateway/` 路由，其他路由会拒绝支付请求。
- **基于符号的认证**：已支付的请求会设置一个不可伪造的符号标志，无法通过请求头伪造。

### 支付签名规则（强制要求）

1. **仅使用主机提供的签名器**：必须使用 OpenClaw 主机提供的支付签名器。
2. **禁止使用原始密钥**：严禁请求、存储或生成私钥。
3. **仅签名 x402 相关的支付数据**：仅对来自 x402 请求的支付数据进行签名。
4. **确保收款人正确**：始终将支付发送到提示中指定的 `payTo` 地址。
5. **使用新的签名**：不得在多次请求中重复使用相同的签名。
6. **失败时返回错误**：如果无法使用签名器，应返回错误信息，而不是跳过支付步骤。

### 请求规则（严禁违反）

- **请求内容必须一致**：重新尝试请求时，请求体内容必须与初次请求完全相同。
- **保持请求方法和路径不变**：重新尝试时，HTTP 方法和路径不得更改。
- **使用新的签名**：不得重复使用过期的或已使用的签名。
- **成功提交即计费**：成功提交到队列中的请求将被视为可计费的操作。
- **钱包地址必须正确**：签名后的支付请求必须指向提示中指定的 `payTo` 地址。

### 违规处理方式

| 违规类型 | 服务器响应 |
|------------|-----------------|
| 重复使用签名 | 402 错误：“Payment signature already used” |
| 收款人地址错误 | 402 错误：“Payment verification failed” |
- 金额不足 | 402 错误：“Payment amount insufficient” |
- 网络错误 | 402 错误：“Invalid payment network” |
- 非网关路由 | 401 错误：“Authentication required” |
- 伪造的请求头 | 401 错误：“Symbol flag not set” |

## 速率限制

| 类别 | 限制 | 限制时间窗口 |
|-------|-------|--------|
| 通用 API 请求 | 500 次请求 | 15 分钟 |
| 支付操作 | 10 次请求 | 5 分钟 |

速率限制相关信息包含在响应中：
- `X-RateLimit-Limit`：允许的最大请求次数。
- `X-RateLimit-Remaining`：当前时间窗口内剩余的请求次数。
- `X-RateLimit-Reset`：时间窗口的重置时间（ISO-8601 格式）。
- `Retry-After`：允许重试的间隔时间（以秒为单位）。

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|---------|--------|
| 402 | 需要支付 | 完成支付操作并重新尝试。 |
| 400 | 输入无效 | 修复请求数据。 |
| 401 | 需要认证（非 x402 路由） | 使用正确的网关端点。 |
| 404 | 找不到工具/路由 | 检查工具 ID 的拼写是否正确。 |
| 429 | 超过速率限制 | 根据 `Retry-After` 头部信息进行延迟重试。 |
| 500 | 服务器错误 | 采用指数级延迟策略进行重试（最多尝试 3 次）。 |

## 常见错误

- **重复使用签名**：每次请求都需要新的签名。
- **重新尝试时更改请求数据**：请求数据必须与初次请求完全相同。
- 使用错误的查询端点**：请使用队列响应中的 `pollUrl`。
- 将 402 错误视为普通错误：实际上这是支付过程中的正常响应，不是系统故障。
- 非 x402 支持的路由：只有 `/api/gateway/` 路由支持 x402 支付。

## 响应格式

成功响应包含以下内容：

```json
{
  "success": true,
  "toolId": "string",
  "result": { ... },
  "x402": {
    "settled": true,
    "amount": "string",
    "transactionHash": "string | null"
  }
}
```

失败响应包含以下内容：

```json
{
  "success": false,
  "error": "string",
  "code": "string (optional)"
}
```

## 发现信息

### 网关信息

```http
GET /api/gateway
```

返回网关元数据、可用类别、工具数量及支持的协议。

### 列出工具

```http
GET /api/gateway/tools
GET /api/gateway/tools?category=image-generation
GET /api/gateway/tools?q=video
```

### 工具详情

```http
GET /api/gateway/tools/:toolId
```

### 查看工具价格

```http
GET /api/gateway/price/:toolId
```

## 替代方案：API 密钥认证

已注册的代理也可以使用 API 密钥代替 x402 协议：

```http
POST /api/gateway/invoke/image.generate.flux-2
Host: seisoai.com
Content-Type: application/json
X-API-Key: sk_live_your_api_key

{"prompt": "test"}
```

API 密钥必须以 `sk_live_` 开头，并已在 SeisoAI 中注册。