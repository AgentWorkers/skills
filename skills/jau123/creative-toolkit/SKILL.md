---
name: "AI Image Generation & Editor — Nanobanana, GPT Image, ComfyUI"
description: **使用多供应商路由功能从文本生成图像**——支持 Nanobanana 2、Seedream 5.0、GPT Image 以及本地 ComfyUI 工作流程。提供了超过 1,300 个精心挑选的提示（prompt），并支持基于风格的提示优化功能。适用于用户需要创建图像、设计资产、优化提示内容或管理 AI 艺术工作流程的场景。
version: 1.0.13
homepage: https://github.com/jau123/MeiGen-AI-Design-MCP
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["mcporter","npx","node"]}}}
---
# 创意工具包

通过一个统一的接口，您可以调用多个AI提供商来生成专业的AI图像。该工具包支持搜索精心策划的创意提示、将简单的想法转化为可用于实际制作的描述内容，以及管理ComfyUI工作流程——所有这些功能都通过一个MCP服务器实现。

## 快速入门

将MCP服务器添加到您的mcporter配置文件（`~/.config/mcporter/config.json`）中：

```json
{
  "mcpServers": {
    "creative-toolkit": {
      "command": "npx",
      "args": ["-y", "meigen@1.2.5"]
    }
  }
}
```

以下免费工具（搜索、优化、启发创意）可立即使用，无需API密钥：

```bash
mcporter call creative-toolkit.search_gallery query="cyberpunk"
mcporter call creative-toolkit.enhance_prompt brief="a cat in space" style="realistic"
```

要启用图像生成功能，请配置以下提供商之一：

