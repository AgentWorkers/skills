---
name: creative-toolkit
description: **使用多供应商路由从文本生成图像**——支持 Nanobanana Pro、GPT Image、Seedream 以及本地的 ComfyUI 工作流程。系统提供了 1,300 多个精心挑选的提示（prompt），并具备基于风格的提示优化功能。适用于用户需要创建图像、设计资产、优化提示内容或管理 AI 艺术工作流程的场景。
version: 1.0.3
homepage: https://github.com/jau123/MeiGen-AI-Design-MCP
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["mcporter"],"env":["MEIGEN_API_TOKEN"]},"primaryEnv":"MEIGEN_API_TOKEN"}}
---
# 创意工具包

通过一个统一的接口，您可以调用多个AI服务来生成专业的AI图像。该接口能够搜索精心策划的提示语，将简单的创意转化为可用于实际制作的描述，并管理本地的ComfyUI工作流程——所有这些操作都可以在一个MCP服务器上完成。

## 快速入门

1. 将MCP服务器添加到您的`mcporter`配置文件（`~/.config/mcporter/config.json`）中：

```json
{
  "mcpServers": {
    "creative-toolkit": {
      "command": "npx",
      "args": ["-y", "meigen@latest"],
      "env": {
        "MEIGEN_API_TOKEN": "${MEIGEN_API_TOKEN}"
      }
    }
  }
}
```

2. 将您的API密钥设置到`~/.clawdbot/.env`文件或shell环境中：

```bash
export MEIGEN_API_TOKEN="meigen_sk_..."
```

3. 生成您的第一张图像：

```bash
mcporter call creative-toolkit.generate_image prompt="a minimalist perfume bottle on white marble, soft directional lighting, product photography"
```

或者，如果您不想进行任何配置，也可以尝试直接使用标准命令行模式：

```bash
mcporter call --stdio "npx -y meigen@latest" generate_image prompt="a ceramic vase with morning light"
```

**没有API密钥？** 免费工具仍然可以使用：

```bash
mcporter call creative-toolkit.search_gallery query="cyberpunk"
mcporter call creative-toolkit.enhance_prompt brief="a cat in space" style="realistic"
```

## 设置

### 获取API密钥

