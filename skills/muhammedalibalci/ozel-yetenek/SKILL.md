---
name: tiktok-skinny-fat
description: >
  TikTok slideshow (carousel) creation skill for the Skinny Fat AI app.
  Generates viral TikTok photo carousels: hook writing, image generation prompts,
  text overlays, captions, and hashtags. Trigger this skill when the user says
  "create TikTok", "make slideshow", "generate carousel", "create content",
  "make a post", "today's content", "write hooks", "plan TikTok", "batch content",
  "transformation post", "skinny fat content", or any variation of these.
triggers:
  - "create tiktok"
  - "make slideshow"
  - "generate carousel"
  - "create content"
  - "make a post"
  - "today's content"
  - "write hooks"
  - "plan tiktok"
  - "batch content"
  - "transformation post"
  - "skinny fat content"
tools:
  - filesystem
  - shell
---

# TikTok幻灯片制作技巧 — Skinny Fat AI

本技巧用于为Skinny Fat AI应用程序生成TikTok照片轮播（幻灯片）内容。目标：制作具有高传播潜力、内容一致且注重转化效果的幻灯片。

---

## 1. 通用规则

### 1.1 幻灯片格式
- 每个幻灯片必须恰好有6张图片，不多也不少。
- 所有图片均为肖像画格式（1024x1536像素），严禁使用横屏图片。
- 第1张幻灯片必须包含吸引注意力的文字（hook text）。
- 第6张幻灯片必须包含呼吁行动的文字（CTA，Call to Action）。
- 第2至5张幻灯片应包含变化效果图片、对比图或信息图表。

### 1.2 质量标准
- 所有图片必须看起来真实自然，类似手机拍摄的照片。
- 避免使用AI生成的效果。在提示中务必使用“iPhone照片”、“自然光线”、“真实感”等描述。
- 禁止生成人脸图片——请使用身体轮廓、测量数据图片、食物图片以及应用程序界面截图。
- 品牌颜色：深海蓝（#1a1a2e）、霓虹绿/蓝（#00d4aa），文字颜色为白色。

---

## 2. 吸引注意力的文案公式

这是整个技巧中最关键的部分。文案决定了幻灯片的效果。

### 2.1 有效的文案公式（请使用此公式）
```
[Another person] + [doubt or conflict] → showed them AI / the result → they changed their mind
```

该公式有效的原因是：
- 它能讲述一个故事（人们喜欢点击故事类内容）；
- 它能引发好奇心（人们想看到用户的反应）；
- 它能自然地展示产品效果（有其他人验证过这些效果）；
- 它能建立情感联系。

### 2.2 经验证的文案示例
请将这些作为模板，并进行变体创作：

**家人/朋友反应类文案：**
- “在我向女朋友展示AI分析结果之前，她一直以为我只是有点瘦而已。”
- “妈妈一直说‘你已经很瘦了’，直到她看到了我的变化。”
- “朋友说我不需要减肥，直到我给他看了这些结果。”
- “哥哥说去健身房是浪费钱，直到他看到了我48天后的变化。”
- “室友说我们吃的东西一样，但AI分析显示我们的营养成分完全不同。”

**教练/专家类文案：**
- “我的私人教练说我不属于‘瘦胖’人群。然后我给他看了AI分析结果。”
- “营养师说我不需要计算卡路里，但在使用AI追踪一周后……”
- “我告诉了一位健身博主我属于‘瘦胖’人群，没想到他会这样反应。”

**自我转变类文案：**
- “大家都说我‘已经很瘦了’，但脱掉衣服后真相大白了。”
- “我体重170磅，穿衣服时看起来很瘦，但体脂率却有28%。”
- “体重相同，但身体状况却完全不同——这就是48天带来的改变。”

**食物/营养类惊喜文案：**
- “我以为自己吃的早餐很健康，但AI分析显示并非如此。”
- “我一直说自己吃得很少，直到AI扫描了我的饮食。”
- “我以为吃沙拉就代表吃得健康，但AI分析结果却相反。”

