---
name: mulerouter
description: 使用 MuleRouter 或 MuleRun 的多模态 API 生成图像和视频。支持文本转图像、图像转图像、文本转视频以及视频编辑（包括 VACE 和关键帧插值等功能）。适用于用户需要利用 Wan2.6、Veo3、Nano Banana Pro、Sora2、Midjourney 等 AI 模型来生成、编辑或转换图像和视频的场景。
compatibility: Requires Python 3.10+, uv, MULEROUTER_API_KEY env var, and one of MULEROUTER_BASE_URL or MULEROUTER_SITE env var. Needs network access to api.mulerouter.ai or api.mulerun.com. The API key is sent in Authorization headers to the configured endpoint.
homepage: https://github.com/mulerouter/mulerouter-skills
allowed-tools: Bash(uv run *) Bash(uv sync *) Read
metadata:
  clawdbot:
    requires:
      env: ["MULEROUTER_API_KEY"]
      env_one_of: ["MULEROUTER_BASE_URL", "MULEROUTER_SITE"]
      bins: ["uv", "python3"]
    primaryEnv: "MULEROUTER_API_KEY"
    install: "uv sync"
    files: ["scripts/*", "models/*", "core/*", "pyproject.toml"]
---
# MuleRouter API

使用 MuleRouter 或 MuleRun 的多模态 API 生成图片和视频。

## 所需的环境变量

在使用此功能之前，需要设置以下环境变量：

| 变量 | 必需 | 说明 |
|----------|----------|-------------|
| `MULEROUTER_API_KEY` | **是** | 用于身份验证的 API 密钥（[在此处获取](https://www.mulerouter.ai/app/api-keys?utm_source=github_claude_plugin) |
| `MULEROUTER_BASE_URL` | **是** | 自定义 API 基础 URL（例如：`https://api.mulerouter.ai`）。此 URL 优先于 `MULEROUTER_SITE`。 |
| `MULEROUTER_SITE` | **是** | API 站点：`mulerouter` 或 `mulerun`。如果未设置 `MULEROUTER_BASE_URL`，则使用此字段。 |

在向配置的 API 端点发起网络请求时，API 密钥会包含在 `Authorization: Bearer` 请求头中。

**如果缺少任何这些变量，脚本将因配置错误而失败。** 请查看下面的配置部分进行设置。

## 配置检查

在运行任何命令之前，请验证配置是否正确：

### 第 1 步：检查现有配置

运行内置的配置检查脚本：

```bash
uv run python -c "from core.config import load_config; load_config(); print('Configuration OK')"
```

如果输出“Configuration OK”，则跳到 **第 3 步**；如果出现 `ValueError`，请继续执行第 2 步。

### 第 2 步：根据需要配置

**如果上述变量未设置**，请让用户提供他们的 API 密钥和首选的 API 端点。

在技能的工作目录中创建一个 `.env` 文件：

```env
# Option 1: Use custom base URL (takes priority over SITE)
MULEROUTER_BASE_URL=https://api.mulerouter.ai
MULEROUTER_API_KEY=your-api-key

# Option 2: Use site (if BASE_URL not set)
# MULEROUTER_SITE=mulerun
# MULEROUTER_API_KEY=your-api-key
```

**注意：** `MULEROUTER_BASE_URL` 优先于 `MULEROUTER_SITE`。如果两者都设置了，将使用 `MULEROUTER_BASE_URL`。

**注意：** 该技能仅从 `.env` 文件中加载以 `MULEROUTER_` 为前缀的变量。文件中的其他变量将被忽略。

**重要提示：** **不要使用 `export` 命令来设置凭据**。请使用 `.env` 文件，或在调用技能之前确保这些变量已经存在于您的 shell 环境中。

### 第 3 步：使用 `uv` 运行脚本

该技能使用 `uv` 来管理依赖关系并执行脚本。请确保 `uv` 已安装并且可以在您的 PATH 中找到。

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

对于图片参数（`--image`、`--images` 等），**建议使用本地文件路径** 而不是 Base64 编码的图片数据。

```bash
# Preferred: local file path (auto-converted to base64)
--image /tmp/photo.png

--images ["/tmp/photo.png"]
```

在读取文件之前，会验证文件路径：仅接受具有以下扩展名的图片文件（`.png`、`.jpg`、`.jpeg`、`.gif`、`.bmp`、`.webp`、`.tiff`、`.tif`、`.svg`、`.ico`、`.heic`、`.heif`、`.avif`）。指向敏感系统目录或非图片文件的路径将被拒绝。有效的图片文件会被转换为 Base64 格式并发送给 API，从而避免因原始 Base64 字符串导致的命令行长度限制。

## 工作流程

1. 检查配置：验证 `MULEROUTER_API_KEY` 以及 `MULEROUTER_BASE_URL` 或 `MULEROUTER_SITE` 是否已设置。
2. 安装依赖关系：运行 `uv sync`。
3. 运行 `uv run python scripts/list_models.py` 以查看可用模型。
4. 运行 `uv run python models/<path>/<action>.py --list-params` 以查看模型参数。
5. 使用适当的参数执行命令。
6. 解析结果中的输出 URL。

## 模型选择

在列出模型时，每个模型的 **标签**（例如 `[SOTA]`）会默认显示在其名称旁边。标签有助于一目了然地了解模型的特点——例如，`SOTA` 表示该模型是最新的（state-of-the-art）模型。

您也可以使用 `--tag` 参数按标签过滤模型：
```bash
uv run python scripts/list_models.py --tag SOTA
```

**如果您不确定使用哪个模型**，可以向用户展示可用的模型选项，并让他们进行选择。可以使用 `AskUserQuestion` 工具（或类似的交互式提示）来询问用户他们希望使用哪个模型。例如，如果用户要求“生成一张图片”但没有指定模型，可以列出相关的图片生成模型及其标签和描述，然后让用户选择一个。

## 提示
1. 图片生成模型的建议超时时间为 5 分钟。
2. 视频生成模型的建议超时时间为 15 分钟。

## 参考资料

- [REFERENCE.md](references/REFERENCE.md) - API 配置和 CLI 选项
- [MODELS.md](references/MODELS.md) - 完整的模型规格说明