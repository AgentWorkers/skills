---
name: pptx
description: "每当涉及到.pptx文件时（无论是作为输入、输出，还是两者兼有），都可以使用此技能。具体应用场景包括：创建幻灯片集、演示文稿；从.pptx文件中读取、解析或提取文本（即使提取的内容将用于其他地方，例如电子邮件或总结中）；编辑、修改或更新现有的演示文稿；合并或拆分幻灯片文件；处理模板、布局、演讲者备注或注释等。只要用户提到“deck”、“slides”、“presentation”或引用.pptx文件名，无论他们之后打算如何使用这些内容，都应触发此技能。如果需要打开、创建或修改.pptx文件，也请使用此技能。"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX 技能

## 快速参考

| 任务 | 指导 |
|------|-------|
| 阅读/分析内容 | `python -m markitdown presentation.pptx` |
| 从模板编辑或创建新幻灯片 | 阅读 [editing.md](editing.md) |
| 从头开始创建新幻灯片 | 阅读 [pptxgenjs.md](pptxgenjs.md) |

---

## 阅读内容

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## 编辑工作流程

**请阅读 [editing.md](editing.md) 以获取详细信息。**

1. 使用 `thumbnail.py` 分析模板结构。
2. 解压文件 → 操作幻灯片内容 → 编辑内容 → 清理文件 → 重新打包文件。

---

## 从头开始创建新幻灯片

**请阅读 [pptxgenjs.md](pptxgenjs.md) 以获取详细信息。**

当没有模板或参考幻灯片时，可以使用此方法创建新幻灯片。

---

## 设计建议

**不要制作枯燥的幻灯片。** 纯白的背景上加上简单的文字列表不会给人留下深刻印象。为每个幻灯片考虑以下设计元素：

### 开始前

- **选择鲜明且与主题相符的配色方案**：配色方案应紧密围绕当前主题设计。如果将配色方案应用于完全不同的幻灯片中仍然适用，那么说明你的选择还不够具体。
- **突出重点颜色**：应有一种颜色占据主导地位（占视觉效果的 60-70%），再搭配 1-2 种辅助色调和 1 种强调色。切勿让所有颜色的视觉权重相同。
- **明暗对比**：标题和结论页使用深色背景，内容页使用浅色背景（采用“三明治”式布局）。或者全程使用深色以营造高级感。
- **坚持使用统一的视觉元素**：选择一种独特的视觉元素并在所有幻灯片中重复使用——例如圆形图像边框、彩色圆圈中的图标、单边粗边框等。

### 配色方案

选择与主题相匹配的颜色——不要默认使用蓝色。以下是一些参考配色方案：

