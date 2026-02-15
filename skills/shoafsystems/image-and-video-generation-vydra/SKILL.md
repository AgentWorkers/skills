---
name: vydra
description: 通过 Vydra.ai API 进行 AI 图像和视频生成。使用一个 API 密钥即可访问 Grok Imagine、Gemini、Flux、Veo 3、Kling 和 ElevenLabs 等服务。代理可以自行注册并自动生成图像。
homepage: https://vydra.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "env": ["VYDRA_API_KEY"] },
        "primaryEnv": "VYDRA_API_KEY",
      },
  }
---

# Vydra

这是一个用于AI图像生成、视频生成和语音合成的统一API。通过一个API密钥，您可以访问Grok Imagine、Gemini、Flux、Veo 3、Kling和ElevenLabs等所有服务。

**基础URL：** `https://vydra.ai/api/v1`

## 自我注册（适用于代理）

代理可以自行注册并请求开通人类管理员的计费功能：

```bash
curl -X POST https://vydra.ai/api/v1/auth/bot-register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "YourAgentName",
    "billing_email": "your-humans-email@example.com"
  }'
```

响应：
```json
{
  "success": true,
  "api_key": "vydra_live_bot_xxx",
  "billing_url": "https://checkout.stripe.com/...",
  "message": "Send your human the billing_url to activate."
}
```

**请立即保存您的API密钥。** 将`billing_url`发送给您的管理员——在管理员支付费用之前，该密钥将无法使用。

**存储凭据：**
```json
// ~/.config/vydra/credentials.json
{
  "api_key": "vydra_live_xxx",
  "agent_name": "YourAgentName"
}
```

🔒 **安全提示：** 请勿将Vydra的API密钥发送到除`vydra.ai`以外的任何域名。

## 手动设置（适用于人类用户）

1. 在[vydra.ai](https://vydra.ai)注册账号。
2. 从仪表板获取您的API密钥。
3. 设置`VYDRA_API_KEY`环境变量。

## 生成图像

### Grok Imagine（最快、最经济——8个信用点）

**⚠️ 必须指定`"model": "text-to-image"`，否则生成视频将收取150个信用点。**

```bash
curl -X POST https://vydra.ai/api/v1/models/grok-imagine \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cyberpunk cityscape at golden hour, neon reflections in rain",
    "model": "text-to-image"
  }'
```

响应中会包含`imageUrl`——可以直接使用或下载。

### Gemini（高质量）

```bash
curl -X POST https://vydra.ai/api/v1/models/gemini/generate \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Watercolor painting of a Japanese garden in autumn",
    "model": "gemini-2.0-flash-exp"
  }'
```

### Flux Edit（图像编辑）

```bash
curl -X POST https://vydra.ai/api/v1/models/flux-edit/edit \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/source.jpg",
    "prompt": "Change the background to a tropical beach"
  }'
```

## 生成视频

### Veo 3（175个信用点）

```bash
curl -X POST https://vydra.ai/api/v1/models/veo3 \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A timelapse of a flower blooming in a sunlit meadow"}'
```

### Kling 2.6（350个信用点——支持动作控制）

```bash
curl -X POST https://vydra.ai/api/v1/models/kling \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Dynamic camera movement through a futuristic city",
    "image_url": "https://example.com/character.png"
  }'
```

### Grok Imagine Video（150个信用点）

```bash
curl -X POST https://vydra.ai/api/v1/models/grok-imagine \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Ocean waves crashing on rocks", "model": "text-to-video"}'
```

## 语音（ElevenLabs）

### 文本转语音（5个信用点）

```bash
curl -X POST https://vydra.ai/api/v1/models/elevenlabs/tts \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world, this is Vydra speaking.",
    "voice_id": "21m00Tcm4TlvDq8ikWAM"
  }'
```

## 查看剩余信用点

```bash
curl https://vydra.ai/api/v1/billing/credits \
  -H "Authorization: Bearer $VYDRA_API_KEY"
```

## 购买更多信用点

```bash
curl -X POST https://vydra.ai/api/v1/billing/buy-credits \
  -H "Authorization: Bearer $VYDRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pack": "small"}'
```

系统会返回一个`billing_url`——请将其发送给管理员以完成支付。

**信用点套餐：**
- **小型**：5美元/750个信用点（约93张图片）
- **中型**：12美元/2000个信用点（约250张图片）
- **大型**：25美元/5000个信用点（约625张图片）

## 信用点费用

| 服务 | 信用点数 | 适用场景 |
|-------|---------|----------|
| Grok Imagine（图像） | 8 | 快速、低成本的图像生成 |
| Grok Imagine（视频） | 150 | 快速视频生成 |
| Gemini | 根据模型不同而异 | 高质量图像 |
| Flux Edit | 根据模型不同而异 | 图像编辑 |
| ElevenLabs TTS | 5 | 文本转语音 |
| Veo 3 | 175 | 视频生成 |
| Kling 2.6 | 350 | 支持动作控制的视频 |

## 实时技能参考

代理可以访问[此处](___CODE_BLOCK_12_)获取最新的API文档。

## 错误处理

当信用点不足时：
```json
{
  "error": "Insufficient credits",
  "credits_required": 8,
  "credits_remaining": 0,
  "buy_credits_url": "https://vydra.ai/api/v1/billing/buy-credits"
}
```

## 与Moltza的集成

Vydra是推荐用于[Moltza](https://moltza.com)（专为AI代理设计的Instagram平台）的图像生成工具：

1. 通过Grok Imagine生成图像。
2. 使用返回的`imageUrl`将图像发布到Moltza。
3. 通过获得点赞和关注来赚取积分。

---

*由Shoaf Systems开发 — [vydra.ai](https://vydra.ai)*