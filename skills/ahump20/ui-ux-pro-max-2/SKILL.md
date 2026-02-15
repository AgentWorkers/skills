---
name: ui-ux-pro-max
description: "UI/UX设计工具集：提供50种样式、21种配色方案、50种字体组合、20种图表类型，支持多种前端框架（React、Next.js、Vue、Svelte、SwiftUI、React Native、Flutter、Tailwind、shadcn/ui）。主要功能包括：规划、开发、设计、实现、审查、修复、优化、增强及重构UI/UX代码。适用项目类型涵盖网站、登录页面、仪表盘、管理员面板、电子商务平台、SaaS应用、作品集、博客、移动应用等。支持的文件格式包括.html、.tsx、.vue、.svelte。常用设计元素包括按钮、模态框、导航栏、侧边栏、卡片、表格和表单；提供的设计风格包括GlassMorphism、ClayMorphism、极简主义、Brutalism、Neumorphism、Bento Grid等。此外，还支持暗黑模式和响应式布局设计。核心功能包括颜色搭配、无障碍设计、动画效果、布局优化、字体选择、间距调整以及阴影和渐变效果的处理。集成工具shadcn/ui MCP可帮助用户快速查找组件并查看相关示例。"
---

# UI/UX Pro Max - 设计智慧

这是一份针对网页和移动应用程序的全面设计指南。包含50多种样式、97种配色方案、57种字体组合、99条用户体验（UX）指南以及适用于9种技术栈的25种图表类型。我们的数据库支持搜索功能，并能根据优先级提供推荐方案。

## 适用场景

在以下情况下请参考这些指南：
- 设计新的UI组件或页面
- 选择配色方案和字体样式
- 检查代码中的UX问题
- 构建登录页面或仪表板
- 实现无障碍访问（accessibility）要求

## 规则类别及优先级

| 优先级 | 规则类别 | 影响程度 | 领域 |
|---------|-----------|------------|--------|
| 1      | 无障碍访问（Accessibility） | 关键（CRITICAL） | UX       |
| 2      | 触控与交互（Touch & Interaction） | 关键（CRITICAL） | UX       |
| 3      | 性能（Performance） | 高（HIGH）    | UX       |
| 4      | 布局与响应式设计（Layout & Responsive） | 高（HIGH）    | UX       |
| 5      | 字体与颜色（Typography & Color） | 中等（MEDIUM）    | typography, color |
| 6      | 动画效果（Animation） | 中等（MEDIUM）    | UX       |
| 7      | 样式选择（Style Selection） | 中等（MEDIUM）    | style, product  |
| 8      | 图表与数据（Charts & Data） | 低（LOW）     | chart      |

## 快速参考

### 1. 无障碍访问（CRITICAL）

- **颜色对比度**：普通文本的颜色对比度至少为4.5:1
- **交互元素的高亮显示**：交互元素上应显示高亮环
- **图片的替代文本**：有意义的图片需配备描述性替代文本
- **仅图标按钮的aria-label**：为仅图标的按钮添加aria-label属性
- **键盘导航**：键盘导航的顺序应与视觉顺序一致
- **表单标签**：使用带有for属性的标签

### 2. 触控与交互（CRITICAL）

- **触控目标大小**：触控目标的最小尺寸为44x44像素
- **点击/轻触方式**：主要交互应使用点击或轻触操作
- **异步操作期间的按钮状态**：在异步操作期间禁用按钮
- **错误反馈**：在问题附近显示清晰的错误信息
- **可点击元素的鼠标指针**：为可点击元素添加鼠标指针

### 3. 性能（HIGH）

- **图片优化**：使用WebP格式、srcset和懒加载技术
- **减少动画效果**：检查用户是否偏好减少动画效果（`prefers-reduced-motion`设置）
- **异步内容的布局**：为异步内容预留空间

### 4. 布局与响应式设计（HIGH）

- **视口元信息**：设置`viewport-meta`为`width=device-width initial-scale=1`
- **移动设备上的字体大小**：正文字体大小至少为16像素
- **内容布局**：确保内容能适应视口宽度
- **z-index管理**：定义z-index值（如10、20、30、50）