**恐惧/紧迫感类文案：**
- “‘瘦胖’比你想象的更危险——AI给出的风险等级是……”
- “你可能看起来很瘦，但实际上可能有内脏脂肪堆积。AI分析证明了这一点。”
- “我的BMI正常，但内脏脂肪却进入了危险区间。”

### 2.3 不建议使用的文案格式
这些文案效果不佳，请避免使用：
- 仅强调功能的文案：“使用Skinny Fat AI追踪你的营养成分” → 人们不会感兴趣。
- 普通的健身类文案：“48天内改变你的体型” → 太泛泛而谈，听起来像所有广告。
- 仅强调价格的文案：“免费获取身体分析” → 像广告一样。
- 以问题形式提出的文案：“你是‘瘦胖’人群吗？” → 互动率低。
- 模糊不清的文案：“你的身体在告诉你什么？” → 不够明确。
- 仅强调产品功能的文案：“我们应用程序的最佳功能” → 人们不会关心这些功能。

### 2.4 文案写作规则
- 最多15个单词，简洁有力。
- 必须包含“其他人”的元素或“意外反应”的元素。
- 文案结尾不应是疑问句，而应该是一个引发好奇心的陈述。
- 避免使用专业术语，如“recomp”、“visceral”、“macro”等，除非在特定上下文中使用。
- 为全球用户使用英文写作。

---

## 3. 图片生成

### 3.1 提示结构
每个提示必须遵循以下结构：

```
iPhone photo of [scene description]. [Detailed physical description].
Natural phone camera quality, realistic lighting. Portrait orientation 1024x1536.
[Style/mood/variation for this specific slide]
```

### 3.2 一致的背景描述
在整个幻灯片中使用相同的背景描述。只需更换服装、姿势或场景。

**男性瘦胖模板：**
```
Male body silhouette, mid-20s, approximately 175cm tall, 78kg.
Narrow shoulders relative to waist. Soft midsection with visible
belly fat, no visible muscle definition. Arms thin but not toned.
Slight forward head posture. Shot from [angle].
```

**女性瘦胖模板：**
```
Female body silhouette, mid-20s, approximately 165cm tall, 62kg.
Slim frame but soft midsection. No visible muscle tone in arms.
Slight lower belly pouch. Narrow shoulders.
Shot from [angle].
```

**重要提示：** 请勿包含面部细节。使用身体轮廓、背影或半身照。

### 3.3 食物图片模板
```
iPhone photo of [food description] on [plate/table description].
Overhead shot, natural kitchen lighting, slightly messy realistic table.
A phone screen next to the plate showing a nutrition scanning app interface
with calories and macros visible. Portrait orientation 1024x1536.
```

### 3.4 应用程序界面图片
如果可用，请优先使用真实的应用程序截图。如果需要模拟图片：
```
Clean mobile app screenshot mockup on dark background (#1a1a2e).
Modern fitness app UI showing [feature: body analysis / meal scan / workout plan].
Neon accent color (#00d4aa). Minimal, premium design.
Portrait orientation 1024x1536.
```

### 3.5 幻灯片内容规划

**格式A：转变故事（效果最佳）**
| 幻灯片 | 内容 | 视觉类型 |
|-------|---------|-------------|
| 1 | 吸引注意力的文字 | 引人注目的“变化前”场景或情感画面 |
| 2 | “变化前”的状态 | 瘦胖的身体轮廓/不健康的饮食 |
| 3 | AI分析结果 | 应用程序界面——身体分析界面 |
| 4 | 计划/方案 | 应用程序界面——锻炼或营养计划 |
| 5 | “变化后”的状态/进步 | 更健康的身体轮廓/健康的饮食 |
| 6 | 呼吁行动的文字 | 应用程序图标 + “生物信息中的链接” |

