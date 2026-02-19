---
name: x402-creative-resources
description: 您可以通过 api.xona-agent.com 访问 Xona 的 x402 创意资源 API。这些 API 支持以下功能：创意总监（设计研究）、图像生成（nano-banana、seedream、grok-imagine、qwen、designer）、视频生成、X 新闻提取以及 PumpFun 代币信息的查询。当用户需要研究设计趋势、生成图像或视频、获取 X 的最新新闻，或查看 PumpFun 的热门代币时，可以使用这些 API。
---
# x402 创意资源

所有端点均位于 `https://api.xona-agent.com`，并通过 x402（Solana USDC 微支付）进行支付。代理钱包会自动完成支付。

## 如何调用 x402 端点

使用工作区脚本文件夹中的 `x402-fetch.js` 脚本。该脚本会使用代理的 Solana 钱包自动处理 402 支付流程。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js <endpoint> [payload_json]
```

**POST 示例：**
```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /image/creative-director '{"idea":"futuristic Solana DeFi dashboard"}'
```

**GET 示例：**
```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /token/pumpfun-trending
```

该脚本会输出 JSON 数据。解析响应并提取相关字段（`image_url`、`video_url`、`banner_url` 等），然后展示给用户。

## 资源发现

```bash
curl -s https://api.xona-agent.com/x402-resources
```

---

## 创意总监（设计研究）——0.03 美元

在 X 和 Google 上研究热门的设计趋势，分析用户需求，提供精炼的设计方向。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /image/creative-director \
  '{"idea":"futuristic Solana DeFi dashboard aesthetic","reference_images":["https://example.com/ref.jpg"]}'
```

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `idea` | 是 | 创意想法或设计研究查询 |
| `reference_images` | 否 | 参考图片 URL 的数组 |

**响应格式：`{ success, data: { intent, research, direction } }`

`direction` 数组包含生成计划的详细信息（包含 `output_metadata.prompt`），这些信息可以用于调用图像生成端点。

---

## 图像生成

所有图像端点都接受以下参数：

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `prompt` | 是 | 详细的图像描述 |
| `aspect_ratio` | 否 | 默认值：`1:1`、`16:9`、`9:16`、`4:3`、`3:4` |
| `referenceImage` | 否 | 参考图片 URL 的数组 |

所有端点的返回格式为：`{ success, data: { image_url, image_description, metadata } }`

### 设计师（风格融合）——0.08 美元

也可以提供 `style` 参数（用于在提示中融合多种风格）。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /image/designer \
  '{"prompt":"a glowing Solana logo floating in space","style":["digital art","futuristic","neon"],"aspect_ratio":"16:9"}'
```

### Grok Imagine — 0.04 美元

具有较高的艺术表现力，擅长处理文本与图像的结合。是最经济实惠的选项。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /image/grok-imagine \
  '{"prompt":"...","aspect_ratio":"1:1"}'
```

### Qwen Image — 0.05 美元

在质量和成本之间取得了良好的平衡。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /image-model/qwen-image \
  '{"prompt":"...","aspect_ratio":"1:1"}'
```

### Seedream 4.5 — 0.08 美元

ByteDance 开发的超真实模型，适合生成高细节、逼真的图像。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /image-model/seedream-4.5 \
  '{"prompt":"...","aspect_ratio":"1:1"}'
```

### Nano Banana — 0.10 美元

快速生成创意内容，是常用的默认选项。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /image/nano-banana \
  '{"prompt":"...","aspect_ratio":"1:1"}'
```

### Nano Banana Pro — 0.20 美元

提供最高质量的图像生成服务。

---

## 视频生成——0.50 美元

使用 Grok Imagine Video 生成 10 秒长的 AI 视频。支持从文本或图像生成视频。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /video/short-generation \
  '{"prompt":"camera slowly orbiting a glowing Solana logo in deep space","aspect_ratio":"16:9"}'
```

对于从图像生成视频的情况，需要传递之前生成的 `image_url` 作为参数：

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /video/short-generation \
  '{"prompt":"smooth zoom into center","aspect_ratio":"16:9","image":"https://cdn.example.com/img.jpg"}'
```

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `prompt` | 是 | 包含动作提示的视频描述 |
| `aspect_ratio` | 否 | 宽高比（默认值：`16:9`） |
| `image` | 否 | 用于动画化的静态图片 URL |

**响应格式：`{ success, data: { video_url, duration, model, metadata } }`

生成视频可能需要最多 5 分钟，请告知用户正在处理中。

---

## X 新闻提取——0.50 美元

从任意 X 账户中提取最新新闻，并生成推文草稿和横幅。

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /ai/x-news \
  '{"x_username":"solana"}'
```

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `x_username` | 是 | X 账户名称（可带 @ 符号） |
| `x_persona` | 否 | 用于模仿其风格的 X 账户 |

**响应格式：`{ success, data: { x_username, trending_news: { title, tweet_draft, banner_url } } }`

---

## PumpFun 代币情报

### 热门代币——0.10 美元

```bash
node /home/node/.openclaw/workspace/scripts/x402-fetch.js /token/pumpfun-trending
```

**响应格式：`{ success, data: { summary, suggestions, trending_tokens, count } }`

### 最具影响力的代币——0.10 美元**

响应格式与“热门代币”相同。

---

## 推荐的工作流程

### 完整的创意流程
1. 使用用户的创意调用 `/image/creative-director`
2. 使用返回的 `direction[].output_metadata.prompt` 呼叫图像生成端点
3. 将生成的 `image_url` 传递给 `/video/short-generation` 以生成动画视频

### 新闻 + 视觉内容流程
1. 使用目标 X 账户调用 `/ai/x-news`
2. 展示生成的推文草稿和横幅

### 市场情报
1. 调用 `/token/pumpfun-trending` 获取当前市场动态
2. 调用 `/token/pumpfun-movers` 了解最具影响力的代币走势
3. 根据主流市场趋势生成相应的图像内容