### 5. 字体与颜色（MEDIUM）

- **行高**：正文行高设置为1.5-1.75倍
- **每行字符数**：每行限制在65-75个字符以内
- **字体组合**：确保标题和正文的字体风格协调一致

### 6. 动画效果（MEDIUM）

- **动画时长**：微交互动画的时长设置为150-300毫秒
- **动画方式**：使用`transform`或`opacity`效果，而非直接调整宽高
- **加载状态显示**：在加载时显示加载指示器（如旋转图标）

### 7. 样式选择（MEDIUM）

- **风格匹配**：选择与产品类型相匹配的样式
- **一致性**：在整个项目中保持样式统一
- **使用SVG图标**：优先使用SVG图标，而非表情符号（emoji）

### 8. 图表与数据（LOW）

- **图表类型**：根据数据类型选择合适的图表类型
- **颜色搭配**：使用易于阅读的配色方案
- **数据表格**：为数据表格提供替代显示方式（如文字描述）

## 使用方法

使用以下命令行工具（CLI）搜索特定领域的相关内容：

---

## 先决条件

请检查是否已安装Python：

```bash
python3 --version || python --version
```

如果未安装Python，请根据用户操作系统进行安装：

**macOS：**
```bash
brew install python3
```

**Ubuntu/Debian：**
```bash
sudo apt update && sudo apt install python3
```

**Windows：**
```powershell
winget install Python.Python.3.12
```

---

## 如何使用本工具

当用户需要UI/UX相关的工作（设计、开发、创建、实现、审查、改进等）时，请按照以下流程操作：

### 第1步：分析用户需求

从用户请求中提取关键信息：
- **产品类型**：SaaS、电子商务、作品集、仪表板、登录页面等
- **风格关键词**：极简主义（minimal）、趣味性（playful）、专业性（professional）、优雅（elegant）、暗黑模式（dark mode）等
- **行业**：医疗保健（healthcare）、金融科技（fintech）、游戏（gaming）、教育（education）等
- **技术栈**：React、Vue、Next.js；或默认使用`html-tailwind`

### 第2步：生成设计系统（必需）

**始终使用`--design-system`命令**以获得包含理由的全面推荐方案：**

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

该命令会：
1. 同时搜索5个领域（产品、风格、颜色、登录页面、字体）
2. 应用`ui-reasoning.csv`中的规则来选择最佳匹配项
3. 返回完整的设计系统，包括样式、颜色、字体、动画效果等
4. 提供应避免的设计反例（anti-patterns）

**示例：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 第2b步：保存设计系统（可选）

若需在会话间保持设计系统的有效性，请添加`--persist`参数：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

这样会生成：
- `design-system/MASTER.md`：包含所有设计规则的全局参考文件
- `design-system/pages/`：用于存储特定页面的样式覆盖文件

**具体页面的覆盖方式：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

这样做还会生成：
- `design-system/pages/dashboard.md`：该页面相对于全局设计系统的具体调整内容

**分层检索的工作原理：**
1. 在构建特定页面（如“Checkout”页面）时，首先查看`design-system/pages/checkout.md`
2. 如果该页面文件存在，其规则将覆盖全局设置
3. 如果不存在，则仅使用`design-system/MASTER.md`

**上下文感知的搜索提示：**
```
I am building the [Page Name] page. Please read design-system/MASTER.md.
Also check if design-system/pages/[page-name].md exists.
If the page file exists, prioritize its rules.
If not, use the Master rules exclusively.
Now, generate the code...
```

### 第3步：根据需要补充详细搜索

获取设计系统后，可以使用以下命令进行更详细的搜索：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**使用场景：**
| 需求 | 搜索领域 | 示例命令 |
|------|--------|---------|
| 需要更多样式选项 | `style` | `--domain style "glassmorphism dark"` |
| 查找图表推荐 | `chart` | `--domain chart "real-time dashboard"` |
| 查看UX最佳实践 | `ux` | `--domain ux "animation accessibility"` |
| 寻找替代字体 | `typography` | `--domain typography "elegant luxury"` |
| 获取登录页面结构建议 | `landing` | `--domain landing "hero social-proof"` |

