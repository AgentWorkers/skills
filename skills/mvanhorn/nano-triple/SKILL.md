---
name: nano-triple
description: 使用 Nano Banana Pro 根据相同的提示生成 3 张图片。选择其中最满意的一张，或者对任何一张图片提出反馈，以便进一步优化生成 3 张更高质量的图片。
triggers:
  - make me an image
  - generate an image
  - create an image
metadata:
  clawdbot:
    emoji: "🎨"
---

# Nano Triple：3张图片，相同提示，由用户选择

当用户请求生成一张图片时，系统会生成3个版本，供用户选择或进一步修改。

## 流程

### 第1步：用户提供提示

用户输入：“生成一张山间日落的图片。”

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

### 第3步：发送标记为1、2、3的图片

每张图片仅附上对应的编号：

- **1** [图片]
- **2** [图片]
- **3** [图片]

**无需任何描述或创意说明，只需标注数字1、2、3以及图片本身。**

### 第4步：用户进行选择或提供反馈

- 选择“2” → 选择该图片作为最终结果。
- 选择“1，但颜色更暖和一些” → 根据用户反馈再生成3张新图片。
- 选择“无，重新生成” → 再使用相同的提示生成3张新图片。

**注意：** 对任何选项的反馈都会导致系统生成3张新的图片。

## 示例

**用户：** 生成一张戴着高礼帽的猫的图片。

**系统：** 根据用户提示生成3张图片，并分别标记为1、2、3发送给用户。

**用户：** 选择“2”，表示喜欢第二张图片（帽子更大一些）。

**系统：** 根据用户反馈，在提示中添加“帽子更大一些”，再生成3张新图片，并分别标记为1、2、3发送给用户。

**用户：** 选择“3”，表示对所有图片都满意。

## 规则

1. **始终生成3张图片**：使用相同的提示，得到3个不同的结果。
2. **禁止创意发挥**：必须严格使用用户提供的提示。
3. **标注图片编号**：图片仅附上数字1、2、3。
4. **反馈机制**：用户对任何一张图片的修改都会触发系统生成3张新的图片。

## API密钥

使用环境变量或clawdbot配置中的`GEMINI_API_KEY`。