---
name: character-design-sheet
description: "**AI生成图像中的角色一致性：结合参考表与LoRA技术**
本文介绍了如何利用LoRA（Large Language Model for Art）技术以及相关工具（如Turnaround Views、Expression Sheets、Color Palettes等），来实现AI生成图像中角色的高度一致性。这些方法适用于角色设计、游戏美术、插画、动画、漫画和视觉小说等领域。
**适用场景：**  
- 角色设计  
- 角色资料表（Character Sheets）  
- 角色一致性（Character Consistency）  
- 角色参考（Character Reference）  
- 角色生成流程（Character Creation）  
- 角色形象（Character Art）  
- 角色概念（Character Concept）  
- 参考表（Reference Sheets）  
**核心内容：**  
- **Turnaround Views**：用于展示角色在不同视角下的形象变化。  
- **Expression Sheets**：记录角色的面部表情和动作细节。  
- **Color Palettes**：统一角色的配色方案。  
- **Style Consistency Tricks**：确保角色风格的一致性。  
**技术要点：**  
- 利用LoRA模型生成多样化的角色模型。  
- 结合参考表和Turnaround Views来调整角色形象。  
- 使用Expression Sheets精确控制角色的表情和动作。  
- 通过统一颜色方案提升视觉效果。  
**应用建议：**  
- 在角色设计初期，制定详细的角色风格指南。  
- 定期更新和优化角色资料表，确保信息的准确性。  
- 在开发过程中持续监控角色的视觉一致性。  
**参考资料：**  
- OpenClaw  
- ClawHub  
- API  
- CLI（Command Line Interface）  
**注意事项：**  
- 保持代码示例、命令和URL的原始格式。  
- 仅翻译技术性较强的内容，避免对非技术性文字进行不必要的解释。"
allowed-tools: Bash(infsh *)
---
# 字符设计文档

