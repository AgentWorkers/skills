---
name: ui-ux-pro-max
model: fast
version: 1.1.0
description: >
  Searchable UI/UX design databases: 50+ styles, 97 palettes, 57 font pairings, 99 UX rules,
  25 chart types. CLI generates design systems from natural language. Data-driven complement to ui-design.
tags: [design, ui, ux, color, typography, style, accessibility, charts]
related: [ui-design, frontend-design, web-design]
---

# UI/UX Pro Max

这是一个可搜索的设计数据库，通过命令行界面（CLI）可以根据自然语言查询生成完整的设计系统。

> **另请参阅：** `ui-design`，了解基础知识和决策方法。该技能通过CLI提供数据驱动的建议。

## 使用场景

- 设计新的UI组件或页面
- 选择颜色调色板和字体样式
- 检查代码中的UX问题
- 构建登录页面或仪表板
- 实现无障碍访问要求

## 规则分类（按优先级）

| 优先级 | 分类 | 影响 | 领域 |
|----------|----------|--------|--------|
| 1 | 无障碍访问 | 关键 | `ux` |
| 2 | 触控与交互 | 关键 | `ux` |
| 3 | 性能 | 高 | `ux` |
| 4 | 布局与响应式 | 高 | `ux` |
| 5 | 字体与颜色 | 中等 | `typography`, `color` |
| 6 | 动画 | 中等 | `ux` |
| 7 | 风格选择 | 中等 | `style`, `product` |
| 8 | 图表与数据 | 低 | `chart` |

## 快速参考

### 无障碍访问（关键）

- **颜色对比度**：普通文本的颜色对比度至少为4.5:1
- **焦点状态**：交互元素上显示可见的焦点环
- **替代文本**：为有意义的图片添加描述性的替代文本
- **aria-label**：仅图标按钮的`aria-label`
- **键盘导航**：Tab键顺序与视觉顺序一致
- **表单标签**：使用带有`for`属性的标签

### 触控与交互（关键）

- **触控目标大小**：触控目标的最小尺寸为44x44像素
- **悬停与点击**：主要交互使用点击/轻触
- **加载按钮**：在异步操作期间禁用按钮
- **错误反馈**：在问题附近显示清晰的错误信息
- **光标指针**：为可点击元素添加光标指针

### 性能（高）

- **图片优化**：使用WebP格式、srcset和懒加载
- **减少动画效果**：检查`prefers-reduced-motion`设置
- **内容跳转**：为异步内容预留空间

### 布局与响应式（高）

- `viewport-meta`：初始缩放设置为`width=device-width`
- **可读字体大小**：移动设备上的正文字体大小至少为16像素
- **水平滚动**：确保内容适应视口宽度
- **z-index管理**：定义z-index值（例如10, 20, 30, 50）

### 字体与颜色（中等）

- **行高**：正文文本的行高设置为1.5-1.75倍
- **每行字符数**：每行限制在65-75个字符
- **字体搭配**：确保标题和正文的字体风格一致

### 动画（中等）

- **动画持续时间**：微交互动画的持续时间设置为150-300毫秒
- **使用变换/透明度效果**：而不是简单的宽度/高度变化
- **加载状态**：使用骨架屏幕或旋转动画来显示加载状态

### 风格选择（中等）

- **风格匹配**：根据产品类型选择合适的风格
- **一致性**：在整个网站中使用统一的风格
- **使用SVG图标**：避免使用表情符号图标

### 图表与数据（低）

- **图表类型**：根据数据类型选择合适的图表类型
- **颜色选择**：使用易于阅读的颜色调色板
- **数据表格**：为无障碍访问提供表格的替代方案

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install ui-ux-pro-max
```


---

## 先决条件

搜索功能需要Python 3环境。

```bash
python3 --version
```

---

## 工作流程

当用户请求UI/UX相关的工作（设计、开发、创建、实施、审查、修改、优化）时，请按照以下步骤操作：

### 第1步：分析需求

从用户请求中提取以下信息：
- **产品类型**：SaaS、电子商务、作品集、仪表板、登录页面
- **风格关键词**：极简主义、趣味性、专业性、优雅、暗黑模式
- **行业**：医疗保健、金融科技、游戏、教育
- **技术栈**：React、Vue、Next.js，或默认使用`html-tailwind`

### 第2步：生成设计系统

始终使用`--design-system`命令来获取全面的设计建议：

```bash
python3 scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

