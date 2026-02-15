---
name: bria-ai
description: **使用说明：**  
Bria.ai 提供了一套强大的工具，可用于生成各种视觉素材，包括产品照片、封面图片、图标以及背景图片等。该工具支持批量处理（同时生成多张图片），并提供了完整的工作流程（生成 → 编辑 → 去除背景），同时支持并行 API 调用模式。适用于网站、演示文稿、电子商务产品目录等场景，适用于任何需要大量 AI 生成图片的任务。
---

# Bria视觉资产生成器

使用Bria商业级安全的AI模型，为网站、演示文稿、文档和应用程序生成可用于实际发布的视觉资产。

## 适用场景

- **网站/应用程序开发**：用于制作标题图片、产品照片、背景图和插图
- **演示文稿**：用于制作幻灯片视觉元素、图表、图标和封面图片
- **文档**：用于生成报告图表、信息图、标题和装饰性元素
- **市场营销**：用于制作社交媒体素材、横幅和宣传图片
- **电子商务**：用于拍摄产品照片和展示产品使用场景的图片
- **批量生成**：可以同时根据不同提示生成多张图片
- **工作流程集成**：支持一系列连续的操作（生成 → 编辑 → 去除背景 → 调整场景）

## 核心功能

| 功能 | 用途示例 |
|------|------------|
| 创建新图片 | 生成产品标题图片、产品照片和插图 |
| 通过文本编辑 | 修改图片颜色、对象和场景 |
| 带有遮罩的编辑 | 进行精确的图像修复，添加或替换特定区域 |
| 添加/替换/删除对象 | 通过文本指令添加或删除对象（例如：添加花瓶、将苹果替换为梨、移除桌子） |
| 透明背景 | 提供RMBG-2.0功能，用于提取图片中的主体部分以用于叠加或制作Logo |
| 背景处理 | 可以替换、模糊或删除图片背景 |
| 扩展图片尺寸 | 改变图片的尺寸或宽高比 |
| 图像放大 | 将图片分辨率提高2倍或4倍 |
| 图像质量优化 | 改善图片的亮度、色彩和细节 |
| 图像风格转换 | 可以将图片转换为油画、动漫、卡通或3D渲染风格 |
| 调整光线效果 | 可以模拟不同的光照效果（如黄金时刻、聚光灯等） |
| 更改季节效果 | 可以调整图片中的季节场景（如春夏秋冬） |
| 图像合成 | 可以将多张图片合并或应用纹理、Logo等效果 |
| 文本替换 | 可以修改图片中的文字内容 |
| 图像修复 | 可以修复旧照片或损坏的图片 |
| 上色处理 | 可以为黑白图片添加颜色，或将彩色图片转换为黑白 |
| 从草图生成照片 | 可以将手绘草图转换为逼真的照片 |
| 产品摄影 | 可以拍摄产品使用场景的图片 |

## 快速参考

### 生成图片（FIBO）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "your description",
    "aspect_ratio": "16:9"
  }'
```

**支持的图片尺寸比例**：`1:1`（正方形）、`16:9`（标题图片/横幅）、`4:3`（演示文稿）、`9:16`（手机/故事图片）、`3:4`（竖屏图片）

> **高级用法**：如需对生成过程进行精确的控制，建议使用**[VGL结构化提示语言](../vgl/SKILL.md)**，而不是自然语言描述。VGL允许以JSON格式明确指定所有视觉元素（如对象、光线效果和构图）。

### 去除背景（RMBG-2.0）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/remove_background" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://..."}'
```

返回带有透明背景的PNG图片。

### 图像编辑（FIBO-Edit） - 无需遮罩

可以使用自然语言指令编辑图片：

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "images": ["https://..."],
    "instruction": "change the mug to red"
  }'
```

**Python示例：**
```python
from bria_client import BriaClient
client = BriaClient()
result = client.edit_image(image_url, "change the mug to red")
print(result['result']['image_url'])
```

### 带有遮罩的图像编辑（FIBO-Edit）

如需精确控制编辑区域：

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/gen_fill" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "https://...",
    "mask": "https://...",
    "prompt": "what to generate in masked area"
  }'
```

