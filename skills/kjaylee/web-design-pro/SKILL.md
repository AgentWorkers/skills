---
name: web-design-pro
description: 现代网页设计工程技能包括设计规范（design tokens）、先进的用户界面/用户体验（UI/UX）方法论、可访问性（accessibility）以及针对特定类型应用（如游戏）的UI设计模式。这些技能用于开发具有商业竞争力、高性能且符合可访问性标准的网页界面。
metadata:
  author: misskim
  version: "1.0"
  origin: Synthesized from 2024-2026 web design standards research
---

# Web Design Pro (现代设计工程)

这不仅仅是一套关于网页设计的技能集，它还整合了系统设计、性能优化、可访问性以及专为游戏设计的用户体验（UX）等方面的专业技术。

## 1. 设计系统与设计令牌（Design Systems & Tokens）

通过将设计决策数据化，消除了设计与代码之间的隔阂。

### 设计令牌的层次结构
- **基础令牌（Primitive Tokens）：** 基本值（例如：`blue-500: #3B82F6`）
- **语义令牌（Semantic Tokens）：** 赋予元素特定的含义和用途（例如：`action-primary: var(--blue-500)`）
- **组件令牌（Component Tokens）：** 专为特定组件设计的令牌（例如：`btn-bg: var(--action-primary)`）

### 实现指南
- **CSS自定义属性（CSS Custom Properties）：** 使用浏览器内置的令牌实现实时主题切换。
- **Tokens Studio（Figma）：** 直接从设计源代码中提取JSON/CSS数据。
- **自动化流程：** 当令牌发生变化时，通过`Style Dictionary`等工具在构建时自动更新各个平台的样式。

---

## 2. 现代用户体验方法论（Modern UX Methodologies）

这套方法论旨在解决用户的“实际”问题。

### 主要方法论
- **“待办事项”（Jobs to Be Done, JTBD）：** “玩家不想阅读游戏介绍，他们希望能在3秒内判断游戏是否有趣。” → 因此在“Hero”区域放置游戏实况视频而非文字。
- **设计思维（Design Thinking）：** 通过共鸣、定义、构思、原型制作和测试的循环来推进设计。
- **设计冲刺（Design Sprints）：** 在2到5天内验证核心假设的快速迭代过程。

---

## 3. 响应式设计模式（Responsive Design Patterns）

利用现代CSS技术，确保所有设备上都能呈现完美的布局。

### 流动式排版与布局（Fluid Typography & Layout）
- **使用`clamp()`函数：** 不需要媒体查询，即可根据屏幕大小动态调整字体大小和间距。
  ```css
  h1 { font-size: clamp(2rem, 5vw + 1rem, 4rem); }
  ```
- **容器查询（Container Queries）：** 组件的布局会根据父容器的大小而非视口大小进行调整。
- **以移动设备为先（Mobile-First）：** 先设计320px分辨率的移动版布局，然后通过`@media (min-width: ...)`逐步扩展到其他屏幕。

---

## 4. 可访问性标准（Accessibility Standards - WCAG 2.1）

确保没有用户被设计所排斥。

### 关键检查点
- **语义化HTML（Semantic HTML）：** 使用`<nav>`、`<main>`、`<article>`、`<section>`等标签来明确页面结构。
- **颜色对比度（Color Contrast）：** 文本与背景的颜色对比度至少为4.5:1（符合AA级可访问性标准）。
- **键盘友好性（Keyboard Friendly）：** 所有交互操作都应支持Tab/Enter键。
- **ARIA标签（ARA Labels）：** 为仅有图标的按钮添加`aria-label`属性。
- **减少动画效果（Reduced Motion）：** 通过`prefers-reduced-motion`设置来控制动画的播放。

---

## 5. 性能与网页核心指标（Performance & Web Vitals）

速度直接影响用户体验。

### 2024年的核心网页性能指标（Core Web Vitals）
- **LCP（Largest Contentful Paint）：** 最大内容绘制时间小于2.5秒。
- **INP（Interaction to Next Paint）：** 用户交互后的响应时间小于200毫秒（替代FID指标）。
- **CLS（Cumulative Layout Shift）：** 布局抖动小于0.1。

### 优化技巧
- **图片优化（Image Optimization）：** 使用WebP/AVIF格式压缩图片，并指定`width`和`height`以避免布局抖动。
- **预加载（Preload）：** 首先加载关键字体和游戏封面图片。
- **延迟加载JavaScript（Defer JS）：** 将非必要的脚本设置为`defer`或`async`加载。

---

## 6. 专为游戏设计的UI/UX（Game UI/UX Specifics）

这些技巧旨在提升玩家的沉浸感。

### 游戏UI设计原则
- **即时反馈（Immediate Feedback）：** 所有点击或悬停操作都应立即有视觉/听觉反馈。
- **视觉层次结构（Visual Hierarchy）：** 最重要的操作（如“立即播放”）应置于页面最显眼的位置。
- **沉浸式布局（Immersive Layout）：** UI的设计应与游戏世界的纹理、字体和色调保持一致。

---

## 7. 适用于eastsea.monster Redesign的实用技能

以下是三项可以立即应用的技能：
1. **流动式排版（Fluid Typography）：** 使用`clamp()`函数统一所有页面的字体大小，实现流畅的移动端与桌面端切换。
2. **WebP批量转换（WebP Batch Conversion）：** 将所有游戏缩略图和资源转换为WebP格式，以优化LCP性能。
3. **自动播放游戏视频（Hero Video Autoplay）：** 在“Hero”区域播放静音的游戏实况视频（遵循JTBD原则）。

---

## 游戏作品集的最佳实践检查清单（Best-Practice Checklist for Game Portfolio）
- [ ] “Hero”区域是否包含静音的游戏实况视频？
- [ ] 主要字体是否通过`clamp()`函数实现动态调整？
- [ ] 所有图片是否采用WebP格式，并指定了`width`和`height`？
- [ ] 是否仅通过Tab键即可选择和播放所有游戏？
- [ ] 悬停按钮是否有响应效果（如缩放或发光）？
- [ ] 使用Lighthouse工具进行的可访问性测试得分是否超过90分？
- [ ] 启用`prefers-reduced-motion`设置后，动画效果是否被关闭？