| 主题 | 主色调 | 辅助色调 | 强调色 |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761`（深蓝色） | `CADCFC`（冰蓝色） | `FFFFFF`（白色） |
| **Forest & Moss** | `2C5F2D`（森林绿） | `97BC62`（苔藓绿） | `F5F5F5`（米色） |
| **Coral Energy** | `F96167`（珊瑚色） | `F9E795`（金色） | `2F3C7E`（深蓝色） |
| **Warm Terracotta** | `B85042`（赤褐色） | `E7E8D1`（沙色） | `A7BEAE`（鼠尾草色） |
| **Ocean Gradient** | `065A82`（深蓝色） | `1C7293`（海蓝色） | `21295C`（午夜蓝） |
| **Charcoal Minimal** | `36454F`（炭灰色） | `F2F2F2`（米白色） | `212121`（黑色） |
| **Teal Trust** | `028090`（海蓝色） | `00A896`（海泡沫色） | `02C39A`（薄荷色） |
| **Berry & Cream** | `6D2E46`（浆果色） | `A26769`（粉玫瑰色） | `ECE2D0`（米色） |
| **Sage Calm** | `84B59F`（鼠尾草色） | `69A297`（桉树绿） | `50808E`（板岩色） |
| **Cherry Bold** | `990011`（樱桃红） | `FCF6F5`（米白色） | `2F3C7E`（深蓝色） |

### 每个幻灯片的元素设计

**每个幻灯片都需要包含视觉元素**——图片、图表、图标或形状。只有文字的幻灯片很容易被忽略。

**布局选项：**
- 两栏布局（文字在左侧，图片在右侧）
- 图标 + 文字组合（图标放在彩色圆圈中，上方是加粗的标题，下方是描述）
- 2x2 或 2x3 的网格布局（一侧放置图片，另一侧放置内容块）
- 半透明图片（覆盖整个左侧或右侧，内容位于图片上方）

**数据展示方式：**
- 大字号的数据标注（数字 60-72pt，下方附有小标签）
- 对比柱状图（如前后对比、优缺点对比、并列选项）
- 时间线或流程图（编号步骤、带箭头）

**视觉细节处理：**
- 在章节标题旁边使用小彩色圆圈中的图标
- 用斜体字显示关键数据或标语

### 字体设计

**选择有特色的字体组合**——不要默认使用 Arial。为标题选择有特色的字体，并与正文字体搭配使用。

| 标题字体 | 正文字体 |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

| 元素 | 字体大小 |
|---------|------|
| 幻灯片标题 | 36-44pt（加粗） |
| 章节标题 | 20-24pt（加粗） |
| 正文文字 | 14-16pt |
| 图片说明 | 10-12pt（较淡的字体） |

### 间距设置

- 最小边距为 0.5 英寸
- 内容块之间保持 0.3-0.5 英寸的间距
- 适当留白，不要让页面过于拥挤

### 避免常见错误

- **不要在多个幻灯片中重复相同的布局**——尝试变化列的排列方式、图标的样式和数据标注的位置
- **不要将正文文字居中显示**——段落和列表应左对齐；只有标题可以居中
- **不要忽视字体对比度**——标题字体至少需要 36pt 以上才能与正文区分开来
- **不要默认使用蓝色**——选择与主题相符的颜色
- **不要随意调整间距**——统一使用 0.3 英寸或 0.5 英寸的间距
- **不要只对某个幻灯片进行设计，而忽略其他幻灯片**——要么全面统一设计，要么保持整体简洁
- **不要制作只有文字的幻灯片**——添加图片、图标、图表等视觉元素；避免简单的标题加文字列表
- **不要忘记设置文本框的边距**——在对齐文本或形状时，为文本框设置 `margin: 0`，或调整形状的位置以增加间距
- **不要使用对比度低的元素**——图标和文字需要与背景有明显的对比；避免在浅色背景上使用浅色文字，或在深色背景上使用深色文字
- **切勿在标题下方使用强调线**——这是 AI 生成的幻灯片的常见缺陷；使用空白区域或背景色代替

---

## 质量检查（QA）

**假设存在问题。你的任务是发现这些问题。**

初次生成的幻灯片几乎总是有错误的。将质量检查视为一次漏洞排查过程，而不仅仅是确认步骤。如果初次检查没有发现问题，可能是因为你没有仔细检查。

### 内容质量检查

```bash
python -m markitdown output.pptx
```

检查是否有内容缺失、拼写错误或顺序错误。

**使用模板时，检查是否有残留的占位符文本：**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

如果 `grep` 命令返回结果，请在宣布成功之前修复这些问题。

### 视觉质量检查

**⚠️ 即使只有 2-3 个幻灯片，也要使用辅助检查工具**——你可能会因为熟悉代码而忽略实际存在的问题。辅助检查工具能提供新的视角。

将幻灯片转换为图片（参见 [转换为图片](#converting-to-images)），然后使用以下命令进行进一步检查：

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### 验证流程

1. 生成幻灯片 → 转换为图片 → 检查
2. **列出发现的问题**（如果没有问题，请再次仔细检查）
3. 修复问题
4. **重新验证受影响的幻灯片**——一次修复可能会引发新的问题
5. 重复此过程，直到没有新的问题出现

**在完成至少一个修复和验证循环之前，不要宣布任务完成。**

---

## 转换为图片

将幻灯片转换为单独的图片文件以便进行视觉检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

这样会生成 `slide-01.jpg`、`slide-02.jpg` 等文件。

要修复特定幻灯片后重新生成图片，请使用以下命令：

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## 所需依赖库

- `pip install "markitdown[pptx]"` — 用于提取文本内容
- `pip install Pillow` — 用于生成幻灯片缩略图
- `npm install -g pptxgenjs` — 用于从头开始创建幻灯片
- LibreOffice (`soffice`) — 用于 PDF 转换（在沙箱环境中自动配置，通过 `scripts/office/soffice.py` 实现）
- Poppler (`pdftoppm`) — 用于将 PDF 文件转换为图片