该命令会同时搜索5个领域（产品、风格、颜色、登录页面、字体），应用`ui-reasoning.csv`中的规则，并返回一个完整的设计系统，包括设计模式、风格、颜色、字体、效果和反例。

**示例：**

```bash
python3 scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 第2b步：保存设计系统

将设计系统保存下来，以便在不同会话中分层查询：

```bash
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

生成的文件包括：
- `design-system/MASTER.md`：全局的设计系统配置文件
- `design-system/pages/`：用于存储特定页面的样式覆盖文件

**对于页面样式覆盖：**

```bash
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

**分层查询**：在构建特定页面时，首先检查`design-system/pages/<page>.md`文件。如果存在该文件，其规则将覆盖全局配置文件`design-system/MASTER.md`中的内容。否则，仅使用全局配置文件。

### 第3步：补充特定领域的搜索

在生成设计系统后，可以使用特定领域的搜索来获取更多细节：

```bash
python3 scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| 需求 | 领域 | 示例 |
|------|--------|---------|
| 更多样式选项 | `style` | `--domain style "glassmorphism dark"` |
| 图表推荐 | `chart` | `--domain chart "real-time dashboard"` |
| UX最佳实践 | `ux` | `--domain ux "animation accessibility"` |
| 替代字体 | `typography` | `--domain typography "elegant luxury"` |
| 登录页面结构 | `landing` | `--domain landing "hero social-proof"` |

### 第4步：获取技术栈指南

获取与实现相关的最佳实践。如果未指定，默认使用`html-tailwind`技术栈。

```bash
python3 scripts/search.py "<keyword>" --stack html-tailwind
```

可用技术栈：`html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## 搜索参考

### 领域

| 领域 | 用途 | 示例关键词 |
|--------|---------|------------------|
| `product` | 产品类型建议 | SaaS、电子商务、作品集、医疗保健 |
| `style` | UI样式、颜色、动画效果 | glassmorphism、极简主义、暗黑模式 |
| `typography` | 字体搭配、Google Fonts字体库 | 优雅、趣味性、专业性 |
| `color` | 根据产品类型选择颜色调色板 | SaaS、电子商务、医疗保健、金融科技 |
| `landing` | 页面结构、呼叫行动（CTA）策略 | 标题元素、用户评价、价格信息、社交验证功能 |
| `chart` | 图表类型、图表库推荐 | 趋势图、对比图表、时间线图表 |
| `ux` | 最佳实践、反例 | 动画效果、无障碍访问、z-index设置 |
| `react` | React/Next.js的性能优化 | 水fall布局、组件组合、动画效果 |
| `web` | 网页界面指南 | ARIA属性、键盘交互、语义化设计 |
| `prompt` | 人工智能提示、CSS相关关键词 | （例如：特定样式名称） |

### 技术栈

| 技术栈 | 重点 | |
|-------|-------|
| `html-tailwind` | Tailwind框架的实用工具、响应式布局、符合A11Y标准（默认推荐） |
| `react` | React状态管理、钩子函数、性能优化、设计模式 |
| `nextjs` | 静态服务器渲染（SSR）、路由功能、图片处理、API路由 |
| `vue` | Composition API、Pinia状态管理、Vue Router |
| `svelte` | Svelte组件库、状态管理、导航功能 |
| `swiftui` | SwiftUI框架、视图组件、导航系统、动画效果 |
| `react-native` | 移动应用开发组件、导航系统、列表渲染 |
| `flutter` | Flutter框架、组件开发、布局管理、主题设置 |
| `shadcn` | UI组件库、主题系统、表单设计 |
| `jetpack-compose` | Composable组件、样式修饰器、状态管理 |

### 输出格式

```bash
# ASCII box (default) — best for terminal display
python3 scripts/search.py "fintech crypto" --design-system

# Markdown — best for documentation
python3 scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## 示例工作流程

**用户请求：**“为一家专业护肤服务创建一个登录页面”

**步骤1 — 分析需求：** 该服务属于美容/ spa行业，风格要求为优雅且专业，默认使用`html-tailwind`技术栈。

**步骤2 — 生成设计系统：**

