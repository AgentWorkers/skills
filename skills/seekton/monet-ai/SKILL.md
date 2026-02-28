---
name: monet-ai-skill
description: Monet AI – 一款专为AI代理设计的全面AI内容生成API。支持视频生成（Sora、Veo、Doubao Seedance、Wan、Hailuo、Kling）、图像生成（GPT-4o、Nano Banana、Seedream、Flux、Imagen、Ideogram）以及音乐生成（MiniMax Music）。通过多模型AI生成技术，帮助构建智能的工作流程。
metadata:
  openclaw:
    requires:
      env:
        - MONET_API_KEY # Required: API key from monet.vision
      bins: []
---
# Monet AI 技能

这是一个专为 AI 代理设计的全面 AI 内容生成 API。Monet AI 提供了对最先进的 AI 生成模型的统一访问权限，这些模型可用于视频（Sora、Veo、Doubao Seedance、Wan、Hailuo、Kling）、图像（GPT-4o、Nano Banana、Seedream、Flux、Imagen、Ideogram）和音乐（MiniMax Music）的生成。您可以利用这些模型构建智能工作流程，以实现自动化的内容创作。

## 使用场景

在以下情况下使用此技能：

- **视频生成**：使用最先进的模型根据文本提示生成 AI 视频：
  - **Sora**：OpenAI 的视频生成模型，可生成高质量、逼真的视频
  - **Veo**：Google 的视频生成模型
  - **Doubao Seedance**：ByteDance 的 AI 视频模型，支持音视频同步
  - **Wan**：Alibaba 的视频生成模型，具有出色的本地化支持
  - **Hailuo**：生成速度快，画质与速度平衡良好
  - **Kling**：Kuaishou 的视频生成模型
- **图像生成**：根据文本描述生成具有多种艺术风格的图像：
  - **GPT-4o**：OpenAI 的多模态图像生成模型
  - **Nano Banana**：Google 的图像模型，具有极高的角色一致性
  - **Seedream**：ByteDance 的智能视觉推理模型
  - **Wan**：Alibaba 的图像模型，可生成高质量且富有表现力的图像
  - **Flux**：生成高质量、逼真的图像
  - **Imagen**：Google 的文本到图像模型
  - **Ideogram**：专门用于文本渲染和精确构图
- **音乐生成**：根据文本描述创建原创音乐和音频：
  - **MiniMax Music**：支持自定义歌词和文本到音乐的转换的 AI 音乐生成工具

- **AI 代理集成**：结合多种 AI 生成能力，构建智能工作流程，以实现自动化的内容创作流程

## 获取 API 密钥

1. 访问 https://monet.vision 注册账户
2. 登录后，前往 https://monet.vision/skills/keys 创建 API 密钥
3. 将 API 密钥配置在环境变量或代码中

如果您没有 API 密钥，请联系您的负责人在 monet.vision 上申请。

## 快速入门

### 创建视频生成任务

```bash
curl -X POST https://monet.vision/api/v1/tasks/async \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -d '{
    "type": "video",
    "input": {
      "model": "sora-2",
      "prompt": "A cat running in the park",
      "duration": 5,
      "aspect_ratio": "16:9"
    },
    "idempotency_key": "unique-key-123"
  }'
```

> ⚠️ **重要提示**：`idempotency_key` 是必需的。请使用唯一值（例如 UUID）以防止重复创建任务。

**响应：**

```json
{
  "id": "task_abc123",
  "status": "pending",
  "type": "video",
  "created_at": "2026-02-27T10:00:00Z"
}
```

### 获取任务状态和结果

任务处理是异步的。您需要不断轮询任务状态，直到它变为 `success` 或 `failed`。**建议的轮询间隔：5 秒**。

```bash
curl https://monet.vision/api/v1/tasks/task_abc123 \
  -H "Authorization: Bearer $MONET_API_KEY"
```

任务完成时的响应：

```json
{
  "id": "task_abc123",
  "status": "success",
  "type": "video",
  "outputs": [
    {
      "model": "sora-2",
      "status": "success",
      "progress": 100,
      "url": "https://files.monet.vision/..."
    }
  ],
  "created_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T10:01:30Z"
}
```

