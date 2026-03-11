---
name: baoyu-cover-image
description: 生成具有5个维度的文章封面图片（类型、调色板、渲染方式、文字内容、整体氛围），支持使用10种不同的调色板和7种渲染风格。图片格式可设置为电影格式（2.35:1）、宽屏格式（16:9）或正方形格式（1:1）。当用户请求“生成封面图片”、“创建文章封面”或“制作封面”时，可使用该功能。
version: 1.56.1
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-cover-image
---
# 图片生成器

该工具可为文章生成精美的封面图片，并提供5个维度的自定义选项。

## 使用方法

```bash
# Auto-select dimensions based on content
/baoyu-cover-image path/to/article.md

# Quick mode: skip confirmation
/baoyu-cover-image article.md --quick

# Specify dimensions
/baoyu-cover-image article.md --type conceptual --palette warm --rendering flat-vector

# Style presets (shorthand for palette + rendering)
/baoyu-cover-image article.md --style blueprint

# With reference images
/baoyu-cover-image article.md --ref style-ref.png

# Direct content input
/baoyu-cover-image --palette mono --aspect 1:1 --quick
[paste content]
```

## 选项说明

| 选项          | 描述                                      |
|-----------------|-------------------------------------------|
| `--type <名称>`     | 图片类型：hero（英雄式）、conceptual（概念式）、typography（排版式）、metaphor（隐喻式）、scene（场景式）、minimal（极简式） |
| `--palette <名称>`    | 色调方案：warm（温暖）、elegant（优雅）、cool（冷色调）、dark（深色系）、earth（自然色）、vivid（鲜艳）、pastel（淡色调）、mono（单色）、retro（复古）、duotone（双色） |
| `--rendering <名称>` | 渲染方式：flat-vector（平面矢量）、hand-drawn（手绘）、painterly（绘画风格）、digital（数字风格）、pixel（像素风格）、chalk（粉笔风格）、screen-print（丝网印刷） |
| `--style <名称>`     | 预设样式（详见[样式预设](references/style-presets.md)         |
| `--text <级别>`     | 文本内容：none（无文本）、title-only（仅标题）、title-subtitle（标题加副标题）、text-rich（包含详细文本） |
| `--mood <级别>`     | 情感基调：subtle（柔和）、balanced（平衡）、bold（鲜明）         |
| `--font <名称>`     | 字体类型：clean（简洁无衬线）、handwritten（手写体）、serif（衬线体）、display（装饰性字体） |
| `--aspect <比例>`    | 宽高比：16:9（默认）、2.35:1、4:3、3:2、1:1、3:4             |
| `--lang <代码>`     | 标题语言（en、zh、ja等）                         |
| `--no-title`      | 等同于`--text none`                         |
| `--quick`       | 跳过确认步骤，使用自动选择                   |
| `--ref <文件...>`     | 参考图片文件（用于指导风格和构图）                   |

## 五个自定义维度

| 维度            | 可选值                        | 默认值                         |
|-----------------|-------------------------------------------|
| **Type**          | hero, conceptual, typography, metaphor, scene, minimal | auto                          |
| **Palette**        | warm, elegant, cool, dark, earth, vivid, pastel, mono, retro, duotone | auto                          |
| **Rendering**       | flat-vector, hand-drawn, painterly, digital, pixel, chalk, screen-print | auto                          |
| **Text**          | none, title-only, title-subtitle, text-rich         | title-only                        |
| **Mood**          | subtle, balanced, bold                     | balanced                         |
| **Font**          | clean, handwritten, serif, display                | clean                          |

自动选择规则：[references/auto-selection.md](references/auto-selection.md)

## 图片样式库

- **图片类型**：hero、conceptual、typography、metaphor、scene、minimal
  → 详情：[references/types.md](references/types.md)
- **色调方案**：warm、elegant、cool、dark、earth、vivid、pastel、mono、retro、duotone
  → 详情：[references/palettes/](references/palettes/)
