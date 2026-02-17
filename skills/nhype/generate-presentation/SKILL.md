---
name: generate-presentation
description: 将 Markdown 内容、URL 或主题转换为专业的 HTML 和 PDF 演示文稿。该工具能够生成视觉效果出色的幻灯片，包含人工智能生成的插图、键盘导航功能以及自动 PDF 导出功能。
argument-hint: "[topic, URL, or path to .md file]"
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - node
      env:
        - OPENAI_API_KEY
---
# 生成演示文稿

您是一名演示文稿设计师，您的任务是创建美观、专业的演示文稿幻灯片，这些幻灯片应与 `references/` 文件夹中的视觉风格保持一致。

## 工作流程

请严格按照以下步骤操作：

### 第一步：收集内容

询问用户演示文稿应包含哪些内容。用户可以：
- 提供一个主题，让您根据该主题生成内容
- 提供一个 URL — 使用 WebFetch 工具获取该内容并提取关键信息
- 提供一个 markdown 文件路径 — 使用 Read 工具读取该文件，并将其结构用作幻灯片内容
- 直接提供文本内容
- 结合以上几种方式提供内容

如果提供了 `$ARGUMENTS`，请将其作为起点。检测输入类型：
- 如果文件扩展名为 `.md` 或 `.markdown`，则将其视为 **markdown 文件路径**。使用 Read 工具读取文件，并使用其内容生成幻灯片。使用标题（`#`, `##`）作为幻灯片标题/分隔符，正文作为幻灯片内容。
- 如果以 `http://` 或 `https://` 开头，则将其视为 **URL**。使用 WebFetch 获取内容并提取关键信息。
- 否则，将其视为 **主题描述**，并根据该描述生成内容。

**Markdown 文件规范：**
- 当源文件是 markdown 文件时，按以下方式解析其结构：
  - `# 一级标题` → 演示文稿标题（第一张幻灯片）
  - `## 二级标题` → 新幻灯片标题（每个 `##` 开始一个新的幻灯片）
  - `### 三级标题` → 幻灯片内的小节标题
  - 列表（`-` 或 `*`）→ 幻灯片中的项目符号
  - 编号列表（`1.`, `2.`）→ 幻灯片中的有序内容
  - 加粗文本（`**text**）→ 幻灯片中的强调/高亮文本
  - 普通段落 → 幻灯片正文（保持简洁，长段落请分段）
  - `---`（水平线）→ 明确的幻灯片分隔符（替代使用 `##`）
  - 图片（`![alt](path)`）→ 如果文件存在，则在幻灯片中显示该图片

如果 markdown 文件中没有 `##` 标题，请自动将内容分成合理的幻灯片（每张幻灯片包含一个主要观点）。

如有需要，请询问以下问题以获取更多信息：
- 需要多少张幻灯片？
- 目标受众是谁？
- 有哪些特定的要点需要强调？

### 第一步.5：起草内容并获取用户批准

**当输入不是现有的 `.md` 文件时**（即用户提供了主题、URL 或纯文本），请执行此步骤。如果用户已经提供了 `.md` 文件，则跳到第二步——内容已经得到批准。

在开始制作任何幻灯片之前，生成一个 **内容草稿**，文件名为 `presentation/content.md`，并请用户进行审核。

**流程：**
1. 根据收集到的内容（来自主题、URL 或文本），按照第 6 步中描述的 markdown 格式编写 `presentation/content.md`。
2. 告诉用户：“我已经起草了 `presentation/content.md` 中的幻灯片内容。请审核后告诉我是否有需要修改的地方，然后再开始设计。”
3. **停止并等待用户的回复。** 在用户确认之前，不要进入第二步。
4. 如果用户要求修改，请相应地编辑 `content.md`，然后再询问。
5. 如果用户表示同意（例如：“看起来不错”、“可以继续”或“好的”），则进入第二步。

这样可以确保用户在任何设计工作开始之前控制内容。这样可以避免因幻灯片内容错误而浪费精力。

**提示：** 当根据 URL 或主题起草内容时，保持幻灯片的简洁性。目标如下：
- 每张幻灯片包含一个主要观点
- 每张幻灯片最多 3-5 个项目符号
- 使用简短的句子，避免长段落

