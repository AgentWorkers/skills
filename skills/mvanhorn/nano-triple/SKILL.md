---
name: nano-triple
version: "1.0.0"
description: "3张图片，1个提示，即可立即生成A/B/C三个版本。Nano Banana Pro的随机生成功能能够让你对任何图片创意得到三种不同的呈现效果——这些效果是同时生成的。你可以选择最满意的版本，或者对某个版本提出反馈，以便进一步生成另外3个版本。这是找到理想图片的最快捷方法。"
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/nano-triple
homepage: https://aistudio.google.com
triggers:
  - make me an image
  - generate an image
  - create an image
  - make an image
metadata:
  openclaw:
    emoji: "🎨"
    tags:
      - image-generation
      - nano-banana-pro
      - creative
      - parallel
      - ai-art
---
# Nano Triple: 生成3张图片，使用相同的提示，用户自行选择

当用户需要一张图片时，系统会生成3个版本，供用户选择或进一步修改。

## 流程

### 第1步：用户提供提示

用户输入：“为我生成一张山景日落的图片。”

### 第2步：使用相同的提示生成3张图片

系统会严格使用用户提供的提示来生成3张图片，不得进行任何修改或创意发挥。模型自身的随机性会生成3个不同的结果。

同时运行这3个生成任务：

```bash
# Same prompt, 3 times
uv run ~/.npm-global/lib/node_modules/clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[USER'S EXACT PROMPT]" \
  --filename "option-1.png" --resolution 1K

uv run ~/.npm-global/lib/node_modules/clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[USER'S EXACT PROMPT]" \
  --filename "option-2.png" --resolution 1K

uv run ~/.npm-global/lib/node_modules/clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[USER'S EXACT PROMPT]" \
  --filename "option-3.png" --resolution 1K
```

### 第3步：将生成的图片分别标记为1、2、3并发送

每张图片仅附上编号：
- **1** [图片]
- **2** [图片]
- **3** [图片]

**无需任何描述或创意说明，只需标注数字1、2、3以及图片本身。**

### 第4步：用户进行选择或提供反馈

- 选择“2” → 选择完成，该图片即为最终结果。
- 选择“1，但颜色更暖和一些” → 根据用户反馈再次生成3张新的图片。
- 选择“无，重新生成” → 根据相同的提示再次生成3张新的图片。

**注意：** 对任何选项的反馈都会导致系统生成3张新的图片。

## 示例

**用户：** 为我生成一张戴着高顶礼帽的猫的图片。

**系统：** 使用该提示生成3张图片，并分别标记为1、2、3发送给用户。

**用户：** 选择“2”，并要求“礼帽再大一些”。

**系统：** 根据用户反馈，在提示中添加“礼帽再大一些”，然后生成3张新的图片，并再次发送给用户（标记为1、2、3）。

**用户：** 选择“3”。

**系统：** 👍（表示选择满意）

## 规则

1. **始终生成3张图片**：使用相同的提示，生成3个不同的结果。
2. **禁止创意发挥**：严格遵循用户提供的提示。
3. **标注编号**：每张图片仅标注数字1、2、3。
4. **反馈机制**：任何修改请求都会触发系统生成3张新的图片。

## API密钥

使用环境变量或openclaw配置文件中的`GEMINI_API_KEY`。