### 扩展图片尺寸

可以调整图片的尺寸以适应新的宽高比：

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/expand" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64-or-url",
    "aspect_ratio": "16:9",
    "prompt": "coffee shop background, wooden table"
  }'
```

### 图像放大

可以将图片分辨率提高2倍或4倍：

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/increase_resolution" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://...", "scale": 2}'
```

### 产品使用场景拍摄

可以将产品放入特定的场景中：

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/lifestyle_shot_by_text" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "https://product-with-transparent-bg.png",
    "prompt": "modern kitchen countertop, natural morning light"
  }'
```

---

## 资产生成工作流程

### 网站标题图片

生成适合首页的宽幅横幅图片：

```json
{
  "prompt": "Modern tech startup workspace with developers collaborating, bright natural lighting, clean minimal aesthetic",
  "aspect_ratio": "16:9",
  "negative_prompt": "cluttered, dark, low quality"
}
```

**生成标题图片的提示建议：**
- 使用`16:9`的比例制作全宽横幅
- 明确描述光线效果和整体氛围
- 使用“专业”、“高质量”、“适合商业用途”等描述词以获得更好的效果
- 指定“干净背景”或“简洁背景”，以便添加文字

### 产品摄影

生成适合电子商务使用的产品照片：

```json
{
  "prompt": "Professional product photo of [item] on white studio background, soft shadows, commercial photography lighting",
  "aspect_ratio": "1:1"
}
```

**之后可以使用RMBG-2.0去除背景，以便将图片用于其他场景：**

```json
{"image": "generated_image_url"}
```

### 演示文稿视觉元素

生成适合幻灯片的图片：

```json
{
  "prompt": "Abstract visualization of data analytics, blue and purple gradient, modern corporate style, clean composition with space for text",
  "aspect_ratio": "16:9"
}
```

**常见的演示文稿主题：**
- “抽象科技背景” - 适用于技术类幻灯片
- “团队协作” - 适用于展示企业文化
- “增长图表” - 适用于展示数据指标的幻灯片
- “极简几何图案” - 适用于分隔不同内容的幻灯片

### 文档图片

生成报告或文章中使用的图片：

```json
{
  "prompt": "Isometric illustration of cloud computing infrastructure, flat design, vibrant colors, white background",
  "aspect_ratio": "4:3"
}
```

### 图标和插图

先生成图标，然后去除背景：

```json
{
  "prompt": "3D icon of a shield with checkmark, glossy material, soft gradient background, app icon style",
  "aspect_ratio": "1:1"
}
```

之后使用RMBG-2.0得到透明背景的PNG图片。

### 社交媒体素材

**Instagram帖子（1:1比例）：**
```json
{
  "prompt": "Lifestyle photo of coffee and laptop on wooden desk, morning light, cozy atmosphere",
  "aspect_ratio": "1:1"
}
```

**Instagram故事/视频（9:16比例）：**
```json
{
  "prompt": "Vertical product showcase of smartphone, floating in gradient background, tech aesthetic",
  "aspect_ratio": "9:16"
}
```

---

## 提示编写技巧

### 明确指定风格
- 如何描述图片的风格（例如：“专业的产品照片” vs “随意的快照”）
- 如何描述插图的风格（例如：“平面设计插图” vs “3D渲染图”）
- 如何描述整体设计风格（例如：“现代企业风格” vs “活泼多彩的风格”）

### 指定技术细节
- 详细说明光线效果（例如：“柔和的自然光”、“摄影棚灯光”、“戏剧性的阴影”）
- 说明背景类型（例如：“白色摄影棚背景”、“渐变背景”、“模糊的办公室背景”、“透明背景”）
- 说明构图方式（例如：“居中构图”、“三分法则”、“左侧留白用于文字）

### 用于提升质量的关键词
- 使用这些关键词以获得更好的效果：**“高质量”、“专业级”、“适合商业用途”**
- 如需高质量图片，可以使用“4K分辨率”、“清晰的对焦”等描述
- 对于照片，可以使用“获奖摄影”等描述

### 需要避免的描述
- 避免使用负面或模糊的描述（例如：“模糊的图片”、“低质量的图片”、“像素化的图片”）
- 避免包含不需要的元素（例如：“文字、水印、Logo”）
- 避免使用混乱或杂乱的描述

---

## 异步响应处理

所有API接口返回异步响应：

```json
{
  "request_id": "uuid",
  "status_url": "https://engine.prod.bria-api.com/v2/status/uuid"
}
```

需要不断检查`status_url`的状态，直到状态变为“COMPLETED”，然后获取`result.image_url`。

```python
import requests, time

