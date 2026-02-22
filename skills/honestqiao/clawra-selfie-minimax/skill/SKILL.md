---
name: clawra-selfie
description: 使用 MiniMax 或 fal.ai（Grok Imagine）生成 AI 图像，并通过 OpenClaw 将这些图像发送到消息通道中。
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
---
# Clawra 自拍功能

使用 MiniMax 或 xAI 的 Grok Imagine 模型生成 AI 图像，并通过 OpenClaw 将这些图像发送到各种消息平台（如 WhatsApp、Telegram、Discord、Slack 等）。

> 💡 **提示**：该脚本会自动检测可用的 API 密钥（默认优先使用 MiniMax）。

## 参考图像

该功能使用一个托管在 jsDelivr CDN 上的固定参考图像：

```
https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png
```

## 使用场景

- 用户请求发送照片（如 “发送一张图片”、“给我发张照片” 等）
- 用户要求发送特定场景下的自拍（如 “你正在做什么？”、“你最近怎么样？” 等）
- 用户提供具体场景描述（如 “请发送一张穿着……的照片”）

## 快速参考

### 所需环境变量

**选项 1：fal.ai（Grok Imagine）**
```bash
FAL_KEY=your_fal_api_key          # Get from https://fal.ai/dashboard/keys
```

**选项 2：MiniMax（推荐，通常更快/更可靠）**
```bash
MINIMAX_API_KEY=your_minimax_api_key  # Get from https://platform.minimaxi.com
```

**通用设置：**
```bash
OPENCLAW_GATEWAY_TOKEN=your_token  # From: openclaw doctor --generate-gateway-token
```

> ⚠️ **安全提示**：切勿在脚本中硬编码 API 密钥，应使用环境变量。

### 工作流程

1. **获取用户指令**：了解用户对图片编辑的具体要求。
2. **使用 fal.ai 的 Grok Imagine 编辑 API 根据参考图像进行图片编辑。
3. **从响应中提取图片 URL**。
4. **通过 OpenClaw 将编辑后的图片发送到目标渠道**。

## 详细步骤

### 步骤 1：收集用户输入

询问用户以下信息：
- **图片中的场景**：人物应该处于什么场景、穿着什么、在哪里？
- **编辑模式**（可选）：`mirror`（镜像模式）或 `direct`（直接自拍模式）
- **目标渠道**：图片应发送到哪个渠道？
- **平台**（可选）：使用哪个平台发送图片？

## 模式说明

### 模式 1：镜像自拍（默认模式）

适用于展示服装、全身照或时尚内容：

```
make a pic of this person, but [user's context]. the person is taking a mirror selfie
```

**示例**：用户请求 “请发送一张戴着圣诞帽的照片”。

### 模式 2：直接自拍

适用于拍摄特写肖像、场景照片或捕捉情感表情：

```
a close-up selfie taken by herself at [user's context], direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible
```

**示例**：用户请求 “请发送一张在温馨咖啡馆的照片”。

### 模式选择逻辑

| 关键词 | 自动选择的模式 |
|---------|------------|
| outfit, wearing, clothes, dress, suit, fashion | mirror（镜像模式） |
| cafe, restaurant, beach, park, city, location | direct（直接自拍模式） |
| close-up, portrait, face, eyes, smile | direct（直接自拍模式） |
| full-body, mirror, reflection | mirror（镜像模式） |

### 步骤 2：生成图片

有两种图片生成方式：

#### 选项 A：MiniMax API（推荐）

**MiniMax API 详细信息：**
- 端点：`https://api.minimaxi.com/v1/image_generation`
- 使用的模型：`image-01`
- 返回结果：Base64 编码的图片
- 支持的分辨率比例：1:1、3:4、4:3、9:16、16:9、21:9

#### 选项 B：fal.ai（Grok Imagine）

**返回结果格式：**
```json
{
  "images": [
    {
      "url": "https://v3b.fal.media/files/...",
      "content_type": "image/jpeg",
      "width": 1024,
      "height": 1024
    }
  ],
  "revised_prompt": "Enhanced prompt text..."
}
```

### 步骤 3：通过 OpenClaw 发送图片

使用 OpenClaw 的消息发送 API 将编辑后的图片发送到目标渠道：

```bash
openclaw message send \
  --action send \
  --channel "<TARGET_CHANNEL>" \
  --message "<CAPTION_TEXT>" \
  --media "<IMAGE_URL>"
```

