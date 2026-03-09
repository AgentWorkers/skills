---
name: even-g2-bridge
description: "通过 Cloudflare Worker 将 Even Realities G2 智能眼镜连接到 OpenClaw。该解决方案会搭建一个桥梁，将 G2 的语音指令路由到 OpenClaw Gateway——使用相同的代理、相同的内存和相同的工具，只不过输入方式是从语音变为文字。支持简短对话（在眼镜上直接回复），以及长时间运行的任务（通过 Telegram 进行后台处理），还可以生成图像（使用 DALL-E 并通过 Telegram 发送结果）。适用场景包括：配置 G2 智能眼镜与 OpenClaw 的连接、部署 G2 相关的桥接服务，或排查 G2 与 OpenClaw 之间的连接问题。"
license: MIT
compatibility: "Requires: Cloudflare account (free plan works), OpenClaw Gateway with HTTP API enabled. Optional: OpenAI API key (image gen), Telegram bot (rich content delivery)."
metadata:
  author: dAAAb
  version: "5.0.0"
  repository: https://github.com/dAAAb/openclaw-even-g2-bridge-skill
  icon: assets/icon.png
  required_secrets:
    - name: GATEWAY_URL
      description: "Your OpenClaw Gateway URL (e.g. https://your-gateway.example.com)"
      required: true
    - name: GATEWAY_TOKEN
      description: "OpenClaw Gateway auth token — stored in CF Worker secrets, never exposed to glasses"
      required: true
    - name: G2_TOKEN
      description: "Token for G2 glasses authentication — you choose this value"
      required: true
    - name: ANTHROPIC_API_KEY
      description: "Anthropic API key for fallback when Gateway is unreachable"
      required: true
    - name: TELEGRAM_BOT_TOKEN
      description: "Telegram bot token for delivering rich content (images, code, long text)"
      required: false
    - name: TELEGRAM_CHAT_ID
      description: "Telegram chat ID for content delivery"
      required: false
    - name: OPENAI_API_KEY
      description: "OpenAI API key for DALL-E image generation"
      required: false
  security_notes: |
    Two-layer token auth: G2 glasses only know G2_TOKEN. GATEWAY_TOKEN stays in
    Worker secrets, never exposed to glasses. If glasses are lost, change only G2_TOKEN.
    Consider using a scoped, least-privilege Gateway token for the Worker.
---
# Even Realities G2 × OpenClaw Bridge

部署一个 Cloudflare Worker，用于将 Even Realities G2 智能眼镜与您的 OpenClaw Gateway 连接起来。

## 功能介绍

```
G2 Glasses → (voice→text) → CF Worker → OpenClaw Gateway → Full Agent
                                ↓                              ↓
                          G2 display (text)            Telegram (rich content)
```

- **简单任务**（如聊天、提问）：Gateway 处理后结果会显示在 G2 上。
- **复杂任务**（如编写代码、撰写文章）：G2 会显示“正在处理中……”，处理完成后结果会发送到 Telegram。
- **图像生成**：使用 DALL-E 生成图像后，结果会发送到 Telegram（G2 本身无法显示图像）。
- **备用方案**：如果 Gateway 出现故障，系统会自动切换到 Claude API 进行处理。

## 前提条件

1. 搭配 Even 应用的 Even Realities G2 智能眼镜（版本需达到 v0.0.7 或更高，且支持“添加代理”功能）。
2. OpenClaw Gateway 已启用 HTTP API。
3. 拥有 Cloudflare 账户（免费计划即可）。
4. 拥有 Anthropic API 密钥（用于图像生成）。
5. （可选）：拥有 OpenAI API 密钥（用于图像生成）以及 Telegram 机器人令牌（用于富媒体内容传输）。

## 设置步骤

### 1. 启用 OpenClaw Gateway 的 HTTP API

在您的 OpenClaw 服务器上，启用聊天完成功能的相关端点：

```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
openclaw gateway restart
```

验证设置是否正确：

