---
name: cliproxy-media
description: 通过 CLIProxyAPI 分析图片（jpg、png、gif、webp）和 PDF 文件——这是一个基于 Claude Max 的代理服务，能够通过您的订阅计划路由请求，且无需额外费用。每当您需要分析、描述图片或照片中的内容（如 “分析图片”、“描述照片”、“这张图片里有什么”），读取或总结 PDF 文档（如 “读取 PDF”、“文档摘要”），或通过支持 CLIProxy 的接口处理任何媒体文件（如 “通过代理处理媒体文件”、“cliproxy vision”、“cliproxy media”）时，都可以使用此功能。**切勿** 使用内置的 `image` 或 `pdf` 工具，因为它们会直接调用 Anthropic API，而使用 Anthropic API 需要额外支付费用。请始终优先使用 CLIProxyAPI 来完成所有的视觉分析和文档处理任务。
---
# cliproxy-media

**来源:** https://github.com/bencoremans/site/tree/main/skills/cliproxy-media

通过 CLIProxyAPI 分析图像和 PDF 文件（需订阅 Claude Max 服务，无额外费用）。

## 设置

将端点设置为你的 CLIProxy 实例：

```bash
export CLIPROXY_URL=http://your-host:8317/v1/messages
```

对于 Docker 设置，请将 `your-host` 替换为容器主机名（例如 `cliproxyapi`、`localhost` 或容器 IP）。

## 快速入门

```bash
# Analyze an image
python3 skills/cliproxy-media/scripts/analyze.py /path/to/image.jpg "What is in this image?"

# Read a PDF
python3 skills/cliproxy-media/scripts/analyze.py /path/to/document.pdf "Give a summary"

# Compare multiple images
python3 skills/cliproxy-media/scripts/analyze.py img1.jpg img2.jpg "Compare these images"

# With streaming (output appears immediately)
python3 skills/cliproxy-media/scripts/analyze.py --stream image.jpg "Describe in detail"

# With system prompt
python3 skills/cliproxy-media/scripts/analyze.py --system "You are a medical expert" scan.jpg "What do you see?"

# With higher token limit
python3 skills/cliproxy-media/scripts/analyze.py --max-tokens 4096 document.pdf "Extensive analysis"
```

## 支持的功能 ✅ / 不支持的功能 ❌

### ✅ 支持的文件类型

| 类型 | 格式 | 备注 |
|------|--------|------|
| 图像 | `.jpg` / `.jpeg` | 需要有效的 JPEG 数据 |
| 图像 | `.png` | 完全支持 |
| 图像 | `.gif` | 完全支持 |
| 图像 | `.webp` | 完全支持 |
| 文档 | `.pdf` | 通过 `document` 内容类型进行 Base64 编码 |
| 通过 URL 的图像 | `http://` / `https://` | 直接引用 URL，无需下载 |

**同时处理多个文件：** 在请求前提供多个文件路径。每次请求最多支持约 100 个文件（Anthropic 的限制）。

### ❌ 不支持的功能

- **Office 文件**（`.docx`、`.xlsx`、`.pptx`）——解决方法：转换为 PDF 格式 |
- **音频**（`.mp3`、`.wav`、`.ogg`）——使用 Whisper 进行转录 |
- **视频**（`.mp4`、`.mov`、`.avi`）——模型不支持 |
- **其他文档类型**（`.txt`、`.html`、`.md`）——直接以字符串形式发送文本 |

## ⚠️ 系统提示警告

CLIProxyAPI **仅** 支持数组形式的系统提示。字符串形式的系统提示会被 **忽略**——模型无法识别这些提示，但你也不会收到错误信息！

```python
# ❌ DOES NOT WORK — ignored without error message
payload["system"] = "You are an expert."

# ✅ WORKS — always use array notation
payload["system"] = [{"type": "text", "text": "You are an expert."}]
```

`analyze.py` 中的 `--system` 参数会自动使用正确的数组格式。

## 配置（环境变量）

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `CLIPROXY_URL` | `http://localhost:8317/v1/messages` | 完整的端点 URL |
| `CLIPROXY_MODEL` | `claude-sonnet-4-6` | 要使用的模型 |

示例：
```bash
export CLIPROXY_URL=http://localhost:8317/v1/messages
export CLIPROXY_MODEL=claude-opus-4-6
python3 skills/cliproxy-media/scripts/analyze.py image.jpg "question"
```

## 其他选项

```
--stream          Streaming output via SSE (output appears immediately)
--system TEXT     System prompt (automatically sent as array)
--max-tokens N    Maximum output tokens (default: 1024)
--model MODEL     Model override (overrides CLIPROXY_MODEL)
--url URL         Endpoint override (overrides CLIPROXY_URL)
```

## 兼容性

该脚本适用于任何支持 Anthropic Messages 格式的 API：

| 提供商 | 兼容性 | 备注 |
|----------|-----------|------|
| **CLIProxyAPI** | ✅ 是 | 主要经过测试，需要使用数组形式的系统提示 |
| **OpenRouter** | ✅ 是 | 使用 Bearer 令牌代替 `x-api-key: dummy` |
| **LiteLLM** | ✅ 是 | 作为 Anthropic 格式的代理 |
| **Anthropic 直接调用** | ✅ 是 | 使用 `ANTHROPIC_API_KEY` 作为 x-api-key |

**对于非 CLIProxy 端点的提示：** 一些代理支持字符串形式的系统提示。为确保最大兼容性，请始终使用数组格式。

## CLIProxyAPI 的已知限制

- `temperature` 和 `top_p` 不能同时使用（会返回 HTTP 400 错误） |
- 通过 URL 指定的 PDF 文档无法下载（提示 “Unable to download the file”） |
- 只支持 `claude-sonnet-4-6` 和 `claude-opus-4-6` 模型（`haiku` 模型已弃用） |
- `inference_geo` 在响应中始终不可用 |

## 直接使用 Python API

如果你想从自己的 Python 代码中调用该脚本：

```python
import subprocess, json

result = subprocess.run(
    ["python3", "skills/cliproxy-media/scripts/analyze.py", "image.jpg", "Describe this"],
    capture_output=True, text=True
)
print(result.stdout)
```

或者使用内置的 exec 工具：
```
exec: python3 skills/cliproxy-media/scripts/analyze.py /path/to/image.jpg "question"
```