def get_result(status_url, api_key):
    while True:
        r = requests.get(status_url, headers={"api_token": api_key})
        data = r.json()
        if data["status"] == "COMPLETED":
            return data["result"]["image_url"]
        if data["status"] == "FAILED":
            raise Exception(data.get("error"))
        time.sleep(2)
```

---

## 批量与并行图像生成

### 同时生成多张图片

为了高效生成多张图片，可以并行发送请求并同时检查响应：

```python
import asyncio
import aiohttp

async def generate_image(session, api_key, prompt, aspect_ratio="1:1"):
    """Launch a single generation request."""
    async with session.post(
        "https://engine.prod.bria-api.com/v2/image/generate",
        headers={"api_token": api_key, "Content-Type": "application/json"},
        json={"prompt": prompt, "aspect_ratio": aspect_ratio}
    ) as resp:
        return await resp.json()

async def poll_status(session, api_key, status_url, timeout=120):
    """Poll until complete or failed."""
    for _ in range(timeout // 2):
        async with session.get(status_url, headers={"api_token": api_key}) as resp:
            data = await resp.json()
            if data["status"] == "COMPLETED":
                return data["result"]["image_url"]
            if data["status"] == "FAILED":
                raise Exception(data.get("error", "Generation failed"))
        await asyncio.sleep(2)
    raise TimeoutError(f"Timeout polling {status_url}")

async def generate_batch(api_key, prompts, aspect_ratio="1:1", max_concurrent=5):
    """Generate multiple images with different prompts concurrently."""
    semaphore = asyncio.Semaphore(max_concurrent)  # Rate limiting

    async def generate_one(prompt):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                # Launch request
                result = await generate_image(session, api_key, prompt, aspect_ratio)
                # Poll for completion
                return await poll_status(session, api_key, result["status_url"])

    # Run all concurrently
    results = await asyncio.gather(*[generate_one(p) for p in prompts], return_exceptions=True)
    return results

# Usage
prompts = [
    "Professional photo of running shoes on white background",
    "Professional photo of leather handbag on white background",
    "Professional photo of smartwatch on white background",
    "Professional photo of sunglasses on white background",
]
image_urls = asyncio.run(generate_batch("YOUR_API_KEY", prompts, max_concurrent=3))
```

**关键点：**
- 使用`asyncio.Semaphore`来限制并发请求的数量（建议限制在3-5个）
- 设置`return_exceptions=True`可以防止某个请求失败导致所有请求被取消
- 每个请求的结果可能是URL字符串或异常对象

### TypeScript/Node.js并行生成示例

```typescript
type AspectRatio = "1:1" | "4:3" | "16:9" | "3:4" | "9:16";

interface BriaResponse {
  request_id: string;
  status_url: string;
}

interface BriaStatusResponse {
  status: "IN_PROGRESS" | "COMPLETED" | "FAILED";
  result?: { image_url: string };
  error?: string;
}

interface GenerateBatchResult {
  prompt: string;
  imageUrl: string | null;
  error: string | null;
}

async function generateBatch(
  apiKey: string,
  prompts: string[],
  aspectRatio: AspectRatio = "1:1",
  maxConcurrent = 5
): Promise<GenerateBatchResult[]> {
  const semaphore = { count: 0, max: maxConcurrent };

  async function withLimit<T>(fn: () => Promise<T>): Promise<T> {
    while (semaphore.count >= semaphore.max) {
      await new Promise(r => setTimeout(r, 100));
    }
    semaphore.count++;
    try {
      return await fn();
    } finally {
      semaphore.count--;
    }
  }

  async function generateOne(prompt: string): Promise<string> {
    return withLimit(async () => {
      // Launch request
      const res = await fetch("https://engine.prod.bria-api.com/v2/image/generate", {
        method: "POST",
        headers: { "api_token": apiKey, "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, aspect_ratio: aspectRatio })
      });
      const { status_url } = (await res.json()) as BriaResponse;

      // Poll for result
      for (let i = 0; i < 60; i++) {
        const statusRes = await fetch(status_url, { headers: { "api_token": apiKey } });
        const data = (await statusRes.json()) as BriaStatusResponse;
        if (data.status === "COMPLETED") return data.result!.image_url;
        if (data.status === "FAILED") throw new Error(data.error || "Generation failed");
        await new Promise(r => setTimeout(r, 2000));
      }
      throw new Error("Timeout waiting for generation");
    });
  }

  const results = await Promise.allSettled(prompts.map(generateOne));

  return results.map((result, i) => ({
    prompt: prompts[i],
    imageUrl: result.status === "fulfilled" ? result.value : null,
    error: result.status === "rejected" ? result.reason.message : null
  }));
}

// Usage
const results = await generateBatch(process.env.BRIA_API_KEY!, [
  "Modern office workspace with natural lighting",
  "Abstract tech background with blue gradient",
  "Professional headshot studio setup"
], "16:9", 3);

results.forEach(r => {
  if (r.imageUrl) console.log(`✓ ${r.prompt}: ${r.imageUrl}`);
  else console.log(`✗ ${r.prompt}: ${r.error}`);
});
```
```

---

## Pipeline Workflows

Chain multiple operations on images (generate → edit → remove background).

### Complete Pipeline Example

```python
async def product_pipeline(api_key, product_descriptions, scene_prompt):
    """
    生成产品图片 → 去除背景 → 将图片放入特定场景中
    """
    async with aiohttp.ClientSession() as session:
        results = []

        for desc in product_descriptions:
            # 第一步：生成产品图片
            gen_result = await generate_image(session, api_key,
                f"Professional product photo of {desc} on white background, studio lighting",
                aspect_ratio="1:1")
            product_url = await poll_status(session, api_key, gen_result["status_url"])

            # 第二步：去除背景
            async with session.post(
                "https://engine.prod.bria-api.com/v2/image/edit/remove_background",
                headers={"api_token": api_key, "Content-Type": "application/json"},
                json={"image": product_url}
            ) as resp:
                rmbg_result = await resp.json()
            transparent_url = await poll_status(session, api_key, rmbg_result["status_url"])

            # 第三步：将图片放入场景中
            async with session.post(
                "https://engine.prod.bria-api.com/v2/image/edit/lifestyle_shot_by_text",
                headers={"api_token": api_key, "Content-Type": "application/json"},
                json={"image": transparent_url, "prompt": scene_prompt}
            ) as resp:
                lifestyle_result = await resp.json()
            final_url = await poll_status(session, api_key, lifestyle_result["status_url"])

            results.append({
                "product": desc,
                "original": product_url,
                "transparent": transparent_url,
                "lifestyle": final_url
            })

        return results

# 使用示例
products = ["coffee mug", "water bottle", "notebook"]
scene = "modern minimalist desk, natural morning light, plants in background"
results = asyncio.run(product_pipeline("YOUR_API_KEY", products, scene))
```

### Parallel Pipeline (Advanced)

Process multiple products through the pipeline concurrently:

```

### 并行处理多个产品的示例

### TypeScript示例
async def parallel_pipeline(api_key, products, scene_prompt, max_concurrent=3):
    """并行处理多个产品的生成流程."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(product):
        async with semaphore:
            return await single_product_pipeline(api_key, product, scene_prompt)

    return await asyncio.gather(*[process_one(p) for p in products], return_exceptions=True)
```

### Common Pipeline Patterns

| Pipeline | Steps | Use Case |
|----------|-------|----------|
| Product → Transparent | generate → remove_background | E-commerce cutouts |
| Product → Lifestyle | generate → remove_background → lifestyle_shot | Marketing photos |
| Edit → Upscale | edit → increase_resolution | High-res edited images |
| Generate → Restyle | generate → restyle | Artistic variations |
| Generate → Variations | generate (num_results=4) | A/B testing options |

---

## Integration Examples

### React/Next.js Component

```

### JavaScript示例
// 生成并显示标题图片
const [imageUrl, setImageUrl] = useState(null);

async function generateHero(prompt) {
  const res = await fetch('/api/bria/generate', {
    method: 'POST',
    body: JSON.stringify({ prompt, aspect_ratio: '16:9' })
  );
  const { image_url } = await res.json();
  setImageUrl(image_url);
}
```

### Python Script for Batch Generation

```

### Python示例
import asyncio

# 详见“批量与并行图像生成”部分的示例代码

async def main():
    api_key = "YOUR_API_KEY"
    products = ["running shoes", "leather bag", "smart watch"]
    prompts = [f"Professional product photo of {p} on white background" for p in products]

    results = await generate_batch(api_key, prompts, aspect_ratio="1:1", max_concurrent=3)

    for product, result in zip(products, results):
        if isinstance(result, Exception):
            print(f"{product}: FAILED - {result}")
        else:
            print(f"{product}: {result}")

asyncio.run(main())
```

---

## API Reference

See `references/api-endpoints.md` for complete endpoint documentation.

### Key Endpoints

**Generation**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/generate` | Generate images from text (FIBO) |

**Edit by Text (No Mask)**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit` | Edit image with natural language instruction |
| `POST /v2/image/edit/add_object_by_text` | Add objects to image |
| `POST /v2/image/edit/replace_object_by_text` | Replace objects in image |
| `POST /v2/image/edit/erase_by_text` | Remove objects by name |

**Edit with Mask**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/gen_fill` | Inpaint/generate in masked region |
| `POST /v2/image/edit/erase` | Erase masked region |

**Background Operations**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/remove_background` | Remove background (RMBG-2.0) |
| `POST /v2/image/edit/replace_background` | Replace with AI-generated background |
| `POST /v2/image/edit/blur_background` | Apply blur to background |
| `POST /v2/image/edit/erase_foreground` | Remove foreground, fill background |
| `POST /v2/image/edit/crop_foreground` | Crop tightly around subject |

**Image Transformation**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/expand` | Outpaint to new aspect ratio |
| `POST /v2/image/edit/enhance` | Enhance quality and details |
| `POST /v2/image/edit/increase_resolution` | Upscale 2x or 4x |
| `POST /v2/image/edit/blend` | Blend/merge images or textures |
| `POST /v2/image/edit/reseason` | Change season/weather |
| `POST /v2/image/edit/restyle` | Transform artistic style |
| `POST /v2/image/edit/relight` | Modify lighting |

**Text & Restoration**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/replace_text` | Replace text in image |
| `POST /v2/image/edit/sketch_to_image` | Convert sketch to photo |
| `POST /v2/image/edit/restore` | Restore old/damaged photos |
| `POST /v2/image/edit/colorize` | Colorize B&W or convert to B&W |

**Product Photography**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/lifestyle_shot_by_text` | Place product in scene by text |
| `POST /v2/image/edit/shot_by_image` | Place product on reference background |

**Utilities**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/structured_instruction/generate` | Generate JSON instruction (no image) |
| `GET /v2/status/{id}` | Check async request status |

### Authentication

All requests need `api_token` header:
```

### API密钥示例
api_token: YOUR_BRIA_API_KEY