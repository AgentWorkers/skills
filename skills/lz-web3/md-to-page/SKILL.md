---
name: md-to-page
description: Convert Markdown files into beautiful, scrollable wide-screen HTML pages with dark/light theme toggle, scroll animations, and rich directive components. Use when the user wants to turn a .md file into a presentable HTML page, create a long-form web article from markdown, generate a scrollable one-pager, or make a shareable HTML document from notes/outlines. Triggers on: markdown to HTML, generate page from md, scrollable page, wide-screen page, one-pager, web article from markdown.
---

# md-to-page

将 Markdown 文件转换为精美的、可滚动的宽屏 HTML 页面，并支持内置的深色/浅色主题切换功能。

## 快速入门

```bash
python3 SKILL_DIR/scripts/md_to_page.py INPUT.md OUTPUT.html [options]
```

### 参数选项

| 参数          | 描述                                      | 默认值         |
|--------------|-----------------------------------------|--------------|
| `--embed-images` | 压缩本地图片（使用 Pillow 库）并将其嵌入为 base64 数据 URI           | 关闭           |
| `--title TEXT`   | 覆盖 HTML 页面标题                         | 首个 H1 标题       |
| `--footer TEXT`   | 自定义页脚文本                             | “由 md-to-page 生成”     |

## 主要功能

### 标准 Markdown 支持

- **H1**：全屏标题（H1 下的第一段文字为副标题）  
- **H2**：编号的章节分隔符（01, 02, ...）  
- **H3/H4**：章节/子章节标题  
- **加粗文字**、**斜体文字**、**内联代码**、**链接**、**图片**  
- 无序列表和有序列表  
- 带有语法显示的代码块  
- 引用格式（`>`, `> 💡`, `> ⚠️`）  
- Markdown 表格：自动生成的响应式表格  
- 水平分隔线：被忽略（章节本身已提供视觉分隔）

### 文件结构显示

```
workspace/
├── SOUL.md         # 系统提示文件
├── memory/
│   └── 2026-03-01.md
└── skills/
```

### ::: 指令块

使用 `:::` 语法创建丰富的页面元素：

#### 卡片（Card）

```markdown
::: card
Content with **bold** and `code`
:::
```

#### 卡片网格（Card Grid）

```markdown
::: card-grid
::: card {icon=💬 title="Chat"}
Natural language interface
:::
::: card {icon=📄 title="Docs"}
Auto-generated documentation
:::
:::
```

#### 对比（Good vs Bad）

```markdown
::: compare
::: side bad {label="❌ Before"}
Manual copy-paste workflow
:::
::: side good {label="✅ After"}
Automated pipeline
:::
:::
```

#### 流程图（Flow）

```markdown
::: flow
Write docs → AI helps write → *Store in Confluence* → AI reads → Summary
:::
```

- **普通文本**：普通步骤  
- `*文本*`：高亮显示的步骤（带有边框和渐变效果）  
- `~文本~`：被标记为过时的步骤（带有删除线）  
- 箭头 `→` `←`：以连接符的形式显示  

#### 过时的流程图样式（不推荐使用）

```markdown
::: flow dead-suffix
Store in Confluence ← No longer needed
:::
```

#### 引用块（Quote Block）

```markdown
::: quote
The best interface is no interface.
— Golden Krishna
:::
```

#### 图层效果（Layers）

```markdown
::: layers
Personal | Your preferences, projects, habits
Team | Onboarding, SOP, tech decisions
Organization | Company policies, cross-BU knowledge
:::
```

格式：`标签 | 描述`，每行一个元素。每个图层都有不同的颜色（支持最多 4 种内置颜色）。

#### 循环图（Cycle）

```markdown
::: cycle negative
Wrote docs → Nobody updates → Outdated → Nobody reads → ↻
:::

::: cycle positive
Write to memory → AI answers → People use → AI updates → ↻
:::
```

极性选项：`negative`（粉红色）或 `positive`（青色）。

#### 命令列表（Command List）

```markdown
::: cmd-list
/status — Check agent status
/model — Switch model
/new — Reset context
:::
```

格式：`命令 — 描述`，每行显示，命令以等宽字体呈现，关键部分带有高亮颜色。

### 图片嵌入

启用 `--embed-images` 选项后，`![alt](path)` 格式的本地图片会：
1. 从磁盘加载（相对于输入的 Markdown 文件）
2. 使用 Pillow 库压缩（最大宽度 1200px，JPEG 品质 75%）
3. 以 `data:image/jpeg;base64,...` 的形式嵌入到页面中
4. 如果未安装 Pillow，图片会以原始字节形式进行 base64 编码

外部链接（`http://`, `https://`）保持不变。

### 主题切换

生成的每页都会在右上角提供一个 🌙/☀️ 切换按钮，用于在深色和浅色主题之间切换。用户偏好设置会保存在 `localStorage` 中：
- **深色主题**（默认）：深蓝色背景，渐变效果，紫色/青色元素  
- **浅色主题**：白色背景，灰色卡片，简洁的字体设计

## Markdown 表格

标准格式的表格会被自动识别并转换为格式化的表格：

```markdown
| Feature | Status |
|---------|--------|
| Dark mode | ✅ |
| Light mode | ✅ |
```

## 不推荐使用的情况

- **幻灯片/演示文稿**：请使用 `presentation-generator` 或 `slides-cog`  
- **Obsidian 笔记**：请使用 `obsidian-markdown`