| 提供商 | 配置参数 | 所需信息 |
|----------|--------|---------------|
| **MeiGen Cloud** | `MEIGEN_API_TOKEN` | 来自[meigen.ai](https://www.meigen.ai)的API密钥（在“设置”→“API密钥”中获取） |
| **本地ComfyUI** | `comfyuiUrl` | 运行中的ComfyUI实例（无需外部API） |
| **任何支持OpenAI的API** | `openaiApiKey` + `openaiBaseUrl` + `openaiModel` | 来自Together AI、Fireworks AI等平台的API密钥 |

请将相应的配置信息添加到`~/.clawdbot/.env`或`~/.config/meigen/config.json`文件中，或直接在mcporter配置文件中添加`"env"`块。详情请参阅`references/providers.md`。

## 可用工具

### 免费工具（无需API密钥）

| 工具 | 功能 |
|------|-------------|
| `search_gallery` | 在1,300多个AI图像提示中进行语义搜索，支持分类筛选和精选浏览。返回提示文本、缩略图和元数据。 |
| `get_inspiration` | 获取任何图像条目的完整提示内容和高分辨率图片。可在`search_gallery`之后使用，以获取可复制的提示内容。 |
| `enhance.prompt` | 将简短的创意想法扩展为包含光线、构图和材质细节的详细提示，支持真实风格、动漫风格和插画风格。 |
| `list_models` | 列出所有已配置提供商提供的模型及其功能和特性。 |

### 需要配置提供商的工具

| 工具 | 功能 |
|------|-------------|
| `generate_image` | 根据文本提示生成图像，自动选择最适合的提供商。支持调整图像比例、种子图像和参考图像。 |
| `upload_reference_image` | 压缩本地图像（最大2MB，2048像素），并将其上传到临时存储空间（有效期24小时），作为风格参考。ComfyUI用户可以直接提供本地文件路径给`generate_image`使用。 |
| `comfyui_workflow` | 列出、查看、导入、修改和删除ComfyUI工作流程模板。无需编辑JSON文件即可调整步骤、CFG比例、采样器和检查点。 |
| `manage_preferences` | 保存和加载用户偏好设置（默认风格、图像比例、风格说明、常用提示等）。 |

## 重要规则

### 严禁描述生成的图像

生成后的图像不可被用户直接查看。在展示结果时，只能提供工具返回的原始数据：

```
**Direction 1: Modern Minimal**
- Image URL: https://images.meigen.art/...
- Saved to: ~/Pictures/meigen/2026-02-08_xxxx.jpg
```

**严禁**对生成的图像进行任何主观评价或描述。

### 严禁指定模型或提供商

除非用户明确要求，否则不要在`generate_image`函数中指定`model`或`provider`参数。系统会自动选择最适合的提供商和模型。

### 生成多张图像前务必确认

当用户需要多个变体时，首先展示所有可选方案，并询问用户希望尝试的方向。务必提供“全部选项”作为选择之一。未经用户确认，切勿自动生成所有变体。

---

## 工作流程模式

### 模式1：单张图像

用户只需生成一张图像。编写提示内容（如果描述简短，可以直接使用`enhance_prompt`），生成图像后提供相应的URL和文件路径。

### 模式2：提示优化 + 图像生成

对于描述简短（少于30个词）且缺乏视觉细节的想法，先使用`enhance_prompt`进行优化：

```
1. enhance_prompt brief="futuristic city" style="realistic"
   -> Returns detailed prompt with camera lens, lighting, atmospheric effects

2. generate_image prompt="<enhanced prompt>" aspectRatio="16:9"
```

### 模式3：并行生成（多张图像）

用户需要多个不同的图像变体（例如不同的风格或概念）：

1. 列出所有可能的生成方向。
2. 询问用户希望尝试的方向。
3. 为每个方向编写独立的提示内容（不要只是修改一个词）。
4. 生成选定的图像变体（API提供商最多支持同时生成4个变体，ComfyUI每次生成1个）。
5. 提供生成的图像URL和文件路径。

### 模式4：多步骤创作（基础设计 + 派生设计）

用户需要一个基础设计及其衍生版本（例如设计一个标志并制作原型）：

1. 规划3-5个设计方向，询问用户希望尝试的方向。
2. 生成选定的方向对应的图像。
3. 展示结果，征求用户意见或请求尝试其他方向。
4. 使用已生成的图像URL作为参考，进一步设计衍生内容。
5. 生成最终的衍生图像。

**切勿跳过规划步骤，直接生成所有图像。**

### 模式5：编辑/修改现有图像

用户提供一张图像并请求进行修改（例如添加文字、更换背景等）：

- 如果使用的是本地图像，请先上传该图像。
- 使用简短的提示内容来描述修改内容（仅限于描述修改的部分）。
- 参考图像包含了所有的视觉背景信息，切勿重新描述原始图像。
- 示例提示：“在图像底部添加‘meigen.ai’字样”。

### 模式6：创意灵感搜索

```
1. search_gallery query="dreamy portrait with soft light"
   -> Finds semantically similar prompts with thumbnails

2. get_inspiration id="<entry_id>"
   -> Get full prompt text — copy and modify for your own generation
```

### 模式7：使用参考图像生成新图像

利用现有的图像来指导新图像的风格设计：

```
1. upload_reference_image filePath="~/Desktop/my-logo.png"
   -> Compresses and returns a temporary URL (expires in 24 hours)

2. generate_image prompt="coffee mug mockup with this logo" referenceImages=["<url>"]
```

参考图像来源：图库URL、之前生成的图像URL，或通过`upload_reference_image`上传的本地图像文件。ComfyUI用户可以直接提供本地文件路径，无需上传。

### 模式8：ComfyUI工作流程管理

```
1. comfyui_workflow action="list"           -> See saved workflows
2. comfyui_workflow action="view" name="txt2img"  -> See adjustable parameters
3. comfyui_workflow action="modify" name="txt2img" modifications={"steps": 30}
4. generate_image prompt="..." workflow="txt2img"  -> Generate
```

## 替代提供商

您也可以使用自己支持的OpenAI兼容API或本地ComfyUI实例，替代或与默认的MeiGen提供商一起使用。详细配置信息、模型价格和提供商对比请参阅`references/providers.md`。

## 故障排除

有关常见问题、解决方案以及安全性和隐私方面的信息，请参阅`references/troubleshooting.md`。