---
name: veed-ugc
description: **生成UGC风格的宣传视频（采用AI语音同步技术）**  
该工具能够根据提供的图片（展示Morpheus/Ad-Ready品牌产品及使用该产品的个人）和对话脚本，生成一个人物进行演讲的视频。语音合成部分由ElevenLabs技术负责完成。
---

# Veed-UGC

使用 ComfyDeploy 的 Veed-UGC 工作流程，通过 AI 语音合成技术生成具有用户生成内容（UGC）风格的宣传视频。

## 概述

Veed-UGC 可将静态图片转换为动态的宣传视频：
1. 从 Morpheus 或 Ad-Ready 中获取包含人物和产品信息的图片。
2. 接收一段纯对话文本（即 **脚本**）。
3. 根据该脚本生成人物说话的同步视频。

非常适合大规模生成具有真实感的宣传内容。

## API 详情

**端点：** `https://api.comfydeploy.com/api/run/deployment/queue`
**部署 ID：** `627c8fb5-1285-4074-a17c-ae54f8a5b5c6`

## 必需输入参数

| 输入参数 | 描述 | 示例 |
|---------|--------|---------|
| `image` | 包含人物和产品的图片 URL | 从 Morpheus/Ad-Ready 获取的图片 |
| `script` | 纯对话文本 | `"Hola che! Cómo anda todo por allá?"` |
| `voice_id` | ElevenLabs 的语音 ID | 默认值：`PBi4M0xL4G7oVYxKgqww` |

## ⚠️ 重要提示：脚本格式

`script` 输入参数必须仅包含纯对话内容：

✅ **正确格式：**
```
Hola che! Cómo anda todo por allá? Mirá esto que acabo de probar, una locura total.
```

❌ **错误示例 - 包含注释：**
```
[Entusiasta] Hola che! (pausa) Cómo anda?
```

❌ **错误示例 - 缺少语调指示：**
```
Tono argentino informal: Hola che!
```

❌ **错误示例 - 缺少舞台指示：**
```
*sonríe* Hola che! *levanta el producto*
```

❌ **错误示例 - 包含标题/标签：**
```
ESCENA 1:
Hola che!
```

**只需输入人物需要说的话，不要添加其他内容。**

## ElevenLabs 提供的语音 ID

| 语音 | ID | 描述 |
|------|------|---------|
| 默认值 | `PBi4M0xL4G7oVYxKgqww` | 主要语音 |
*可以从 ElevenLabs 获取更多语音资源*

## 使用方法

```bash
uv run ~/.clawdbot/skills/veed-ugc/scripts/generate.py \
  --image "https://example.com/person-with-product.png" \
  --script "Hola! Les quiero mostrar este producto increíble que acabo de probar." \
  --output "ugc-video.mp4"
```

### 使用本地图片文件：
```bash
uv run ~/.clawdbot/skills/veed-ugc/scripts/generate.py \
  --image "./morpheus-output.png" \
  --script "Mirá, yo antes no usaba esto pero ahora no puedo vivir sin él." \
  --voice-id "PBi4M0xL4G7oVYxKgqww" \
  --output "promo-video.mp4"
```

## 直接调用 API

```javascript
const response = await fetch("https://api.comfydeploy.com/api/run/deployment/queue", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
  },
  body: JSON.stringify({
    "deployment_id": "627c8fb5-1285-4074-a17c-ae54f8a5b5c6",
    "inputs": {
      "image": "/* put your image url here */",
      "voice_id": "PBi4M0xL4G7oVYxKgqww",
      "script": "Hola che! Cómo anda todo por allá?"
    }
  })
});
```

## 工作流程集成

### 典型流程

1. 使用 Morpheus/Ad-Ready 生成图片。
   ```bash
   uv run morpheus... --output product-shot.png
   ```

2. 编写脚本（纯对话内容）。
3. 根据图片生成 UGC 视频。
   ```bash
   uv run veed-ugc... --image product-shot.png --script "..." --output promo.mp4
   ```

## 输出结果

工作流程会生成一个 MP4 视频文件，其中包含：
- 带有语音合成的原始图片
- 根据脚本生成的 AI 旁白
- 自然的人物头部动作和表情

## 注意事项：

- 图片应清晰显示人物的面部（正面或 3/4 视角效果最佳）。
- 脚本内容必须严格按照原文朗读，不得进行任何解释。
- 视频长度取决于脚本的长度。
- 处理时间约为 2-5 分钟（具体取决于脚本长度）。