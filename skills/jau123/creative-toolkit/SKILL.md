---
name: "AI Image Generator & Editor — Nanobanana, GPT Image, ComfyUI"
description: **使用多供应商路由功能从文本生成图像**——支持 Nanobanana 2、Seedream 5.0、GPT Image 以及本地 ComfyUI 工作流程。提供超过 1,300 个精心挑选的提示（prompt）以及基于样式识别的提示优化功能。适用于用户需要生成图像、设计资源、优化提示内容或管理 AI 艺术工作流程的场景。
version: 1.0.10
homepage: https://github.com/jau123/MeiGen-AI-Design-MCP
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["mcporter","npx","node"],"env":["MEIGEN_API_TOKEN"]}}}
---
# 创意工具包

通过一个统一的接口，您可以调用多个AI生成服务来创建专业的AI图像。该接口能够搜索精心策划的提示语，将简单的创意转化为可用于实际制作的描述，并管理本地ComfyUI工作流程——所有这些操作都可以在一个MCP服务器上完成。

## 快速入门

1. 将MCP服务器添加到您的`mcporter`配置文件（`~/.config/mcporter/config.json`）中：

```json
{
  "mcpServers": {
    "creative-toolkit": {
      "command": "npx",
      "args": ["-y", "meigen@1.2.4"],
      "env": {
        "MEIGEN_API_TOKEN": "${MEIGEN_API_TOKEN}"
      }
    }
  }
}
```

2. 在`~/.clawdbot/.env`或shell环境中设置您的API密钥：

```bash
export MEIGEN_API_TOKEN="meigen_sk_..."
```

3. 生成您的第一张图像：

```bash
mcporter call creative-toolkit.generate_image prompt="a minimalist perfume bottle on white marble, soft directional lighting, product photography"
```

或者，如果您不想进行任何配置，也可以尝试使用临时的标准输入模式：

```bash
mcporter call --stdio "npx -y meigen@1.2.4" generate_image prompt="a ceramic vase with morning light"
```

**没有API密钥？** 免费工具仍然可以使用：

```bash
mcporter call creative-toolkit.search_gallery query="cyberpunk"
mcporter call creative-toolkit.enhance_prompt brief="a cat in space" style="realistic"
```

## 设置

### 获取API密钥

