---
name: ui-ux-master
description: 掌握UI/UX设计技能，融合Apple Human Interface Guidelines（HIG）、现代网页设计理念、SuperDesign设计模式以及通用设计原则。能够应用于各种UI/UX设计项目，包括iOS/macOS/Web应用程序、登录页面、仪表盘、设计系统、可访问性优化、响应式布局、动画设计等，从而在所有平台和框架上创造出既美观又功能完善的用户界面。
---

# UI/UX设计大师技能

这是一项集成了Apple人类界面指南（Apple Human Interface Guidelines, HIG）、现代网页设计模式、SuperDesign设计原则以及通用用户体验最佳实践的终极设计技能，旨在为所有平台创造卓越的用户体验。

## 设计哲学

### 核心原则

**1. 清晰胜过复杂**
- 信息层次结构清晰明了
- 用户操作可预测
- 反馈即时
- 在不需要时隐藏复杂性

**2. 一致性带来熟悉感**
- 界面中重复使用相同的模式
- 术语统一
- 视觉语言连贯
- 遵循平台规范

**3. 通过简洁展现美感**
- 每个元素都有其存在的意义
- 适当的空白区域有助于提升视觉效果
- 减少视觉干扰
- 细节处理精致

**4. 可访问性是不可或缺的**
- 无论用户能力如何，都能使用该设计
- 支持键盘导航
- 适合屏幕阅读器
- 提供高对比度选项

## 平台特定的设计

### Apple平台（iOS、macOS、watchOS、tvOS、visionOS）

有关完整的Apple HIG设计模式，请参阅 [references/apple-platforms.md](references/apple-platforms.md)

**关键的Apple设计原则：**
- **清晰性：** 易读的文本、精确的图标、简洁的装饰
- **内容优先**：界面设计应服务于内容
- **层次感**：视觉层次分明、动作自然、空间感强烈

**适用场景：** 原生iOS、macOS、watchOS、tvOS或visionOS应用程序

### 现代网页设计

有关完整的网页设计模式，请参阅 [references/web-design.md](references/web-design.md)

**关键的网页设计原则：**
- **响应式**：以移动设备为先，适应各种屏幕尺寸
- **高性能**：加载速度快、资源优化
- **渐进式**：在所有设备上都能正常工作，并在可能的情况下进行优化
- **语义化**：正确的HTML结构、易于访问的标记

**适用场景：** 网站、Web应用程序、Progressive Web Applications (PWA)、登录页面、仪表板

## 设计系统

### 色彩理论

**现代色彩系统：**
- **oklch()** 色彩空间（感知上均匀、现代）
- **HSL** 用于快速调整颜色
- **RGB/Hex** 用于兼容旧版浏览器

**推荐的颜色：**
```css
/* Light/Dark mode compatible */
--primary: oklch(0.649 0.237 267);
--secondary: oklch(0.556 0 0);
--background: oklch(0.145 0 0); /* dark */
--foreground: oklch(0.985 0 0); /* light text */
--muted: oklch(0.556 0 0 / 0.5);
--border: oklch(0.922 0 0 / 0.15);
```

