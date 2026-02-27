---
name: ad-designer
description: 使用 Nano Banana Pro（Gemini 3 Pro Image）生成营销广告图片。该工具能够接收来自广告策划团队的创意要求，参考品牌视觉风格指南来构建适合营销的图像模板，并生成符合平台要求的图片（支持 1:1、9:16、16:9、4:5 等格式）。系统内置自我审核机制，可检测图片中的错误（如错误的 logo、文字内容或图像质量问题）。采用“先草图、再优化”的工作流程：快速生成 1K 分辨率的初步版本，最终输出 4K 分辨率的成品图片。生成的图片会被保存在 `/tmp/marketing/assets/images/` 目录下。
---
# 广告设计师

根据活动策划工具（campaign-planner）提供的创意简报生成营销广告图片。该工具会使用 `nano-banana-pro` 图像生成引擎，并结合品牌视觉规范来构建生成提示；同时，系统会进行自我审查，以确保图片质量在最终确定之前没有问题。

## 角色

- **广告设计师**（负责执行此技能）：唯一执行者
- **nano-banana-pro**：图像生成引擎（上游依赖项）
- **活动策划工具（campaign-planner）**：创意简报的来源
- **品牌视觉规范构建工具（brand-bible-builder）**：品牌视觉标识的来源

---

## 先决条件

在开始之前，请确认以下内容是否已准备：

```bash
command -v uv
test -n "$GEMINI_API_KEY"
test -f ~/.codex/skills/nano-banana-pro/scripts/generate_image.py
```

- 如果缺少 `uv`：提示用户使用以下命令安装它：`curl -LsSf https://astral.sh/uv/install.sh | sh`
- 如果 `GEMINI_API_KEY` 未设置：提示用户从 Google AI Studio 中导出该密钥。
- 如果脚本缺失：提示用户先安装 `nano-banana-pro` 工具。

---

## 第一步：收集输入信息

确定对话或文件系统中存在的输入内容：

| 输入内容 | 来源 | 所在位置 |
|---------|--------|---------|
| 创意简报 | 活动策划工具 | `/tmp/marketing/campaigns/<brand>-campaign-plan.json`（作为 `ad_creatives` 数组，或直接在对话中提供） |
| 品牌视觉规范 | 品牌视觉规范构建工具 | `/tmp/marketing/brands/<brand>/brand-bible.md`（或直接提供） |
- 宽高比 | 用户或创意简报 | 未指定时默认为 1:1 |
- 分辨率模式 | 用户设置 | 未指定时默认为“草图”（1K），除非用户指定为“最终版”（4K） |

如果缺少创意简报，请询问：
> “我需要一个创意简报来生成广告。请先运行 `/campaign-planner`，或者直接提供简报的详细信息：标题、视觉方向、呼叫行动（CTA）和目标受众。”

如果缺少品牌视觉规范，请使用默认的视觉样式，并在输出中注明这一点，并建议用户运行 `/brand-bible-builder` 以获得符合品牌风格的结果。

---

## 第二步：读取品牌视觉规范

打开品牌视觉规范文件，提取以下关键信息作为参考：

- **主要颜色**：十六进制代码或描述性词汇（例如：`#1A2E5A`（深海军蓝），`#F5A623`（暖琥珀色）
- **辅助/点缀颜色**：辅助色调
- **字体风格**：衬线字体与无衬线字体、字体粗细、风格描述（例如：“粗体几何无衬线字体”，“轻量级编辑风格衬线字体”）
- **图像风格**：摄影图片与插图、生活场景图片与产品图片、色彩基调（温暖/冷色调/柔和色调/鲜艳色调）
- **布局风格**：极简风格与内容密集型布局、空白较多的布局与层次丰富的布局
- **整体基调**：正式风格、休闲风格、大胆风格、趣味风格、高端风格、亲和风格

将这些信息作为内部参考，不要展示给用户。在第三步构建生成提示时使用这些信息。

---

## 第三步：构建图像生成提示

每次生成图像时都必须遵循以下规则（这些规则不可更改）：

### 核心规则（来自最佳实践的图像生成建议）

**规则 1：简洁为上。** 简洁、明确的提示比冗长的描述性提示效果更好。视觉描述建议控制在 15–30 个词以内。避免重复使用相同的形容词。

**规则 2：禁止使用品牌名称或公司名称。** 生成提示时绝对不要包含品牌名称、产品名称、标志描述或任何商标。图像生成引擎可能无法正确识别这些元素，这些内容需要在后期添加。

**规则 3：仅包含明确指定的文本。** 如果简报中指定了要显示在图片中的标题，请严格按照原样使用——不要改写。如果没有指定任何文本，则不要在提示中添加任何内容。除非简报明确要求，否则不要添加呼叫行动（CTA）、标语或文案。

