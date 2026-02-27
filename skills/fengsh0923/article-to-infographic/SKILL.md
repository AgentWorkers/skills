---
name: article-to-infographic
description: 将文章、博客帖子、报告或任何文本内容转换为视觉效果出众的、自包含的 HTML 信息图。适用于用户希望将文本转换为信息图、从书面内容创建可视化摘要、从 URL、文件或粘贴的文本中生成信息图的情况。支持多种信息图样式（时间线、统计数据、对比图、流程图、列表文章），并具有独特且非通用的设计风格。
---
# 将文章转换为信息图

将任何文章或文本内容转换为视觉上引人注目、自包含的HTML信息图。输出是一个包含内联CSS/JS的单一HTML文件——无需任何依赖项，可在任何浏览器中打开，并支持PDF导出。

## 核心理念

1. **内容优先**——在选择布局之前先分析文章内容。
2. **智能布局**——自动匹配信息图类型与内容类型。
3. **独特设计**——避免使用通用的AI设计风格，每个信息图都应具有定制感。
4. **零依赖**——单一HTML文件，包含内联CSS/JS。
5. **适合打印**——包含打印媒体查询，以便生成清晰的PDF文件。

---

## 工作流程概述

**严格的3步确认流程：**

```
Step 1: Outline Confirmation (BLOCKING)
   ↓ User must confirm
Step 2a: Layout Selection (BLOCKING)
   ↓ User must confirm
Step 2b: Style Selection (BLOCKING)
   ↓ User must confirm
Step 2c: Illustrations (BLOCKING)
   ↓ User must confirm
Step 3: Output Format (BLOCKING)
   ↓ User must confirm
Generation Phase (automatic)
```

**重要规则**：每个步骤都需要用户的明确确认才能继续进行。切勿批量确认。在当前步骤未得到确认之前，切勿进入下一步。

---

## 详细工作流程

1. 获取并分析文章内容
2. 提取关键信息并分类内容类型
3. **步骤1：展示大纲 → 获取明确确认**
4. **步骤2a：展示布局选项 → 获取明确确认**
5. **步骤2b：展示样式选项 → 获取明确确认**
6. **步骤2c：展示插图选项 → 获取明确确认**
7. **步骤3：展示输出格式选项 → 获取明确确认**
8. 生成HTML信息图（仅在所有确认完成后）
9. 如果在步骤3中选择了PNG格式，则进行导出
10. 提供最终输出

## 确认流程总结（供AI参考）

执行此功能时，请严格遵循以下顺序：

| 阶段 | 步骤 | 操作 | 需要用户确认 |
|-------|------|--------|---------------------------|
| 1 | 内容获取 | 获取文章URL/文件/文本 | ❌ 不需要 |
| 2 | 内容分析 | 提取信息，分类类型 | ❌ 不需要 |
| 2.5 | **步骤1** | 展示大纲表格 | ✅ **必须确认** |
| 3a | **步骤2a** | 展示布局选项 | ✅ **必须确认** |
| 3b | **步骤2b** | 展示样式选项 | ✅ **必须确认** |
| 3c | **步骤2c** | 展示插图选项 | ✅ **必须确认** |
| 4 | **步骤3** | 展示输出格式选项 | ✅ **必须确认** |
| 5 | 生成 | 创建HTML | ❌ 自动完成 |
| 6 | 提交 | 展示结果 | ❌ 自动完成 |
| 7 | PNG导出 | 如果在步骤3中选择了PNG格式 | ❌ 自动完成 |

**禁止的操作：**
- ❌ 绝不允许将步骤1和步骤2的确认合并
- ❌ 绝不允许将步骤2a、2b和2c合并为一个问题
- ❌ 绝不允许在未完成所有3个步骤的确认之前进行生成

---

## 第1阶段：内容获取

确定内容来源：

- **URL**——使用WebFetch获取文章内容
- **文件**——直接读取文件内容
- **粘贴的文本**——按原样使用

如果内容不明确或太短，请请求澄清。

---

## 第2阶段：内容分析

从文章中提取以下信息：

1. **标题和副标题**——主要主题和次要背景信息
2. **关键统计数据**——数字、百分比、数据点
3. **关键要点**——4-8个最重要的要点
4. **引文**——值得注意的陈述
5. **对比**——前后对比、优缺点、A与B的对比
6. **顺序步骤**——流程、时间线、按时间顺序的事件
7. **类别**——自然分组
8. **实体**——人物、组织、地点

根据内容类型选择最合适的信息图类型：

| 内容特征 | 信息图类型 |
|---|---|
| 日期、里程碑、按时间顺序的事件 | **时间线** |
| 数字、百分比、调查数据 | **统计仪表盘** |
| A与B的对比、优缺点 | **对比图** |
| 分步指南、教程 | **流程图** |
| 多个独立提示/事实 | **列表文章/卡片网格** |
| 混合类型的内容 | **杂志/编辑风格** |

