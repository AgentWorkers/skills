---
name: gemini-image-gen
description: 通过 Google Gemini API 生成和编辑图片。支持 Gemini 的原生图像生成功能、Imagen 3、样式预设，以及使用 HTML 图库进行批量生成。完全不依赖任何第三方库，仅使用 Python 的标准库即可实现。
homepage: https://github.com/IISweetHeartII/gemini-image-gen
metadata:
  openclaw:
    emoji: "🎨"
    category: creative
    requires:
      bins:
        - python3
      env:
        - GEMINI_API_KEY
    primaryEnv: GEMINI_API_KEY
    tags:
      - image-generation
      - gemini
      - imagen
      - ai-art
      - creative
      - editing
      - batch
      - gallery
---
# Gemini 图像生成工具

通过使用纯 Python 标准库，可以利用 Google Gemini API 生成和编辑图片。该工具支持 Gemini 的原生生成和编辑功能、Imagen 3 生成技术、批量处理以及 HTML 图库输出。

## 快速入门

```bash
export GEMINI_API_KEY="your-key-here"

# Default: Gemini native, 4 random prompts
python3 scripts/gen.py

# Custom prompt
python3 scripts/gen.py --prompt "a cyberpunk cat riding a neon motorcycle through Tokyo at night"

# Imagen 3 engine
python3 scripts/gen.py --engine imagen --count 4 --aspect 16:9

# Edit an existing image (Gemini engine only)
python3 scripts/gen.py --edit path/to/image.png --prompt "change the background to a sunset beach"

# Use a style preset
python3 scripts/gen.py --style watercolor --prompt "floating islands above a calm sea"

# List available styles
python3 scripts/gen.py --styles
```

## 风格预设

| 风格 | 描述 |
| --- | --- |
| `photo` | 极具细节的写实摄影效果，8K 分辨率，清晰的对焦 |
| `anime` | 高质量的动漫风格插画，受吉卜力工作室启发，色彩鲜艳 |
| `watercolor` | 细腻的水彩画效果，柔和的边缘，色彩渐变自然 |
| `cyberpunk` | 带有霓虹灯效果的赛博朋克场景，被雨水浸湿的街道，全息显示屏，具有《银翼杀手》的风格 |
| `minimalist` | 极简的设计风格，几何形状，有限的色彩搭配，大量的空白空间 |
| `oil-painting` | 具有明显笔触的经典油画效果，丰富的纹理，文艺复兴时期的光照效果 |
| `pixel-art` | 详细的像素艺术风格，复古的 16 位画面，清晰的边缘，怀旧的色彩搭配 |
| `sketch` | 在奶油色纸上绘制的素描，包含阴影和交叉阴影效果，具有艺术性的瑕疵 |
| `3d-render` | 专业的 3D 渲染效果，包括环境光、全局光照和逼真的材质效果 |
| `pop-art` | 强烈的波普艺术风格，使用鲜明的色彩对比和强烈的轮廓线 |

## 完整的 CLI 参考

| 标志 | 默认值 | 描述 |
| --- | --- | --- |
| `--prompt` | （随机） | 生成图片的文本提示。如需随机创意提示，请省略此参数 |
| `--count` | 4 | 生成图片的数量 |
| `--engine` | gemini | 使用的引擎：`gemini`（原生引擎，支持编辑）或 `imagen`（Imagen 3） |
| `--model` | （自动） | 模型名称。默认值为 `gemini-2.5-flash-image` 或 `imagen-3.0-generate-002` |
| `--edit` | | 输入图片的路径（仅适用于 Gemini 引擎） |
| `--aspect` | 1:1 | 图像的宽高比：`1:1`、`16:9`、`9:16`、`4:3`、`3:4` |
| `--out-dir` | （自动） | 输出目录（默认为带有时间戳的文件夹） |
| `--style` | | 要添加到提示中的风格预设 |
| `--styles` | | 可用的风格预设列表，输入此参数后程序将退出 |

## Python 示例

```python
import subprocess

subprocess.run(
    [
        "python3",
        "scripts/gen.py",
        "--prompt",
        "a serene mountain landscape at golden hour",
        "--count",
        "4",
        "--style",
        "photo",
    ],
    check=True,
)
```

## 故障排除

- 缺少 API 密钥：在环境中设置 `GEMINI_API_KEY` 并重新尝试。
- 由于速率限制导致的错误（429 错误）：稍等片刻后重试，减少生成图片的数量，或更换使用其他引擎。
- 模型相关错误：检查模型名称，尝试使用默认模型，或更换引擎。

## 与其他工具的集成

- **[AgentGram](https://clawhub.org/skills/agentgram)** — 将生成的图片分享到 AI 代理的社交网络中！创建视觉内容并发布到您的 AgentGram 订阅源中。
- **[agent-selfie](https://clawhub.org/skills/agent-selfie)** — 专注于 AI 代理的头像和视觉身份。使用相同的 Gemini API 密钥生成个性化的自画像。
- **[opencode-omo](https://clawhub.org/skills/opencode-omo)** — 使用 Sisyphus 工作流程运行确定性的图像生成任务。

## 更新日志

- v1.3.1：添加了与 opencode-omo 的集成指南。
- v1.1.0：新增了风格预设选项 `--style` 和 `--styles`，并扩展了文档内容。
- v1.0.0：首次发布，支持 Gemini 的原生生成和 Imagen 3 生成技术，支持批量生成图片以及 HTML 图库输出。

## 仓库地址

https://github.com/IISweetHeartII/gemini-image-gen