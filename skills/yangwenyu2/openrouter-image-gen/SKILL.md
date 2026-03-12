---
name: gemini-image-gen
description: >
  **使用 OpenRouter API 通过 Google Gemini 生成图像**  
  支持文本到图像的转换，以及基于参考图像的生成功能。当用户需要生成、创建、绘制或设计图像/插图/封面/头像时，可以使用该功能。
---
# Gemini 图像生成

在 OpenRouter 上使用 `google/gemini-3.1-flash-image-preview` 生成图像。价格便宜（输入费用为 0.25 美元/百万 token，输出费用为 1.5 美元/百万 token），速度快，质量良好。

## 快速入门

```bash
python3 scripts/generate.py "a watercolor illustration of a cozy café" -o output.png
```

使用参考图像（用于指导风格/角色设计）：
```bash
python3 scripts/generate.py "same character but waving hello" -o wave.png --ref reference.png
```

脚本路径：`skills/gemini-image-gen/scripts/generate.py`

## 所需条件

- `OPENROUTER_API_KEY` 环境变量（或 `--api-key` 标志）
- Python 3.10 或更高版本（仅需要标准库，无需安装 pip）

## 工作原理

1. 向 OpenRouter 发送请求，请求方式如下：`/chat/completions`，参数设置为 `modalities: ["text", "image"]`
2. （可选）将参考图像编码为 Base64 格式并包含在消息中
3. 从响应数据中提取生成的图像路径（格式通常为 `data:image/png;base64,...`）
4. 将提取到的图像解码并保存到指定路径

## 提示工程技巧（基于实际使用经验）

### 长宽比与构图
- Gemini 会遵循提示中指定的长宽比要求：
  - 垂直布局（例如手机壁纸、小红书封面）：使用 “vertical composition, 3:4 aspect ratio”
  - 水平布局（例如横幅）：使用 “horizontal composition, 16:9 aspect ratio”
  - 正方形布局：使用 “square composition, 1:1 aspect ratio”
  **务必指定** 长宽比，否则 Gemini 会默认生成近似正方形的图像，可能导致裁剪不美观

### 角色细节的一致性
- 使用 `--ref` 选项时，需在提示中明确描述角色的特征，并提供参考图像：
  - 重要细节包括：头发颜色/样式、眼睛颜色、服装、配饰、表情等
  - 例如：“参考图像中的角色特征：银蓝色渐变的齐肩长发、冰蓝色眼睛、浅蓝色衬衫搭配奶油色开衫、雪花形状的耳环”
  - Gemini 能在一定程度上保持角色细节的一致性，但在小细节上可能会有所偏差，因此请务必重新指定这些特征

### 风格控制
- 明确指定艺术风格：
  - “soft watercolor illustration”（柔和的水彩风格）
  - “anime cel-shading”（动漫风格的赛璐璐渲染）
  - “photorealistic”（写实风格）
  - “flat vector”（扁平矢量风格）
  - “oil painting”（油画风格）
  - 对于温暖/舒适的风格：使用 “warm color palette”（暖色调调色板）、”cream and peach gradient background”（奶油色与桃色渐变背景）、”bokeh light spots”（模糊光晕效果）
  - 对于暗色调/忧郁的风格：使用 “dark gradient background”（深蓝色渐变背景）、”deep navy to black”（深海军蓝至黑色）、”subtle glow effects”（微弱的光晕效果）
  - 可以参考知名艺术风格，例如 “in the style of Studio Ghibli”（吉卜力工作室的风格）、”Makoto Shinkai lighting”（新海诚的灯光效果）

### 图像中的文字
- Gemini 可以在图像中渲染简短文字，但对中文/日文字符的处理效果不佳：
  - 英文文字：如果指定了字体样式（如 “bold sans-serif”、”handwritten script”），效果还算不错
  - 中文/日文：**建议避免** 在图像中添加文字，可以使用 ImageMagick 或 Pillow 等工具单独处理文字叠加

### 常见问题

- **人物比例**：Gemini 有时会压缩或扭曲人物形象。对于角色画像，请添加 “natural human body proportions, do not squash or stretch”（保持自然的人体比例）的提示。
- **手部**：仍然是 Gemini 的薄弱环节。尽量减少手部的可见部分，或明确描述手的姿势。
- **多个主体**：超过 2-3 个主体会导致图像效果不一致。请保持场景的焦点清晰。
- **批量生成**：如需生成多个变体，请多次运行脚本（每次请求都是独立的），切勿在一条提示中请求多个选项。

## 在 Feishu 上发送图像

⚠️ **重要提示**：图像必须保存在 `localRoots` 目录下（通常是你的 OpenClaw 工作区目录）。`/tmp` 目录不在 Feishu 的允许访问范围内。

```python
# Save to workspace, not /tmp
output_path = "my_image.png"  # relative to workspace

# Send via message tool:
#   media: "file://<workspace_path>/my_image.png"
#   (use 'media' parameter, NOT 'filePath')
```

发送图像后，请清理临时文件，以保持工作区的整洁。

## 高级用法：通过 Python 调用（无需使用 CLI）

```python
import os, sys
sys.path.insert(0, "skills/gemini-image-gen/scripts")
from generate import generate

generate(
    prompt="a cute robot reading a philosophy book",
    output="robot.png",
    ref_image=None,  # or path to reference image
)
```

## 可用模型对比

| 模型 | 费用 | 说明 |
|-------|------|-------|
| `google/gemini-3.1-flash-image-preview` | 每百万 token 0.25/1.5 美元 | **默认模型**，性价比最高 |
| `google/gemini-3.1-pro-preview` | 每百万 token 2/12 美元 | 质量更高，但价格也更高 |
| `openai/gpt-image-1` | 费用不定 | OpenAI 的图像模型，使用不同的 API 格式——本脚本不支持该模型 |

## 故障排除

- **“没有返回图像”**：检查生成的 `.debug.json` 文件。通常是因为提示触发了安全过滤机制，或者模型仅返回了文本。
- **图像质量差或失真**：尝试重新表述请求内容，增加 “high quality, detailed” 等描述，以更具体地说明图像要求。
- **API 错误 429**：请求次数达到限制，请等待 30 秒后重试。
- **API 错误 402**：OpenRouter 的信用额度不足，请补充信用额度后再尝试。