---

## 第2.5阶段：步骤1 - 大纲确认（强制确认）

**⚠️ 重要提示：在进入第3阶段之前，必须获得用户的明确确认。**

内容分析完成后，以表格形式向用户展示结构化的大纲：

```
| Block | Content | Notes |
|---|---|---|
| Header | Title + subtitle | Top section |
| Hero Stats (3) | [stat1] / [stat2] / [stat3] | Key data highlights |
| ... | ... | ... |
```

**在用户明确确认之前，切勿继续。**

使用AskUserQuestion工具：
- 标题：“步骤1/3：大纲确认”
- 问题：“请查看上述大纲。确认后继续，或请求修改：”
- 选项：
  - “✅ 大纲确认 - 继续选择样式”
  - “📝 需要调整” – 用户指定修改内容（添加/删除/修改部分），然后重新确认
  - “🔄 简化为核心部分” – 自动修剪为核心部分，然后重新确认

**硬性规则**：如果用户选择调整，请更新大纲并返回此确认步骤。在用户选择“✅ 大纲确认”之前，切勿进入第3阶段。

---

## 第3阶段：步骤2 - 样式选择（强制确认）

**⚠️ 重要提示：在进入第4阶段之前，必须同时获得布局和样式的明确确认。**

此阶段需要**两次单独的确认**：

### 步骤2a：布局选择（强制确认）

使用AskUserQuestion工具：
- 标题：“步骤2a/3：布局选择”
- 问题：“根据您的文章，我推荐使用**[检测到的类型]**布局。确认您的选择：”
- 选项：
  - “✅ [检测到的类型] - 推荐”
  - “📊 统计仪表盘”
  - “📅 时间线”
  - “⚖️ 对比图”
  - “🔄 流程图”
  - “📝 列表文章/卡片网格”
  - “📖 杂志/编辑风格”

**在此处停止**。等待用户选择。此时不要显示样式选项。

### 步骤2b：样式选择（强制确认）

仅在布局确认后，再展示样式选项：

使用AskUserQuestion工具：
- 标题：“步骤2b/3：视觉样式选择”
- 问题：“您希望[已确认的布局]使用哪种视觉样式？”
- 选项（展示4-5种最相关的样式）：

  **标准样式：**
  - “🎨 突出鲜明** – 高对比度、饱和色彩、强烈的视觉效果
  - “🌿 清洁简约** – 空白较多、色彩柔和、优雅的排版
  - “🌃 深暗科技** – 深色背景、霓虹色调、现代感
  - “📰 温暖编辑风格** – 杂志风格、温暖色调、衬线字体

  **高级样式：**
  - “🚀 科幻控制台** – 未来派终端、粒子效果、霓虹光效
  - “💎 高端杂志** – 豪华编辑风格、大号衬线字体
  - “🔮 玻璃质感** – 霜璃效果、动态极光效果

**在此处停止**。等待用户选择。

### 步骤2c：插图（可选，但需询问）

使用AskUserQuestion工具：
- 标题：“步骤2c/3：插图（可选）”
- 问题：“您希望在[已确认的样式]信息图中添加插图吗？”
- 选项：
  - “🚫 不添加插图 - 仅显示文本和数据”
  - “🔹 装饰性图标 - 在标题旁边显示小SVG图标”
  - “👤 角色插图 - 使用开源库中的完整SVG角色”

**只有在所有2a→2b→2c步骤都得到确认后，才能进入第4阶段。**

有关每种样式的详细颜色调色板和字体搭配，请参阅[references/style-presets.md](references/style-presets.md)。

---

## 第3阶段：步骤3 - 输出格式确认（强制确认）

**⚠️ 重要提示：在生成任何内容之前，必须获得用户对输出格式的明确确认。**

使用AskUserQuestion工具：
- 标题：“步骤3/3：输出格式”
- 问题：“您希望如何接收[已确认的样式]信息图？”
- 选项：
  - “📄 仅HTML文件 - 在浏览器中打开”
  - “🖼️ HTML + PNG - 包含高分辨率图片导出”
  - “📦 两种格式 - 同时提供两种文件”

**仅在输出格式得到确认后，才能进入第5阶段（生成）。**

---

## 第4阶段：生成信息图

### HTML架构

生成一个自包含的单一HTML文件：