```bash
python3 scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**步骤3 — 补充细节：**

```bash
python3 scripts/search.py "animation accessibility" --domain ux
python3 scripts/search.py "elegant luxury serif" --domain typography
```

**步骤4 — 选择技术栈：**

```bash
python3 scripts/search.py "layout responsive form" --stack html-tailwind
```

然后综合设计系统结果和详细搜索结果，进行实际开发。

---

## 搜索技巧

1. **具体化请求**：例如，“医疗保健行业的SaaS仪表板”比“app”这样的描述更具体。
2. **多次搜索**：使用不同的关键词可以获得不同的搜索结果。
3. **结合多个领域**：结合使用“风格”、“字体”和“颜色”等关键词，以获取完整的设计方案。
4. **始终检查UX相关内容**：搜索“动画效果”、“z-index”和“无障碍访问”等关键词，以发现潜在问题。
5. **使用技术栈筛选**：根据具体需求获取相应的最佳实践建议。
6. **迭代优化**：如果第一次搜索结果不满意，可以尝试使用不同的关键词。

## 专业UI设计的通用规则

### 图标与视觉元素

| 规则 | 应遵循 | 应避免 |
|------|-----|-------|
| **使用SVG图标**：优先使用SVG图标（如Heroicons、Lucide、Simple Icons） | **避免使用表情符号作为图标** |
| **稳定的悬停效果**：使用颜色或透明度变化来表示悬停状态 | **避免使用会导致布局变化的缩放效果** |
| **使用正确的品牌Logo**：使用官方提供的SVG版本 | **避免使用错误的Logo文件路径** |
| **保持图标尺寸一致**：图标尺寸统一为24x24像素 | **避免使用不同大小的图标** |

### 交互与光标

| 规则 | 应遵循 | 应避免 |
|------|-----|-------|
| **为所有可点击元素添加光标指针** | **确保所有可点击元素都显示光标指针** | **避免使用默认的光标效果** |
| **提供清晰的悬停反馈**：通过颜色、阴影或边框来指示交互状态 | **避免没有明显的交互提示** |
| **平滑的过渡效果**：过渡效果的时间设置为150-300毫秒 | **避免突然的变化或过渡时间过长（超过500毫秒）** |

### 明暗模式下的对比度

| 规则 | 应遵循 | 应避免 |
|------|-----|-------|
| **明亮模式下的对比度**：背景颜色应为`bg-white/80`或更高透明度 | **背景颜色`bg-white/10`（过于透明）** |
| **文本对比度**：文本颜色应为`#0F172A`（深灰色） | **正文颜色`#94A3B8`（较浅的灰色）** |
| **暗黑模式下的文本颜色**：文字颜色至少应为`#475569`（较深的灰色） | **避免使用更浅的灰色** |
| **边框可见性**：在明亮模式下边框应可见 | **在暗黑模式下边框应不可见** |

### 布局与间距

| 规则 | 应遵循 | 应避免 |
|------|-----|-------|
| **浮动导航栏**：间距设置为`top-4 left-4 right-4` | **保持导航栏的固定位置（top-0 left-0 right-0）** |
| **内容间距**：考虑导航栏的高度对内容布局的影响 | **避免内容被导航栏遮挡** |
| **一致的容器宽度**：所有容器宽度应统一设置为`max-w-6xl`或`max-w-7xl` | **避免使用不同的容器宽度** |

## 预交付检查清单

### 视觉质量

- **所有图标均为SVG格式**：避免使用表情符号图标。
- **使用统一的图标集（如Heroicons/Lucide）**。
- **验证品牌Logo的正确性**。
- **悬停状态不会导致布局混乱**。
- **主题颜色直接使用**：避免使用变量（`var()`）来定义颜色。

### 交互效果

- **所有可点击元素都显示光标指针**。
- **悬停状态有明显的视觉反馈**。
- **过渡效果的时间设置为150-300毫秒**。
- **键盘导航时的焦点状态清晰可见**。

### 明暗模式下的显示效果

- **明亮模式下的文本对比度至少为4.5:1**。
- **明亮模式下的透明元素清晰可见**。
- **两种模式下边框都应可见**。
- **两种模式都经过测试**。

### 布局规范

- **浮动元素具有适当的间距**。
- **内容不会被固定的导航栏遮挡**。
- **页面在375px、768px、1024px、1440px分辨率下都能正常显示**。
- **移动设备上没有水平滚动条**。

### 无障碍访问

- **所有图片都配有替代文本**。
- **表单输入字段都有标签**。
- **颜色不是唯一的视觉提示方式**。
- **尊重用户的`prefers-reduced-motion`设置（减少动画效果）**。