1. 访问[meigen.ai](https://www.meigen.ai) → 登录 → 点击头像 → **设置** → **API密钥**
2. 创建一个新的密钥（密钥名称以`meigen_sk_`开头）
3. 将密钥设置为环境变量或保存到配置文件中：

```bash
# Shell environment or ~/.clawdbot/.env
export MEIGEN_API_TOKEN="meigen_sk_..."
```

或者，您也可以将其保存到`~/.config/meigen/config.json`文件中：

```json
{
  "meigenApiToken": "meigen_sk_..."
}
```

### 替代提供商

您可以使用自己兼容OpenAI的API，或者使用本地的ComfyUI实例，作为默认提供商的替代方案。请将相关配置保存到`~/.config/meigen/config.json`文件中：

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

您可以使用`comfyui_workflow`工具导入工作流程（命令：`import`）。服务器会自动检测关键节点（如KSampler、CLIPTextEncode、EmptyLatentImage），并在运行时填充提示语、种子图像和图像尺寸等信息。

您可以同时配置多个提供商。自动检测的优先级顺序为：MeiGen > ComfyUI > OpenAI。

## 可用工具

### 免费工具（无需API密钥）

| 工具 | 功能 |
|------|-------------|
| `search_gallery` | 按关键词、风格或类别搜索1,300多个精心策划的提示语。返回提示语文本、缩略图和元数据。 |
| `get_inspiration` | 获取任何图库条目的完整提示语和高分辨率图片。在`search_gallery`之后使用该工具可获取可复制的提示语。 |
| `enhance_prompt` | 将简短的创意（例如“太空中的猫”）扩展为包含光线、构图和材质细节的详细提示语。支持三种风格：写实、动漫、插画。 |
| `list_models` | 列出所有已配置提供商提供的模型及其功能和特性。 |

### 需要配置提供商的工具

| 工具 | 功能 |
|------|-------------|
| `generate_image` | 根据文本提示生成图像。系统会自动选择最适合的提供商。支持调整图像的宽高比、使用种子图像以及指定参考图像。 |
| `upload_reference_image` | 压缩并上传本地图像（最大2MB，2048像素），作为生成图像时的风格参考。返回该图像的公共URL。 |
| `comfyui_workflow` | 列出、查看、导入、修改和删除ComfyUI工作流程模板。无需编辑JSON文件即可调整参数，如步骤、CFG比例、采样器和检查点。 |

## 使用方式

### 基本生成

```
Generate a product photo of a ceramic vase with morning light
```

服务器会自动选择最佳的提供商来生成图像，并返回图像的URL和本地文件路径。

### 先增强提示语再生成图像

对于简单的创意，先对其进行增强处理，可以获得更好的结果：

```
1. enhance_prompt brief="futuristic city" style="realistic"
   → Returns detailed prompt with camera lens, lighting setup, atmospheric effects

2. generate_image prompt="<enhanced prompt>" aspectRatio="16:9"
   → Generates with the enhanced prompt
```

### 使用参考图像

您可以使用现有的图像来指导图像的风格和构图：

```
1. upload_reference_image filePath="~/Desktop/my-logo.png"
   → Returns public URL

2. generate_image prompt="coffee mug mockup with this logo" referenceImages=["<url>"]
   → Generates using the reference for style guidance
```

所有提供商都支持使用参考图像。

### 浏览图库

```
1. search_gallery query="product photography" category="Product"
   → Browse thumbnails and prompts

2. get_inspiration id="<entry_id>"
   → Get full prompt text — copy and modify for your own generation
```

### 管理ComfyUI工作流程

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

## 提供商对比

| | MeiGen平台 | 兼容OpenAI的提供商 | 本地ComfyUI |
|---|---|---|---|
| **模型** | Nanobanana Pro、GPT Image 1.5、Seedream 4.5等 | 任何终端提供的模型 | 您机器上的任何检查点文件 |
| **参考图像** | 支持原生导入 | 仅支持gpt-image-1.5模型 | 需要使用LoadImage节点 |
| **并发处理** | 最多支持4个并发任务 | 最多支持4个并发任务 | 由于GPU限制，一次只能处理1个任务 |
| **响应时间** | 通常为10-30秒 | 因提供商而异 | 取决于硬件配置 |
| **费用** | 基于API密钥的费用 | 根据提供商收费 | 免费（使用您的硬件资源） |
| **离线使用** | 不支持 | 不支持 | 支持离线使用 |

## 提示语增强样式

`enhance_prompt`支持三种风格模式，每种模式会产生不同的细节表现：

| 样式 | 重点 | 适用场景 |
|-------|-------|----------|
| **写实** | 相机镜头、光圈、焦距、光线方向、材质纹理 | 产品照片、肖像、建筑效果图 |
| **动漫** | 关键视觉元素（眼睛、头发、服装等细节）、触发词 | 动漫插画、角色设计 |
| **插画** | 艺术媒介、色彩搭配、构图方向、笔触风格 | 概念艺术、数字绘画、水彩画 |

## 安全性与隐私

- **远程包执行**：该功能通过`npx meigen@latest`作为MCP服务器运行。该包在[npmjs.com](https://www.npmjs.com/package/meigen)上发布，源代码托管在[GitHub](https://github.com/jau123/MeiGen-AI-Design-MCP)上。代码经过标准TypeScript编译后，没有进行任何混淆或压缩处理。
- **参考图像上传**：`upload_reference_image`工具会压缩本地图像（最大2MB，2048像素），并将其上传到CDN服务器作为生成图像的参考。此操作完全由用户发起；工具不会在未经明确请求的情况下访问或上传任何文件。上传的图像仅用于图像生成时的风格参考。
- **API密钥**：`MEIGEN_API_TOKEN`存储在环境变量或`~/.config/meigen/config.json`文件中，并设置权限为`chmod 600`。密钥仅会被发送到配置好的提供商的API端点，不会被记录或传输给其他第三方。
- **数据安全**：MCP服务器不会收集任何分析数据或使用情况信息，也不会将任何数据发送给第三方。

## 常见问题解决方法

- **“未配置图像生成提供商”**：请设置`MEIGEN_API_TOKEN`，或在`~/.config/meigen/config.json`中配置其他提供商。
- **生成图像时超时**：图像生成通常需要10-30秒。在高需求时段，可能需要更长时间。服务器的请求间隔为5分钟。
- **无法连接到ComfyUI**：请确保ComfyUI正在运行，并且可以在配置的URL地址访问。可以使用`curl <url>/system_stats`进行测试。
- **找不到模型**：运行`list_models`命令查看可用的模型。
- **参考图像被拒绝**：请确保使用的参考图像是公共URL（而非本地路径）。可以使用`upload_reference_image`工具将本地文件转换为公共URL后再进行上传。