---
name: seisoai
description: "通过 SeisoAI（包含 120 多种工具）生成图像、视频、音乐和 3D 模型以及音频。采用按请求计费的模式，基础费用为 x402 USDC。当用户需要生成、编辑、放大图像或训练 AI 内容时，可以使用该服务。"
homepage: https://seisoai.com
version: 2.1.0
last_synced: 2026-02-15
files: ["scripts/x402-sign.mjs", "scripts/package.json"]
metadata: {"openclaw": {"emoji": "🎨", "homepage": "https://seisoai.com", "requires": {"bins": ["curl", "node"], "env": ["SEISOAI_WALLET_KEY"]}, "primaryEnv": "SEISOAI_WALLET_KEY"}}
---
# SeisoAI

提供了120多种AI生成工具。支付方式：基于Base币种的x402 USDC。

## 设置

### `SEISOAI_WALLET_KEY`

这是一个用于授权通过EIP-3009 `transferWithAuthorization`向SeisoAI进行USDC支付的签名密钥。该密钥仅保存在您的设备上；签名脚本会硬编码SeisoAI的收款地址，并拒绝任何其他收款地址。

请使用一个余额在5至20美元之间的专用钱包。大多数生成服务的费用为0.01至0.33美元。

```bash
export SEISOAI_WALLET_KEY="0x<key>"
```

### 依赖项

```bash
cd {baseDir}/scripts && npm ci --ignore-scripts
```

依赖项通过lockfile进行管理。首次使用前请运行一次该脚本。

## 发现（Discovery）

```bash
curl -s "https://seisoai.com/api/gateway/tools"
curl -s "https://seisoai.com/api/gateway/tools/{toolId}"
curl -s "https://seisoai.com/api/gateway/price/{toolId}"
```

## 调用（完整的x402流程）

### 第1步：发送请求，接收402挑战

```bash
CHALLENGE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "https://seisoai.com/api/gateway/invoke/{toolId}" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "..."}')
# Expect HTTP 402. Capture the full body:
BODY=$(curl -s -X POST "https://seisoai.com/api/gateway/invoke/{toolId}" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "..."}')
echo "$BODY"
```

402响应中包含标准的x402支付挑战信息：

```json
{
  "x402Version": 2,
  "error": "Payment required",
  "resource": { "url": "...", "description": "...", "mimeType": "application/json" },
  "accepts": [{
    "scheme": "exact",
    "network": "eip155:8453",
    "maxAmountRequired": "32500",
    "asset": "USDC",
    "payTo": "0xa0aE05e2766A069923B2a51011F270aCadFf023a",
    "extra": { "priceUsd": "$0.0325" }
  }]
}
```

`PAYMENT-REQUIRED`响应头中包含了相同的payload（已进行Base64编码）。

### 第2步：向用户显示支付信息并获取批准

从402的JSON响应中解析`accepts[0]`字段，向用户展示以下信息：
- 工具名称及其功能
- 支付货币：USDC
- 金额：`maxAmountRequired`（除以1000000转换为易于阅读的美元金额）
- 收款人（`payTo`）：`0xa0aE05e2766A069923B2a51011F270aCadFf023a`（SeisoAI）
- 网络：Base（`eip155:8453`）

**等待用户的明确批准，切勿自动批准。**

### 第3步：签名并重试

```bash
PAYMENT=$(echo "$BODY" | node {baseDir}/scripts/x402-sign.mjs)

curl -s -X POST "https://seisoai.com/api/gateway/invoke/{toolId}" \
  -H "Content-Type: application/json" \
  -H "payment-signature: $PAYMENT" \
  -d '{"prompt": "..."}'
```

请求体必须与第1步完全相同。

### 第4步：处理响应

**同步模式（`executionMode: "sync"）**：结果包含在响应体中，其中包含结算信息：

```json
{
  "success": true,
  "result": { ... },
  "x402": {
    "settled": true,
    "transactionHash": "0x...",
    "amount": "32500",
    "status": "settled"
  },
  "x402_amount": "32500",
  "x402_status": "settled",
  "x402_confirmation_id": "...",
  "x402_timestamp": "2025-06-15T00:00:00.000Z",
  "x402_recipient": "0xa0aE05e2766A069923B2a51011F270aCadFf023a"
}
```

**队列模式（`executionMode: "queue"）**：每5秒轮询一次：

```bash
curl -s "https://seisoai.com/api/gateway/jobs/{jobId}?model={model}"
curl -s "https://seisoai.com/api/gateway/jobs/{jobId}/result?model={model}"
```

