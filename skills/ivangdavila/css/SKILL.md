---
name: CSS
slug: css
version: 1.0.1
description: 使用正确的堆叠上下文（stacking contexts）、布局模式（layout patterns）、响应式技术（responsive techniques）以及性能优化（performance optimization）来编写现代CSS。
metadata: {"clawdbot":{"emoji":"🎨","os":["linux","darwin","win32"]}}
---

## 使用场景

当用户需要CSS相关专业知识时——无论是解决布局问题还是进行生产环境下的优化，都可以使用该工具。该工具能够处理元素的堆叠顺序、Flexbox/Grid布局模式、响应式设计、性能优化以及可访问性相关问题。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 布局模式 | `layout.md` |
| 响应式技术 | `responsive.md` |
| 选择器与特异性 | `selectors.md` |
| 性能优化 | `performance.md` |

## CSS设计原则

- 布局应具有灵活性——能够适应任何类型的内容，而不仅仅是示例内容。
- 使用现代CSS特性——这些特性的浏览器支持程度比你想象的要好。
- 尽量使用“内在尺寸”（intrinsic sizing）——让内容本身决定元素的尺寸。
- 使用极端情况（如长名称、缺失的图片或空白状态）进行测试。

## 堆叠顺序相关的问题

- `z-index` 仅适用于具有定位属性（`position`）的元素，或者Flexbox/Grid布局中的子元素。
- `isolation: isolate` 会创建一个新的堆叠上下文，导致`z-index`值混乱（即使元素没有`position`属性）。
- 当`opacity < 1`、`transform`或`filter`被应用时，也会创建新的堆叠上下文，从而影响`z-index`的行为。
- 新的堆叠上下文会重置`z-index`的层级关系——即使子元素的`z-index`设置为9999，也无法覆盖父元素的`z-index`。

## 布局相关的问题

- `margin`的合并（margin collapse）仅发生在垂直方向，且仅适用于块级元素（block-level elements）；Flexbox/Grid布局中的子元素不受此规则影响。
- 在Flexbox容器上使用`overflow: hidden`可能会导致布局问题——如果不需要滚动功能，建议使用`overflow: clip`。

## Flexbox相关的问题

- `flex: 1` 实际上表示 `flex: 1 1 0%`——这里的“1”是指基准值（basis），而不是自动分配的宽度（auto）。
- 如果为Flexbox子元素设置`min-width: 0`，可能会导致文本被截断；默认情况下，`min-width`的值是`min-content`。
- `flex-basis` 和 `width` 的区别在于：`flex-basis`是在元素扩展或收缩之前确定的尺寸，而`width`是在之后确定的；通常推荐使用`flex-basis`。
- 现在`gap`属性也可以用于Flexbox布局中——不再需要通过`margin`来调整元素间距。

## Grid布局相关的问题

- `fr`单位不会自动考虑到`min-content`的值；建议使用`minmax(min-content, 1fr)`来设置元素的宽度。
- `auto-fit` 和 `auto-fill` 的区别在于：`auto-fit`会合并空的网格单元格，而`auto-fill`会保留这些单元格。
- `grid-template-columns: 1fr 1fr` 并不等于50%；它表示剩余空间的平均分配。
- 隐式的网格单元格（implicit grid tracks）可能会带来意外的布局效果——即使元素被放置在显式的网格单元格之外，它们仍然会显示在布局中。

## 响应式设计的原则

- 应该优先考虑移动设备的布局需求——使用`min-width`媒体查询为移动设备设置基础样式。
- 使用容器查询（container queries）：例如`@container (min-width: 400px)`来实现基于容器的响应式设计。
- 确保父元素具有`container-type: inline-size`属性，才能使容器查询生效。
- 在真实设备上进行测试——模拟器无法准确模拟触控操作和实际的页面性能。

## 尺寸设置相关函数

- `clamp(min, preferred, max)` 用于实现流动式的文本排版——例如 `clamp(1rem, 2.5vw, 2rem)`。
- `min()` 和 `max()` 可以简化尺寸设置——例如 `width: min(100%, 600px)` 可以替代媒体查询。
- `fit-content` 可以根据内容自动调整元素的大小，最大值为`max`值——例如 `width: fit-content` 或 `width: fit-content(300px)`。

## 现代CSS选择器

- `:is()` 可用于组合多个选择器——例如 `:is(h1, h2, h3) + p` 可以减少代码重复。
- `:where()` 的特异性为0，因此更容易被覆盖。
- `:has()` 是一个用于检测父元素属性的选择器——例如 `.card:has(img)` 可以为包含图片的卡片元素设置样式。
- `:focus-visible` 仅用于表示元素在键盘焦点下的可见性——鼠标点击时不会显示轮廓。

## 滚动行为相关设置

- `scroll-behavior: smooth` 可使滚动效果更加平滑。
- `overscroll-behavior: contain` 可防止滚动行为影响到父元素或整个页面。
- `scroll-snap-type` 和 `scroll-snap-align` 可实现无需JavaScript的滚动效果。
- `scrollbar-gutter: stable` 可确保滚动条的位置稳定，避免布局变形。

## 简写语法相关的问题

- `inset: 0` 等同于 `top/right/bottom/left: 0`——减少代码重复。
- `place-items` 实际上是 `align-items` 和 `justify-items` 的组合——例如 `place-items: center` 可以同时居中元素。
- `margin-inline` 和 `margin-block` 分别用于设置元素的水平/垂直内边距（margin），这些属性会考虑文本的书写方向。

## 性能优化相关建议

- 使用`contain: layout` 可以减少不必要的重绘操作——尤其适用于独立的组件。
- `content-visibility: auto` 可避免不必要的离屏渲染——对于长页面来说非常有用。
- 谨慎使用`will-change`属性——它可能会创建额外的渲染层并占用更多内存。
- 避免频繁地修改DOM结构——尽量批量读取和写入DOM数据。

## 可访问性相关的基本要求

- `prefers-reduced-motion` 可以为有前庭功能障碍的用户禁用动画效果。
- `prefers-color-scheme` 可根据用户偏好设置页面颜色方案（例如 `@media (prefers-color-scheme: dark)` 用于暗色模式）。
- `forced-colors: active` 可以调整页面的颜色对比度以适应高对比度显示环境。
- 焦点指示器必须可见——不要仅依赖颜色来判断元素的可见性。