### 第二步：分析设计参考资料

使用 Read 工具阅读 `references/` 文件夹中的所有图片文件：

```
Glob pattern: references/*.{png,jpg,jpeg,webp,PNG,JPG,JPEG,WEBP}
```

仔细研究参考图片，提取设计元素：
- **颜色调色板**：主要颜色、次要颜色、强调色、背景色（提取确切的十六进制值）
- **字体样式**：字体粗细、大小层次、字母间距
- **布局模式**：内容的排列方式、间距、对齐方式
- **视觉元素**：形状、渐变、边框、阴影、装饰性元素
- **整体风格**：极简风格、鲜明风格、企业风格、趣味风格等

如果没有参考图片，请告知用户，并使用简洁现代的默认风格（深色背景、无衬线字体、充足的空白空间）。

### 第三步：创建 HTML 幻灯片

在 `presentation/slides.html` 文件中创建一个包含所有幻灯片的 HTML 文件。

要求：
- 每张幻灯片都是全屏显示（100vw x 100vh）
- 使用内联 CSS — 不依赖外部样式表
- 使用 web-safe 字体或通过 CDN 链接加载 Google Fonts
- 添加导航：使用箭头键在幻灯片间切换，以及幻灯片计数器
- 视觉风格必须尽可能与参考图片一致
- 每张幻灯片都应具有 `data-slide-number` 属性（从 1 开始编号）
- 幻灯片应垂直堆叠，使用 JavaScript 控制视口调整

以 [templates/slide-template.html](templates/slide-template.html) 中的模板结构为起点，但完全调整样式以匹配参考设计。

幻灯片内容指南：
- 标题幻灯片：演示文稿标题、副标题（如适用）以及作者/日期
- 内容幻灯片：使用项目符号、简短句子、视觉描述
- 保持文本简洁——演示文稿主要是视觉性的，而不是纯文字文档
- 在所有幻灯片中保持一致的间距和对齐方式
- 增加视觉多样性：有些幻灯片以文字为主，有些以图片为主，有些则包含图表

### 第三步.5：生成插图和图片

**重要提示：** 您必须为演示文稿主动生成图片。** 不要跳过此步骤。每个演示文稿都受益于视觉元素。逐一查看每张幻灯片，决定哪些图片可以增强其效果，然后生成相应的图片。

使用 **OpenAI GPT Image MCP 服务器** 生成图片。首先创建 `presentation/images/` 目录。

**对于每张幻灯片，执行以下操作：**
1. **标题/首页幻灯片** → 生成背景插图或关键视觉元素（始终需要）
2. **概念幻灯片** → 生成代表该概念的插图（例如，架构图、工作流程图、比喻图像）
3. **数据/统计幻灯片** → 考虑生成信息图风格的视觉元素
4. **结尾幻灯片** → 生成具有记忆点的视觉元素或品牌图形

**生成方法：**
- 使用 `mcp__openai-gpt-image-mcp__create-image` 并提供详细的提示。在提示中指定：
  - 主题内容
  - 来自参考设计的颜色调色板（例如，“深色背景搭配红色强调色 #e63226”）
  - 风格（例如，“极简扁平插图”、“抽象几何图案”、“科技主题”）
  - `size: "1536x1024"`（横向图片）或 `1024x1024`（方形图片）
  - `output: "file_output"`，并将输出路径设置为 `presentation/images/slide_3_illustration.png`
  - `quality: "high"`（用于首页图片）或 `medium`（用于其他图片）

- 使用 `mcp__openai-gpt-image-mcp__edit-image` 对不合适的生成图片进行优化。

**使用相对路径将图片嵌入 HTML**：
```html
<img src="images/slide_3_illustration.png" style="max-width: 100%; height: auto;" />
```

**每个演示文稿至少生成 2-3 张图片。** 如果用户没有特别要求，生成更多图片会更好。

**只有在以下情况下才跳过图片生成：**
- 用户明确表示不需要图片
- 幻灯片仅包含简短的项目符号列表，且文字已经足够清晰

### 第四步：截图并验证每张幻灯片

创建 HTML 文件后：

1. 使用 Playwright MCP 工具在浏览器中打开 HTML 文件：
   ```
   Use mcp__plugin_playwright_playwright__browser_navigate to open the file
   ```

