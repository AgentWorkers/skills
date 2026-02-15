---
name: google-gemini-media
description: 使用 Gemini API（用于生成 Nano Banana 图像、处理 Veo 视频、以及实现 Gemini TTS 语音和音频理解功能），来构建端到端的多模态媒体工作流程，并提供相应的代码模板，以实现“生成 + 理解”的完整流程。
license: MIT
---

# Gemini 多模态媒体（图像/视频/语音）技能

## 1. 目标与范围

本技能将 Gemini 的六项 API 功能整合为可重用的工作流程和实现模板：

- **图像生成**（Nano Banana：文本转图像、图像编辑、多轮迭代）
- **图像理解**（字幕/问答/分类/比较、多图像提示；支持内联和文件 API）
- **视频生成**（Veo 3.1：文本转视频、宽高比/分辨率控制、参考图像指导、首/尾帧、视频扩展、原生音频）
- **视频理解**（上传/内联/YouTube URL；摘要、问答、带时间戳的证据）
- **语音生成**（Gemini 原生 TTS：单声道和多声道；可控制风格/口音/语速/语气）
- **音频理解**（上传/内联；描述、转录、时间范围转录、词元计数）

> **约定**：本技能遵循官方的 Google Gen AI SDK（Node.js/REST）作为主要规范；目前仅提供 Node.js/REST 示例。如果您的项目使用了其他语言或框架，请将本技能的请求结构、模型选择和 I/O 规范映射到您的封装层中。

---

## 2. 快速选择功能

1) **需要生成图像吗？**
- 需要从零开始生成图像或根据现有图像进行编辑 -> 使用 **Nano Banana 图像生成**（见第 5 节）

2) **需要理解图像吗？**
- 需要识别、描述、问答、比较或提取信息 -> 使用 **图像理解**（见第 6 节）

3) **需要生成视频吗？**
- 需要生成 8 秒的视频（可选包含原生音频） -> 使用 **Veo 3.1 视频生成**（见第 7 节）

4) **需要理解视频吗？**
- 需要生成摘要/问答/带时间戳的片段 -> 使用 **视频理解**（见第 8 节）

5) **需要朗读文本吗？**
- 需要可控制的旁白、播客/有声书风格等 -> 使用 **语音生成（TTS）**（见第 9 节）

6) **需要理解音频吗？**
- 需要音频描述、转录、时间范围转录、词元计数 -> 使用 **音频理解**（见第 10 节）

---

## 3. 统一的工程约束和 I/O 规范（必须阅读）

### 3.0 先决条件（依赖项和工具）

- Node.js 18+（与您的项目版本匹配）
- 安装 SDK（示例）：
```bash
npm install @google/genai
```
- REST 示例仅需要 `curl`；如果需要解析图像 Base64，可以安装 `jq`（可选）。

### 3.1 认证和环境变量

- 将您的 API 密钥放入 `GEMINI_API_KEY`
- REST 请求使用 `x-goog-api-key: $GEMINI_API_KEY`

### 3.2 两种文件输入模式：内联 vs 文件 API

**内联（嵌入字节/Base64）**
- 优点：调用链较短，适合小文件。
- 关键限制：总请求大小（文本提示 + 系统指令 + 嵌入字节）通常有约 20MB 的上限。

**文件 API（上传后引用）**
- 优点：适合大文件、重复使用同一文件或多轮对话。
- 常见流程：
  1. `files.upload(...)`（SDK）或 `POST /upload/v1beta/files`（REST 可暂停）
  2. 在 `generateContent` 中使用 `file_data` / `file_uri`

> **工程建议**：实现 `ensure_file_uri()`，以便当文件超过阈值（例如 10-15MB）或被重复使用时，自动通过文件 API 处理。

### 3.3 二进制媒体输出的统一处理

- **图像**：通常以 `inline_data`（Base64）的形式返回在响应中；在 SDK 中使用 `part.as_image()` 或解码 Base64 并保存为 PNG/JPG。
- **语音（TTS）**：通常返回 **PCM** 字节（Base64）；保存为 `.pcm` 或封装为 `.wav`（常见为 24kHz，16 位，单声道）。
- **视频（Veo）**：长时间异步任务；轮询操作；下载文件（或使用返回的 URI）。

---

