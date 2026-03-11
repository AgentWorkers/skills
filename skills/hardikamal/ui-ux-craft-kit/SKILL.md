---
name: ui-ux-craft-kit
description: "适用于网页和移动设备的UI/UX设计工具。提供超过50种设计风格、161种配色方案、57种字体组合、161种产品类型以及99条UX设计指南；支持10种开发框架（React、Next.js、Vue、Svelte、SwiftUI、React Native、Flutter、Tailwind、shadcn/ui以及HTML/CSS）。支持的功能包括：规划、构建、创建、设计、实现、审查、修复、优化、增强、重构和检查UI/UX代码。适用的项目类型包括网站、登录页面、仪表盘、管理面板、电子商务平台、SaaS应用、作品集、博客和移动应用程序。涵盖的元素包括按钮、模态框、导航栏、侧边栏、卡片、表格、表单和图表。提供的设计风格包括Glassmorphism、Claymorphism、极简主义（Minimalism）、Brutalism、Neumorphism、Bento Grid、暗黑模式（Dark Mode）、响应式设计（Responsive Design）以及Skeuomorphism和平面设计（Flat Design）。涵盖的主题包括色彩系统（Color Systems）、无障碍设计（Accessibility）、动画（Animation）、布局（Layout）、排版（Typography）、字体搭配（Font Pairing）、间距调整（Spacing）、交互状态（Interaction States）、阴影效果（Shadow Effects）和渐变效果（Gradient Effects）。"
---
# UI/UX CraftKit — 设计智能工具包

这是一份针对网页和移动应用程序的全面设计指南。该工具包包含50多种设计风格、161个配色方案、57种字体组合、161种产品类型及其设计规则、99条用户体验（UX）指导原则，以及适用于10种技术栈的25种图表类型。用户可以通过搜索功能快速找到所需的设计资源，并获得基于优先级的推荐结果。