**格式B：食物惊喜（互动率较高）**
| 幻灯片 | 内容 | 视觉类型 |
|-------|---------|-------------|
| 1 | 吸引注意力的文字 | 桌子上摆放的不健康食物 |
| 2 | 食物细节 | 食物照片 |
| 3 | AI扫描结果 | 应用程序界面——食物扫描结果（评分不佳） |
| 4 | 正确的替代方案 | 健康食物照片 |
| 5 | AI扫描结果（评分良好） | 应用程序界面——食物扫描结果（评分良好） |
| 6 | 呼吁行动的文字 | “瘦胖评分解释” + “生物信息中的链接” |

**格式C：教育/信息类（效果中等，有助于建立信任）**
| 幻灯片 | 内容 | 视觉类型 |
|-------|---------|-------------|
| 1 | 吸引注意力的文字 | 令人震惊的统计数据 |
| 2 | 问题解释 | 信息图表形式 |
| 3 | 原因分析 | 信息图表 |
| 4 | 解决方案 | 应用程序功能展示 |
| 5 | 证据/结果 | 变化前后的对比或数据 |
| 6 | 呼吁行动的文字 | 下载按钮 |

---

## 4. 文本叠加规则

### 4.1 技术规格
- 字体大小：至少占幻灯片宽度的6.5%。严禁低于5%。
- 颜色：白色（#FFFFFF），文字背景为半透明的黑色。
- 位置：位于图片的上1/3区域。严禁放在最顶部——TikTok的状态栏会覆盖文字。
- 安全区域：顶部留出15%，底部留出20%的空间（以适应TikTok的界面元素）。
- 每行最多20个字符，超过则换行。
- 最多3行文本，超过3行会导致文字难以阅读。

### 4.2 文本叠加使用
- 第1张幻灯片：必须放置吸引注意力的文字，字体要大且加粗，便于阅读。
- 第2至5张幻灯片：可选。如有需要，可添加简短的描述性文字（2-4个单词）。
- 第6张幻灯片：放置呼吁行动的文字，格式为“Skinny Fat AI — 生物信息中的链接”或“免费试用 — 生物信息中的链接”。
- 文本绝不能遮挡图片的主要内容。

### 4.3 文本渲染（使用Pillow库）
```python
# Core text overlay parameters
FONT_SIZE_RATIO = 0.065  # 6.5% of width
MAX_LINE_CHARS = 20      # Characters per line
TEXT_Y_POSITION = 0.20   # 20% from top
SHADOW_OFFSET = 3
SHADOW_COLOR = (0, 0, 0, 180)
TEXT_COLOR = (255, 255, 255, 255)
BACKGROUND_PADDING = 20
BACKGROUND_COLOR = (0, 0, 0, 120)  # Semi-transparent black
```

**重要提示：** 在使用Pillow库渲染文本时，文本不得被水平压缩。如果一行超过最大宽度，必须换行显示。

---

## 5. 字幕编写

### 5.1 字幕格式
字幕应该是一个简短的故事，而不是功能列表。

**结构：**
```
[1–2 sentence story — expand the hook, add emotion]
[1 sentence mentioning the app naturally]
[CTA — "Link in bio" or "Try it from the link in my profile"]

#skinnyfat #bodyrecomp #[3 more niche hashtags]
```

**好的字幕示例：**
```
Showed my girlfriend my AI body analysis. She stopped saying
"you're already skinny." My body fat came back at 26%, skinny fat
risk level high. Started the 48-day program. Get your own
analysis with Skinny Fat AI, link in bio.

#skinnyfat #bodyrecomp #bodyanalysis #fitnessmotivation #skinnyfattransformation
```

**不好的字幕示例（请避免使用）：**
```
Analyze your body with Skinny Fat AI! Count calories, track macros,
get a 48-day program. Download now!

#fitness #gym #workout #health #app
```