```html
<!DOCTYPE html>
<html lang="[content language]">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Infographic Title]</title>
    <link rel="stylesheet" href="[Google Fonts / Fontshare URL]">
    <style>
        :root {
            --bg-primary: ...; --bg-secondary: ...;
            --text-primary: ...; --text-secondary: ...;
            --accent-1: ...; --accent-2: ...;
            --font-display: ...; --font-body: ...;
        }
        /* Layout, components, animations */
        @media print { /* linearize, remove animations */ }
        @media (prefers-reduced-motion: reduce) { /* disable animations */ }
    </style>
</head>
<body>
    <article class="infographic">
        <header class="infographic-header">...</header>
        <main class="infographic-body">...</main>
        <footer class="infographic-footer">...</footer>
    </article>
    <script>/* Intersection Observer animations, counter effects */</script>
</body>
</html>
```

### 设计规则

**排版：**
- 使用独特的Google字体或Fontshare字体——严禁使用Inter、Roboto、Arial或系统字体
- 标题使用显眼字体，正文使用简洁的字体
- 使用`clamp()`实现响应式大小调整

**颜色：**
- 使用CSS自定义属性设置整个调色板
- 最多使用3-4种颜色：一种主导色、一种强调色、一两种中性色
- 保证WCAG AA级别的对比度以便阅读

**布局：**
- 使用CSS网格进行整体布局，使用Flexbox布局组件
- 最大宽度为1200px，居中显示
- **紧凑间距**：各部分之间的间距为2-3rem，不要超过5rem。信息图应显得紧凑且信息丰富，不要拉伸。标题内边距：2-2.5rem。部分内边距：2-3rem。网格间距：2-2.5rem。
- 响应式设计：在移动设备上显示为单列，在桌面设备上显示为多列

**数据可视化：**
- 使用纯CSS绘制简单图表（条形图使用宽度百分比，饼图使用渐变效果）
- 使用内联SVG绘制复杂形状
- 使用Intersection Observer实现数字的动态效果
- 必须清晰标注数据

**动画：**
- 使用Intersection Observer触发`.visible`类
- 使用动画延迟 stagger子元素
- 使用淡入淡出效果和垂直平移效果
- 必须设置`prefers-reduced-motion`媒体查询

**打印：**
- 使用`@media print`规则：线性化布局，移除动画，确保可读性
- 在各部分之间添加适当的页眉分隔

### 布局样式**

**时间线：**
- 垂直中心线，左右交替显示条目
- 日期标签居中显示，内容卡片偏移
- 在移动设备上显示为单列

**统计仪表盘：**
- 顶部显示主要统计数据（大数字+背景信息）
- 使用网格布局显示统计卡片（2-3列）
- 根据需要使用CSS条形图/饼图
- 滚动时显示计数器动画

**对比图：**
- 并排显示两侧的列，中间有分隔线
- 行匹配，两侧使用不同颜色编码
- 在移动设备上显示为垂直堆叠

**流程图：**
- 带有连接线的编号步骤
- 每个步骤都配有图标+标题+描述
- 显示进度指示器

**列表文章/卡片网格：**
- 在桌面设备上使用响应式网格显示编号/图标卡片（2-3列），在移动设备上显示为单列
- 每张卡片包含图标/数字+标题+描述
- 卡片可悬停显示效果

**杂志/编辑风格：**
- 混合使用全宽卡片、卡片网格、引用、统计亮点
- 交替使用密集和宽松的布局
- 强烈的排版层次结构

**禁止的布局样式：**
- 白色背景上的紫色渐变
- 无视觉特色的通用卡片布局
- 过度使用Font Awesome或表情符号作为装饰
- 单调、无生气的色彩方案
- 过多的文字（违背信息图的目的）
- 无标签的图表
- 刻板固定的布局

---

## 第6阶段：提交

**所有3个确认步骤已完成。正在生成最终输出...**

编写HTML文件并展示总结：

```
✅ Infographic generated!

📄 File: [filename].html
📐 Layout: [confirmed layout]
🎨 Style: [confirmed style]
🖼️ Illustrations: [confirmed option]
📦 Output: [confirmed format]
📊 Sections: [count]

Open in browser to view. Ctrl+P / Cmd+P to save as PDF.
```

**生成完成。无需进一步确认。**

---

## 特殊情况

**短文章（<200字）：** 使用紧凑的单一部分，以卡片形式展示3-5个关键点。

**长文章（>3000字）：** 将内容总结为最多6-10个关键部分。优先展示数据和要点。

**无统计数据：** 重点展示引文、流程或列表文章。使用图标代替图表。

**技术/代码密集型内容：** 使用代码片段、带有CSS图形的架构图、概念性流程图。

**非英文内容：** 在`<html>`标签上正确设置`lang`属性。为CJK、RTL等内容使用合适的字体。

---

## 第7阶段：PNG导出（如果在步骤3中选择了PNG格式）

生成HTML文件后，如果用户在步骤3中选择了PNG格式，请进行导出：

### 方法A：浏览器工具（在Claude Code / HappyCapy中推荐）

如果可以使用`browser` CLI工具：