- **渲染方式**：flat-vector、hand-drawn、painterly、digital、pixel、chalk、screen-print
  → 详情：[references/renderings/](references/renderings/)
- **文本内容**：none（纯视觉效果）、title-only（默认）、title-subtitle、text-rich（包含标签）
  → 详情：[references/dimensions/text.md](references/dimensions/text.md)
- **情感基调**：subtle（柔和）、balanced（平衡）、bold（鲜明）
  → 详情：[references/dimensions/mood.md](references/dimensions/mood.md)
- **字体类型**：clean（无衬线）、handwritten、serif、display（装饰性字体）
  → 详情：[references/dimensions/font.md](references/dimensions/font.md)

## 文件结构

输出文件将根据`default_output_dir`的设置存放：
- 如果设置为`same-dir`，则输出文件位于`{article-dir}/imgs/`目录下；
- 如果设置为`independent`（默认值），则输出文件位于`cover-image/{topic-slug}/`目录下。

```
<output-dir>/
├── source-{slug}.{ext}    # Source files
├── refs/                  # Reference images (if provided)
│   ├── ref-01-{slug}.{ext}
│   └── ref-01-{slug}.md   # Description file
├── prompts/cover.md       # Generation prompt
└── cover.png              # Output image
```

**文件命名规则**：
文件名由2-4个单词组成，使用kebab-case（驼峰式命名法）。如果名称冲突，会在文件名后添加`-YYYYMMDD-HHMMSS`作为唯一标识。

## 工作流程

### 进度检查

```
Cover Image Progress:
- [ ] Step 0: Check preferences (EXTEND.md) ⛔ BLOCKING
- [ ] Step 1: Analyze content + save refs + determine output dir
- [ ] Step 2: Confirm options (6 dimensions) ⚠️ unless --quick
- [ ] Step 3: Create prompt
- [ ] Step 4: Generate image
- [ ] Step 5: Completion report
```

### 流程图

```
Input → [Step 0: Preferences] ─┬─ Found → Continue
                               └─ Not found → First-Time Setup ⛔ BLOCKING → Save EXTEND.md → Continue
        ↓
Analyze + Save Refs → [Output Dir] → [Confirm: 6 Dimensions] → Prompt → Generate → Complete
                                              ↓
                                     (skip if --quick or all specified)
```

### 第0步：加载用户偏好设置 ⛔ （此步骤为必选）

检查`EXTEND.md`文件是否存在（优先级：项目设置 > 用户设置）：
```bash
# macOS, Linux, WSL, Git Bash
test -f .baoyu-skills/baoyu-cover-image/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-cover-image/EXTEND.md" && echo "xdg"
test -f "$HOME/.baoyu-skills/baoyu-cover-image/EXTEND.md" && echo "user"
```

### 结果处理

| 结果 | 对应操作                          |
|--------|-------------------------------------------|
| 文件找到 | 加载设置并显示摘要 → 继续下一步            |
| 文件未找到 | ⛔ 运行首次设置流程（[references/config/first-time-setup.md]）→ 保存设置 → 继续下一步            |

**重要提示**：如果`EXTEND.md`文件不存在，请在开始任何其他操作前完成设置。

### 第1步：分析内容

1. 保存参考图片（如果提供）→ [references/workflow/reference-images.md](references/workflow/reference-images.md)
2. 保存文章内容（若内容已粘贴，保存至`source.md`文件）
3. 分析文章主题、风格和关键词
4. 深入分析参考图片中的元素（⚠️）：提取具体细节
5. 确定输出文件的语言（根据用户设置或`EXTEND.md`文件）
6. 根据文件结构规则确定输出目录

### 第2步：确认用户选项 ⚠️

完整确认流程：[references/workflow/confirm-options.md](references/workflow/confirm-options.md)