通过 [inference.sh](https://inference.sh) 命令行工具，在多张由 AI 生成的图像中创建一致的角色形象。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a character concept
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character design reference sheet, front view of a young woman with short red hair, green eyes, wearing a blue jacket and white t-shirt, full body, white background, clean lines, concept art style, character turnaround",
  "width": 1024,
  "height": 1024
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。也可以选择 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 一致性问题

即使使用相同的提示，AI 生成的图像中的角色形象也会每次都有所不同。这是任何需要在多张图像中使用相同角色的 AI 艺术项目面临的首要挑战。

### 解决方案（按效果排序）

| 技术 | 一致性 | 需要的工作量 | 适用场景 |
|---------|------------|------------------|-------------------|
| **FLUX LoRA**（基于角色数据进行训练） | 非常高 | 需要训练数据 | 长期项目、大量图像需求 |
| **详细描述锚点** | 中等偏高 | 较低 | 短期项目、少量图像 |
| **相同的种子值 + 类似的提示** | 中等 | 较低 | 适用于需要单一姿势变体的情况 |
| **图像到图像的细化** | 中等 | 中等 | 用于优化现有图像 |
| **在提示中包含参考图像** | 效果因模型而异 | 适用于模型支持该功能的场景 |

## 参考文档类型

### 1. 多角度展示文档

从多个角度展示角色形象：

```
┌────────┬────────┬────────┬────────┐
│        │        │        │        │
│ FRONT  │  3/4   │  SIDE  │  BACK  │
│  VIEW  │  VIEW  │  VIEW  │  VIEW  │
│        │        │        │        │
└────────┴────────┴────────┴────────┘
```

```bash
# Generate front view
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character design, front view, young woman with short asymmetric red hair, bright green eyes, wearing navy blue bomber jacket over white graphic tee, dark jeans, red sneakers, standing in neutral pose, full body, clean white background, concept art, sharp details",
  "width": 768,
  "height": 1024
}' --no-wait

# Generate 3/4 view (same description)
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character design, three-quarter view, young woman with short asymmetric red hair, bright green eyes, wearing navy blue bomber jacket over white graphic tee, dark jeans, red sneakers, standing, full body, clean white background, concept art, sharp details",
  "width": 768,
  "height": 1024
}' --no-wait

# Generate side view
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character design, side profile view, young woman with short asymmetric red hair, bright green eyes, wearing navy blue bomber jacket over white graphic tee, dark jeans, red sneakers, standing, full body, clean white background, concept art, sharp details",
  "width": 768,
  "height": 1024
}' --no-wait

# Generate back view
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character design, back view, young woman with short asymmetric red hair, wearing navy blue bomber jacket over white graphic tee, dark jeans, red sneakers, standing, full body, clean white background, concept art, sharp details",
  "width": 768,
  "height": 1024
}' --no-wait

# Stitch into reference sheet
infsh app run infsh/stitch-images --input '{
  "images": ["front.png", "three-quarter.png", "side.png", "back.png"],
  "direction": "horizontal"
}'
```

### 2. 表情文档

展示角色在不同情绪下的面部表情：

```
┌────────┬────────┬────────┐
│NEUTRAL │ HAPPY  │ ANGRY  │
│        │        │        │
├────────┼────────┼────────┤
│  SAD   │SURPRISE│THINKING│
│        │        │        │
└────────┴────────┴────────┘
```

至少包含 6 种表情：中性、快乐、愤怒、悲伤、惊讶、思考。

```bash
# Neutral
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character portrait, close-up face, young woman with short red hair and green eyes, neutral calm expression, clean white background, concept art, consistent character design",
  "width": 512,
  "height": 512
}' --no-wait

# Happy
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character portrait, close-up face, young woman with short red hair and green eyes, warm genuine smile, happy expression, clean white background, concept art, consistent character design",
  "width": 512,
  "height": 512
}' --no-wait

# Angry
infsh app run falai/flux-dev-lora --input '{
  "prompt": "character portrait, close-up face, young woman with short red hair and green eyes, furrowed brows, angry determined expression, clean white background, concept art, consistent character design",
  "width": 512,
  "height": 512
}' --no-wait

# (Continue for sad, surprised, thinking...)
```

### 3. 服装文档

为同一角色提供多种服装搭配：

| 服装 | 说明 |
|--------|-------------|
| 休闲装 | 运动夹克、T恤、牛仔裤 |
| 职业装 | 西装外套、衬衫、休闲裤 |
| 运动装 | 运动胸罩、紧身裤、运动鞋 |
| 正装 | 晚礼服、高跟鞋 |

### 4. 色彩调色板文档

记录准确的色彩信息以确保一致性：

```
CHARACTER: Maya Chen

Skin:    ████ #F5D0A9 (warm beige)
Hair:    ████ #C0392B (auburn red)
Eyes:    ████ #27AE60 (emerald green)
Jacket:  ████ #2C3E50 (navy blue)
T-shirt: ████ #ECF0F1 (off-white)
Jeans:   ████ #34495E (dark slate)
Shoes:   ████ #E74C3C (bright red)
```

## 详细描述锚点技术

这是最实用的一致性保障方法：编写一段 **50 字以上的详细描述**，并在每个提示中完全重复使用这段描述。

### 模板

```
[age] [gender] with [hair: color, length, style], [eye color] eyes,
[skin tone], [facial features: any distinctive marks],
wearing [top: specific color and style], [bottom: specific color and style],
[shoes: specific color and style], [accessories: specific items]
```

### 示例

```
young woman in her mid-twenties with short asymmetric auburn red hair
swept to the right side, bright emerald green eyes, light warm skin
with a small beauty mark below her left eye, wearing a fitted navy
blue bomber jacket with silver zipper over a white crew-neck t-shirt,
dark slate slim jeans, and bright red canvas sneakers, small silver
stud earrings
```

**在每个提示中都使用这段相同的描述**，只需更改动作/姿势/场景即可。

## 比例指南

| 风格 | 头部与身体的比例 | 适用场景 |
|-------|-------------------|-------------------|
| 现实主义 | 7.5 : 1 | 电影、写实风格 |
| 英雄风格 | 8 : 1 | 超级英雄、动作场景 |
| 动画/漫画风格 | 5-6 : 1 | 日本动画风格 |
| 可爱风格 | 4-5 : 1 | 西方动画风格 |
| 奇特风格 | 2-3 : 1 | 可爱、幽默风格、吉祥物 |

在提示中明确说明比例要求，例如：“使用现实主义比例”或“动漫风格比例”。

## 使用 LoRA 实现一致性

对于需要大量相同角色图像的项目，可以训练 LoRA 模型：

```bash
# Use FLUX with a character LoRA
infsh app run falai/flux-dev-lora --input '{
  "prompt": "maya_chen character, sitting at a cafe reading a book, warm afternoon light, candid photography style",
  "loras": [{"path": "path/to/maya-chen-lora.safetensors", "scale": 0.8}]
}'
```

**LoRA 训练技巧：**
- 需要 10-20 张风格一致的参考图像 |
- 使用特定的触发词进行训练（例如：“maya_chen”）
- 比例范围在 0.7-0.9 之间，可在一致性和提示灵活性之间取得平衡 |
- 比例越小，创作自由度越高；比例越大，匹配要求越严格

## 常见的一致性问题及解决方法

| 问题 | 原因 | 解决方法 |
|-------|-------------------|-------------------|
| **头发颜色变化** | 模型对“红色头发的理解不同** | 使用具体颜色值：#C0392B（深红） |
| **眼睛颜色变化** | 生成过程中颜色变化较小 | 在提示中提前说明眼睛颜色 |
| **服装不一致** | 模型会自由填充细节 | 明确描述每件服装的细节 |
| **年龄差异** | 描述年龄模糊 | 使用具体年龄范围（如“二十多岁”） |
| **面部结构变化** | 不同的生成结果会导致面部变化 | 使用 LoRA 模型或相同的种子值 |
| **比例变化** | 不同风格会导致比例差异 | 明确指定比例（如 7.5:1） |

## 角色设计文档模板

对于长期项目，应维护一个角色设计文档：

```markdown
# Character: Maya Chen

## Visual Description (use in all prompts)
young woman in her mid-twenties with short asymmetric auburn red hair...
[full 50+ word anchor description]

## Color Palette
- Skin: #F5D0A9
- Hair: #C0392B
- Eyes: #27AE60
- Primary outfit: Navy #2C3E50
- Accent: Red #E74C3C

## Personality Notes (for expression/pose choices)
- Confident but approachable
- Default expression: slight curious smile
- Gestures: talks with hands, leans forward when interested

## Style Keywords
concept art, clean lines, sharp details, [art style reference]

## LoRA (if trained)
Path: ./loras/maya-chen-v2.safetensors
Trigger: maya_chen
Recommended scale: 0.8
```

## 常见错误及解决方法

| 错误 | 问题 | 解决方法 |
|---------|---------|-------------------|
| 描述模糊 | 每次生成的字符形象都不同 | 使用 50 字以上的详细描述 |
| 提示结构不一致 | 提示的重点不同会导致结果不一致 | 保持提示结构一致，仅更改动作/场景 |
| 仅生成一个视角的图像 | 无法在不同场景中使用该角色 | 创建完整的参考文档 |
| 无色彩记录 | 不同图像中的颜色可能不一致 | 记录颜色的十六进制代码 |
| 忽略表情文档 | 角色形象缺乏立体感 | 生成 6 种以上的表情 |
| 大型项目未使用 LoRA | 一致性难以保证 | 对于需要大量图像的项目，务必使用 LoRA 模型 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@flux-image
npx skills add inference-sh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`