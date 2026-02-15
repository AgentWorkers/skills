---
name: Icons
description: 实现可访问的图标，确保其具有合适的尺寸、颜色继承功能以及良好的性能。
metadata: {"clawdbot":{"emoji":"🔣","requires":{},"os":["linux","darwin","win32"]}}
---

## SVG 与图标字体

SVG 是现代的标准选择：
- 更好的可访问性（原生支持 ARIA）
- 不会出现不可见或错误的图标显示问题（FOIT 问题）
- 支持多色显示
- 通过代码优化（tree-shaking）可以减小文件大小

只有在需要兼容旧版 IE11 的情况下，才考虑使用图标字体。

## 可访问性最佳实践

**装饰性图标（位于可见文本旁边）：**
```html
<button>
  <svg aria-hidden="true" focusable="false">...</svg>
  Save
</button>
```

**信息性图标（独立显示，无需标签）：**
```html
<button aria-label="Save document">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- Or with visually hidden text -->
<button>
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">Save document</span>
</button>
```

**带有可访问性名称的 SVG：**
```html
<svg role="img" aria-labelledby="icon-title">
  <title id="icon-title">Warning: system error</title>
  <!-- paths -->
</svg>
```

**重要规则：**
- 对于重复显示可见文本的 SVG，应设置 `aria-hidden="true"`；
- 设置 `focusable="false"` 可以避免在 IE/Edge 浏览器中不必要的焦点停顿；
- 为了支持屏幕阅读器，`<title>` 标签必须作为 `<svg>` 元素的第一个子元素；
- 如果有多个 SVG 元素内联显示，它们的 ID 必须唯一。

## 颜色继承

`currentColor` 会从 CSS 的 `color` 属性继承颜色。当鼠标悬停时，图标的颜色会自动改变：

```svg
<svg fill="currentColor">
  <path d="..."/>
</svg>
```

在使用 `currentColor` 之前，请先删除 SVG 中硬编码的 `fill="#000"`。

对于基于描边的图标，应使用 `stroke="currentColor"`。

## 图标尺寸

标准的网格尺寸为：16px、20px、24px、32px。

根据图标尺寸调整描边粗细：
| 尺寸 | 描边粗细 | 使用场景 |
|------|--------|----------|
| 16px | 1px | 密集布局、小字号文本 |
| 20px | 1.25px | 默认用户界面元素 |
| 24px | 1.5px | 按钮、主要操作按钮 |
| 32px | 2px | 标题、导航链接 |

可点击的图标至少需要 44x44px 的尺寸；如果可点击区域通过内边距扩大，图标尺寸可以更小。

```css
.icon-button {
  width: 24px;
  height: 24px;
  padding: 10px; /* Creates 44x44 touch target */
}
```

## 图标与文本的缩放

图标会自动根据周围文本的大小进行缩放。

## 符号精灵（Symbol Sprites）

对于大量重复使用的图标，可以使用符号精灵来减少 DOM 节点：

```html
<!-- Define once, hidden -->
<svg style="display:none">
  <symbol id="icon-search" viewBox="0 0 24 24">
    <path d="..."/>
  </symbol>
  <symbol id="icon-menu" viewBox="0 0 24 24">
    <path d="..."/>
  </symbol>
</svg>

<!-- Use anywhere -->
<svg aria-hidden="true"><use href="#icon-search"/></svg>
```

外部符号精灵（如 `<use href="/icons.svg#search"/>`）在没有 polyfill 的旧版 Safari 浏览器中无法正常工作。

## 性能测试

（针对 1000 个图标的性能测试结果）：
- 使用 data URI 的 `<img>`：67ms（最快）
- 优化后的内联 SVG：75ms
- 符号精灵：99ms
- 外部链接的 `<img>`：76ms

**建议：**
- 使用支持 tree-shaking 功能的图标库（例如 Lucide、Heroicons）；
- 不要导入整个 Font Awesome 图标集（通常超过 1MB）——仅使用其中的一部分，或改用 SVG 图标；
- 对于关键图标使用内联方式，对于非关键图标则使用懒加载的符号精灵。

## 一致性原则

- 保持图标风格的统一性——混用不同风格的图标会显得不专业；
- 将图标的描边粗细与字体粗细相匹配（普通文本对应的描边粗细为 1.5px）；
- 根据使用场景选择图标样式：非活动状态使用轮廓线样式，活动状态使用实心填充样式；
- 注意图标的视觉对齐方式：圆形图标会填充到边框内，而方形图标则不会；
- 为图标命名时应根据其外观，而非含义（例如，将图标命名为“stopwatch”而非“speed”）。

## 常见错误

- 装饰性图标缺少 `aria-hidden` 属性——会导致屏幕阅读器读取到无意义的文字；
- 在同一界面中混用不同风格的图标（圆形和方形）；
- 为 10 个图标创建庞大的图标库——会导致文件体积过大；
- 仅使用图标作为按钮且没有可访问性名称——屏幕阅读器无法识别这些按钮；
- 硬编码的颜色设置会妨碍主题切换；
- 描边宽度不随图标尺寸变化——例如，16px 的图标如果使用 2px 的描边会显得过于厚重。