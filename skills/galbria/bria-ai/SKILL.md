---
name: bria-ai
description: 使用 Bria.ai 提供的商业安全 AI 模型，可以实现可控的图像生成与编辑功能。您可以精细地控制生成、编辑或删除的内容：通过文本指令进行编辑，对特定区域进行遮罩处理，添加/替换/删除单个对象，独立调整图像的光线、色调和风格。该功能非常适合用于构建需要产品图片、封面图片、图标、插图或背景的网站、应用程序或文档。同时，它也适用于电子商务产品摄影、背景去除、图像缩放、风格转换以及批量处理工作流程（生成 -> 编辑 -> 去除背景）。该功能会在涉及 AI 图像生成、可控图像编辑、背景去除或视觉资产创建的任务中被自动触发。
license: MIT
metadata:
  author: Bria AI
  version: "1.2.1"
---
# Bria — 可控的图像生成与编辑

使用 Bria 的商业级安全 AI 模型（FIBO、RMBG-2.0、GenFill 等）来生成并精确控制视觉资产。与黑盒生成器不同，Bria 提供了细粒度的控制功能：可以通过文本指令进行编辑、遮罩特定区域、添加/替换/删除单个对象、独立调整光照或季节效果，以及在不同操作之间进行流程化处理。

## 设置 — API 密钥检查

在进行任何 Bria API 调用之前，请检查 API 密钥，并在密钥缺失时指导用户进行设置：

### 第 1 步：检查密钥是否存在

```bash
echo $BRIA_API_KEY
```

如果输出结果 **不为空**，则跳转到下一节。

### 第 2 步：如果密钥缺失，指导用户

在浏览器中打开 Bria 的 API 密钥页面：

```bash
open "https://platform.bria.ai/console/account/api-keys?utm_source=skill&utm_campaign=bria_skills&utm_content=adjust_photoshop_for_agent"   # macOS
# xdg-open "https://platform.bria.ai/console/account/api-keys?utm_source=skill&utm_campaign=bria_skills&utm_content=adjust_photoshop_for_agent"  # Linux
```

然后告诉用户：
> 我已经在您的浏览器中打开了 Bria 网站。要使用图像生成功能，您需要一个免费的 API 密钥。
>
> 1. 在我刚刚打开的页面上注册或登录
> 2. 点击 **创建 API 密钥**
> 3. 复制密钥并 **粘贴到这里**

等待用户提供他们的 API 密钥。在收到密钥之前，请勿继续操作。

### 第 3 步：永久保存密钥

用户提供密钥后，将其保存以便在会话之间保持一致。

**在 macOS/Linux 上**，检测 shell 并将其添加到正确的配置文件中：

```bash
# Detect the shell profile
if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = */zsh ]; then
  PROFILE_FILE="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  PROFILE_FILE="$HOME/.bashrc"
else
  PROFILE_FILE="$HOME/.profile"
fi

# Append the export (only if not already present)
grep -q 'export BRIA_API_KEY=' "$PROFILE_FILE" 2>/dev/null && \
  sed -i.bak '/export BRIA_API_KEY=/d' "$PROFILE_FILE"
echo 'export BRIA_API_KEY="THE_KEY_THE_USER_GAVE_YOU"' >> "$PROFILE_FILE"

# Make it available immediately in this session
export BRIA_API_KEY="THE_KEY_THE_USER_GAVE_YOU"
```

**在 Windows（PowerShell）上**：

```powershell
[System.Environment]::SetEnvironmentVariable("BRIA_API_KEY", "THE_KEY_THE_USER_GAVE_YOU", "User")
$env:BRIA_API_KEY = "THE_KEY_THE_USER_GAVE_YOU"
```

将 `THE_KEY_THE_USER_GAVE_YOU` 替换为用户提供的实际密钥。

### 第 4 步：验证

```bash
echo $BRIA_API_KEY
```

确认密钥已设置完成后，告诉用户：
> 您的 API 密钥已保存，并将在会话之间保持一致。现在您可以开始进行图像生成或编辑了！

**请确保 API 密钥已正确设置后再继续操作。**

---

## 核心功能

| 需求 | 功能 | 使用场景 |
|------|------------|----------|
| 创建新图像 | FIBO Generate | 主角图片、产品照片、插图 |
| 通过文本编辑 | FIBO-Edit | 更改颜色、修改对象、变换场景 |
| 带遮罩编辑 | GenFill/Erase | 精确修复图像、添加/替换特定区域 |
| 添加/替换/删除对象 | 基于文本的编辑 | 添加花瓶、将苹果替换为梨、删除桌子 |
| 透明背景 | RMBG-2.0 | 提取用于叠加、徽标、裁剪的图像元素 |
| 背景处理 | 替换/模糊/删除 | 更改、模糊或删除背景 |
| 扩展图像 | 图像修补 | 扩展图像边界、调整纵横比 |
| 提升图像质量 | 图像增强 | 改善光照、颜色、细节 |
| 变换风格 | 风格转换 | 油画、动漫、卡通、3D 渲染 |
| 调整光照 | 重新布光 | 金色时刻、聚光灯、戏剧性光照效果 |
| 更改季节 | 调整季节 | 春季、夏季、秋季、冬季 |
| 混合/合成 | 图像合成 | 应用纹理、徽标、合并图像 |
| 文本替换 | 替换文本 | 更改图像中的文字 |
| 恢复照片 | 照片修复 | 修复旧照片或损坏的照片 |
| 上色 | 上色 | 为黑白图像添加颜色，或将图像转换为黑白 |
| 从草图转换为照片 | Sketch2Image | 将绘图转换为真实照片 |
| 产品摄影 | 产品生活方式拍摄 | 将产品放入场景中 |