**示例：轮询直到任务完成**

```typescript
const TASK_ID = "task_abc123";
const MONET_API_KEY = process.env.MONET_API_KEY;

async function pollTask() {
  while (true) {
    const response = await fetch(
      `https://monet.vision/api/v1/tasks/${TASK_ID}`,
      {
        headers: {
          Authorization: `Bearer ${MONET_API_KEY}`,
        },
      },
    );

    const data = await response.json();
    const status = data.status;

    if (status === "success") {
      console.log("Task completed successfully!");
      console.log(JSON.stringify(data, null, 2));
      break;
    } else if (status === "failed") {
      console.log("Task failed!");
      console.log(JSON.stringify(data, null, 2));
      break;
    } else {
      console.log(`Task status: ${status}, waiting...`);
      await new Promise((resolve) => setTimeout(resolve, 5000)); // Wait 5 seconds
    }
  }
}

pollTask();
```

## 支持的模型

### 视频生成

#### Sora (OpenAI)

**sora-2** - Sora 2
- OpenAI 最新的视频生成模型
- **适用场景**：需要 OpenAI 最新技术的视频项目
- **耗时**：10-15 秒
- **特点**：支持音频生成、参考图像

```typescript
{
  model: "sora-2",
  prompt: string,                // Required
  images?: string[],             // Optional: Reference images
  duration?: 10 | 15,           // Optional, default: 10
  aspect_ratio?: "16:9" | "9:16"
}
```

**sora-2-pro** - Sora 2 Pro
- 适用于电影级场景的完美质量
- **适用场景**：专业电影制作、广告制作和高端制作
- **耗时**：15-25 秒
- **特点**：支持音频生成、参考图像

```typescript
{
  model: "sora-2-pro",
  prompt: string,
  images?: string[],
  duration?: 15 | 25,           // Optional, default: 15
  aspect_ratio?: "16:9" | "9:16"
}
```

#### Veo (Google)

**veo-3-1-fast** - Google Veo 3.1 Fast
- 极快的视频生成速度
- **适用场景**：需要快速生成视频的项目
- **耗时**：8 秒
- **分辨率**：1080p，支持音频生成

```typescript
{
  model: "veo-3-1-fast",
  prompt: string,
  images?: string[],             // Reference images
  aspect_ratio?: "16:9" | "9:16"
}
```

**veo-3-1** - Google Veo 3.1
- 高级 AI 视频模型，支持声音
- **适用场景**：专业级视频制作
- **耗时**：8 秒
- **分辨率**：1080p，支持音频生成

```typescript
{
  model: "veo-3-1",
  prompt: string,
  images?: string[],
  aspect_ratio?: "16:9" | "9:16"
}
```

**veo-3-fast** - Google Veo 3 Fast
- 比标准 Veo 3 快 30%
- **适用场景**：需要快速迭代的项目
- **耗时**：8 秒
- **分辨率**：1080p，支持否定性提示（负向提示）

```typescript
{
  model: "veo-3-fast",
  prompt: string,
  images?: string[],
  negative_prompt?: string       // Specify unwanted content
}
```

**veo-3** - Google Veo 3
- 高质量的视频生成
- **适用场景**：标准的高质量视频制作
- **耗时**：8 秒
- **分辨率**：1080p，支持否定性提示

```typescript
{
  model: "veo-3",
  prompt: string,
  images?: string[],
  negative_prompt?: string
}
```

#### Wan

**wan-2-6** - Wan 2.6
- 支持多镜头和自动音频
- **适用场景**：需要多镜头切换的视频制作
- **耗时**：5-15 秒
- **分辨率**：720p-1080p，支持音频生成

```typescript
{
  model: "wan-2-6",
  prompt: string,
  images?: string[],
  duration?: 5 | 10 | 15,
  resolution?: "720p" | "1080p",
  aspect_ratio?: "16:9" | "9:16" | "4:3" | "3:4" | "1:1",
  shot_type?: "single" | "multi"  // Single/multi-shot switching
}
```

**wan-2-5** - Wan 2.5
- 支持自动音频生成
- **适用场景**：快速生成带音频的视频
- **耗时**：5-10 秒
- **分辨率**：480p-1080p，支持音频

```typescript
{
  model: "wan-2-5",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "720p" | "1080p",
  aspect_ratio?: "16:9" | "9:16" | "4:3" | "3:4" | "1:1"
}
```

**wan-2-2-flash** - Wan 2.2 Flash
- 支持指令理解，可控制摄像机移动
- **适用场景**：需要精确控制摄像机移动的场景
- **耗时**：5-10 秒
- **分辨率**：480p-1080p

```typescript
{
  model: "wan-2-2-flash",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "720p" | "1080p",
  negative_prompt?: string
}
```

**wan-2-2** - Wan 2.2
- 图像细节出色，运动稳定性强
- **适用场景**：需要高稳定性的视频制作
- **耗时**：5-10 秒
- **分辨率**：480p-1080p

```typescript
{
  model: "wan-2-2",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "1080p",
  aspect_ratio?: "16:9" | "9:16" | "4:3" | "3:4" | "1:1",
  negative_prompt?: string
}
```

#### Kling

**kling-2-6** - Kling 2.6
- 适合电影制作的视频和音频
- **适用场景**：电影级视频制作
- **耗时**：5-10 秒
- ✨ **特点**：强大的视觉真实感，支持音频生成

```typescript
{
  model: "kling-2-6",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  generate_audio?: boolean
}
```

**kling-2-5** - Kling 2.5 Turbo
- 运动流畅，一致性更强
- **适用场景**：需要高一致性的视频制作
- **耗时**：5-10 秒
- ✨ **特点**：支持否定性提示

```typescript
{
  model: "kling-2-5",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  negative_prompt?: string
}
```

**kling-v2-1-master** - Kling 2.1 Master
- 视觉真实感强，功能增强
- **适用场景**：专业级的高质量视频制作
- **耗时**：5-10 秒
- ✨ **特点**：支持强度调整，支持否定性提示

```typescript
{
  model: "kling-v2-1-master",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  strength?: number,            // 0-1: Control generation effect
  negative_prompt?: string
}
```

**kling-v2-1** - Kling 2.1
- 视觉真实感强
- **适用场景**：高真实感视频制作
- **耗时**：5-10 秒
- ✨ **特点**：支持强度调整，支持否定性提示

```typescript
{
  model: "kling-v2-1",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  strength?: number,            // 0-1
  negative_prompt?: string
}
```

**kling-v2** - Kling 2.0
- 美学效果出色
- **适用场景**：艺术创作和注重美学的视频
- **耗时**：5-10 秒
- ✨ **特点**：支持强度调整，支持否定性提示

```typescript
{
  model: "kling-v2",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  aspect_ratio?: "1:1" | "16:9" | "9:16",
  strength?: number,            // 0-1
  negative_prompt?: string
}
```

#### Hailuo

**hailuo-2-3** - Hailuo 2.3
- 视频中的动作和物理效果出色
- **适用场景**：需要真实物理效果的视频
- **耗时**：6-10 秒
- **分辨率**：768p-1080p，支持极端物理模拟

```typescript
{
  model: "hailuo-2-3",
  prompt: string,
  images?: string[],
  duration?: 6 | 10,
  resolution?: "768p" | "1080p"
}
```

**hailuo-2-3-fast** - Hailuo 2.3 Fast
- 生成速度很快
- **适用场景**：需要快速迭代的项目
- **耗时**：6-10 秒
- **分辨率**：768p-1080p

```typescript
{
  model: "hailuo-2-3-fast",
  prompt: string,
  images?: string[],
  duration?: 6 | 10,
  resolution?: "768p" | "1080p"
}
```

**hailuo-02** - Hailuo 02
- 极端的物理模拟
- **适用场景**：需要精确物理模拟的场景
- **耗时**：6-10 秒
- **分辨率**：768p-1080p

```typescript
{
  model: "hailuo-02",
  prompt: string,
  images?: string[],
  duration?: 6 | 10,
  resolution?: "768p" | "1080p"
}
```

**hailuo-01-live2d** - Hailuo 01 Live2D
- Hailuo 的 Live2D 模型
- **适用场景**：2D 角色动画制作
- ✨ **特点**：适用于 2D 角色动画

```typescript
{
  model: "hailuo-01-live2d",
  prompt: string,
  images?: string[]
}
```

**hailuo-01** - Hailuo 01
- 最高的视频质量
- **适用场景**：需要最高质量视频的项目
- ✨ **特点**：适用于高质量需求

```typescript
{
  model: "hailuo-01",
  prompt: string,
  images?: string[]
}
```

#### Doubao Seedance

**doubao-seedance-1-5-pro** - Seedance 1.5 Pro
- 专业的音视频同步
- **适用场景**：需要音视频同步的专业制作
- **耗时**：4-12 秒
- **分辨率**：480p-720p，支持音频生成

```typescript
{
  model: "doubao-seedance-1-5-pro",
  prompt: string,
  images?: string[],
  duration?: number,
  resolution?: "480p" | "720p",
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16" | "21:9",
  generate_audio?: boolean
}
```

**doubao-seedance-1-0-pro-fast** - Seedance 1.0 Pro Fast
- 高品质且效率无可匹敌
- **适用场景**：需要快速高质量输出的项目
- **耗时**：2-12 秒
- **分辨率**：720p-1080p，ByteDance 的下一代 AI 视频模型

```typescript
{
  model: "doubao-seedance-1-0-pro-fast",
  prompt: string,
  images?: string[],
  duration?: number,
  resolution?: "720p" | "1080p",
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16" | "21:9"
}
```

**doubao-seedance-1-0-pro** - Seedance 1.0 Pro
- 动作表现稳定
- **适用场景**：需要稳定动作的视频制作
- **耗时**：5-10 秒
- **分辨率**：480p-1080p

```typescript
{
  model: "doubao-seedance-1-0-pro",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "1080p",
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16"
}
```

**doubao-seedance-1-0-lite** - Seedance 1.0 Lite
- 精确的语义理解
- **适用场景**：需要精确语义理解的场景
- **耗时**：5-10 秒
- **分辨率**：480p-1080p

```typescript
{
  model: "doubao-seedance-1-0-lite",
  prompt: string,
  images?: string[],
  duration?: 5 | 10,
  resolution?: "480p" | "720p" | "1080p"
}
```

#### 特殊功能

**kling-motion-control** - Kling 动作控制
- 通过视频参考进行精确的动作控制
- **适用场景**：需要从参考视频复制动作的场景
- **耗时**：3-30 秒
- **分辨率**：720p/1080p，支持音频生成
- 💰 **价格**：720p：8 信用点/秒，1080p：15 信用点/秒

```typescript
{
  model: "kling-motion-control",
  prompt: string,                // Required: Detailed motion description
  images: string[],              // Required: min 1 reference image
  videos: string[],              // Required: min 1 reference video
  resolution?: "720p" | "1080p"
}
```

**runway-act-two** - Runway Act Two
- 下一代动作捕捉模型
- **适用场景**：从视频中捕捉动作并应用于新角色
- **耗时**：3-30 秒
- ✨ **特点**：支持动作转移
- 💰 **价格**：10 信用点/秒

```typescript
{
  model: "runway-act-two",
  images: string[],              // Required: min 1 target character image
  videos: string[],              // Required: min 1 motion reference video
  aspect_ratio?: "1:1" | "4:3" | "16:9" | "3:4" | "9:16" | "21:9"
}
```

**wan-animate-mix** - Wan Animate Mix（标准）
- 适用于角色替换场景
- **适用场景**：视频中的角色替换
- **耗时**：3-30 秒
- ✨ **特点**：用指定图像角色替换视频中的角色
- 💰 **价格**：10 信用点/秒

```typescript
{
  model: "wan-animate-mix",
  videos: string[],              // Required: Original videos
  images: string[]               // Required: Target character images
}
```

**wan-animate-mix-pro** - Wan Animate Mix Pro（专业版）
- 动画流畅性更高，效果更好
- **适用场景**：专业级的视频角色替换
- **耗时**：3-30 秒
- ✨ **特点**：更高质量的角色替换效果
- 💰 **价格**：20 信用点/秒

```typescript
{
  model: "wan-animate-mix-pro",
  videos: string[],              // Required
  images: string[]               // Required
}
```

**wan-animate-move** - Wan Animate Move（标准）
- 复制舞蹈和复杂的动作
- **适用场景**：动作捕捉和转移
- **耗时**：3-30 秒
- ✨ **特点**：将动作从参考视频应用到目标图像
- 💰 **价格**：10 信用点/秒

```typescript
{
  model: "wan-animate-move",
  videos: string[],              // Required: Motion reference videos
  images: string[]               // Required: Target character images
}
```

**wan-animate-move-pro** - Wan Animate Move Pro（专业版）
- 动画流畅性更高，效果更好
- **适用场景**：专业级的动作捕捉和转移
- **耗时**：3-30 秒
- ✨ **特点**：更高质量的动作转移效果
- 💰 **价格**：20 信用点/秒

### 图像生成

#### GPT (OpenAI)

**gpt-4o** - GPT 4o
- 生成准确、逼真的图像
- **适用场景**：需要高质量、逼真图像的项目
- ✨ **特点**：支持多个参考图像，多种分辨率比，可自定义风格

```typescript
{
  model: "gpt-4o",
  prompt: string,
  images?: string[],             // Reference images for style guidance
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string                 // Custom style description
}
```

**gpt-image-1-5** - GPT Image 1.5
- 真实颜色精确渲染
- **适用场景**：需要颜色准确性的专业图像生成
- ✨ **特点**：支持最多 10 个参考图像，可调节质量

```typescript
{
  model: "gpt-image-1-5",
  prompt: string,
  images?: string[],             // max 10 reference images
  aspect_ratio?: "1:1" | "3:2" | "2:3",
  quality?: "auto" | "low" | "medium" | "high"
}
```

#### Nano Banana (Google)

**nano-banana-1** - Google Nano Banana
- 角色一致性极高
- **适用场景**：需要角色外观一致性的图像系列
- ✨ **特点**：支持最多 5 个参考图像，多种分辨率比

```typescript
{
  model: "nano-banana-1",
  prompt: string,
  images?: string[],             // max 5 reference images
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "4:3" | "3:4" | "16:9" | "9:16"
}
```

**nano-banana-1-pro** - Nano Banana Pro
- Google 的旗舰生成模型
- **适用场景**：专业级的高质量图像生成
- ✨ **特点**：支持 1K-4K 分辨率，最多 14 个参考图像，超宽 21:9 比例

```typescript
{
  model: "nano-banana-1-pro",
  prompt: string,
  images?: string[],             // max 14 reference images
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "4:3" | "3:4" | "4:5" | "5:4" | "16:9" | "9:16" | "21:9",
  resolution?: "1K" | "2K" | "4K"
}
```

**nano-banana-2** - Nano Banana 2
- Google Gemini 的最新模型
- **适用场景**：需要最新技术的高质量图像生成
- ✨ **特点**：支持 1K-4K 分辨率，最多 14 个参考图像，超宽 21:9 比例

```typescript
{
  model: "nano-banana-2",
  prompt: string,
  images?: string[],             // max 14 reference images
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "4:3" | "3:4" | "4:5" | "5:4" | "16:9" | "9:16" | "21:9" | "4:1" | "1:4" | "8:1" | "1:8",
  resolution?: "1K" | "2K" | "4K"
}
```

**wan-i-2-6** - Wan 2.6
- 高质量且富有表现力
- **适用场景**：需要高表现力的创意图像生成
- ✨ **特点**：支持最多 4 个参考图像，超宽 21:9 比例

```typescript
{
  model: "wan-i-2-6",
  prompt: string,
  images?: string[],             // max 4 reference images
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16" | "21:9"
}
```

**wan-2-5** - Wan 2.5
- 快速、创意的图像生成
- **适用场景**：需要快速创作和迭代的项目
- ✨ **特点**：支持最多 2 个参考图像，超宽 21:9 比例

```typescript
{
  model: "wan-2-5",
  prompt: string,
  images?: string[],             // max 2 reference images
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16" | "21:9"
}
```

#### Seedream (ByteDance)

**seedream-5-0** - Seedream 5.0 Lite
- 智能的视觉推理
- **适用场景**：需要智能理解和推理的复杂场景
- ✨ **特点**：2K-3K 分辨率，最多 14 个参考图像，超宽 21:9 比例

```typescript
{
  model: "seedream-5-0",
  prompt: string,
  images?: string[],             // max 14 reference images
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "3:4" | "4:3" | "4:5" | "5:4" | "9:16" | "16:9" | "21:9",
  resolution?: "2K" | "3K"
}
```

**seedream-4-5** - Seedream 4.5
- ByteDance 的 4K 图像模型
- **适用场景**：需要高分辨率的专业图像生成
- ✨ **特点**：2K-4K 分辨率，最多 14 个参考图像，超宽 21:9 比例

```typescript
{
  model: "seedream-4-5",
  prompt: string,
  images?: string[],             // max 14 reference images
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "3:4" | "4:3" | "4:5" | "5:4" | "9:16" | "16:9" | "21:9",
  resolution?: "2K" | "4K"
}
```

**seedream-4-0** - Seedream 4.0
- 支持风格统一的图像
- **适用场景**：需要风格一致的图像系列
- ✨ **特点**：支持最多 10 个参考图像

```typescript
{
  model: "seedream-4-0",
  prompt: string,
  images?: string[],             // max 10 reference images
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16"
}
```

#### Flux (Black Forest Labs)

**flux-2-dev** - Flux.2 Dev
- 生成逼真的图像
- **适用场景**：需要高真实感的图像生成
- ✨ **特点**：Black Forest Labs 的模型，支持多种分辨率比

```typescript
{
  model: "flux-2-dev",
  prompt: string,
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16"
}
```

**flux-kontext-pro** - Flux Kontext Pro
- 适用于编辑和合成
- **适用场景**：专业的图像编辑和合成工作
- ✨ **特点**：支持参考图像，可自定义风格

```typescript
{
  model: "flux-kontext-pro",
  prompt: string,
  images?: string[],
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string
}
```

**flux-kontext-max** - Flux Kontext Max
- 生成结果精确度高
- **适用场景**：需要精确控制生成结果的场景
- ✨ **特点**：支持参考图像，可自定义风格

```typescript
{
  model: "flux-kontext-max",
  prompt: string,
  images?: string[],
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string
}
```

**flux-1-schnell** - Flux Schnell
- 适用于简单的基本场景
- **适用场景**：快速原型设计和简单场景
- ✨ **特点**：生成速度快

```typescript
{
  model: "flux-1-schnell",
  prompt: string
}
```

#### Imagen (Google)

**imagen-3-0** - Imagen 3.0
- 生成速度快，质量高
- **适用场景**：需要快速高质量图像的项目
- ✨ **特点**：Google 的先进图像模型，可自定义风格

```typescript
{
  model: "imagen-3-0",
  prompt: string,
  aspect_ratio?: "1:1" | "3:4" | "4:3" | "9:16" | "16:9",
  style?: string
}
```

**imagen-4-0** - Imagen 4.0
- Google 的最新生成模型
- **适用场景**：需要最新技术的高质量图像
- ✨ **特点**：更高质量，更精细

```typescript
{
  model: "imagen-4-0",
  prompt: string,
  aspect_ratio?: "1:1" | "3:4" | "4:3" | "9:16" | "16:9",
  style?: string
}
```

#### Ideogram

**ideogram-v2** - Ideogram V2
- 非常适合文本编辑
- **适用场景**：需要将文本添加到图像中的场景
- ✨ **特点**：出色的文本渲染性能

```typescript
{
  model: "ideogram-v2",
  prompt: string,
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string
}
```

**ideogram-v3** - Ideogram V3
- 设计能力出众
- **适用场景**：设计师和创意专业人士的首选
- ✨ **特点**：更好的文本渲染和排版

```typescript
{
  model: "ideogram-v3",
  prompt: string,
  aspect_ratio?: "1:1" | "4:3" | "3:2" | "16:9" | "3:4" | "2:3" | "9:16",
  style?: string
}
```

#### Stability AI

**stability-1-0** - Stability 1.0
- 适用于生成细节丰富的图像
- **适用场景**：需要精细控制和高质量图像的项目
- ✨ **特点**：支持否定性提示，可自定义风格

### 音乐生成

**minimax-music** - MiniMax Music
- 根据文本生成音乐，支持自定义歌词
- **提供者**：MiniMax
- ✨ **特点**：支持文本到音乐的转换，支持自定义歌词
- **适用场景**：根据文本描述或歌词创建音乐

---

## API 参考

### 创建任务（异步）

POST `/api/v1/tasks/async` - 创建异步任务。立即返回任务 ID。

**请求：**

```bash
curl -X POST https://monet.vision/api/v1/tasks/async \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -d '{
    "type": "video",
    "input": {
      "model": "sora-2",
      "prompt": "A cat running"
    },
    "idempotency_key": "unique-key-123"
  }'