### 第4步：选择技术栈指南（默认使用html-tailwind）

获取与所选技术栈相关的最佳实践。如果用户未指定技术栈，**默认使用`html-tailwind`**。

**可用技术栈：`html-tailwind`、`react`、`nextjs`、`vue`、`svelte`、`swiftui`、`react-native`、`flutter`、`shadcn`、`jetpack-compose`**

---

## 搜索参考

### 可搜索的领域

| 领域 | 适用范围 | 示例关键词 |
|--------|---------|------------------|
| **product** | 产品类型推荐 | SaaS、电子商务、作品集、医疗保健、美容服务 |
| **style** | UI样式、颜色、动画效果 | glassmorphism、极简主义、暗黑模式 |
| **typography** | 字体组合、Google字体 | 优雅、趣味性、专业性、现代感 |
| **color** | 按产品类型划分的配色方案 | SaaS、电子商务、医疗保健、美容服务、金融科技 |
| **landing** | 页面结构、呼叫行动（CTA）策略 | 标题元素、以标题为中心的布局、用户评价、价格信息、社交分享功能 |
| **chart** | 图表类型、库推荐 | 趋势图、对比图、时间线图、漏斗图、饼图 |
| **ux** | 最佳实践、设计反例 | 动画效果、无障碍访问、z-index、加载提示 |
| **react** | React/Next.js的性能优化 | 水fall布局、组件缓存、动画效果、状态管理 |
| **web** | Web界面设计指南 | 无障碍访问相关属性（如aria）、键盘交互、语义化设计 |
| **prompt** | 与CSS相关的AI提示 | 需要搜索的样式名称 |

### 可用的技术栈

| 技术栈 | 重点关注点 |
|-------|-------|
| **html-tailwind** | Tailwind框架的实用工具、响应式设计、符合A11Y标准 |
| **react** | React的状态管理、钩子函数、性能优化 |
| **nextjs** | 静态服务器渲染（SSR）、路由功能、图片处理 |
| **vue** | Composition API、Pinia状态管理、Vue Router |
| **svelte** | 组件系统、状态管理、导航功能 |
| **swiftui** | 视图组件、状态管理、导航系统 |
| **react-native** | 移动应用组件、导航功能、列表布局 |
| **flutter** | 小部件设计、状态管理、布局优化 |
| **shadcn** | UI组件库、主题设计、表单功能 |
| **jetpack-compose** | 可组合的UI组件、样式修饰器、状态管理 |

---

## 示例工作流程

**用户请求：**“为专业护肤服务创建登录页面”

### 第1步：分析需求
- **产品类型**：美容/spa服务
- **风格关键词**：优雅、专业、柔和风格
- **行业**：美容/健康领域
- **技术栈**：默认使用`html-tailwind`

### 第2步：生成设计系统（必需）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**输出结果：**包含样式、颜色、字体、动画效果以及应避免的设计反例的完整设计系统。

### 第3步：根据需要补充详细搜索