**规则 4：描述情感和构图，而非具体数据。** 例如，不要写“一个正在节省账单费用的女性”，而应该写“自信的女性、明亮的家庭办公环境、温暖的晨光、放松的表情”。情感是传达信息的关键；模型会处理其余的细节。

**规则 5：在描述颜色时不要直接使用品牌名称。** 将十六进制代码转换为描述性词汇：`#1A2E5A` 可以描述为“深海军蓝”，`#F5A623` 可以描述为“暖琥珀色”。在提示中自然地使用这些颜色词汇。

### 提示构建公式

按照以下顺序组合提示内容：
```
[SUBJECT] — who or what is the focal element
[SETTING] — environment or background context
[MOOD / EMOTION] — feeling the image should evoke
[COMPOSITION] — framing, shot type, perspective
[LIGHTING] — quality and direction of light
[COLOR PALETTE] — 2–3 colors derived from brand bible
[STYLE] — photography/illustration style from brand bible
[AVOID] — explicit exclusions (text, logos, clutter, etc.)
```

并非每次都需要使用所有 8 个字段。只使用与简报相关的字段。通常，5 个字段的提示比 8 个字段的提示更有效。

### 示例构建过程

**简报输入：**
```
headline: "Finally, sleep that works"
visual_direction: "Woman waking up refreshed, natural light bedroom"
cta: "Try free tonight"
target_persona: "Aisha, 28, KL, stressed professional"
```

**品牌视觉规范：** 温暖珊瑚色 `#E8735A`、米白色 `#FAF7F2`、编辑风格无衬线字体、温暖且极简的摄影风格。

**生成的提示：**
```
Young woman waking up peacefully, sunlit minimalist bedroom, linen textures,
warm coral and off-white tones, soft morning light through sheer curtains,
close-up on relaxed expression, warm editorial photography style
```

**未包含的内容：** 品牌名称、呼叫行动文本、产品名称、标题文本（因为简报中没有指定显示的文本）。

---

## 第四步：选择宽高比

根据简报中指定的平台或格式，选择正确的宽高比和像素尺寸：

| 平台/格式 | 宽高比 | 像素尺寸 | 使用场景 |
|---------|---------|-----------|----------|
| Instagram/Facebook 主页 | 1:1 | 1080 × 1080 | 方形布局的帖子 |
| Instagram 故事/Reel | 9:16 | 1080 × 1920 | 全屏竖屏 |
| Facebook 主页（竖版） | 4:5 | 1080 × 1350 | 更高的屏幕布局 |
| YouTube/LinkedIn 封面 | 16:9 | 1920 × 1080 | 横屏/横幅 |

如果简报中没有指定平台，默认使用 1:1 的宽高比。

对于轮播广告：所有图片应使用相同的宽高比。除非简报另有要求，否则使用 1:1 的比例。

通过 `--resolution` 参数将宽高比传递给脚本。`nano-banana-pro` 脚本会自动处理图片尺寸。草图版本使用 1K 分辨率生成，最终版本使用 4K 分辨率生成。

---

## 第五步：生成图像

创建输出目录：
```bash
mkdir -p /tmp/marketing/assets/images
```

### 单张图片生成

使用以下命令模式。请始终使用绝对路径来调用脚本：
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "<constructed prompt>" \
  --filename "/tmp/marketing/assets/images/<timestamp>-<brief-id>-draft.png" \
  --resolution 1K