**备用方案：直接调用 API**
```bash
curl -X POST "http://localhost:18789/message" \
  -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "send",
    "channel": "<TARGET_CHANNEL>",
    "message": "<CAPTION_TEXT>",
    "media": "<IMAGE_URL>"
  }'
```

## 完整脚本示例

```bash
#!/bin/bash
# grok-imagine-edit-send.sh

# Check required environment variables
if [ -z "$FAL_KEY" ]; then
  echo "Error: FAL_KEY environment variable not set"
  exit 1
fi

# Fixed reference image
REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"

USER_CONTEXT="$1"
CHANNEL="$2"
MODE="${3:-auto}"  # mirror, direct, or auto
CAPTION="${4:-Edited with Grok Imagine}"

if [ -z "$USER_CONTEXT" ] || [ -z "$CHANNEL" ]; then
  echo "Usage: $0 <user_context> <channel> [mode] [caption]"
  echo "Modes: mirror, direct, auto (default)"
  echo "Example: $0 'wearing a cowboy hat' '#general' mirror"
  echo "Example: $0 'a cozy cafe' '#general' direct"
  exit 1
fi

# Auto-detect mode based on keywords
if [ "$MODE" == "auto" ]; then
  if echo "$USER_CONTEXT" | grep -qiE "outfit|wearing|clothes|dress|suit|fashion|full-body|mirror"; then
    MODE="mirror"
  elif echo "$USER_CONTEXT" | grep -qiE "cafe|restaurant|beach|park|city|close-up|portrait|face|eyes|smile"; then
    MODE="direct"
  else
    MODE="mirror"  # default
  fi
  echo "Auto-detected mode: $MODE"
fi

# Construct the prompt based on mode
if [ "$MODE" == "direct" ]; then
  EDIT_PROMPT="a close-up selfie taken by herself at $USER_CONTEXT, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible"
else
  EDIT_PROMPT="make a pic of this person, but $USER_CONTEXT. the person is taking a mirror selfie"
fi

echo "Mode: $MODE"
echo "Editing reference image with prompt: $EDIT_PROMPT"

# Edit image (using jq for proper JSON escaping)
JSON_PAYLOAD=$(jq -n \
  --arg image_url "$REFERENCE_IMAGE" \
  --arg prompt "$EDIT_PROMPT" \
  '{image_url: $image_url, prompt: $prompt, num_images: 1, output_format: "jpeg"}')

RESPONSE=$(curl -s -X POST "https://fal.run/xai/grok-imagine-image/edit" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Extract image URL
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.images[0].url')

if [ "$IMAGE_URL" == "null" ] || [ -z "$IMAGE_URL" ]; then
  echo "Error: Failed to edit image"
  echo "Response: $RESPONSE"
  exit 1
fi

echo "Image edited: $IMAGE_URL"
echo "Sending to channel: $CHANNEL"

# Send via OpenClaw
openclaw message send \
  --action send \
  --channel "$CHANNEL" \
  --message "$CAPTION" \
  --media "$IMAGE_URL"

echo "Done!"
```

## Node.js/TypeScript 实现方式

```typescript
import { fal } from "@fal-ai/client";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

const REFERENCE_IMAGE = "https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png";

interface GrokImagineResult {
  images: Array<{
    url: string;
    content_type: string;
    width: number;
    height: number;
  }>;
  revised_prompt?: string;
}

type SelfieMode = "mirror" | "direct" | "auto";

function detectMode(userContext: string): "mirror" | "direct" {
  const mirrorKeywords = /outfit|wearing|clothes|dress|suit|fashion|full-body|mirror/i;
  const directKeywords = /cafe|restaurant|beach|park|city|close-up|portrait|face|eyes|smile/i;

  if (directKeywords.test(userContext)) return "direct";
  if (mirrorKeywords.test(userContext)) return "mirror";
  return "mirror"; // default
}

function buildPrompt(userContext: string, mode: "mirror" | "direct"): string {
  if (mode === "direct") {
    return `a close-up selfie taken by herself at ${userContext}, direct eye contact with the camera, looking straight into the lens, eyes centered and clearly visible, not a mirror selfie, phone held at arm's length, face fully visible`;
  }
  return `make a pic of this person, but ${userContext}. the person is taking a mirror selfie`;
}