```

> ⚠️ **重要提示**：`idempotency_key` 是必需的。请使用唯一值（例如 UUID）以防止重复创建任务。

**响应：**

```json
{
  "id": "task_abc123",
  "status": "pending",
  "type": "video",
  "created_at": "2026-02-27T10:00:00Z"
}
```

### 创建任务（流式）

POST `/api/v1/tasks/sync` - 创建带有 SSE 流式的任务。等待任务完成并实时显示进度。

**请求：**

```bash
curl -X POST https://monet.vision/api/v1/tasks/sync \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -N \
  -d '{
    "type": "video",
    "input": {
      "model": "sora-2",
      "prompt": "A cat running"
    },
    "idempotency_key": "unique-key-123"
  }'
```

### 获取任务信息

GET `/api/v1/tasks/{taskId}` - 获取任务状态和结果。

**请求：**

```bash
curl https://monet.vision/api/v1/tasks/task_abc123 \
  -H "Authorization: Bearer $MONET_API_KEY"
```

**响应：**

```json
{
  "id": "task_abc123",
  "status": "success",
  "type": "video",
  "outputs": [
    {
      "model": "sora-2",
      "status": "success",
      "progress": 100,
      "url": "https://files.monet.vision/..."
    }
  ],
  "created_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T10:01:30Z"
}
```

### 列出任务

GET `/api/v1/tasks/list` - 列出任务（支持分页）

**请求：**

```bash
curl "https://monet.vision/api/v1/tasks/list?page=1&pageSize=20" \
  -H "Authorization: Bearer $MONET_API_KEY"