```

文件命名格式：`yyyy-mm-dd-hh-mm-ss-<brief-id>-draft.png`
- `brief-id`：从简报标题中提取的小写字符串（例如：`finally-sleep-works`）
- 使用当前日期和时间作为文件时间戳

### 先生成草图版本

始终按照以下顺序操作：
1. **先生成 1K 分辨率的草图** — 先生成 1K 分辨率的图片以获取快速反馈。
2. **迭代**：如果在自我审查（第六步）中发现问题，调整提示内容并重新生成 1K 分辨率的图片。最多尝试 3 次。
3. **生成最终版本（4K）**：只有在用户批准草图或自我审查通过后，才生成 4K 分辨率的图片。此时将文件后缀从 `-draft` 更改为 `-final`，并设置 `--resolution 4K`。

### 轮播广告

每张图片都应作为单独的文件生成。命名规则如下：
```
yyyy-mm-dd-hh-mm-ss-<brief-id>-card-01-draft.png
yyyy-mm-dd-hh-mm-ss-<brief-id>-card-02-draft.png
```

确保所有图片在视觉上保持一致：
- 每张图片的提示中使用相同的颜色描述
- 每张图片的提示中使用相同的风格描述
- 每张图片的提示中使用相同的灯光描述
- 每张图片的主题和构图可以有所不同

---

## 第六步：自我审查循环（至关重要）

生成每张图片后，必须进行结构化的自我审查，然后再展示给用户。不要跳过这一步。

对每张生成的图片执行以下检查：

| 检查项 | 通过条件 | 失败处理方式 |
|---------|-----------------|-------------------|
| 文本准确性 | 所有指定的文本都正确显示且可读 | 简化提示内容；添加明确的文本指示 |
| 无多余的标志或品牌元素 | 图片中不能出现品牌标志、商标、图标或水印 | 在提示中添加“禁止使用标志、文本或水印” |
| 无品牌名称或产品名称**：图片中不能出现品牌名称或产品名称 | 在提示中添加“禁止使用品牌名称或产品名称” |
| 宽高比 | 符合要求的格式 | 使用正确的宽高比重新生成图片 |
| 颜色一致性 | 主要颜色与品牌规范一致 | 在提示中加强颜色描述 |
| 整体质量 | 图片内容连贯、专业且符合简报要求 | 重新构建提示，使用更简洁的结构 |

### 失败处理

如果任何检查项未通过：
1. 从上述列表中确定具体的问题。
2. 对提示内容进行相应的修改。
3. 重新生成 1K 分辨率的图片。
4. 对新的图片再次进行自我审查。
5. 如果经过 3 次尝试仍然失败，向用户展示最佳结果，并说明问题所在及采取的修复措施。

不要默默地展示失败的图片。一定要告诉用户问题所在以及采取了哪些修复措施。

---

## 第七步：展示给用户审核

在自我审查通过后（或尝试 3 次后），展示生成的图片结果：
```
Ad image(s) generated for: [brief headline]

Draft(s) saved to /tmp/marketing/assets/images/:
  [timestamp]-[brief-id]-draft.png   ← [ratio] | 1K

Self-review: [PASS / notes on any issues found and fixed]

Review the image and reply with one of:
  A) Approve → I'll upscale to 4K final
  B) Adjust → describe what to change
  C) Skip → move to next brief
```

在生成最终版本的 4K 图片或处理下一个简报之前，请等待用户的反馈。

如果用户提出修改要求：
- 根据用户的修改建议调整提示内容（每次只修改一处）
- 重新生成 1K 分辨率的图片
- 再次进行自我审查
- 再次展示结果

如果用户批准修改：
- 生成 4K 分辨率的图片，并将文件后缀设置为 `-final`
- 确认文件路径：`/tmp/marketing/assets/images/[filename]-final.png`

---

## 处理多个简报

如果输入中包含多个简报（例如，来自活动策划工具的 JSON 文件，其中包含 3–5 张广告图片），请按顺序处理每个简报。完成每个简报的完整流程（生成 → 自我审查 → 用户审核 → 最终确认）后再处理下一个简报。

所有简报处理完成后，提供总结：
```
All ad images complete.

Generated:
  /tmp/marketing/assets/images/[file-1]-final.png   [ratio]
  /tmp/marketing/assets/images/[file-2]-final.png   [ratio]
  /tmp/marketing/assets/images/[file-3]-final.png   [ratio]

Next step: run /meta-ads-publisher to upload these to your ad account,
or /campaign-planner to review the full campaign.
```

---

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| `Error: No API key provided.` | 告诉用户运行 `export GEMINI_API_KEY=<key>` 并重试 |
| `Error loading input image:` | 确认 `--input-image` 路径是否存在；修复路径后重试 |
| `quota / 403 / permission` API 错误 | 密钥错误或超出使用额度；请用户检查 Google AI Studio 的使用额度 |
| Script not found at `~/.codex/skills/...` | `nano-banana-pro` 工具未安装；请用户从 ClawHub 安装该工具 |
| `uv: command not found` | 运行 `curl -LsSf https://astral.sh/uv/install.sh | sh` 后重试 |
| Image generation returns blank/empty | 提示内容可能过于严格；删除不必要的限制条件，仅保留主题和风格相关的信息 |

---

## 文件路径参考
```
/tmp/marketing/
├── assets/
│   └── images/
│       ├── yyyy-mm-dd-hh-mm-ss-<brief-id>-draft.png    ← draft outputs
│       └── yyyy-mm-dd-hh-mm-ss-<brief-id>-final.png    ← approved 4K finals
├── brands/<brand>/
│   └── brand-bible.md                                   ← brand visual reference
└── campaigns/
    └── <brand>-campaign-plan.json                       ← input brief source
```