### 5.2 标签规则
- 最多使用5个标签（TikTok的限制）。
- 前两个标签必须为：#skinnyfat #bodyrecomp
- 剩下的3个标签应根据内容选择相关主题标签。
- 常用标签示例：
  - #skinnyfattransformation
  - #bodyfatpercentage
  - #mealprep
  - #macrotracking
  - #fitnessjourney
  - #gymtok
  - #workouttok
  - #beforeandafter
  - #bodytransformation
  - #recomp
  - #caloriecounting
  - #fitnesstok
  - #bodycomposition
  - #healthyeating

---

## 6. 内容制作流程

### 步骤1：选择文案
- 使用第2节中的文案公式编写吸引注意力的文案。
- 与用户确认：“我可以使用这个文案：[文案内容]吗？”
- 只有得到批准后才能继续下一步。

### 步骤2：幻灯片计划
- 为6张幻灯片制定计划（选择第3.5节中的格式）。
- 为每张幻灯片准备视觉描述、文字叠加（如需要）和提示草稿。
- 向用户展示计划并获取批准。

### 步骤3：确定背景描述
- 根据幻灯片主题编写固定的身体/食物/场景描述（参考第3.2-3.3节）。
- 这个描述在所有幻灯片中必须保持一致，仅改变风格或状态。

### 步骤4：编写提示
- 为每张幻灯片准备单独的图片生成提示。
- 复制并粘贴固定的背景描述，仅更新需要变化的部分。
- 确保每个提示中都指定使用肖像画格式（1024x1536像素）。

### 步骤5：生成图片
- 调用图片生成API（用户可以选择合适的模型）。
- 将每张图片保存为`slides/[幻灯片ID]/slide-[1-6].png`。

### 步骤6：添加文字叠加
- 按照第4节中的规则添加文字叠加。
- 第1张幻灯片放置吸引注意力的文字，第6张幻灯片放置呼吁行动的文字。
- 将带有文字叠加的图片保存为`slides/[幻灯片ID]/final-slide-[1-6].png`。

### 步骤7：编写字幕和标签
- 按照第5节中的规则编写字幕。
- 将字幕文件保存为`slides/[幻灯片ID]/caption.txt`。

### 步骤8：交付成果
- 将所有6张最终图片和字幕文件交付给用户。
- 待用户审核并批准后，用户手动将图片上传到TikTok，并添加热门音效后发布。

---

## 7. 批量内容规划

当用户要求“规划本周的内容”或“制作5个幻灯片”时：

### 7.1 规划流程
1. 查看之前的数据表现（从内存文件中获取）。
2. 提出5-10个不同的文案建议。
3. 与用户共同选择最佳的5个文案。
4. 为每个幻灯片指定相应的格式（格式A、B或C）。
5. 准备所有提示内容。
6. 可以顺序生成或批量生成（如果批量API可用，可节省50%的成本）。

### 7.2 内容多样性规则
- 同一格式不得连续使用超过2次。
- 每周至少包括：2个转变故事、2个食物惊喜内容和1个教育/信息类内容。
- 不要连续使用相同的文案公式，要交替使用不同的“人物”（如妈妈、爸爸、朋友、伴侣、营养师、私人教练、室友等）。

---

## 8. 记录与学习系统

### 8.1 表现追踪
每次发布内容后，将以下信息记录到`memory/tiktok-performance.md`文件中：

```markdown
## [Date] - [Short hook summary]
- Hook: [full hook text]
- Format: [A/B/C]
- Views: [number]
- Likes: [number]
- Shares: [number]
- Comments: [number]
- App downloads (estimated): [number]
- Notes: [what worked, what didn't]
```

### 8.2 失败记录
对于每次失败的发布或技术错误，记录到`memory/failure-log.md`文件中：

```markdown
## [Date] - ERROR: [short description]
- What happened: [detail]
- Why it happened: [analysis]
- Fix: [what was done]
- Rule: [new rule to prevent this from happening again]
```

### 8.3 学习循环
每发布10条内容后，分析数据表现。
- 对比表现最好的3条和最差的3条内容。
- 将有效的创作模式添加到技巧文件中作为规则。
- 将失败的创作模式添加到“禁止使用”的列表中。

---

## 9. 技术说明

