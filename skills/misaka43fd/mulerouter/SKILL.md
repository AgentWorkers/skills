---
name: mulerouter
description: 使用 MuleRouter 或 MuleRun 的多模态 API 生成图像和视频。支持文本转图像、图像转图像、文本转视频以及视频编辑（包括 VACE、关键帧插值等功能）。适用于用户需要利用 Wan2.6、Veo3、Nano Banana Pro、Sora2、Midjourney 等 AI 模型来生成、编辑或转换图像和视频的场景。
compatibility: Requires Python 3.10+, uv, MULEROUTER_API_KEY env var, and one of MULEROUTER_BASE_URL or MULEROUTER_SITE env var. Needs network access to api.mulerouter.ai or api.mulerun.com. The API key is sent in Authorization headers to the configured endpoint.
allowed-tools: Bash Read
---
# MuleRouter API

使用 MuleRouter 或 MuleRun 的多模态 API 生成图片和视频。

## 所需的环境变量

在使用此功能之前，需要设置以下环境变量：

| 变量 | 是否必填 | 说明 |
|----------|----------|-------------|
| `MULEROUTER_API_KEY` | **是** | 用于身份验证的 API 密钥（[在此处获取](https://www.mulerouter.ai/app/api-keys?utm_source=github_claude_plugin) |
| `MULEROUTER_BASE_URL` | **是** | 自定义的 API 基础 URL（例如：`https://api.mulerouter.ai`）。优先于 `MULEROUTER_SITE`。 |
| `MULEROUTER_SITE` | **是** | API 站点：`mulerouter` 或 `mulerun`。当 `MULEROUTER_BASE_URL` 未设置时使用。 |

*必须至少设置 `MULEROUTER_BASE_URL` 或 `MULEROUTER_SITE` 中的一个。*

在向配置的 API 端点发起网络请求时，API 密钥会包含在 `Authorization: Bearer` 标头中。

**如果缺少任何这些变量，脚本将因配置错误而失败。** 请查看下面的配置部分进行设置。

## 配置检查

在运行任何命令之前，请验证配置是否正确：

### 第 1 步：检查现有配置

```bash
# Check environment variables
echo "MULEROUTER_BASE_URL: $MULEROUTER_BASE_URL"
echo "MULEROUTER_SITE: $MULEROUTER_SITE"
echo "MULEROUTER_API_KEY: ${MULEROUTER_API_KEY:+[SET]}"

# Check for .env file
ls -la .env 2>/dev/null || echo "No .env file found"
```

### 第 2 步：根据需要配置

**如果上述变量未设置**，请让用户提供他们的 API 密钥和首选的 API 端点，然后使用以下选项之一进行配置：

**选项 A：带有自定义基础 URL 的环境变量（优先级最高）**
```bash
export MULEROUTER_BASE_URL="https://api.mulerouter.ai"  # or your custom API endpoint
export MULEROUTER_API_KEY="your-api-key"
```

**选项 B：带有站点名称的环境变量（当基础 URL 未设置时使用）**
```bash
export MULEROUTER_SITE="mulerun"    # or "mulerouter"
export MULEROUTER_API_KEY="your-api-key"
```

**选项 C：创建 `.env` 文件**

在当前工作目录中创建 `.env` 文件：

```env
# Option 1: Use custom base URL (takes priority over SITE)
MULEROUTER_BASE_URL=https://api.mulerouter.ai
MULEROUTER_API_KEY=your-api-key

# Option 2: Use site (if BASE_URL not set)
# MULEROUTER_SITE=mulerun
# MULEROUTER_API_KEY=your-api-key
```

**注意：** `MULEROUTER_BASE_URL` 的优先级高于 `MULEROUTER_SITE`。如果两者都设置了，将使用 `MULEROUTER_BASE_URL`。

**注意：** 该功能在启动时会从当前工作目录加载 `.env` 文件。请仅在此文件中存储与 MuleRouter 相关的变量。避免在运行此功能的目录中的 `.env` 文件中存储无关的敏感信息。**

### 第 3 步：使用 `uv` 运行脚本

该功能使用 `uv` 来管理依赖关系并执行脚本。请确保 `uv` 已安装并且可以在您的 PATH 中找到。

运行 `uv sync` 来安装依赖关系。

## 快速入门

### 1. 列出可用模型

```bash
uv run python scripts/list_models.py
```

### 2. 检查模型参数

```bash
uv run python models/alibaba/wan2.6-t2v/generation.py --list-params
```

### 3. 生成内容

**文本转视频：**
```bash
uv run python models/alibaba/wan2.6-t2v/generation.py --prompt "A cat walking through a garden"
```

**文本转图片：**
```bash
uv run python models/alibaba/wan2.6-t2i/generation.py --prompt "A serene mountain lake"
```

**图片转视频：**
```bash
uv run python models/alibaba/wan2.6-i2v/generation.py --prompt "Gentle zoom in" --image "https://example.com/photo.jpg" #remote image url
```
```bash
uv run python models/alibaba/wan2.6-i2v/generation.py --prompt "Gentle zoom in" --image "/path/to/local/image.png" #local image path
```

## 图片输入

对于图片参数（`--image`、`--images` 等），**建议使用本地文件路径** 而不是 base64 编码的字符串。

```bash
# Preferred: local file path (auto-converted to base64)
--image /tmp/photo.png

--images ["/tmp/photo.png"]
```

该功能会自动读取本地文件路径，将其转换为 base64 编码，然后将编码后的数据发送给 API。这样可以避免使用原始 base64 字符串时可能出现的命令行长度限制。

## 工作流程

1. 检查配置：验证 `MULEROUTER_API_KEY` 以及 `MULEROUTER_BASE_URL` 或 `MULEROUTER_SITE` 是否已设置
2. 安装依赖关系：运行 `uv sync`
3. 运行 `uv run python scripts/list_models.py` 以查看可用模型
4. 运行 `uv run python models/<path>/<action>.py --list-params` 以查看模型参数
5. 使用适当的参数执行命令
6. 解析结果中的输出 URL

## 模型选择

在列出模型时，每个模型的 **标签**（例如 `[SOTA]`）会默认显示在其名称旁边。标签有助于一目了然地识别模型的特性——例如，`SOTA` 表示该模型是最先进的模型。

您还可以使用 `--tag` 参数按标签过滤模型：
```bash
uv run python scripts/list_models.py --tag SOTA
```

**如果您不确定使用哪个模型**，可以向用户展示可用的模型选项，并让他们进行选择。可以使用 `AskUserQuestion` 工具（或类似的交互式提示）来询问用户他们希望使用哪个模型。例如，如果用户请求“生成一张图片”但没有指定模型，可以列出相关的图片生成模型及其标签和描述，然后让用户选择一个。

## 提示
1. 对于图片生成模型，建议的超时时间为 5 分钟。
2. 对于视频生成模型，建议的超时时间为 15 分钟。

## 参考资料

- [REFERENCE.md](references/REFERENCE.md) - API 配置和 CLI 选项
- [MODELS.md](references/MODELS.md) - 完整的模型规格说明