## 4. 模型选择矩阵（根据场景选择）

> **重要提示**：模型名称、版本、限制和配额可能会随时间变化。使用前请核对官方文档。最后更新：2026-01-22。

### 4.1 图像生成（Nano Banana）
- **gemini-2.5-flash-image**：优化了速度/吞吐量；适合频繁、低延迟的生成/编辑。
- **gemini-3-pro-image-preview**：更强的指令遵循能力和高保真度文本渲染；更适合专业资产和复杂编辑。

### 4.2 通用图像/视频/音频理解
- 文档中使用 `gemini-3-flash-preview` 进行图像、视频和音频理解（根据需要选择更强大的模型以获得更好的质量和成本效益）。

### 4.3 视频生成（Veo）
- 示例模型：`veo-3.1-generate-preview`（生成 8 秒的视频，并可原生生成音频）。

### 4.4 语音生成（TTS）
- 示例模型：`gemini-2.5-flash-preview-tts**（原生 TTS，目前处于预览阶段）。

---

## 5. 图像生成（Nano Banana）

### 5.1 文本转图像

**SDK（Node.js）最小模板**
```js
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents:
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
});

const parts = response.candidates?.[0]?.content?.parts ?? [];
for (const part of parts) {
  if (part.text) console.log(part.text);
  if (part.inlineData?.data) {
    fs.writeFileSync("out.png", Buffer.from(part.inlineData.data, "base64"));
  }
}
```

**REST（带 imageConfig）最小模板**
```bash
curl -s -X POST   "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"   -H "x-goog-api-key: $GEMINI_API_KEY"   -H "Content-Type: application/json"   -d '{
    "contents":[{"parts":[{"text":"Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"}]}],
    "generationConfig": {"imageConfig": {"aspectRatio":"16:9"}}
  }'
```

**REST 图像解析（Base64 解码）**
```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"A minimal studio product shot of a nano banana"}]}]}' \
  | jq -r '.candidates[0].content.parts[] | select(.inline_data) | .inline_data.data' \
  | base64 --decode > out.png

# macOS can use: base64 -D > out.png
```

### 5.2 文本和图像转图像

**用例**：给定一张图像，**添加/删除/修改元素**，更改风格、颜色分级等。

**SDK（Node.js）最小模板**
```js
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const prompt =
  "Add a nano banana on the table, keep lighting consistent, cinematic tone.";
const imageBase64 = fs.readFileSync("input.png").toString("base64");

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: [
    { text: prompt },
    { inlineData: { mimeType: "image/png", data: imageBase64 } },
  ],
});

const parts = response.candidates?.[0]?.content?.parts ?? [];
for (const part of parts) {
  if (part.inlineData?.data) {
    fs.writeFileSync("edited.png", Buffer.from(part.inlineData.data, "base64"));
  }
}
```

### 5.3 多轮图像迭代（多轮编辑）

最佳实践：使用聊天进行连续迭代（例如：先生成图像，然后“仅编辑特定区域/元素”，接着“以相同风格制作变体”）。
- 要输出混合的“文本 + 图像”结果，将 `response_modalities` 设置为 `["TEXT", "IMAGE"]`。

### 5.4 ImageConfig

您可以在 `generationConfig.imageConfig` 或 SDK 配置中设置：
- `aspectRatio`：例如 `16:9`，`1:1`。
- `imageSize`：例如 `2K`，`4K`（更高分辨率通常速度更慢/成本更高，且模型支持可能有所不同）。

---

## 6. 图像理解（图像理解）

### 6.1 提供输入图像的两种方式

- **内联图像数据**：适合小文件（总请求大小 < 20MB）。
- **文件 API 上传**：更适合大文件或在多个请求中重复使用。

### 6.2 内联图像（Node.js）最小模板**
```js
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const imageBase64 = fs.readFileSync("image.jpg").toString("base64");

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: [
    { inlineData: { mimeType: "image/jpeg", data: imageBase64 } },
    { text: "Caption this image, and list any visible brands." },
  ],
});

console.log(response.text);
```

### 6.3 使用文件 API 上传和引用（Node.js）最小模板**
```js
import { GoogleGenAI, createPartFromUri, createUserContent } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const uploaded = await ai.files.upload({ file: "image.jpg" });

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: createUserContent([
    createPartFromUri(uploaded.uri, uploaded.mimeType),
    "Caption this image.",
  ]),
});