## 结果字段

| 类型 | 字段 | 备用值 |
|------|-------|----------|
| 图像 | `result.images[0].url` | `result.images[0]` |
| 视频 | `result.video.url` | `result.video_url` |
| 音频 | `result.audio.url` | `result.audio_url` |
| 3D模型 | `result.model_glb.url` | `result.model_mesh.url` |

## 错误处理

| HTTP状态码 | 处理方式 |
|------|--------|
| 402 | 正常情况 — 继续解析、签名并重试（按照上述步骤操作） |
| 402 + "already used" | 重新生成签名并重试 |
| 400 | 检查payload是否与工具的规范匹配（通过`GET /tools/{toolId}`查询） |
| 429 | 等待`Retry-After`秒数后重试 |
| 500 | 采用退避策略重试 |

## 工具列表（共120多种）

### 图像生成（19种工具）
`image.generate.flux-pro-kontext` $0.065 · `image.generate.flux-2` $0.03 · `image.generate.flux-2-flex` $0.03 · `image.generate.flux-2-klein-realtime` $0.016 · `image.generate.nano-banana-pro` $0.33（360°）· `image.generate.flux-controlnet-canny` $0.065 · `image.generate.grok-imagine` $0.05 · `image.generate.kling-image-v3` $0.06 · `image.generate.kling-image-o3` $0.065 · `image.generate.hunyuan-instruct` $0.05 · `image.generate.qwen-image-max` $0.04 · `image.generate.bria-fibo` $0.05 · `image.generate.seedream-4` $0.05 · `image.generate.recraft-v3` $0.05（SOTA，矢量格式）· `image.generate.omnigen-v2` $0.05（多模态尝试）· `image.generate.pulid` $0.04（面部识别）· `image.generate.imagineart` $0.05 · `training.lora-inference` $0.04`

### 图像编辑（15种工具）
`image.generate.flux-pro-kontext-edit` $0.065 · `image.generate.flux-pro-kontext-multi` $0.065 · `image.generate.flux-2-edit` $0.03 · `image.edit.flux-2-flex` $0.03（多参考图像编辑）· `image.generate.nano-banana-pro-edit` $0.33 · `image.edit.grok-imagine` $0.05 · `image.edit.seedream-4` $0.05 · `image.edit.recraft-v3` $0.05 · `image.edit.kling-image-v3` $0.06 · `image.edit.kling-image-o3` $0.065 · `image.edit.bria-fibo` $0.05 · `image.edit.reve` $0.05 · `image.face-swap` $0.03 · `image.inpaint` $0.04 · `image.outpaint` $0.04`

### 图像处理（9种工具）
`image.upscale` $0.04 · `image.upscale.topaz` $0.065（高级版）· `image.extract-layer` $0.01 · `image.background-remove` $0.01 · `image.segment.sam2` $0.01 · `image.depth.depth-anything-v2` $0.01 · `image.generate.genfocus` $0.03 · `image.generate.genfocus-all-in-focus` $0.03`

### 视觉处理（3种工具）
`vision.describe` $0.01 · `vision.describe.florence-2` $0.01（OCR，检测）· `vision.nsfw-detect` $0.007

### 视频生成（29种工具）——每秒生成速率
`video.generate.veo3` $0.13/s · `video.generate.veo3-image-to-video` $0.13/s · `video.generate.veo3-first-last-frame` $0.13/s · `video.generate.veo3-reference` $0.13/s · `video.generate.sora-2-text` $0.20/s · `video.generate.sora-2-image` $0.20/s · `video.generate.sora-2-pro-text` $0.26/s · `video.generate.sora-2-pro-image` $0.26/s · `video.generate.ltx-2-19b-image` $0.13/s · `video.generate.kling-3-pro-text` $0.20/s · `video.generate.kling-3-pro-image` $0.20/s · `video.generate.kling-3-std-text` $0.16/s · `video.generate.kling-3-std-image` $0.16/s · `video.generate.kling-o3-image` $0.18/s · `video.generate.kling-o3-reference` $0.18/s · `video.generate.kling-o3-pro-text` $0.23/s · `video.generate.kling-o3-pro-image` $0.23/s · `video.generate.kling-o3-pro-reference` $0.23/s · `video.generate.kling-o3-std-text` $0.18/s · `video.generate.grok-imagine-text` $0.16/s · `video.generate.grok-imagine-image` $0.16/s · `video.generate.vidu-q3-text` $0.18/s · `video.generate.vidu-q3-image` $0.18/s · `video.generate.wan-2.6-reference` $0.09/s · `video.generate.dreamactor-v2` $0.13/s · `video.generatepixverse-v5` $0.13/s · `video.generate.lucy-14b` $0.10/s · `audio.lip-sync` $0.05`

