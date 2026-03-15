---
name: bria-ai
description: 使用商业上成熟的人工智能模型来生成、编辑和转换图像。能够根据文本生成图像，通过自然语言指令进行图像编辑，去除背景（生成透明PNG格式的图像），替换背景，添加或移除物体，进行图像修复（如修补缺失的部分），调整图像质量，对图像进行风格转换（如转换为油画风格、动漫风格或3D效果），调整光照效果，修复旧照片的颜色，为照片添加色彩，以及将草图转换为真实图像。这些功能可应用于网站、应用程序、演示文稿中需要使用的特色图片、横幅、产品图片、产品场景中的图像展示、图标、插图或背景素材。此外，这些技术还适用于电子商务摄影、批量图像生成以及图像处理工作流程。主要功能包括：图像生成、图像编辑、背景去除、背景替换、产品拍摄、场景建模、风格转换、图像修复、色彩调整、草图转图像、图像修复、主体裁剪，以及将产品融入到特定场景中。
license: MIT
metadata:
  author: Bria AI
  version: "1.2.6"
  openclaw:
    requires:
      env:
        - BRIA_API_KEY
      bins:
        - curl
    primaryEnv: BRIA_API_KEY
---
# Bria — 使用人工智能生成、编辑和去除图片背景

Bria 提供了多种商业上安全的人工智能模型（如 Fibo、Fibo-Edit、RMBG-2.0、GenFill 等），可以帮助您生成、编辑和创建视觉素材。它支持去除或替换图片背景、制作产品生活照、生成透明 PNG 图像、批量处理图片以及构建工作流程。与黑盒式生成工具不同，Bria 提供了精细的控制功能：您可以通过文本指令进行编辑、遮罩特定区域、添加/替换/移除单个对象、独立调整光线或季节效果。

## 设置 — API 密钥检查

在调用任何 Bria API 之前，请检查 API 密钥，并在密钥缺失时指导用户进行设置：

### 第一步：检查密钥是否存在（不要显示密钥）

```bash
if [ -z "$BRIA_API_KEY" ]; then
  echo "BRIA_API_KEY is not set"
else
  echo "BRIA_API_KEY is set"
fi
```

如果输出结果 **不为空**，则跳转到下一节。

### 第二步：如果密钥缺失，指导用户

请明确告知用户：
> 要使用图片生成功能，您需要一个免费的 Bria API 密钥。
>
> 1. 访问 https://platform.bria.ai/console/account/api-keys
> 2. 注册或登录
> 3. 点击 **创建 API 密钥**

等待用户提供 API 密钥。在获得密钥之前，请勿继续进行任何图片生成或编辑操作。

---

## 核心功能

| 功能需求 | 功能 | 使用场景 |
|------|------------|----------|
| 从文本生成图片 | FIBO Generate | 主题图片、产品照片、插图、社交媒体图片、横幅 |
| 通过文本指令编辑图片 | FIBO-Edit | 更改颜色、修改对象、变换场景 |
| 使用遮罩编辑图片区域 | GenFill/Erase | 精确修复图像、添加/替换特定区域 |
| 添加/替换/移除对象 | 基于文本的编辑 | 添加花瓶、将苹果替换为梨、移除桌子 |
| 去除背景（生成透明 PNG） | RMBG-2.0 | 提取图片中的主体用于叠加、添加徽标 |
| 替换/模糊/去除背景 | 背景操作 | 修改、模糊或去除背景 |
| 扩展/修复图片边界 | 图像修复 | 扩展图片边界、调整纵横比 |
| 提升图片分辨率 | 高分辨率处理 | 将分辨率提升 2 倍或 4 倍 |
| 提升图片质量 | 图像优化 | 改善光线、颜色、细节 |
| 重新风格化图片 | 图像风格转换 | 转换为油画、动漫、卡通或 3D 效果 |
| 调整光线 | 光线调整 | 选择最佳拍摄时间、使用聚光灯或营造戏剧性光线效果 |
| 更改季节效果 | 季节转换 | 春天、夏天、秋天、冬天 |
| 合并/融合图片 | 图片合成 | 应用纹理、徽标、合并多张图片 |
| 恢复旧照片 | 照片修复 | 修复老旧或损坏的照片 |
| 给图片上色 | 图像上色 | 为黑白图片添加颜色或将其转换为黑白 |
| 将草图转换为照片 | Sketch2Image | 将手绘草图转换为真实照片 |
| 制作产品生活照 | 生活照制作 | 将产品放入场景中以用于电商展示 |
| 将产品嵌入场景 | 产品整合 | 在精确坐标处嵌入产品 |