console.log(response.text);
```

### 6.4 多图像提示

将多个图像作为多个 `Part` 条目添加到相同的 `contents` 中；您可以混合上传的参考图像和内联字节。

---

## 7. 视频生成（Veo 3.1）

### 7.1 核心功能（必须了解）
- 生成 **8 秒** 的高保真视频，可选 720p / 1080p / 4k，并支持原生音频生成（对话、环境音效）。
- 支持：
  - 宽高比（16:9 / 9:16）
  - 视频扩展（扩展生成的视频；通常限于 720p）
  - 首/尾帧控制（特定帧）
  - 最多 3 张参考图像（基于图像的方向）

### 7.2 SDK（Node.js）最小模板：异步轮询 + 下载
```js
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const prompt =
  "A cinematic shot of a cat astronaut walking on the moon. Include subtle wind ambience.";
let operation = await ai.models.generateVideos({
  model: "veo-3.1-generate-preview",
  prompt,
  config: { resolution: "1080p" },
});

while (!operation.done) {
  await new Promise((resolve) => setTimeout(resolve, 10_000));
  operation = await ai.operations.getVideosOperation({ operation });
}

const video = operation.response?.generatedVideos?.[0]?.video;
if (!video) throw new Error("No video returned");
await ai.files.download({ file: video, downloadPath: "out.mp4" });
```

### 7.3 REST 最小模板：predictLongRunning + 轮询 + 下载

**关键点**：Veo REST 使用 `:predictLongRunning` 返回操作名称，然后轮询 `GET /v1beta/{operation_name}`；完成后，从响应中的视频 URI 下载文件。

### 7.4 常见控制（建议使用统一封装）

- `aspectRatio`：`"16:9"` 或 `"9:16"`
- `resolution`：`"720p" | "1080p" | "4k"`（更高分辨率通常速度更慢/成本更高）
- 在编写提示时：将对话放在引号中；明确说明音效和环境音效；使用电影语言（摄像机位置、移动、构图、镜头效果、氛围）。
- **负面限制**：如果 API 支持负面提示字段，请使用它；否则列出您不希望显示的元素。

### 7.5 重要限制（需要工程回退）

- 延迟可能从几秒到几分钟不等；实现超时和重试。
- 生成的视频仅在服务器上保留有限时间（请及时下载）。
- 输出包含 SynthID 水印。

**轮询回退（带超时/退避）伪代码**
```js
const deadline = Date.now() + 300_000; // 5 min
let sleepMs = 2000;
while (!operation.done && Date.now() < deadline) {
  await new Promise((resolve) => setTimeout(resolve, sleepMs));
  sleepMs = Math.min(Math.floor(sleepMs * 1.5), 15_000);
  operation = await ai.operations.getVideosOperation({ operation });
}
if (!operation.done) throw new Error("video generation timed out");
```

---

## 8. 视频理解（视频理解）

### 8.1 视频输入选项
- **文件 API 上传**：当文件大于 100MB、视频长度超过 1 分钟或需要重复使用时推荐。
- **内联视频数据**：适用于较小文件。
- **直接 YouTube URL**：可以分析公共视频。

### 8.2 文件 API（Node.js）最小模板**
```js
import { GoogleGenAI, createPartFromUri, createUserContent } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const uploaded = await ai.files.upload({ file: "sample.mp4" });

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: createUserContent([
    createPartFromUri(uploaded.uri, uploaded.mimeType),
    "Summarize this video. Provide timestamps for key events.",
  ]),
});

console.log(response.text);
```

### 8.3 时间戳提示策略
- 请求带有“(mm:ss)”时间戳的分段列表。
- 如果需要，要求提供“带特定时间范围的证据”并在同一提示中包含结构化的提取内容（JSON）。

---

## 9. 语音生成（文本转语音，TTS）

### 9.1 定位
- **原生 TTS**：适用于“精确朗读 + 可控制风格”（播客、有声书、广告旁白等）。
- 与 Live API 区分：Live API 更具交互性且是非结构化的音频/多模态对话；TTS 专注于可控的旁白。

### 9.2 单声道 TTS（Node.js）最小模板**
```js
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-preview-tts",
  contents: [{ parts: [{ text: "Say cheerfully: Have a wonderful day!" }] }],
  config: {
    responseModalities: ["AUDIO"],
    speechConfig: {
      voiceConfig: {
        prebuiltVoiceConfig: { voiceName: "Kore" },
      },
    },
  },
});