1. 启动一个本地HTTP服务器来服务HTML文件
2. 在浏览器中打开该页面
3. 强制所有`.reveal`元素显示（跳过滚动动画）
4. 强制所有条形图填充和计数器显示最终值
5. 截取全页截图
6. 关闭浏览器

```javascript
// JS to inject before screenshot:
document.querySelectorAll('.reveal').forEach(el => {
    el.classList.add('visible');
    el.style.opacity = '1';
    el.style.transform = 'none';
});
document.querySelectorAll('.ba-fill, .bar-fill').forEach(bar => {
    const w = bar.dataset.width;
    if (w) bar.style.width = w + '%';
});
document.querySelectorAll('[data-counter]').forEach(el => {
    const target = el.dataset.counter;
    const suffix = el.dataset.suffix || '';
    el.textContent = parseInt(target).toLocaleString() + suffix;
});
```

### 方法B：Playwright脚本（独立环境）

运行捆绑的脚本：

```bash
python3 scripts/html_to_png.py infographic.html output.png --width 1200 --scale 2
```

该脚本使用Playwright和无头Chromium。如果需要，它会自动安装依赖项。

参数：
- `--width`：视口宽度（单位：px，默认为1200）
- `--scale`：高 DPI缩放因子（默认为2，生成2400px宽的图片）

### 何时导出PNG

在提交HTML文件后，询问用户：

- 标题：“需要PNG图片导出吗？”
- 选项：
  - “是的，导出PNG” – 运行导出操作
  - “仅需要HTML文件” – 跳过此步骤

---

## OpenClaw / 非交互式使用

在无法进行交互式问答的环境中（例如OpenClaw、仅通过API的环境）使用时，该功能将以**参数化模式**运行，此时所有选项都必须提前指定。

**⚠️ 重要提示：**在参数化模式下，必须一次性提供所有确认信息，因为系统无法再次提问。

### 参数化调用（一次性输入）

用户必须在一个提示中指定所有3个确认步骤：

```
Generate an infographic from [article source].

STEP 1 - OUTLINE:
[Provide your preferred outline structure, or "use auto-generated outline"]

STEP 2 - STYLE:
Layout: [timeline|statistics|comparison|process|listicle|magazine]
Style: [bold-vibrant|clean-minimal|dark-techy|warm-editorial|scifi-hud|premium-magazine|glassmorphism]
Illustrations: [none|icons|characters]

STEP 3 - OUTPUT:
Format: [html|png|both]
```

**示例完整提示：**
```
Generate an infographic from https://example.com/article.

STEP 1: Use auto-generated outline

STEP 2: 
Layout: timeline
Style: dark-techy
Illustrations: icons

STEP 3:
Format: both
```

### 参数参考

**样式选项：**
- `bold-vibrant` – 高对比度、饱和色彩
- `clean-minimal` – 空白较多、色彩柔和、衬线字体
- `dark-techy` – 深色背景、霓虹色调
- `warm-editorial` – 杂志风格、温暖色调
- `scifi-hud` – 未来派终端、粒子效果、霓虹光效（高级选项）
- `premium-magazine` – 豪华编辑风格、大号衬线字体、奶油色/炭黑色/亮红色（高级选项）
- `glassmorphism` – 玻璃质感、极光效果、苹果风格（高级选项）

**布局选项：**
- `timeline` – 按时间顺序的事件
- `statistics` – 数据仪表盘
- `comparison` – 并列对比
- `process` – 分步流程
- `listicle` – 卡片网格
- `magazine` – 混合编辑风格（复杂文章的默认选项）
- `auto` – 根据内容分析自动选择布局

**大纲调整**（自然语言）：
- “删除[块名称]”
- “添加[块描述]”
- “用[新内容]替换[块]”
- “简化” / “扩展”

**导出选项：**
- `html` – 仅HTML文件（默认）
- `png` – HTML + PNG文件导出
- `both` – 同时输出两种格式

### 回退方案

如果未指定样式/布局，且AskUserQuestion不可用，则使用以下默认设置：
- **布局**：`auto`（根据内容自动选择）
- **样式**：技术内容使用`dark-techy`，叙事内容使用`warm-editorial`，数据密集型内容使用`bold-vibrant`
- **导出**：`html`文件

### 中国地区的字体CDN设置

在GFW（防火墙）后部署时，替换Google Fonts CDN：

```html
<!-- Instead of: -->
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">

<!-- Use mirror: -->
<link href="https://fonts.loli.net/css2?family=..." rel="stylesheet">
<!-- Or use: -->
<link href="https://fonts.font.im/css2?family=..." rel="stylesheet">
```

或者，对于中文内容较多的情况，使用系统字体作为替代方案：

```css
--font-heading: 'Noto Serif SC', 'STSong', 'SimSun', serif;
--font-body: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
```