## 快速参考

### 生成图像（FIBO）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "your description",
    "aspect_ratio": "16:9"
  }'
```

**纵横比**：`1:1`（正方形）、`16:9`（主角/横幅）、`4:3`（演示文稿）、`9:16`（手机/故事）、`3:4`（肖像）

> **高级**：为了实现对生成过程的精确控制，请使用 **[VGL 结构化提示](../vgl/SKILL.md)**，而不是自然语言。VGL 以明确的 JSON 格式定义了所有视觉属性（对象、光照、构图）。

### 去除背景（RMBG-2.0）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/remove_background" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://..."}'
```

返回带有透明度的 PNG 图像。

### 不使用遮罩编辑图像（FIBO-Edit）

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "images": ["https://..."],
    "instruction": "change the mug to red"
  }'
```

### 带遮罩编辑图像区域（GenFill）

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

### 扩展图像（图像修补）

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

### 提升图像质量

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/increase_resolution" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://...", "scale": 2}'
```

### 产品生活方式拍摄

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

## 异步响应处理

所有端点都会返回异步响应：

```json
{
  "request_id": "uuid",
  "status_url": "https://engine.prod.bria-api.com/v2/status/uuid"
}
```

不断轮询 `status_url`，直到返回 `status: "COMPLETED"`，然后获取 `result.image_url`。

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

## 提示工程技巧

- **风格**：例如 “专业产品摄影” 对比 “休闲快照”，“平面设计插图” 对比 “3D 渲染”
- **光照**：例如 “柔和的自然光” 对比 “摄影室灯光”，“戏剧性的阴影”
- **背景**：例如 “白色摄影室背景”、“渐变背景”、“模糊的办公室背景”、“透明背景”
- **构图**：例如 “居中构图”、“三分法则”、“左侧留白用于文字”
- **质量相关关键词**：例如 “高质量”、“专业级”、“商业级”、“4K”、“清晰对焦”
- **负面提示**：例如 “模糊的、低质量的、像素化的图像”、“包含文字的水印、徽标”

---

## API 参考

请参阅 `references/api-endpoints.md` 以获取完整的端点文档。

### 主要端点

**生成**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/generate` | 从文本生成图像（FIBO） |

**通过文本编辑（无需遮罩）**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit` | 使用自然语言指令编辑图像 |
| `POST /v2/image/edit/add_object_by_text` | 向图像中添加对象 |
| `POST /v2/image/edit/replace_object_by_text` | 通过文本替换图像中的对象 |
| `POST /v2/image/edit/erase_by_text` | 按名称删除图像中的对象 |

**带遮罩编辑**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/gen_fill` | 在遮罩区域内进行修复/生成新内容 |
| `POST /v2/image/edit/erase` | 删除遮罩区域 |

**背景处理**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/remove_background` | 删除背景（RMBG-2.0） |
| `POST /v2/image/edit/replace_background` | 用 AI 生成的背景替换背景 |
| `POST /v2/image/edit/blur_background` | 使背景模糊 |
| `POST /v2/image/edit/erase_foreground` | 删除前景、填充背景 |
| `POST /v2/image/edit/crop_foreground` | 紧贴主体裁剪背景 |

**图像变换**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/expand` | 将图像调整到新的纵横比 |
| `POST /v2/image/edit/enhance` | 提升图像质量和细节 |
| `POST /v2/image/edit/increase_resolution` | 将图像分辨率提升 2 倍或 4 倍 |
| `POST /v2/image/edit/blend` | 合并图像或纹理 |
| `POST /v2/image/edit/reseason` | 更改季节或天气效果 |
| `POST /v2/image/edit/restyle` | 变换艺术风格 |
| `POST /v2/image/edit/relight` | 修改图像光照 |

**文本与修复**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/replace_text` | 更改图像中的文本 |
| `POST /v2/image/edit/sketch_to_image` | 将草图转换为照片 |
| `POST /v2/image/edit/restore` | 修复旧照片或损坏的照片 |
| `POST /v2/image/edit/colorize` | 为黑白图像添加颜色，或将图像转换为黑白 |

**产品摄影**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/image/edit/lifestyle_shot_by_text` | 根据文本描述将产品放入场景中 |

**实用工具**
| 端点 | 功能 |
|----------|---------|
| `POST /v2/structured_instruction/generate` | 生成 JSON 指令（不生成图像） |
| `GET /v2/status/{id}` | 查查异步请求的状态 |

### 认证

所有请求都需要包含 `api_token` 标头：
```
api_token: YOUR_BRIA_API_KEY
```

---

## 额外资源

- **[API 端点参考](references/api-endpoints.md)** — 完整的端点文档，包含请求/响应格式
- **[工作流程与管道](references/workflows.md)** — 批量生成、并行处理流程、集成示例
- **[Python 客户端](references/code-examples/bria_client.py)** — 全功能异步 Python 客户端
- **[TypeScript 客户端](references/code-examples/bria_client.ts)** — 类型化的 Node.js 客户端
- **[Bash/curl 参考](references/code-examples/bria_client.sh)** — 用于所有端点的 Shell 脚本函数

## 相关技能

- **[vgl](../vgl/SKILL.md)** — 编写结构化的 VGL JSON 提示，以实现對 FIBO 图像生成的精确控制
- **[image-utils](../image-utils/SKILL.md)** — 用于后期处理的经典图像操作（缩放、裁剪、合成、水印）