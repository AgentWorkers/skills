---
name: flow-visual-explainer
description: 生成美观、自包含的 HTML 页面，用于直观地展示系统、代码、计划和数据。当用户请求图表、架构概览、差异对比、计划审查、项目总结、对比表、幻灯片集或任何技术概念的可视化解释时，可以使用该功能。当需要渲染复杂的表格（4 行以上或 3 列以上）时，系统会自动转换为 HTML 格式（而非 ASCII 格式）。支持使用 `--slides` 标志来生成高质量杂志风格的幻灯片集。输出文件保存在 `~/clawd/output/diagrams/` 目录中，并可在浏览器中直接打开。
homepage: https://github.com/nicobailon/visual-explainer
metadata:
  openclaw:
    emoji: "🎨"
    version: "1.0.0"
    author: "nicobailon (adapted for OpenClaw by Flo)"
---
# 流程可视化解释器

该工具能够生成自包含的 HTML 文件，用于展示技术图表、可视化内容以及数据表格。请始终在浏览器中打开生成的文件。**在启用此功能时，切勿使用 ASCII 艺术风格来表示内容。**

**输出目录：** `~/clawd/output/diagrams/`  
**在浏览器中打开文件：** `exec: open ~/clawd/output/diagrams/filename.html`

---

## 触发条件

在以下情况下使用此功能：
- 用户请求“绘制”、“可视化”或“以图形方式解释”某些内容  
- 用户需要查看架构概览、系统图、流程图、序列图或 ER 图  
- 用户要求进行差异审查、计划评估、项目总结或事实核查  
- 用户需要制作幻灯片或演示文稿  
- 当需要渲染包含 **4 行以上或 3 列以上** 的表格时（自动转换为 HTML）  
- 用户需要根据 M 个标准比较 N 个对象（始终使用表格形式，因此也生成 HTML）

**无需等待用户明确请求 HTML 文件**。如果输出内容为复杂的表格或图表，请直接以可视化形式呈现。

---

## 命令（基于自然语言的触发）

| 用户请求 | 生成内容 |
|---|---|
| “绘制 X 的图表” / “可视化 X” | `generate-web-diagram` — 生成任意主题的 HTML 图表 |
| “X 的可视化计划” / “实施计划” | `generate-visual-plan` — 生成可视化特性/构建计划 |
| “X 的幻灯片” | `generate-slides` — 生成高质量的幻灯片 |
| “审查这个差异” | `diff-review` — 生成包含架构对比的可视化差异报告 |
| “审查这个计划” | `plan-review` — 生成包含代码库对比和风险评估的可视化报告 |
| “项目总结” | `project-recap` — 生成用于快速了解项目情况的可视化概览 |
| “核实这份文档的准确性” | `fact-check` — 核对文档内容与实际代码的一致性 |
| “分享这个内容” | `share` — 将生成的 HTML 文件部署到 Vercel 并返回可访问的 URL |

**任何能够生成可滚动页面的命令都支持 `--slides` 标志：**  
```
"review this diff as slides"
→ generates slide deck version instead of scrollable page
```

---

## 工作流程

### 第一步：先思考（30 秒）

在编写 HTML 代码之前，先确定方向。回答以下三个问题：

- **目标受众是谁？** 开发者？项目经理？投资者？根据受众选择内容的密度和复杂性。
- **内容类型是什么？**
  - 架构（文本较多的卡片） → 使用 CSS Grid 布局
  - 架构（拓扑结构重要） → 使用 Mermaid 绘图工具
  - 流程图/管道图/状态机 → 使用 Mermaid 绘图工具
  - 序列图 → 使用 Mermaid 绘图工具
  - ER 图/数据模型 → 使用 Mermaid 绘图工具
  - 数据表格/对比表/矩阵 → 使用 HTML `<table>` 格式
  - 仪表盘/指标展示 → 使用 Chart.js 图表库
  - 幻灯片 → 使用滚动式布局

- **视觉风格是什么？** 选择一种风格并坚持使用。可以参考 `references/css-patterns.md` 文档中的样式示例。

