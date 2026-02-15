---
name: CSS
description: 避免常见的CSS陷阱——例如层叠上下文（stacking context）问题、布局上的怪异现象，以及那些未被充分利用的现代CSS特性。
metadata: {"clawdbot":{"emoji":"🎨","os":["linux","darwin","win32"]}}
---

## 堆叠上下文（Stacking Context）
- `z-index` 仅适用于具有定位属性的元素，或者属于 Flex 或 Grid 布局中的子元素。
- `isolation: isolate` 会创建一个新的堆叠上下文，这会导致 `z-index` 的混乱（即使元素没有使用定位属性）。
- 当 `opacity < 1`、`transform` 或 `filter` 被应用时，也会创建一个新的堆叠上下文，从而可能导致 `z-index` 的行为不可预测。
- 新的堆叠上下文会重置 `z-index` 的层级关系：子元素的 `z-index` 为 `9999` 也不会影响到其父元素。

## 布局中的常见陷阱（Layout Gotchas）
- `margin` 的合并（margin collapse）仅发生在垂直方向上，且仅适用于块级元素；Flex 或 Grid 布局中的子元素不会触发这种合并。
- `gap` 现在可以在 Flex 布局中使用了，因此不再需要使用 `margin` 来调整元素间距。
- `flex-basis` 和 `width` 的区别在于：`flex-basis` 是在元素伸缩之前计算的，而 `width` 是在伸缩之后计算的；在 Flex 布局中推荐使用 `flex-basis`。
- 对于 Flex 布局中的文本元素，如果设置 `min-width: 0`，文本可能会被截断；默认情况下，`min-width` 的值是 `min-content`。
- 如果 Flex 容器的 `overflow` 设置为 `hidden`，可能会导致布局问题；如果不需要滚动，可以使用 `overflow: clip`。

## 尺寸调整函数（Sizing Functions）
- `clamp(min, preferred, max)` 可用于实现自适应的文本样式（例如：`clamp(1rem, 2.5vw, 2rem)`）。
- `min()` 和 `max()` 可用于设置元素的宽度：`width: min(100%, 600px)` 可以替代媒体查询（media queries）。
- `fit-content` 可使元素的大小适应其内容，最大值为指定的值（例如：`width: fit-content` 或 `width: fit-content(300px)`）。

## 现代选择器（Modern Selectors）
- `:is()` 用于元素分组（例如：`:is(h1, h2, h3) + p` 可减少代码重复）。
- `:where()` 与 `:is()` 功能相同，但特异性为 0，因此更容易被覆盖。
- `:has()` 是一个父元素选择器，用于选择包含特定元素的子元素（例如：`.card:has(img)` 用于选择包含图片的卡片）。
- `:focus-visible` 仅针对键盘焦点生效，鼠标点击时不会显示轮廓。

## 无需媒体查询的响应式设计（Responsive Without Media Queries）
- `aspect-ratio` 是一个原生的 CSS 属性，可以直接设置元素的宽高比（例如：`aspect-ratio: 16/9`）。
- 使用容器查询（container queries）实现响应式设计（例如：`@container (min-width: 400px)`）。
- 父元素需要设置 `container-type: inline-size`，才能使容器查询生效。

## 滚动行为（Scroll Behavior）
- `scroll-behavior: smooth` 可让锚点滚动更加平滑。
- `overscroll-behavior: contain` 可防止滚动行为影响到父元素或整个页面。
- `scroll-snap-type` 和 `scroll-snap-align` 可实现原生的轮播效果，无需使用 JavaScript。
- `scrollbar-gutter: stable` 可确保滚动条的位置固定，防止布局发生偏移。

## 性能优化（Performance）
- `contain: layout` 可隔离布局的重计算，提高性能；`contain: strict` 可实现更严格的布局隔离。
- `content-visibility: auto` 可避免渲染屏幕外的内容，从而节省大量绘制资源（尤其是在长页面上）。
- `will-change` 属性可以提示 compositor（图形系统）进行布局更新，但不要过度使用，否则可能会增加性能开销。

## 可访问性（Accessibility）
- `prefers-reduced-motion: reduce` 可为有前庭障碍的用户禁用动画效果。
- `prefers-color-scheme` 可设置首选的颜色方案（例如：`@media (prefers-color-scheme: dark)`）。
- `forced-colors` 可在需要高对比度模式下强制使用特定的颜色（例如：`@media (forced-colors: active)`。

## 缩写技巧（Shorthand Traps）
- `inset: 0` 等同于 `top/right/bottom/left: 0`，可以减少代码重复。
- `place-items` 实际上是 `align-items` 和 `justify-items` 的组合，用于设置元素的排列方式（例如：`place-items: center` 可使元素居中）。
- `margin-inline` 和 `margin-block` 分别用于设置元素的水平/垂直内边距，这些属性会考虑文本的书写方向。