1. 访问[meigen.ai](https://www.meigen.ai) → 登录 → 点击头像 → **设置** → **API密钥**
2. 创建一个新的密钥（以`meigen_sk_`开头）
3. 将密钥设置为环境变量或保存到配置文件中：

```bash
# Shell environment or ~/.clawdbot/.env
export MEIGEN_API_TOKEN="meigen_sk_..."
```

或者将其保存到`~/.config/meigen/config.json`中：

```json
{
  "meigenApiToken": "meigen_sk_..."
}
```

### 替代提供商

您可以使用自己兼容OpenAI的API，或者使用本地的ComfyUI实例，作为默认提供商的替代方案。请将相关配置保存到`~/.config/meigen/config.json`中：

**OpenAI / Together AI / Fireworks AI:**

```json
{
  "openaiApiKey": "sk-...",
  "openaiBaseUrl": "https://api.together.xyz/v1",
  "openaiModel": "black-forest-labs/FLUX.1-schnell"
}
```

**本地ComfyUI:**

```json
{
  "comfyuiUrl": "http://localhost:8188"
}
```

您可以使用`comfyui_workflow`工具来导入工作流程（命令：`import`）。服务器会自动检测关键节点（如KSampler、CLIPTextEncode、EmptyLatentImage），并在运行时填充提示语、种子图像和图像尺寸等信息。

您可以同时配置多个提供商。自动检测的优先级顺序为：MeiGen > ComfyUI > OpenAI。

## 可用工具

### 免费工具（无需API密钥）

| 工具 | 功能 |
|------|-------------|
| `search_gallery` | 在AI图像提示语中进行语义搜索——找到概念上相似的结果，而不仅仅是关键词匹配。支持分类过滤和精选浏览。返回提示语文本、缩略图和元数据。 |
| `get_inspiration` | 获取任何图库条目的完整提示语和高分辨率图像。在`search_gallery`之后使用，以获取可复制的提示语。 |
| `enhance_prompt` | 将简短的创意（例如“太空中的猫”）扩展为包含光线、构图和材质细节的详细提示语。支持三种风格：写实、动漫、插画。 |
| `list_models` | 列出所有可用提供商提供的模型及其功能和特性。 |

### 需要配置提供商的工具

| 工具 | 功能 |
|------|-------------|
| `generate_image` | 根据文本提示生成图像。会自动选择最适合的提供商。支持调整纵横比、种子图像和参考图像。 |
| `upload_reference_image` | 压缩本地图像（最大2MB，2048px），以便在`generate_image`中用作风格参考。需要用户手动调用。 |
| `comfyui_workflow` | 列出、查看、导入、修改和删除ComfyUI工作流程模板。无需编辑JSON文件即可调整参数，如步骤、CFG比例、采样器和检查点。 |

## 使用方式

### 基本生成

服务器会选择最适合的提供商来生成图像，并返回图像的URL和本地文件路径。

### 先增强提示语再生成图像

对于简单的创意，先对其进行增强处理，可以获得更好的结果：

```
1. enhance_prompt brief="futuristic city" style="realistic"
   → Returns detailed prompt with camera lens, lighting setup, atmospheric effects

2. generate_image prompt="<enhanced prompt>" aspectRatio="16:9"
   → Generates with the enhanced prompt
```

### 使用参考图像指导生成风格

使用现有的图像来指导生成的视觉风格：

```
1. upload_reference_image filePath="~/Desktop/my-logo.png"
   → Compresses and returns a reference ID

2. generate_image prompt="coffee mug mockup with this logo" referenceImages=["<id>"]
   → Generates using the reference for style guidance
```

### 图库探索

语义搜索能够理解您的需求——“带有柔和光线的梦幻肖像”即使没有完全匹配的关键词也能找到相关结果：

```
1. search_gallery query="dreamy portrait with soft light"
   → Finds semantically similar prompts with thumbnails

2. search_gallery category="Product & Brand"
   → Browse by category from 1,300+ curated prompts

3. get_inspiration id="<entry_id>"
   → Get full prompt text — copy and modify for your own generation
```

### ComfyUI工作流程

```
1. comfyui_workflow action="list"
   → See saved workflows

2. comfyui_workflow action="view" name="txt2img"
   → See adjustable parameters (steps, CFG, sampler, checkpoint)

3. comfyui_workflow action="modify" name="txt2img" modifications={"steps": 30, "cfg": 7.5}
   → Adjust without editing JSON

4. generate_image prompt="..." workflow="txt2img"
   → Generate using the custom workflow
```

## 提供商比较

| | MeiGen平台 | 兼容OpenAI | ComfyUI（本地） |
|---|---|---|---|
| **模型** | Nanobanana 2、Seedream 5.0、GPT Image 1.5等 | 终端上的任何模型 | 您机器上的任何检查点 |
| **参考图像** | 支持原生导入 | 仅支持gpt-image-1.5 | 需要LoadImage节点 |
| **并发处理** | 最多支持4个并发任务 | 最多支持4个并发任务 | 由于GPU限制，一次只能处理1个任务 |
| **延迟** | 通常为10-30秒 | 因提供商而异 | 取决于硬件配置 |
| **费用** | 基于API密钥的费用 | 由提供商收取费用 | 免费（使用您的硬件） |
| **离线使用** | 不支持 | 不支持 | 支持离线使用 |

## MeiGen模型定价

| 模型 | 所需信用点数 | 是否支持4K输出 | 适合的场景 |
|-------|---------|-----|----------|
| Nanobanana 2（默认） | 5 | 支持4K输出 | 通用用途，高质量图像 |
| Seedream 5.0 Lite | 5 | 支持4K输出 | 快速生成，风格化图像 |
| GPT Image 1.5 | 2 | 不支持4K输出 | 经济型模型 |
| Nanobanana Pro | 10 | 支持4K输出 | 高端质量图像 |
| Seedream 4.5 | 5 | 支持4K输出 | 支持风格化图像，宽高比灵活 |
| Midjourney Niji 7 | 15 | 不支持4K输出 | 适合动漫和插画风格 |

如果没有指定模型，服务器将默认使用Nanobanana 2。

## 提示语增强风格

`enhance_prompt`支持三种风格模式，每种模式会产生不同的细节表现：

| 风格 | 重点 | 适用场景 |
|-------|-------|----------|
| **写实** | 相机镜头、光圈、焦距、光线方向、材质纹理 | 产品照片、肖像、建筑场景 |
| **动漫** | 视觉构图、角色细节（眼睛、头发、服装）、关键词 | 动漫插画、角色设计 |
| **插画** | 艺术媒介、色彩搭配、构图方向、笔触风格 | 概念艺术、数字绘画、水彩画 |

## 安全性与隐私

**固定版本**：此功能作为MCP服务器通过`npx meigen@1.2.4`运行（固定版本，非浮动版本）。该软件包在[npmjs.com](https://www.npmjs.com/package/meigen)上发布，源代码托管在[GitHub](https://github.com/jau123/MeiGen-AI-Design-MCP)上。代码经过标准TypeScript编译后，没有进行任何混淆或压缩处理。

**参考图像**：`upload_reference_image`工具会压缩用户指定的图像（最大2MB，2048px），以用作生成图像时的风格参考。该操作完全由用户发起，不会自动访问任何文件。压缩后的图像只会发送到用户配置的图像生成提供商，与任何图像生成API的处理方式相同。

**API密钥**：`MEIGEN_API_TOKEN`存储在环境变量或`~/.config/meigen/config.json`中，并设置权限为`chmod 600`。密钥仅会被发送到配置的提供商的API端点，不会被记录或传输给第三方。

**无数据收集**：MCP服务器不会收集分析数据或使用情况信息，也不会将任何信息发送给第三方。

## 故障排除

- **“未配置图像生成提供商”**：请设置`MEIGEN_API_TOKEN`，或在`~/.config/meigen/config.json`中配置其他提供商。
- **生成过程中超时**：图像生成通常需要10-30秒。在高需求时段，可能需要更长时间。服务器会每隔5分钟进行一次检查。
- **无法连接ComfyUI**：请确保ComfyUI正在运行，并且可以在配置的URL上访问。可以使用`curl <url>/system_stats`进行测试。
- **找不到模型**：运行`list_models`以查看可用模型。

**参考图像被拒绝**：参考图像需要有效的URL。请使用`upload_reference_image`先准备本地图像文件。