**特定风格的约束（这些风格较难通用化）：**
  - **蓝图风格**：技术绘图风格，背景使用点状/网格图案，颜色方案为 Slate/蓝色调，标签使用等宽字体
  - **编辑风格**：标题使用衬线字体（如 Instrument Serif、Crimson Pro），留有足够的空白空间，颜色以柔和的土色调或海军蓝加金色为主
  - **纸质/墨水风格**：背景颜色为温暖的奶油色（#faf7f5），点缀以赤褐色或深绿色，风格较为随意
  - **单色终端风格**：使用绿色/琥珀色在接近黑色的背景下显示内容，使用等宽字体，可选 CRT 风格的显示效果

**灵活的风格（需有意识地使用）：**
  - **IDE 风格**：选择特定的主题方案（如 Dracula、Nord、Catppuccin Mocha、Gruvbox、One Dark），并使用相应的颜色方案
  - **数据密集型风格**：使用较小的字体、紧密的排版、尽可能多的信息展示，颜色较为柔和

**绝对禁止的风格：**
  - 鲜艳的色彩搭配（如青色+品红色+紫色）——这种风格过于花哨
  - 渐变背景（粉色/紫色/青色的色块组合）——过于通用化
  - 使用 Inter 字体搭配紫色/靛蓝色以及渐变效果的文字

**每次生成内容时都可以尝试不同的风格**。如果上一次使用的图表风格较为暗淡且技术性强，那么下一次可以尝试更明亮的、更具编辑风格的图表。

---

### 第二步：阅读参考资料

在生成内容之前，请阅读以下参考资料：
- **对于架构类内容（文本较多的卡片）**：`references/css-patterns.md` + `templates/architecture.html`
- **对于流程图/图表**：`references/libraries.md` + `templates/mermaid-flowchart.html`
- **对于数据表格/对比表**：`templates/data-table.html`
- **对于幻灯片**：`templates/slide-deck.html` + `references/slide-patterns.md`
- **对于 CSS/布局样式**：`references/css-patterns.md`
- **对于包含多个部分的文档（如总结、回顾、仪表盘）**：`references/responsive-nav.md`

---

### 第三步：选择渲染方式

| 内容类型 | 使用的渲染方式 |
|---|---|
| 架构类内容（文本较多） | 使用 CSS Grid 布局和箭头来表示流程 |
| 架构类内容（拓扑结构重要） | 使用 Mermaid 绘制图表 |
- 流程图/管道图 | 使用 Mermaid 绘制流程图 |
- 序列图 | 使用 Mermaid 绘制序列图 |
- 数据流 | 使用带有边标签的 Mermaid 图表 |
- ER 图/数据模型 | 使用 Mermaid 绘制 ER 图 |
- 状态机 | 使用 Mermaid 绘制状态机图 |
- 思维导图 | 使用 Mermaid 绘制思维导图 |
- 类图 | 使用 Mermaid 绘制类图 |
- C4 架构 | 使用 Mermaid 绘制包含子图的流程图 |
- 数据表格/对比表 | 使用带有样式化的 HTML `<table>` |
- 仪表盘/关键绩效指标 | 使用 CSS Grid 布局和 Chart.js 图表库 |
- 幻灯片 | 使用滚动式布局的 `<section>` 元素

---

### 第四步：生成 HTML 文件

**文件命名规则：** `~/clawd/output/diagrams/YYYY-MM-DD-{slug}.html`  
**示例：`~/clawd/output/diagrams/2026-03-10-nexus-architecture.html`**

**所有生成的 HTML 文件必须满足以下要求：**
- **自包含**（除了 CDN 引用的库之外，不依赖任何外部资源）
- **单一文件**  
- **支持深色/浅色主题**（通过 `@media (prefers-color-scheme: dark)` 标签切换）
- **响应式设计**（适合移动设备）
- **使用真实的字体**（优先使用 Google Fonts 或系统提供的字体库，避免使用纯无衬线字体）

