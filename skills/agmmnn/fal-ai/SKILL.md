---
name: fal-api
description: 通过 fal.ai API（支持 FLUX、SDXL、Whisper 等技术）生成图片、视频和音频文件。
version: 0.1.0
metadata:
  {
    "openclaw": { "requires": { "env": ["FAL_KEY"] }, "primaryEnv": "FAL_KEY" },
  }
---

# fal.ai API 技能

使用 fal.ai 的 API 生成图像、视频和文字记录，支持 FLUX、Stable Diffusion、Whisper 等技术。

## 特点

- 基于队列的异步生成（提交 → 轮询 → 结果）
- 支持 600 多种 AI 模型
- 图像生成（FLUX、SDXL、Recraft）
- 视频生成（MiniMax、WAN）
- 语音转文本（Whisper）
- 仅依赖标准库（无需 `fal_client`）

## 设置

1. 从 https://fal.ai/dashboard/keys 获取您的 API 密钥
2. 使用以下方式配置：

```bash
export FAL_KEY="your-api-key"
```

或通过 clawdbot 配置：

```bash
clawdbot config set skill.fal_api.key YOUR_API_KEY
```

## 使用方法

### 交互式模式

```
You: Generate a cyberpunk cityscape with FLUX
Klawf: Creates the image and returns the URL
```

### Python 脚本

```python
from fal_api import FalAPI

api = FalAPI()

# Generate and wait
urls = api.generate_and_wait(
    prompt="A serene Japanese garden",
    model="flux-dev"
)
print(urls)
```

### 可用模型

| 模型            | 端点                          | 类型            |
| ------------------ | ----------------------------- | --------------------------- |
| flux-schnell      | `fal-ai/flux/schnell`                 | 图像（快速生成）                |
| flux-dev        | `fal-ai/flux/dev`                     | 图像生成                    |
| flux-pro        | `fal-ai/flux-pro/v1.1-ultra`          | 高画质图像生成（2K 分辨率）         |
| fast-sdxl       | `fal-ai/fast-sdxl`                    | 图像生成                    |
| recraft-v3       | `fal-ai/recraft-v3`                   | 图像生成                    |
| sd35-large      | `fal-ai/stable-diffusion-v35-large`   | 图像生成                    |
| minimax-video    | `fal-ai/minimax-video/image-to-video` | 视频生成                    |
| wan-video       | `fal-ai/wan/v2.1/1.3b/text-to-video`  | 视频生成                    |
| whisper        | `fal-ai/whisper`                      | 音频生成                    |

如需查看完整模型列表，请运行：

```bash
python3 fal_api.py --list-models
```

## 参数

| 参数            | 类型            | 默认值          | 描述                                      |
| ------------------ | ----------------------------- | ----------------------------------------- |
| prompt        | str            | 必填            | 图像/视频的描述                        |
| model         | str            | "flux-dev"        | 上表中的模型名称                    |
| image_size     | str            | "landscape_16_9"     | 图像尺寸（预设值：square, portrait_4_3, landscape_16_9 等） |
| num_images     | int            | 1              | 要生成的图像数量                        |
| seed          | int            | 可选          | 用于生成一致性的随机种子                    |

## 致谢

本技能基于 krea-api 的设计模式开发，利用 fal.ai 的基于队列的 API 实现可靠的异步生成功能。