**避免使用：**
- 通用的Bootstrap蓝色 (#007bff) —— 过时
- 纯黑色 (#000000) —— 使用深灰色
- 对比度低于4.5:1的文本

**色彩指南：**
有关调色板、对比度比率和色彩心理学的信息，请参阅 [references/color-systems.md](references/color-systems.md)

### 字体排版

**推荐的系统字体：**
- **Apple：** SF Pro (iOS/macOS), SF Compact (watchOS)
- **Web：** Inter, Outfit, DM Sans, Plus Jakarta Sans
- **等宽字体：** JetBrains Mono, Fira Code, Geist Mono
- **备用字体：** -apple-system, system-ui, sans-serif

**字体大小：**
```
Display: 72px / 4.5rem
Heading 1: 48px / 3rem
Heading 2: 36px / 2.25rem
Heading 3: 24px / 1.5rem
Body: 16px / 1rem
Small: 14px / 0.875rem
Caption: 12px / 0.75rem
```

**行高：**
- 标题：1.2 - 1.3像素
- 正文：1.5 - 1.6像素
- 小字号文本：1.4 - 1.5像素

**字体搭配：**
有关字体搭配规则和示例，请参阅 [references/typography.md](references/typography.md)

### 间距与布局

**8点网格系统：**
- 基本单位：8像素 (0.5rem)
- 间距比例：8, 16, 24, 32, 40, 48, 56, 64, 80, 96
- 使用4的倍数进行微调（例如：4, 12, 20, 28等）

**标准边距：**
- 移动设备：16像素
- 平板设备：24像素
- 桌面设备：32-48像素
- 最大宽度：1200-1400像素

**组件间距：**
```
XS:  4px  - Tight groups (icon + text)
S:   8px  - Related items
M:   16px - Standard spacing
L:   24px - Section spacing
XL:  32px - Major sections
2XL: 48px - Page sections
```

**布局模式：**
有关网格、Flexbox和响应式布局的模式，请参阅 [references/layout-patterns.md](references/layout-patterns.md)

## 组件设计

### 按钮

**层次结构：**
1. **主要按钮：** 带填充效果、有突出颜色的按钮，执行主要操作
2. **辅助按钮：** 有轮廓或淡色调的按钮，提供辅助功能
3. **次要按钮：** 仅显示文本的按钮，最不显眼

**状态：**
- 默认状态
- 鼠标悬停状态
- 活动状态（被点击时）
- 禁用状态（透明度降低，不可交互）
- 加载状态（显示加载指示器）

**尺寸：**
- 小按钮：高度32-36像素
- 中等按钮：高度40-44像素（默认）
- 大按钮：高度48-56像素

**最佳实践：**
- 最小触摸目标尺寸为44×44像素（移动设备）
- 明确的按钮标签（例如使用“保存更改”而不是“确定”）
- 异步操作时显示加载状态
- 使用图标和文本以提高可读性

### 表单

**输入字段：**
- 字段上方有清晰的标签
- 使用占位符作为提示，而非标签
- 显示焦点状态
- 实时验证输入内容
- 错误信息显示在输入字段附近
- 显示操作成功后的状态

**字段尺寸：**
- 单行输入字段：高度40-48像素
- 文本区域：最小高度80-120像素
- 宽度根据预期输入内容调整

**表单布局：**
- 单列布局以保持简洁
- 将相关字段分组
- 根据需要逐步显示复杂信息
- 保存按钮放在底部，辅助按钮放在旁边

**最佳实践：**
有关验证规则和可访问性的信息，请参阅 [references/forms.md](references/forms.md)

### 卡片（Cards）

**组件结构：**
- 边缘半径：8-12像素（现代风格），0像素（极简风格）
- 内边距：16-24像素
- 阴影：轻微的阴影，最多使用2层
- 背景：略微高于页面背景

**类型：**
- **扁平式：** 无阴影，仅有边框
- **凸起式：** 有轻微阴影
- **交互式：** 鼠标悬停时显示效果，可点击
- **玻璃质感（Glassmorphic）：** 带有模糊效果和透明度

**内容布局：**
- 顶部可以放置图片/图标（可选）
- 标题（标题级别）
- 描述/正文
- 操作按钮位于底部

### 导航

**设计模式：**
- **顶部导航栏：** 全局性的、始终显示的导航栏（网页）
- **标签栏（Tab Bar）：** 包含3-5个主要功能（移动设备）
- **侧边栏（Sidebar）：** 适用于复杂的应用程序，可折叠（桌面设备）
- **汉堡菜单（Hamburger Menu）：** 移动设备的备用导航方式，尽可能避免使用
- **路径导航（Breadcrumb）：** 显示层次结构

**移动设备导航：**
- 底部标签栏（便于拇指操作）
- 滚动菜单用于显示更多选项
- 固定标题栏，包含返回按钮

**桌面设备导航：**
- 顶部导航栏或侧边栏
- 下拉菜单用于展示更多选项
- 搜索框显眼位置

有关导航设计的更多信息，请参阅 [references/navigation-patterns.md](references/navigation-patterns.md)

## 动画与过渡效果

**动画时长：**
- **快速动画：** 100-200毫秒（如按钮点击、鼠标悬停）
- **标准动画：** 200-400毫秒（如页面切换、元素移动）
- **慢速动画：** 400-600毫秒（如页面过渡、复杂效果）

**缓动函数：**
- **缓出（ease-out）：** 大多数动画（开始快，结束慢）
- **缓入（ease-in）：** 退出动画（开始慢，然后加速）
- **平衡缓动（ease-in-out）：** 开始和结束都平滑
- **弹簧效果（spring）：** 自然、有趣的动画效果（使用CSS或JavaScript实现）

**动画原则：**
1. **预提示（Anticipation）：** 提前提示即将发生的改变
2. **动作连贯性（Follow-through）：** 动作自然完成
3. **元素过渡（Continuity）：** 元素平滑过渡
4. **即时反馈（Responsive）：** 用户操作后立即有反馈

**微交互（Micro-interactions）：**
```
button: 150ms [scale: 1→0.95→1] (press)
hover: 200ms [translateY: 0→-2px] + shadow↗
fadeIn: 400ms [opacity: 0→1, translateY: 20→0]
slideIn: 300ms [translateX: -100%→0]
```

**减少动画效果：**
- 提供淡入淡出的替代方案
- 尊重用户设置 `prefers-reduced-motion`
- 仅使用必要的动画效果

有关动画设计的更多信息，请参阅 [references/animation-guide.md](references/animation-guide.md)

## 现代设计趋势

### 暗黑模式（Dark Mode）

**设计策略：**
- 同时测试两种模式
- 使用语义化颜色（自动适应）
- 通过轻微的阴影增强视觉效果
- 避免使用纯黑色 (#000000)，使用深灰色

**颜色搭配建议：**
```css
/* Light mode */
--background: oklch(1 0 0);
--surface: oklch(0.98 0 0);
--text: oklch(0.15 0 0);

/* Dark mode */
--background: oklch(0.145 0 0);
--surface: oklch(0.205 0 0);
--text: oklch(0.985 0 0);
```

有关黑暗模式设计的更多信息，请参阅 [references/dark-mode.md](references/dark-mode.md)

### 玻璃质感（Glassmorphism）

**设计技巧：**
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
}
```

**适用场景：**
- 叠层元素（模态框、工具提示）
- 导航栏
- 背景复杂的卡片元素
- 适合现代、高端的设计风格

**避免使用：**
- 过度使用（会显得刻意）
- 对性能要求较高的场景
- 浏览器支持不足的情况

### 新极简主义（Neo-Brutalism）

**设计特点：**
- 鲜明的阴影（4px×4px，颜色为黑色）
- 鲜艳、饱和度高的颜色
- 黑色边框（2-3像素）
- 边缘半径为0
- 未经修饰的视觉效果

**适用场景：**
- 适合具有创意、年轻化的品牌
- 用于艺术或设计作品集
- 用于与简洁的极简风格形成对比

**更多设计趋势：**
有关更多设计趋势的信息，请参阅 [references/design-trends.md](references/design-trends.md)

## 响应式设计

**断点（Breakpoints）：**
```
Mobile:    < 640px
Tablet:    640px - 1024px
Desktop:   1024px - 1440px
Wide:      > 1440px
```

**以移动设备为先的设计策略：**
```css
/* Base: Mobile */
.container { padding: 16px; }

/* Tablet */
@media (min-width: 640px) {
  .container { padding: 24px; }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { 
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

**响应式布局模式：**
- **单列布局（Mobile）→ 侧边栏布局（Desktop）**
- **网格布局：** 列数从1列增加到4列
- 根据屏幕大小动态显示/隐藏元素

**有关响应式设计的更多信息，请参阅 [references/responsive-design.md](references/responsive-design.md)

## 可访问性（Accessibility）

### WCAG合规性

**最低要求（Level AA）：**
- 文本对比度达到4.5:1
- 大字号文本（18pt及以上）对比度达到3:1
- 支持键盘导航
- 焦点指示器可见
- 图片配有替代文本
- 表单标签清晰可见

**更高要求（Level AAA）：**
- 文本对比度达到7:1
- 大字号文本对比度达到4.5:1
- 无纯音频内容
- 更完善的焦点指示器

**针对屏幕阅读器的最佳实践：**
- 使用语义化的HTML标签（如`<nav>`、`<main>`、`<article>`
- 根据需要使用ARIA标签（如`aria-label`、`aria-labelledby`）
- 逻辑清晰的标题层次结构（h1 → h2 → h3）
- 跳过导航链接
- 动态内容会进行语音提示

**键盘导航：**
- 键盘导航顺序合理
- 焦点位置明显（通过轮廓或自定义方式显示）
- 按下Enter键可以激活按钮/链接
- 使用箭头键操作列表/菜单

**关于动画与过渡效果：**
- 尊重用户设置 `prefers-reduced-motion`
- 提供静态的替代方案
- 避免自动播放视频
- 提供暂停/停止动画的控制选项

有关可访问性的更多信息，请参阅 [references/accessibility.md](references/accessibility.md)

## 设计工具与资源

### 设计系统**
- **Material Design**（谷歌）
- **Apple人类界面指南（Apple HIG）**
- **Fluent Design**（微软）
- **Lightning Design**（Salesforce）
- **Carbon**（IBM）

### 图标库**
- **SF Symbols**（Apple提供，包含6000多个图标）
- **Lucide**（开源图标库，设计简洁）
- **Heroicons**（Tailwind团队开发）
- **Phosphor**（图标库，提供多种样式）
- **Feather**（简单易用的图标库）

### 色彩工具**
- **oklch.com** —— 现代色彩选择工具
- **coolors.co** —— 调色板生成工具
- **contrast-ratio.com** —— WCAG对比度检查工具
- **color.adobe.com** —— Adobe提供的色彩资源

### 字体排版工具**
- **Google Fonts** —— 免费的Web字体库
- **fonts.google.com** —— 字体浏览与搭配工具
- **fontpair.co** —— 字体搭配建议工具
- **typ.io** —— 字体设计灵感来源

### 组件库**
- **Tailwind CSS** —— 以实用组件为主的设计库
- **shadcn/ui** —— 可复用的UI组件库
- **Flowbite** —— Tailwind提供的组件库
- **Radix UI** —— 无头（headless）UI组件库
- **Chakra UI** —— 适合无障碍设计的React组件库

**设计工具与资源的完整列表，请参阅 [references/tools-resources.md](references/tools-resources.md)

## 设计工作流程

### 1. 研究与发现**
- 了解用户需求
- 分析竞争对手
- 定义核心用户流程
- 识别设计限制

### 2. 线框图设计（Wireframing）**
```
┌─────────────────────────────────────┐
│         HEADER / NAV BAR            │
├─────────────────────────────────────┤
│                                     │
│            HERO SECTION             │
│         (Title + CTA)               │
│                                     │
├─────────────────────────────────────┤
│   FEATURE   │  FEATURE  │  FEATURE  │
│     CARD    │   CARD    │   CARD    │
├─────────────────────────────────────┤
│            FOOTER                   │
└─────────────────────────────────────┘
```

### 3. 视觉设计**
- 确定设计主题（颜色、字体、间距）
- 设计关键界面元素
- 创建组件库
- 构建设计系统

### 4. 原型制作（Prototyping）**
- 制作交互式原型
- 进行用户测试
- 根据反馈进行迭代

### 5. 实现（Implementation）**
- 开发响应式网站
- 进行可访问性测试
- 优化性能
- 在不同浏览器上进行测试

**有关详细设计流程的信息，请参阅 [references/design-workflow.md](references/design-workflow.md)

## 平台特定的资源

### Apple平台**
- [Apple人类界面指南完整版](references/apple-platforms.md)
- [iOS设计模式](references/apple-ios.md)
- [macOS设计模式](references/apple-macos.md)
- [watchOS设计模式](references/apple-watchos.md)
- [SF Symbols图标库](references/sf-symbols.md)

### 网页设计**
- [现代网页设计模式](references/web-design.md)
- **CSS架构**（CSS设计规范）
- **JavaScript交互设计**（JavaScript交互效果）
- **性能优化**（网站性能优化）

### 移动网页与Progressive Web Applications (PWA)**
- **响应式设计模式**（responsive design patterns）
- **触摸交互设计**（touch interactions）
- **PWA最佳实践**（PWA开发指南）

## 快速决策指南

**需要选择颜色？**
→ [references/color-systems.md](references/color-systems.md)

**需要设计表单？**
→ [references/forms.md](references/forms.md)

**需要导航设计方案？**
→ [references/navigation-patterns.md](references/navigation-patterns.md)

**需要为iOS平台设计？**
→ [references/apple-platforms.md](references/apple-platforms.md)

**需要制作动画？**
→ [references/animation-guide.md](references/animation-guide.md)

**有关可访问性的问题？**
→ [references/accessibility.md](references/accessibility.md)

**需要实现响应式布局？**
→ [references/responsive-design.md](references/responsive-design.md)

---

## 设计检查清单

✅ **视觉层次结构（Visual Hierarchy）**
- 最重要的元素突出显示
- 相关元素分组合理
- 适当的空白区域有助于提升视觉效果

✅ **一致性（Consistency）**
- 组件的设计和行为一致
- 术语统一
- 视觉语言连贯

✅ **反馈（Feedback）**
- 用户操作有即时反馈
- 加载状态清晰可见
- 错误信息有帮助且易于操作

✅ **可访问性（Accessibility）**
- 支持键盘导航
- 适合屏幕阅读器
- 色彩对比度合适
- 尊重用户偏好

✅ **性能（Performance）**
- 加载速度快（小于3秒）
- 动画流畅（60帧每秒）
- 图像优化
- 布局变化最小

✅ **响应式（Responsive）**
- 在所有屏幕尺寸上都能正常显示
- 适合触摸操作（按钮目标尺寸为44像素）
- 内容能根据屏幕大小自动调整

✅ **平台原生性（Platform Native）**
- 遵循平台规范
- 尽可能使用原生组件
- 尊重系统设置

---

*这是一份集成了Apple人类界面指南、现代网页设计原则和通用用户体验最佳实践的终极UI/UX设计参考手册。*