**通用模板结构：**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties for theme */
    /* Layout */
    /* Components */
  </style>
</head>
<body>
  <!-- Content -->
  <script>
    /* JS only if needed (Mermaid, Chart.js, interactivity) */
  </script>
</body>
</html>
```

---

### 第五步：在浏览器中打开文件

编写完 HTML 文件后，**告诉用户文件的路径，并告知他们可以在浏览器中打开该文件。**

---

## 关于图表的具体说明

### Mermaid 绘图工具的使用建议：
- 始终使用 `theme: 'base'` 作为默认主题——这是所有样式变量都可以自定义的主题
- **禁止在 `themeVariables` 中使用紫色/靛蓝色/洋红色**  
- **务必为 `.mermaid .nodeLabel` 和 `.mermaid .edgeLabel` 添加 CSS 重写样式，以匹配页面的整体颜色方案**  
- **禁止将 `.node` 作为 CSS 类名使用**（这可能会与 Mermaid 的内部机制冲突，应使用 `.ve-card` 代替）  
- 对于复杂的图表，添加缩放/平移控制功能（详见 `css-patterns.md` 文档）  
- **仅在必要时导入 ELK 布局引擎**——否则会增加文件的大小。

### 幻灯片制作注意事项：
- 每张幻灯片的高度设置为 `100dvh`，并使用 `scroll-snap-align: start` 属性实现滚动定位  
- 添加键盘导航按钮（Left/Right/Space）  
- 添加幻灯片页码（例如 “3 / 12”）  
- 添加进度条  
- 在将内容添加到幻灯片之前，先整理所有源文件内容，避免随意插入内容  
- 通常包含 7 个部分的文档对应的幻灯片数量为 18–25 张，而不是 10–13 张  

### 数据表格的优化：
- 添加固定的页眉  
- 如果表格有超过 8 行，则添加可排序的列  
- 为状态列添加颜色编码的状态指示器  
- 为数据表格提供导出为 CSV 的功能  

---

## 将内容分享到网页

要将生成的 HTML 文件部署到在线平台上，需要使用 Vercel CLI：`npm i -g vercel`。该命令会返回一个可共享的在线 URL。

---

## Flowverse 设计规范

在为 FlowStay、FlowVue、FlowTron 或任何 Flowverse 产品生成图表时，请使用官方指定的颜色方案：

```css
:root {
  --flow-hero: #008FFF;
  --flow-hero-light: #33A5FF;
  --flow-hero-dark: #0070CC;
  --flow-glow: rgba(0, 143, 255, 0.25);
  --flow-bg: #0a0a0f;        /* FlowVue dark bg */
  --flow-surface: #13131a;
  --flow-border: rgba(255,255,255,0.08);
  --flow-text: #e8e8f0;
}
```

**注意：** FlowVue 仅支持深色主题；FlowStay 和 FlowTron 支持深色和浅色两种主题。

---

## 示例：

- **“为我绘制 API 网关的架构图”**  
  → 生成 Mermaid 绘制的架构图，采用蓝图风格，展示客户端 → 网关 → 认证 → 服务 → 数据库的连接关系  

- **“制作我们所有第三方集成的对比表”**  
  → 生成 HTML 数据表格，采用数据密集型布局，列包括：服务名称 | 类别 | 认证方式 | 流量限制 | 状态 | 成本  

- **“提供关于结账重构项目的总结”**  
  → 生成可滚动的 HTML 页面，内容包括项目状态、最近提交的代码更改、当前工作进展以及下一步计划  

- **“制作关于第二季度上市计划的幻灯片”**  
  → 生成包含 15–20 张幻灯片的演示文稿，采用编辑风格，涵盖关键指标、目标销售渠道和项目优先级  

- **“审查第 9 阶段的路由变更”**  
  → 生成可视化差异对比报告，包括变更前的架构图、变更后的架构图以及代码质量评估结果和风险提示  

*改编自 nicobailon/visual-explainer（MIT），适用于 OpenClaw，2026 年 3 月*