```bash
curl -X POST https://YOUR_GATEWAY_URL/v1/chat/completions \
  -H "Authorization: Bearer YOUR_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"hi"}]}'
```

### 2. 部署 Cloudflare Worker

将 `scripts/worker.js` 文件复制到您的项目中，然后进行部署：

```bash
# Install wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
wrangler deploy
```

或者通过 Cloudflare 控制台进行部署：选择“Workers & Pages” → “Create” → 上传 `worker.js` 文件。

### 3. 设置密钥

```bash
# Required
wrangler secret put GATEWAY_URL      # Your OpenClaw Gateway URL
wrangler secret put GATEWAY_TOKEN    # Your Gateway auth token
wrangler secret put G2_TOKEN         # Token for G2 glasses auth (you choose)
wrangler secret put ANTHROPIC_API_KEY # Fallback when Gateway is down

# Optional (for Telegram delivery of rich content)
wrangler secret put TELEGRAM_BOT_TOKEN
wrangler secret put TELEGRAM_CHAT_ID

# Optional (for image generation)
wrangler secret put OPENAI_API_KEY
```

### 4. 配置 G2 智能眼镜

在 Even 应用中进入“Settings” → “Add Agent”：
- **名称**：为您的代理设置一个名称（例如：“Cloud Lobster”）。
- **URL**：输入 `https://YOUR_WORKER.workers.dev`。
- **Token**：使用之前设置的 `G2_TOKEN`。

### 5. 测试

```bash
curl -X POST https://YOUR_WORKER.workers.dev \
  -H "Authorization: Bearer YOUR_G2_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"Hello, who are you?"}]}'
```

## 架构说明

### 请求流程

1. G2 将语音转换为文本，并以 OpenAI 聊天完成的格式发送。
2. Worker 通过 `G2_TOKEN` 进行身份验证。
3. Worker 根据请求类型进行处理：
   - **图像生成**：使用 DALL-E 生成图像后通过 Telegram 发送结果（G2 会立即收到确认）。
   - **复杂任务**：G2 会立即给出确认信息，然后后台调用 Gateway 处理任务结果，最终通过 Telegram 发送结果。
   - **简单任务**：请求会被代理到 Gateway，处理完成后直接返回给 G2。

### 安全性

采用双层令牌认证机制：
```
G2 --[G2_TOKEN]--> Worker --[GATEWAY_TOKEN]--> Gateway
```

- 只有 G2 知道 `G2_TOKEN` 的内容；如果眼镜丢失，只需更换该令牌即可。
- `GATEWAY_TOKEN` 保存在 Worker 的密钥中，不会泄露给 G2。
- Gateway 的 HTTP API 必须经过身份验证（支持令牌或密码认证方式）。

### G2 显示限制

- 显示区域大小为 576×136 像素，单色绿色背景，最多可显示约 48 个字符。
- 仅支持文本显示（不支持图像和 Markdown 格式）。
- Worker 会自动过滤输入内容：URL 会被替换为 `[link]`，代码块会被替换为 `[code]`，过长文本会被截断。
- 无法显示的内容会直接转发到 Telegram。

## 自定义设置

您可以在 `worker.js` 文件中修改任务分类的正则表达式，以自定义不同类型的请求处理方式：
- `isLongTask()`：用于识别需要后台处理的请求。
- `isImageGenRequest()`：用于识别需要使用 DALL-E 生成图像的请求。

## 故障排除

- 如果 G2 显示“Unauthorized”错误，请检查 `G2_TOKEN` 是否在 Worker 和 Even 应用的配置中正确设置。
- 如果出现“Gateway not configured”错误，请确认 `GATEWAY_URL` 和 `GATEWAY_TOKEN` 是否已正确配置。
- 如果简单任务处理超时，请考虑增加 `SHORT_TIMEOUT` 的值（Cloudflare Workers 的默认超时时间为 25 秒）。
- 如果无法通过 Telegram 收到响应，请检查 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 的配置是否正确。
- 如果 Gateway 返回 404 错误，请确保 OpenClaw 配置中 `chatCompletions.enabled` 为 `true`，并重启系统。