const data =
  response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data ?? "";
if (!data) throw new Error("No audio returned");
fs.writeFileSync("out.pcm", Buffer.from(data, "base64"));
```

### 9.3 多声道 TTS（最多 2 个声道）
- **要求**：
- 使用 `multiSpeakerVoiceConfig`
- 每个说话者的名称必须与提示中的对话标签匹配（例如，Joe/Jane）。

### 9.4 语音选项和语言
- `voice_name` 支持 30 个预建语音（例如 Zephyr, Puck, Charon, Kore 等）。
- 模型可以自动检测输入语言并支持 24 种语言（详见文档）。

### 9.5 “导演备注”（强烈推荐用于高质量语音）
提供对风格、语速、口音等的可控指导，但避免过度限制。

---

## 10. 音频理解（音频理解）

### 10.1 常见任务
- 描述音频内容（包括非语音内容，如鸟鸣、警报等）
- 生成转录文本
- 转录特定时间范围
- 计算词元数量（用于成本估算/分段）

### 10.2 文件 API（Node.js）最小模板**
```js
import { GoogleGenAI, createPartFromUri, createUserContent } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const uploaded = await ai.files.upload({ file: "sample.mp3" });

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: createUserContent([
    "Describe this audio clip.",
    createPartFromUri(uploaded.uri, uploaded.mimeType),
  ]),
});

console.log(response.text);
```

### 10.3 关键限制和工程提示
- 支持常见格式：WAV/MP3/AIFF/AAC/OGG/FLAC。
- 音频分词：大约每秒 32 个词元（大约每分钟 1920 个词元；数值可能变化）。
- 每个提示的总音频长度限制为 9.5 小时；多通道音频会被降混；音频会被重新采样（详见文档）。
- 如果总请求大小超过 20MB，必须使用文件 API。

---

## 11. 端到端示例（组合使用）

### 示例 A：图像生成 -> 通过理解进行验证
1) 使用 Nano Banana 生成产品图像（需要排除不需要的元素，保持一致的照明）。
2) 使用图像理解进行自我检查：验证文本清晰度、品牌拼写和不安全的元素。
3) 如果不满意，将生成的图像输入到文本+图像编辑中并迭代。

### 示例 B：视频生成 -> 视频理解 -> 旁白脚本
1) 使用 Veo 生成 8 秒的视频（包含对话或音效）。
2) 下载并保存（遵守保留时间）。
3) 将视频上传到视频理解工具以生成故事板 + 时间戳 + 旁白脚本（然后输入到 TTS）。

### 示例 C：音频理解 -> 时间范围转录 -> TTS 重新配音
1) 上传会议音频并转录全部内容。
2) 转录或总结特定时间范围。
3) 使用 TTS 生成摘要的“广播”版本。

---

## 12. 合规性和风险（必须遵守）

- 确保您有上传图像/视频/音频的必要权限；不要生成侵权、欺骗性、骚扰性或有害的内容。
- 生成的图像和视频包含 SynthID 水印；视频可能还有地区/个人生成的限制。
- 生产系统必须实现超时、重试、故障回退和对生成内容的人工审核/后期处理。

---

## 13. 快速参考（检查清单）

- [ ] 选择正确的模型：图像生成（Flash Image / Pro Image Preview）、视频生成（Veo 3.1）、TTS（Gemini 2.5 TTS）、理解（Gemini Flash/Pro）。
- [ ] 选择正确的输入模式：小文件使用内联；大文件或重复使用使用文件 API。
- [ ] 正确解析二进制输出：图像/音频通过内联数据解码；视频通过操作轮询 + 下载。
- [ ] 对于视频生成：设置宽高比/分辨率，并及时下载（避免过期）。
- [ ] 对于 TTS：设置 `response_modalities=["AUDIO"]`；最多 2 个声道；说话者名称必须与提示匹配。
- [ ] 对于音频理解：在需要时计算词元数量；分段处理长音频或使用文件 API。