### 视频编辑（10种工具）
`video.animate.wan` $0.065/s · `video.edit.grok-imagine` $0.13/s · `video.edit.sora-2-remix` $0.20/s · `video.edit.kling-o3-std` $0.18/s · `video.edit.kling-o3-pro` $0.23/s · `video.generate.kling-o3-std-reference` $0.18/s · `video.generate.kling-o3-pro-reference` $0.23/s · `video.upscale.topaz` $0.13/s · `video.background-remove` $0.04/s`

### 虚拟形象与唇部同步（6种工具）
`avatar.creatify-aurora` $0.13/s · `avatar.veed-fabric` $0.13/s · `avatar.omnihuman-v15` $0.13/s · `avatar.ai-text` $0.10/s · `avatar.sync-lipsync-v2` $0.065/s · `avatar.pixverse-lipsync` $0.065/s`

### 音频生成（10种工具）
`audio.tts` $0.03 · `audio.tts.minimax-hd` $0.04 · `audio.tts.minimax-turbo` $0.03 · `audio.tts.chatterbox` $0.03 · `audio.tts.dia-voice-clone` $0.04 · `audio.personaplex` $0.05 · `audio.kling-video-to-audio` $0.05 · `audio.sfx` $0.04 · `audio.sfx.stable-audio` $0.04 · `audio.sfx.beatoven` $0.04 · `audio.sfx.mirelo-video` $0.04 · `video.video-to-audio` $0.04`

### 音频处理（2种工具）
`audio.transcribe` $0.01 · `audio.stem-separation` $0.04`

### 音乐生成（2种工具）
`music.generate` $0.03/min · `music.generate.beatoven` $0.04/min（免版税）

### 3D建模（9种工具）
`3d.image-to-3d` $0.065 · `3d.image-to-3d.hunyuan-pro` $0.13 · `3d.text-to-3d.hunyuan-pro` $0.16 · `3d.text-to-3d.hunyuan-rapid` $0.05 · `3d.text-to-3d.hunyuan-rapid` $0.065 · `3d.smart-topology` $0.04 · `3d.part-splitter` $0.04 · `3d.image-to-3d.meshy-v6` $0.10 · `3d.text-to-3d.meshy-v6` $0.10`

### 训练工具（12种工具）——每步费用
`training.flux-lora` $0.004/步 · `training.flux-2` $0.007/步 · `training.flux-2-v2` $0.007/步 · `training.flux-kontext` $0.005/步 · `training.flux-portrait` $0.005/步 · `training.flux-2-klein-4b` $0.004/步 · `training.flux-2-klein-9b` $0.005/步 · `training.qwen-image` $0.007/步 · `training.qwen-image-edit` $0.007/步 · `training.wan-video` $0.007/步 · `training.wan-22-image` $0.005/步 · `training.z-image` $0.004/步`

### 工作流辅助工具（5种工具）
`utility.trim-video` $0.007 · `utility.blend-video` $0.007 · `utility.extract-frame` $0.007 · `utility.audio-compressor` $0.007 · `utility.impulse-response` $0.007`

## Claude API功能

该聊天助手支持以下高级Anthropic API功能：
- **网络搜索**（`web_search_20250305`）：Claude可在网络上实时搜索信息，并自动标注来源。非常适合创意研究。
- **代码执行**（`code_execution_20250825`）：Claude可在沙箱环境中运行Python/Bash代码，用于数据分析、计算和可视化。
- **引用**：Claude可以从提供的文档中引用具体段落，为回答提供依据。
- **提示缓存**：系统会缓存提示信息，最多保存1小时，以降低重复对话的成本。
- **批量请求**：批量处理最多10,000个请求，费用降低50%。

## 注意事项：
- `GET /api/gateway/tools/{toolId}` 可查询完整的输入规范，请在调用前查看。
- 支付签名密钥仅限一次性使用，切勿在多次请求中重复使用。
- 请求体在402挑战和支付重试时必须保持一致。
- 最便宜的图像生成工具是`flux-2-klein-realtime`（0.016美元），最便宜的视频生成工具是`wan-2.6-reference`（0.09美元/秒）。
- 签名脚本需要`SEISOAI_WALLET_KEY`，详见上述“设置”部分。
- 该脚本仅授权向SeisoAI的指定收款地址进行支付；其他收款地址将被拒绝。