| 条件       | 是否跳过 | 是否需要确认                         |
|------------|---------|-------------------------------------------|
| 使用`--quick`或`quick_mode: true` | 6个自定义维度是否都选中了？（除非指定了`--aspect`） | 是                         |
| 所有6个维度及`--aspect`都已指定 | 是                         | 否                         |

### 第3步：生成生成提示信息

将提示信息保存至`prompts/cover.md`文件。模板：[references/workflow/prompt-template.md](references/workflow/prompt-template.md)

**重要提示（关于参考图片）**：
- 如果参考图片保存在`refs/`目录下，需将其添加到文章的`references`列表中；
- 如果参考图片信息是通过口头提供的（无文件形式），则无需在参考文献部分列出，但需在正文中说明；
- 在编写提示信息前，请验证：`test -f refs/ref-NN-{slug}.{ext}`

**正文中关于参考图片的描述**必须详细，并使用“MUST”或“REQUIRED”等关键词标明其重要性，同时说明如何整合这些参考元素。

### 第4步：生成图片

1. 如果需要重新生成图片，请先备份现有的`cover.png`文件。
2. 检查图片生成工具的功能；如果有多个参考图片，需询问用户的具体需求。
3. 根据提示文件中的信息生成图片：
   - 直接使用的参考图片可通过`--ref`参数传递给生成工具；
   - 颜色方案或风格相关的信息需提取后添加到提示信息中。
4. 调用生成工具，传入提示文件、输出路径和宽高比参数。
5. 如果生成失败，系统会自动尝试一次。

### 第5步：生成完成报告

```
Cover Generated!

Topic: [topic]
Type: [type] | Palette: [palette] | Rendering: [rendering]
Text: [text] | Mood: [mood] | Font: [font] | Aspect: [ratio]
Title: [title or "visual only"]
Language: [lang] | Watermark: [enabled/disabled]
References: [N images or "extracted style" or "none"]
Location: [directory path]

Files:
✓ source-{slug}.{ext}
✓ prompts/cover.md
✓ cover.png
```

## 图片后期处理

| 操作        | 具体步骤                                      |
|------------|-------------------------------------------|
| 重新生成图片    | 先备份现有图片 → 更新提示文件 → 再重新生成图片             |
| 更改图片尺寸    | 备份图片 → 确认新的尺寸参数 → 更新提示文件 → 重新生成图片             |

## 图片构图原则

- **空白区域**：保持40-60%的空白空间，以增强视觉效果。
- **视觉焦点**：主要元素应居中或稍微偏左显示。
- **人物形象**：使用简化的剪影效果，避免使用真实人物图像。
- **标题**：使用用户提供的或文章中的原始标题，切勿自行创作。

## 扩展功能

通过`EXTEND.md`文件可以自定义更多配置选项。具体路径请参见**第0步**。

支持的功能包括：添加水印、指定默认尺寸和输出格式、启用快速模式、自定义色调方案以及设置语言。

配置项详细信息：[references/configpreferences-schema.md](references/configpreferences-schema.md)

## 参考资料

- 图片相关设置：[text.md](references/dimensions/text.md)、[mood.md](references/dimensions/mood.md)、[font.md](references/dimensions/font.md)
- 颜色方案：[references/palettes/](references/palettes/)
- 渲染方式：[references/renderings/](references/renderings/)
- 图片类型：[references/types.md](references/types.md)
- 自动选择功能：[references/auto-selection.md](references/auto-selection.md)
- 预设样式：[references/style-presets.md](references/style-presets.md)
- 兼容性说明：[references/compatibility.md](references/compatibility.md)
- 视觉元素相关设置：[references/visual-elements.md](references/visual-elements.md)
- 工作流程相关文档：[confirm-options.md](references/workflow/confirm-options.md)、[prompt-template.md](references/workflow/prompt-template.md)、[reference-images.md](references/workflow/reference-images.md)
- 配置文件：[preferences-schema.md](references/config/preferences-schema.md)、[first-time-setup.md](references/config/first-time-setup.md)、[watermark-guide.md](references/config/watermark-guide.md)