## 快速参考

### 生成图片（FIBO）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{
    "prompt": "your description",
    "aspect_ratio": "16:9",
    "resolution": "1MP",
    "sync": true
  }'
```

**纵横比**：`1:1`（正方形）、`16:9`（标题/横幅）、`4:3`（演示文稿）、`9:16`（手机/故事）、`3:4`（肖像）

**分辨率**：`1MP`（默认）或 `4MP`（提升细节，但会增加约 30 秒的延迟）

**同步模式**：在请求体中传递 `"sync": true` 以直接在响应中获取单张图片的结果。对于批量或多张图片生成，省略 `sync`（或设置为 `false`），并使用轮询方式。

> **高级用法**：为了实现对生成过程的精确控制，可以使用 **[VGL 结构化提示](../vgl/SKILL.md)**，而不是自然语言。VGL 以 JSON 格式明确定义所有视觉元素（对象、光线、构图）。

### 去除背景（RMBG-2.0）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/remove_background" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{"image": "https://..."}'
```

返回透明背景的 PNG 图像。

### 编辑图片（FIBO-Edit）——无需遮罩

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{
    "images": ["https://..."],
    "instruction": "change the mug to red"
  }'
```

### 使用遮罩编辑图片区域（GenFill）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/gen_fill" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{
    "image": "https://...",
    "mask": "https://...",
    "prompt": "what to generate in masked area"
  }'
```

### 扩展图片边界（图像修复）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/expand" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{
    "image": "base64-or-url",
    "aspect_ratio": "16:9",
    "prompt": "coffee shop background, wooden table"
  }'
```

### 提升图片分辨率

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/increase_resolution" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{"image": "https://...", "scale": 2}'
```

### 制作产品生活照

```bash
curl -X POST "https://engine.prod.bria-api.com/v1/product/lifestyle_shot_by_text" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{
    "image": "https://product-with-transparent-bg.png",
    "prompt": "modern kitchen countertop, natural morning light"
  }'
```

### 将产品嵌入场景

将一个或多个产品精确地放置在场景中的指定位置。产品会自动裁剪并匹配场景的光线和视角。

```bash
curl -X POST "https://engine.prod.bria-api.com/image/edit/product/integrate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.6" \
  -d '{
    "scene": "https://scene-image-url",
    "products": [
      {
        "image": "https://product-image-url",
        "coordinates": {"x": 100, "y": 200, "width": 300, "height": 400}
      }
    ]
  }'
```

---

## 响应处理

### 同步（单张图片生成）

对于单张图片请求，在请求体中传递 `"sync": true`。响应会直接返回结果，无需轮询。

### 异步处理（批量生成）

对于批量或多张图片生成，省略 `sync`（或设置为 `"sync": false`）。响应会返回一个状态 URL，您需要通过轮询来获取结果：

```json
{
  "request_id": "uuid",
  "status_url": "https://engine.prod.bria-api.com/v2/status/uuid"
}
```

不断轮询 `status_url`，直到状态变为 `status: "COMPLETED"`，然后获取 `result.image_url`。

```python
import requests, time

def get_result(status_url, api_key):
    while True:
        r = requests.get(status_url, headers={"api_token": api_key, "User-Agent": "BriaSkills/1.2.6"})
        data = r.json()
        if data["status"] == "COMPLETED":
            return data["result"]["image_url"]
        if data["status"] == "FAILED":
            raise Exception(data.get("error"))
        time.sleep(2)
```

---

## 提示工程技巧