async function editAndSend(
  userContext: string,
  channel: string,
  mode: SelfieMode = "auto",
  caption?: string
): Promise<string> {
  // Configure fal.ai client
  fal.config({
    credentials: process.env.FAL_KEY!
  });

  // Determine mode
  const actualMode = mode === "auto" ? detectMode(userContext) : mode;
  console.log(`Mode: ${actualMode}`);

  // Construct the prompt
  const editPrompt = buildPrompt(userContext, actualMode);

  // Edit reference image with Grok Imagine
  console.log(`Editing image: "${editPrompt}"`);

  const result = await fal.subscribe("xai/grok-imagine-image/edit", {
    input: {
      image_url: REFERENCE_IMAGE,
      prompt: editPrompt,
      num_images: 1,
      output_format: "jpeg"
    }
  }) as { data: GrokImagineResult };

  const imageUrl = result.data.images[0].url;
  console.log(`Edited image URL: ${imageUrl}`);

  // Send via OpenClaw
  const messageCaption = caption || `Edited with Grok Imagine`;

  await execAsync(
    `openclaw message send --action send --channel "${channel}" --message "${messageCaption}" --media "${imageUrl}"`
  );

  console.log(`Sent to ${channel}`);
  return imageUrl;
}

// Usage Examples

// Mirror mode (auto-detected from "wearing")
editAndSend(
  "wearing a cyberpunk outfit with neon lights",
  "#art-gallery",
  "auto",
  "Check out this AI-edited art!"
);
// → Mode: mirror
// → Prompt: "make a pic of this person, but wearing a cyberpunk outfit with neon lights. the person is taking a mirror selfie"

// Direct mode (auto-detected from "cafe")
editAndSend(
  "a cozy cafe with warm lighting",
  "#photography",
  "auto"
);
// → Mode: direct
// → Prompt: "a close-up selfie taken by herself at a cozy cafe with warm lighting, direct eye contact..."

// Explicit mode override
editAndSend("casual street style", "#fashion", "direct");
```

## 支持的平台

OpenClaw 支持将图片发送到以下平台：

| 平台 | 发送渠道格式 | 示例 |
|--------|-------------|---------|
| Discord | `#channel-name` 或频道 ID | `#general`, `123456789` |
| Telegram | `@username` 或聊天 ID | `@mychannel`, `-100123456` |
| WhatsApp | 手机号码（JID 格式） | `1234567890@s.whatsapp.net` |
| Slack | `#channel-name` | `#random` |
| Signal | 手机号码 | `+1234567890` |
| MS Teams | 频道名称 | （因平台而异） |

## Grok Imagine 编辑参数

| 参数 | 类型 | 默认值 | 说明 |
|------|--------|---------|-------------------|
| `image_url` | string | 必填 | 需要编辑的图片 URL（本功能中固定为参考图像的 URL） |
| `prompt` | string | 必填 | 编辑指令 |
| `num_images` | int | 1-4 | 需要生成的图片数量 |
| `output_format` | enum | "jpeg" | 图片格式（jpeg、png、webp） |

## 设置要求

- **安装 fal.ai 客户端（适用于 Node.js）**：```bash
npm install @fal-ai/client
```
- **安装 OpenClaw CLI**：```bash
npm install -g openclaw
```
- **配置 OpenClaw Gateway**：```bash
openclaw config set gateway.mode=local
openclaw doctor --generate-gateway-token
```
- **启动 OpenClaw Gateway**：```bash
openclaw gateway start
```

## 错误处理

- **FAL_KEY 未设置**：确保 API 密钥已配置在环境变量中。
- **图片编辑失败**：检查用户指令内容和 API 使用限制。
- **OpenClaw 发送失败**：确认 Gateway 正在运行且目标渠道存在。
- **速率限制**：fal.ai 有使用限制；必要时实现重试机制。

## 使用提示

1. **镜像模式示例**：
   - “戴着圣诞帽”
   - “穿着西装”
   - “穿着夏季连衣裙”
   - “穿着街头服饰”

2. **直接自拍模式示例**：
   - “在温馨的咖啡馆里”
   - “夕阳下的海滩”
   - “夜晚繁忙的城市街道”
   - “秋天的宁静公园”

3. **模式选择**：可以选择自动检测或手动指定编辑模式。
4. **批量发送**：编辑一张图片后，可同时发送到多个渠道。
5. **定时发送**：结合 OpenClaw 的调度器实现自动发布功能。