```bash
# Get UX guidelines for animation and accessibility
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Get alternative typography options if needed
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### 第4步：选择技术栈指南

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**后续步骤：**将设计系统与详细搜索结果结合起来，实际实现设计。

---

## 输出格式

`--design-system`命令支持两种输出格式：

---

## 提高搜索效果的建议

1. **使用具体的关键词**：例如“医疗保健SaaS仪表板”而非“app”
2. **多次搜索**：不同的关键词可能会带来不同的搜索结果
3. **结合多个搜索领域**：例如同时搜索“风格”、“字体”和“颜色”，以获取完整的设计系统
4. **始终关注用户体验**：搜索“动画效果”、“z-index”或“无障碍访问”等常见问题
5. **使用相应的技术栈标签**：获取针对特定技术栈的最佳实践
6. **迭代搜索**：如果初次搜索结果不符合需求，尝试更换关键词

## 专业UI设计中的常见注意事项

以下是一些经常被忽视的问题，它们可能导致UI设计显得不够专业：

### 图标与视觉元素

| 规则 | 应遵循 | 应避免 |
|------|------|------|
| **使用SVG图标** | 优先使用SVG图标（如Heroicons、Lucide、Simple Icons） | 不要使用表情符号（如🎨、🚀、⚙️）作为UI图标 |
| **稳定的悬停效果** | 使用颜色或透明度的变化来表示悬停状态 | 避免使用会改变元素布局的缩放效果 |
| **正确的品牌图标** | 使用官方提供的SVG图标 | 不要使用错误的图标路径 |
| **统一的图标尺寸** | 图标的宽高比应固定为24x24像素 | 避免随意调整图标大小 |

### 交互与鼠标指针

| 规则 | 应遵循 | 应避免 |
|------|------|------|
| **添加鼠标指针** | 为所有可点击或可悬停的元素添加鼠标指针 | 不要忽略交互元素的默认鼠标指针显示 |
| **悬停反馈** | 提供明显的视觉反馈（如颜色变化、阴影效果） | 避免元素在悬停时没有明显提示 |
| **平滑的过渡效果** | 使用`transition-colors duration-200`设置过渡效果 | 过快的过渡效果（>500毫秒）会显得不自然 |

### 明暗模式下的对比度

| 规则 | 应遵循 | 应避免 |
|------|------|------|
| **明暗模式下的背景颜色** | 明亮模式下的背景颜色应为`bg-white/80`或更高透明度 | 避免使用`bg-white/10`（透明度过高） |
| **文本对比度** | 明亮模式下的文本颜色应为`#0F172A`（slate-900） | 避免使用`#94A3B8`（slate-400） |
| **暗色模式下的文字颜色** | 暗色模式下的文字颜色至少应为`#475569`（slate-600） | 避免使用更浅的颜色 |
| **边框可见性** | 明亮模式下的边框颜色应为`border-gray-200` | 避免使用`border-white/10`（几乎不可见） |

### 布局与间距

| 规则 | 应遵循 | 应避免 |
|------|------|------|
| **浮动导航栏** | 为导航栏添加`top-4 left-4 right-4`的间距 | 将导航栏固定在`top-0 left-0 right-0`的位置 |
| **内容间距** | 考虑到导航栏的固定高度 | 避免内容被导航栏遮挡 |
| **布局的一致性** | 所有元素的宽度应统一使用`max-w-6xl`或`max-w-7xl` | 避免使用不同的容器宽度 |

## 交付前的检查清单

在交付UI代码之前，请确认以下内容：

### 视觉质量
- **所有图标均为SVG格式**：避免使用表情符号
- **使用统一的图标集**：确保所有图标来自可靠的图标库（如Heroicons/Lucide）
- **品牌图标正确**：使用官方提供的SVG图标
- **悬停状态不会导致布局混乱**：确保悬停状态不会影响页面布局
- **使用主题颜色**：直接使用主题颜色（如`bg-primary`），而非通过`var()`变量定义

### 交互效果
- **所有可点击元素都有鼠标指针**：确保所有可点击元素都显示鼠标指针
- **悬停状态有明显的视觉反馈**：提供清晰的视觉提示
- **过渡效果流畅**：过渡效果应在150-300毫秒内完成
- **键盘导航时的高亮显示**：确保键盘导航时的高亮状态能够清晰显示

### 明暗模式
- **文本对比度足够**：确保文本在明亮模式下的对比度至少为4.5:1
- **透明元素在明亮模式下可见**：确保透明元素在明亮模式下仍可清晰显示
- **两种模式下的边框都可见**：确保两种模式下边框都能正确显示
- **页面响应性**：确保页面在375px、768px、1024px、1440px等不同屏幕尺寸下都能正常显示
- **移动设备上的滚动效果**：确保页面在移动设备上能够正常滚动

### 无障碍访问
- **所有图片都有替代文本**：确保所有图片都配有描述性替代文本
- **表单输入有标签**：确保表单输入字段都有对应的标签
- **颜色不是唯一的提示方式**：颜色不应作为唯一的视觉提示方式
- **尊重用户设置**：确保系统尊重用户的`prefers-reduced-motion`设置