该项目为开源项目，托管在GitHub上：[github.com/hardikamal/ui-ux-craft-kit](https://github.com/hardikamal/ui-ux-craft-kit)

## 搜索命令

```bash
python3 <skill_dir>/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

请将`<skill_dir>`替换为该技能目录的绝对路径。

**搜索范围：**
- `product`：产品类型相关设计建议（SaaS、电子商务、作品集等）
- `style`：UI设计风格（玻璃形态主义、极简主义、野兽主义）及AI辅助设计
- `typography`：基于Google Fonts的字体组合
- `color`：按产品类型划分的配色方案
- `landing`：页面结构和呼叫行动（CTA）策略
- `chart`：图表类型及相关库推荐
- `ux`：最佳实践与设计反例
- `icons`：图标库推荐
- `react`：React/Next.js性能优化指南
- `web`：网页可访问性及界面设计规范
- `google-fonts`：Google Fonts搜索功能

**特定技术栈的搜索方式：**
```bash
python3 <skill_dir>/scripts/search.py "<query>" --stack react-native
```

## 设计系统的生成方式：**
```bash
python3 <skill_dir>/scripts/search.py "<query>" --design-system [-p "Project Name"]
```

## 适用场景

当任务涉及**UI结构设计、视觉设计决策、交互方式或用户体验质量控制**时，可以使用本工具包。

### 必须使用的情况：
- 设计新页面（如登录页面、仪表盘、管理员页面、SaaS应用、移动应用）
- 创建或重构UI组件（按钮、模态框、表单、图表等）
- 选择配色方案、字体系统、间距标准或布局规则
- 审查UI代码的可访问性或视觉一致性
- 实现导航结构、动画效果或响应式设计
- 做出与产品相关的设计决策（如风格选择、信息层次结构、品牌风格等）
- 提高界面的视觉质量、清晰度或可用性

### 不适用的情况：
- 纯粹的后端逻辑开发
- 仅涉及API或数据库设计的任务
- 与界面无关的性能优化工作
- 基础设施或DevOps相关的任务

**使用规则**：如果任务会改变某个功能的**外观、交互方式或用户体验**，请使用本工具包。

## 使用步骤：
### 第一步：确定搜索范围
在生成UI代码之前，先通过搜索获取相关的设计信息：

```bash
# Get style recommendations for a product type
python3 <skill_dir>/scripts/search.py "SaaS dashboard" --domain product

# Get color palette
python3 <skill_dir>/scripts/search.py "fintech app" --domain color

# Get font pairing
python3 <skill_dir>/scripts/search.py "modern minimal" --domain typography

# Generate a full design system
python3 <skill_dir>/scripts/search.py "fitness tracking app" --design-system -p "FitTrack"
```

### 第二步：应用搜索结果
根据搜索结果来指导你的设计决策。搜索结果会按照优先级从数据库中返回相关内容。

### 第三步：根据优先级规则进行质量检查
| 优先级 | 类别 | 关键检查项 |
|----------|----------|------------|
| 1 | 可访问性 | 对比度至少为4.5:1、提供替代文本、支持键盘导航、使用Aria-labels标签 |
| 2 | 触控与交互 | 触控目标尺寸至少为44×44像素（苹果设备）/ 48×48dp（Material Design规范） |
| 3 | 性能 | 使用WebP/AVIF图像格式、采用懒加载技术、CSS样式表重排（CLS）值小于0.1 |
| 4 | 风格选择 | 选择与产品类型相匹配的风格、保持设计一致性、使用SVG图标 |
| 5 | 布局与响应式设计 | 以移动设备优先进行设计、避免横向滚动 |
| 6 | 字体与颜色 | 使用16像素的字体大小、行高设置为1.5、使用语义化的颜色代码 |
| 7 | 动画效果 | 动画时长控制在150–300毫秒内、仅使用`transform`/`opacity`属性 |
| 8 | 表单与反馈 | 输入框需有可见的标签提示、错误信息需在相关字段附近显示 |
| 9 | 导航设计 | 回退按钮的位置应易于识别、底部导航栏中的选项不超过5个 |
| 10 | 图表与数据展示 | 图表需附带图例、提供悬停提示、使用易于识别的颜色 |

## 快速参考：
### 可访问性（至关重要）：
- 正常文本的对比度至少为4.5:1
- 所有交互元素上都需要有可见的焦点指示
- 图片需配有描述性的替代文本
- 仅使用图标的按钮需添加`aria-label`标签
- 切换标签的顺序应与视觉顺序一致
- 支持`prefers-reduced-motion`浏览器设置

### 触控与交互（至关重要）：
- 触控目标尺寸至少为44×44像素（苹果设备）/ 48×48dp（Material Design规范）
- 触控目标之间至少保留8像素的间距
- 主要交互方式应使用点击/轻触操作，而非仅依赖悬停效果
- 异步操作期间禁用按钮并显示加载提示
- 可点击元素上需显示`cursor-pointer`指针

### 性能（较高要求）：
- 使用WebP/AVIF图像格式、采用响应式的`srcset`技术
- 明确指定图片的`width`/`height`属性以避免CSS样式表重排问题
- 对于折叠后的图片采用懒加载机制
- 对于包含50个以上项目的列表，使用虚拟化技术显示

### 风格选择（较高要求）：
- 选择与产品类型相匹配的设计风格
- 使用SVG图标（如Heroicons、Lucide图标库），避免使用表情符号作为图标
- 整个产品范围内使用统一的图标风格和视觉语言
- 每个页面只设置一个主要的呼叫行动（CTA）元素

### 布局与响应式设计（较高要求）：
- 使用`width=device-width, initial-scale=1`的视口设置
- 以移动设备优先进行设计，适配不同屏幕尺寸（375px → 768px → 1024px → 1440px）
- 移动设备上禁止横向滚动
- 使用4像素/8dp的间距规则
- 在移动设备上使用`min-h-dvh`而不是`100vh`的布局方式

### 字体与颜色（中等要求）：
- 正文文本的字体大小至少为16像素（避免iOS设备的自动缩放效果）
- 行高设置为1.5–1.75倍
- 每行显示65–75个字符
- 在组件中使用语义化的颜色代码，而非纯十六进制颜色值
- 标题字体加粗（600–700像素），正文字体（400像素），次要标签（500像素）

### 动画效果（中等要求）：
- 微交互效果的动画时长控制在150–300毫秒内
- 仅使用`transform`/`opacity`属性进行动画效果，避免修改元素的`width`/`height`
- 遵循`prefers-reduced-motion`浏览器设置
- 动画结束时间应在动画开始时间的60–70%时
- 动画必须具有实际意义，而不仅仅是装饰性效果

### 表单与反馈（中等要求）：
- 每个输入框都需要有可见的标签提示
- 错误信息需在相关字段附近显示
- 在用户输入内容后进行实时验证
- 执行破坏性操作前需给出确认提示
- 提示信息应在3–5秒后自动消失

### 导航设计（较高要求）：
- 底部导航栏中的选项不超过5个，并配有清晰的标签
- 回退按钮的位置应易于用户识别
- 所有重要页面都应可以通过深度链接访问
- 用户返回上一级页面时需保持界面状态不变

### 图表与数据展示（较低要求）：
- 根据数据类型选择合适的图表类型（趋势数据使用折线图，对比数据使用条形图）
- 图表附近必须显示图例
- 提供悬停时的提示信息
- 使用易于识别的配色方案（避免仅使用红色/绿色）