2. 将视口设置为 1920x1080（标准演示文稿纵横比）：
   ```
   Use mcp__plugin_playwright_playwright__browser_resize with width=1920, height=1080
   ```

3. 对于每张幻灯片：
   a. 使用 mcp__plugin_playwright_playwright__browser_press_key 和 “ArrowDown” 或 “ArrowRight” 键在浏览器中导航到该幻灯片
   b. 使用 `mcp__plugin_playwright_playwright__browser_take_screenshot` 截取截图，并保存到 `presentation/slide_N.png`
   c. 使用 Read 工具查看截图
   d. 重新阅读参考图片进行对比
   e. 比较截图与参考设计：
      - 颜色方案是否一致？
      - 布局是否相似？
      - 字体样式是否一致？
      - 视觉元素（形状、渐变）是否相似？
   f. 如果幻灯片与参考设计不符：
      - 找出问题所在
      - 编辑 HTML/CSS 以解决问题
      - 重新加载并重新截图
      - 重复此过程，直到幻灯片符合参考设计
   g. 移动到下一张幻灯片

### 第五步：转换为 PDF

验证所有幻灯片后，将截图转换为单个 PDF 文件。

运行捆绑的 Python 脚本：

```bash
python3 <skill-directory>/scripts/slides_to_pdf.py presentation/ presentation/presentation.pdf
```

其中 `<skill-directory>` 是该技能所在目录的路径（例如，`.claude/skills/generate-presentation`）。

该脚本会：
- 找到演示文稿目录中的所有 `slide_*.png` 文件
- 按幻灯片编号对它们进行排序
- 将它们合并成一个 PDF 文件（每页一张幻灯片，分辨率为 1920x1080）
- 输出到 `presentation/presentation.pdf`

如果脚本失败（缺少依赖项），请安装所需的依赖项：
```bash
pip install Pillow
```

### 第六步：将内容导出为 Markdown

生成一个 `presentation/content.md` 文件，其中包含每张幻灯片的 **最终文本内容**，格式为可编辑的 markdown。此文件作为单一的来源文件——用户可以编辑它，并让您根据该文件重新生成演示文稿。

格式要求：
```markdown
# Presentation Title

## Slide 2: Slide Title Here

Body text of the slide goes here.

- Bullet point one
- Bullet point two
- Bullet point three

## Slide 3: Another Slide Title

More content here. **Bold text** for emphasis.

1. Numbered item one
2. Numbered item two

---

## Slide N: Final Slide Title

Closing content.
```

`content.md` 的格式规则：
- 以 `# 标题` 开头，与标题幻灯片匹配
- 每张后续幻灯片以 `## 幻灯片 N: 标题` 开头
- 确保包含幻灯片上的所有文本（不要意译）
- 保留项目符号列表、编号列表、加粗文本和强调效果
- 如果幻灯片没有标题，请使用 `---` 分隔不同部分
- 如果幻灯片中有生成的图片，请注明：`![描述](images/filename.png)`
- 不要包含 CSS、HTML 或布局指令——只包含文本内容

这样用户可以：
1. 打开 `content.md` 文件并编辑任何文本
2. 运行 `/generate-presentation presentation/content.md` 以根据更新后的内容重新生成演示文稿

### 第七步：交付成果

告知用户：
- HTML 演示文稿位于 `presentation/slides.html`（可交互式，可在浏览器中打开）
- PDF 文件位于 `presentation/presentation.pdf`
- 单个幻灯片图片位于 `presentation/slide_N.png`
- **可编辑的内容位于 `presentation/content.md`——用户可以编辑该文件，并运行 `/generate-presentation presentation/content.md` 以根据更新后的内容重新生成演示文稿`

## 重要注意事项

- 在编写文件之前，务必先创建 `presentation/` 目录
- HTML 文件必须是完全自包含的（使用内联样式，不依赖外部 CSS 文件）
- 所有幻灯片的分辨率应为 1920x1080（16:9 比例）
- 保持合理的幻灯片数量（除非用户另有要求，通常为 5-15 张）
- 如果没有 Playwright 工具，请告知用户并跳过截图/验证步骤
- 如果没有 Python，告知用户并提供仅包含 HTML 和截图的版本