### 9.1 文件结构
```
skinny-fat-tiktok/
├── slides/
│   ├── [slideshow-id]/
│   │   ├── slide-1.png
│   │   ├── slide-2.png
│   │   ├── ...
│   │   ├── slide-6.png
│   │   ├── final-slide-1.png  (with overlay)
│   │   ├── ...
│   │   ├── final-slide-6.png
│   │   └── caption.txt
├── memory/
│   ├── tiktok-performance.md
│   └── failure-log.md
├── prompts/
│   └── templates.md
└── assets/
    └── fonts/
```

### 9.2 图片生成API使用
- 图片生成模型由用户选择（如gpt-image-1、DALL-E 3等）。
- 始终请求生成肖像画格式（1024x1536像素）。
- 在提示中务必使用“iPhone照片”、“自然光线”、“真实感”等描述。
- 禁止生成人脸图片，使用身体轮廓、背影或半身照。
- 如果可用，请使用批量API（可节省50%的成本）。

### 9.3 文本叠加脚本
使用Python的Pillow库来生成文本叠加效果。基础脚本如下：
```python
from PIL import Image, ImageDraw, ImageFont

def add_text_overlay(image_path, text, output_path, position="top"):
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    width, height = img.size
    font_size = int(width * 0.065)

    try:
        font = ImageFont.truetype("assets/fonts/bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Wrap text (max 20 chars per line)
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if len(test_line) <= 20:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Calculate position
    y_start = int(height * 0.20) if position == "top" else int(height * 0.75)

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = y_start + i * (text_height + 15)

        # Background box
        padding = 20
        draw.rectangle(
            [x - padding, y - padding // 2, x + text_width + padding, y + text_height + padding // 2],
            fill=(0, 0, 0, 120)
        )

        # Shadow
        draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0, 180))
        # Main text
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))

    img = Image.alpha_composite(img, overlay)
    img.convert("RGB").save(output_path)
```

---

## 10. 重要检查清单

在交付任何幻灯片之前，请确认以下所有内容：
- [ ] 是否恰好有6张图片？
- [ ] 所有图片是否均为1024x1536像素的肖像画格式？
- [ ] 第1张幻灯片是否包含吸引注意力的文字？
- [ ] 文字是否清晰可读（字体大小是否足够）？
- [ ] 文本叠加是否位于TikTok规定的安全区域内？
- [ ] 所有幻灯片的背景和场景是否一致？
- [ ] 是否没有人脸图片？
- [ ] 字幕是否是一个简短的故事，而不是功能列表？
- [ ] 是否使用了5个或更少的标签？
- [ ] 第6张幻灯片是否包含呼吁行动的文字？
- [ ] 文案是否遵循有效的公式（包含“其他人”的元素和引发好奇心的内容）？
- [ ] 文本是否没有被水平压缩？

---

## 11. 绝对禁止的行为

严禁以下行为：
- 生成横屏图片；
- 生成少于或超过6张图片；
- 生成包含人脸的图片；
- 使用包含功能列表的字幕；
- 使用过多的标签（超过5个）；
- 使用过于激进的呼吁行动语句（如“立即下载！”或“购买此产品！”；
- 重复使用相同的文案；
- 将文字叠加放在图片底部；
- 将字体大小设置为低于5%；
- 在不同幻灯片中更改背景描述（影响一致性）；
- 提供医疗建议（该应用程序提供的是“估计”结果，而非医学诊断）；
- 做出不切实际的改变承诺。

---

## 12. 首次使用指南

对于首次使用此技巧的用户：
1. 创建`skinny-fat-tiktok/`文件夹结构；
2. 初始化`memory/tiktok-performance.md`文件（空白模板）；
3. 初始化`memory/failure-log.md`文件（包含基本规则的空模板）；
4. 询问用户的目标受众信息（年龄组、主要关注性别）；
5. 提出3个文案建议并获取用户批准；
6. 制作第一个幻灯片并交付给用户；
7. 根据用户反馈更新技巧文件。