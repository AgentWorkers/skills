---
name: mulerouter
description: 使用 MuleRouter 或 MuleRun 的多模态 API 生成图像和视频。支持文本转图像、图像转图像、文本转视频、图像转视频的功能，以及视频编辑（包括 VACE、关键帧插值等）。适用于用户需要利用 Wan2.6、Veo3、Nano Banana Pro、Sora2、Midjourney 等 AI 模型来生成、编辑或转换图像和视频的场景。
compatibility: Requires Python 3.10+, uv (or pip), and network access to api.mulerouter.ai or api.mulerun.com
---

# MuleRouter API

使用 MuleRouter 或 MuleRun 的多模态 API 生成图片和视频。

## 配置检查

在运行任何命令之前，请验证环境是否已正确配置：

### 第一步：检查现有配置

```bash
# Check environment variables
echo "MULEROUTER_BASE_URL: $MULEROUTER_BASE_URL"
echo "MULEROUTER_SITE: $MULEROUTER_SITE"
echo "MULEROUTER_API_KEY: ${MULEROUTER_API_KEY:+[SET]}"

# Check for .env file
ls -la .env 2>/dev/null || echo "No .env file found"
```

### 第二步：根据需要配置

**选项 A：使用带有自定义基础 URL 的环境变量（优先级最高）**
```bash
export MULEROUTER_BASE_URL="https://api.mulerouter.ai"  # or your custom API endpoint
export MULEROUTER_API_KEY="your-api-key"
```

**选项 B：使用带有站点名称的环境变量（在未设置基础 URL 时使用）**
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

**注意：** 该工具仅读取当前目录下的 `.env` 文件。请从技能根目录（`skills/mulerouter-skills/`）运行脚本。

### 第三步：使用 `uv` 运行脚本

该技能使用 `uv` 来管理依赖关系并执行脚本。请确保 `uv` 已安装并且可以在您的 PATH 环境变量中找到。

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

对于图片参数（如 `--image`、`--images` 等），**建议使用本地文件路径** 而不是 base64 编码的字符串。

```bash
# Preferred: local file path (auto-converted to base64)
--image /tmp/photo.png

--images ["/tmp/photo.png"]
```

该技能会在将文件发送到 API 之前自动将本地文件路径转换为 base64 编码。这样可以避免因 raw base64 字符串过长而导致的命令行长度限制。

## 工作流程

1. 检查配置：确保 `MULEROUTER_BASE_URL` 或 `MULEROUTER_SITE` 以及 `MULEROUTER_API_KEY` 已设置。
2. 安装依赖关系：运行 `uv sync`。
3. 运行 `uv run python scripts/list_models.py` 以查看可用模型。
4. 运行 `uv run python models/<path>/<action>.py --list-params` 以查看模型参数。
5. 使用相应的参数执行命令。
6. 解析结果中的输出 URL。

## 提示
1. 对于图片生成模型，建议的超时时间为 5 分钟。
2. 对于视频生成模型，建议的超时时间为 15 分钟。

## 参考资料

- [REFERENCE.md](references/REFERENCE.md) - API 配置和 CLI 选项
- [MODELS.md](references/MODELS.md) - 完整的模型规格说明