- **风格**：例如“专业产品摄影” vs “休闲快照”、“平面设计插图” vs “3D 渲染”
- **光线**：例如“柔和的自然光”、“工作室灯光”、“戏剧性阴影”
- **背景**：例如“白色工作室背景”、“渐变背景”、“模糊的办公室背景”、“透明背景”
- **构图**：例如“居中构图”、“三分法则”、“左侧留白用于文字”
- **质量相关关键词**：例如“高质量”、“专业级”、“商业级”、“4K”、“清晰对焦”
- **负面提示**：例如“模糊的、低质量的、像素化的图片”、“带有文字的水印”、“带有徽标的图片”

---

## API 参考

请参阅 `references/api-endpoints.md` 以获取完整的端点文档。

### 主要端点

**图片生成**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/generate` | 从文本生成图片（FIBO） |

**基于文本的编辑（无需遮罩）**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit` | 使用自然语言指令编辑图片 |
| `POST /v2/image/edit/add_object_by_text` | 向图片中添加对象 |
| `POST /v2/image/edit/replace_object_by_text` | 用新对象替换图片中的对象 |
| `POST /v2/image/edit/erase_by_text` | 按名称移除图片中的对象 |

**使用遮罩编辑**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/gen_fill` | 在遮罩区域内修复或生成新内容 |
| `POST /v2/image/edit/erase` | 清除遮罩区域 |

**背景操作**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/remove_background` | 去除背景（RMBG-2.0） |
| `POST /v2/image/edit/replace_background` | 用 AI 生成的背景替换现有背景 |
| `POST /v2/image/edit/blur_background` | 使背景模糊 |
| `POST /v2/image/edit/erase_foreground` | 移除前景，填充背景 |
| `POST /v2/image/edit/crop_foreground` | 紧紧围绕主体裁剪图片 |

**图片转换**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/expand` | 将图片调整到新的纵横比 |
| `POST /v2/image/edit/enhance` | 提升图片质量和细节 |
| `POST /v2/image/edit/increase_resolution` | 将分辨率提升 2 倍或 4 倍 |
| `POST /v2/image/edit/blend` | 合并图片或纹理 |
| `POST /v2/image/edit/reseason` | 更改图片的季节或天气 |
| `POST /v2/image/edit/restyle` | 转换图片的风格 |
| `POST /v2/image/edit/relight` | 调整图片的光线 |

**图片修复**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/sketch_to_colored_image` | 将草图转换为照片 |
| `POST /v2/image/edit/restore` | 修复老旧或损坏的照片 |
| `POST /v2/image/edit/colorize` | 为黑白图片添加颜色或将其转换为黑白 |

**产品摄影**
| 端点 | 功能 |
|----------|---------|
| `POST /v1/product/lifestyle_shot_by_text` | 根据文本描述制作产品生活照 |
| `POST /image/edit/product/integrate` | 在精确坐标处将产品嵌入场景 |

**实用工具**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/structured_instruction/generate` | 生成 JSON 格式的指令（不生成图片） |
| `GET /v2/status/{id}` | 查询异步请求的状态 |

### 认证

所有请求都需要包含 `api_token` 头部信息：
```
api_token: YOUR_BRIA_API_KEY
User-Agent: BriaSkills/<version>
```
> **要求**：在每次 API 请求中都必须包含 `User-Agent: BriaSkills/<version>` 头部信息（其中 `<version>` 是来自 `package.json` 的当前技能版本，例如 `BriaSkills/1.2.6`），包括状态查询请求。

---

## 其他资源

- **[API 端点参考](references/api-endpoints.md)** — 完整的端点文档，包括请求和响应格式 |
- **[工作流程与管道](references/workflows.md)** — 批量生成、并行处理流程、集成示例 |
- **[Python 客户端](references/code-examples/bria_client.py)** — 全功能异步 Python 客户端 |
- **[TypeScript 客户端](references/code-examples/bria_client.ts)** — 类型化的 Node.js 客户端 |
- **[Bash/curl 参考](references/code-examples/bria_client.sh)** — 用于所有端点的 Shell 脚本函数

## 相关技能

- **[vgl](../vgl/SKILL.md)** — 使用结构化的 VGL JSON 提示来实现对 FIBO 图像生成的精确控制 |
- **[image-utils](../image-utils/SKILL.md)** — 提供经典的图片处理功能（缩放、裁剪、合成、添加水印）以用于后期处理