```

**响应：**

```json
{
  "tasks": [
    {
      "id": "task_abc123",
      "status": "success",
      "type": "video",
      "outputs": [
        {
          "model": "sora-2",
          "status": "success",
          "progress": 100,
          "url": "https://files.monet.vision/..."
        }
      ],
      "created_at": "2026-02-27T10:00:00Z",
      "updated_at": "2026-02-27T10:01:30Z"
    }
  ],
  "page": 1,
  "pageSize": 20,
  "total": 100
}
```

### 上传文件

POST `/api/v1/files` - 上传文件以获取在线访问 URL。

> 📁 **文件存储**：上传的文件将存储 **24 小时**，过期后将自动删除。

**请求：**

```bash
curl -X POST https://monet.vision/api/v1/files \
  -H "Authorization: Bearer $MONET_API_KEY" \
  -F "file=@/path/to/your/file.mp4" \
  -v
```

**用途**：
- 上传参考图像用于视频/图像生成任务
- 上传视频文件用于视频处理
- 上传音频文件用于音乐任务
- 获取临时在线 URL 以共享文件

**响应：**

```json
{
  "id": "file_xyz789",
  "url": "...",
  "filename": "file.mp4",
  "size": 1048576,
  "content_type": "video/mp4",
  "created_at": "2026-02-27T10:00:00Z"
}
```

## 配置

### 环境变量

```bash
export MONET_API_KEY="monet_xxx"
```

### 认证

所有 API 请求都需要通过 `Authorization` 头进行认证：

```
Authorization: Bearer monet_xxx
```