---
name: character-design-sheet
description: |
  Character consistency across AI-generated images with reference sheets and LoRA techniques.
  Covers turnaround views, expression sheets, color palettes, and style consistency tricks.
  Use for: character design, game art, illustration, animation, comics, visual novels.
  Triggers: character design, character sheet, character consistency, character reference,
  turnaround sheet, expression sheet, character art, consistent character, character concept,
  reference sheet, character creation, oc design, character bible
allowed-tools: Bash(infsh *)
---

# 字符设计文档

通过 [inference.sh](https://inference.sh) 命令行工具，在多张由 AI 生成的图像中保持字符的一致性。

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

## 一致性问题

即使使用相同的提示，AI 生成的图像中的字符外观也会每次都不同。这是任何需要在多张图像中使用相同字符的 AI 艺术项目面临的首要挑战。

### 解决方案（按效果排序）

| 技术 | 一致性 | 需要的努力 | 适用场景 |
|---------|-----------|-----------|---------|
| **FLUX LoRA**（基于字符进行训练） | 非常高 | 需要训练数据 | 长期项目，大量图像 |
| **详细描述锚点** | 中等偏高 | 较低 | 短期项目，少量图像 |
| **相同的种子 + 类似的提示** | 中等 | 较低 | 单一姿势的变体 |
| **图像到图像的细化** | 中等 | 中等 | 优化现有图像 |
| **提示中包含参考图像** | 变化较大 | 当模型支持时 |

## 参考文档类型

### 1. 人物全方位展示文档

从多个角度展示角色：

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

### 2. 表情展示文档

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

至少包含 6 种表情：中立、快乐、愤怒、悲伤、惊讶、思考。

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

### 3. 服装/服饰文档

为同一角色准备多种服装：

| 服装 | 说明 |
|------|---------|
| 休闲装 | 运动夹克、T 恤、牛仔裤 |
| 正装 | 西装外套、纽扣衬衫、休闲裤 |
| 运动装 | 运动胸罩、紧身裤、跑鞋 |
| 正式装 | 晚礼服、高跟鞋 |

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

## 描述锚点技术

最实用的一致性技术：编写一段 **50 多字的详细描述**，并在每个提示中完全重复使用这段描述。

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

**在每个提示中都使用这个模板**，只需更改动作/姿势/场景即可。

## 比例指南

| 风格 | 头身比例 | 适用场景 |
|-------|-----------|---------|
| 现实主义 | 7.5 : 1 | 电影、写实风格 |
| 英雄风格 | 8 : 1 | 超级英雄、动作场景 |
| 动漫/漫画风格 | 5-6 : 1 | 日本动画风格 |
| 可爱风格 | 4-5 : 1 | 西方动画 |
| QUBI/超变形风格 | 2-3 : 1 | 可爱、喜剧风格、吉祥物 |

在提示中明确说明比例风格：例如 “现实主义比例” 或 “动漫风格比例”。

## 使用 LoRA 保持一致性

对于需要大量相同角色图像的项目，可以训练一个 LoRA 模型：

```bash
# Use FLUX with a character LoRA
infsh app run falai/flux-dev-lora --input '{
  "prompt": "maya_chen character, sitting at a cafe reading a book, warm afternoon light, candid photography style",
  "loras": [{"path": "path/to/maya-chen-lora.safetensors", "scale": 0.8}]
}'
```

**LoRA 训练技巧：**
- 需要 10-20 张该角色的参考图像（风格一致）
- 使用特定的触发词进行训练（例如 “maya_chen”）
- 比例设置为 0.7-0.9 可在保持一致性和提示灵活性之间取得平衡
- 比例越低，创作自由度越高；比例越高，匹配要求越严格

## 常见的一致性问题及解决方法

| 问题 | 发生原因 | 解决方法 |
|------|-----------|---------|
| **头发颜色变化** | 模型对“红色头发”的理解不同 | 使用具体的颜色代码：#C0392B（红棕色） |
| **眼睛颜色变化** | 生成时模型对此的重视程度较低 | 在提示中提前说明眼睛的颜色 |
| **服装不一致** | 模型会创造性地填充细节 | 明确描述每件服装的细节 |
| **年龄差异** | 年龄描述模糊 | 使用“二十多岁”等具体年龄 |
| **面部结构变化** | 不同的生成结果会导致面部结构变化 | 使用 LoRA 模型或相同的种子 |
| **比例变化** | 不同的风格会导致比例差异 | 明确指定“7.5 的头身比例” |

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
|------|---------|---------|
| 描述模糊 | 每次生成的字符都不同 | 使用 50 多字的详细描述 |
| 提示结构不一致 | 强调点不同会导致结果不同 | 保持提示结构一致，仅更改动作/场景 |
| 仅生成一个视角 | 无法在不同场景中使用角色 | 创建完整的角色参考资料 |
| 无色彩记录 | 不同生成的图像颜色会不一致 | 记录颜色的十六进制代码 |
| 忽略表情文档 | 角色显得单一 | 生成 6 种以上的表情 |
| 大型项目未使用 LoRA | 一致性问题加剧 | 对于需要大量图像的项目，训练 LoRA 模型 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@flux-image
npx skills add inferencesh/skills@prompt-engineering
```

浏览所有相关应用程序：`infsh app list`