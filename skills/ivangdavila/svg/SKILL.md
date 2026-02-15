---
name: SVG
description: 创建并优化 SVG 图形，确保其具有正确的 `viewBox` 属性、良好的可访问性（accessibility）以及美观的 CSS 样式。
metadata: {"clawdbot":{"emoji":"📐","requires":{},"os":["linux","darwin","win32"]}}
---

## viewBox 的基础知识

```svg
<svg viewBox="min-x min-y width height">
```

- `viewBox` 定义了 SVG 图形的内部坐标系统。
- `<svg>` 标签中的 `width` 和 `height` 属性定义了 SVG 图形的显示尺寸。
- 如果不设置 `viewBox`，SVG 图形将无法根据屏幕大小进行自适应缩放。

```svg
<!-- ✅ Scales to any size -->
<svg viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="10"/>
</svg>

<!-- ❌ Fixed 24x24, won't scale -->
<svg width="24" height="24">
  <circle cx="12" cy="12" r="10"/>
</svg>
```

务必为所有的 SVG 图形添加 `viewBox`。对于需要自适应显示的 SVG 图形，应移除固定的 `width` 和 `height` 属性。

## 坐标必须与 viewBox 保持一致

位于 `viewBox` 范围之外的 SVG 元素将无法被显示：

```svg
<!-- ❌ Circle at 500,500 but viewBox only covers 0-100 -->
<svg viewBox="0 0 100 100">
  <circle cx="500" cy="500" r="40"/>  <!-- invisible -->
</svg>

<!-- ✅ Circle within viewBox range -->
<svg viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40"/>
</svg>
```

## 可访问性

- **具有信息性的 SVG 图形（用于传达具体含义）：** [相关说明](...)
- **仅用于装饰的 SVG 图形（纯粹用于视觉效果）：** [相关说明](...)

**关键规则：**
- 使用 `role="img"` 可以确保辅助技术将 SVG 图形视为普通图片。
- `<title>` 标签必须是 `<svg>` 标签的第一个子元素。
- 对于 SVG 图形而言，`aria-labelledby` 比 `aria-label` 更可靠。
- 设置 `focusable="false"` 可以防止在 Internet Explorer 或 Edge 浏览器中通过 Tab 键选中 SVG 元素。
- 页面上所有内联 SVG 图形的 ID 必须唯一。

## CSS 样式设置

- **颜色继承：** [相关说明](...)
- **在 SVG 内部定义自定义 CSS 属性：** [相关说明](...)
- **注意限制：**
  - 使用 `<img src="icon.svg">` 无法通过 CSS 进行样式设置。
  - `background-image: url'icon.svg)` 也无法通过 CSS 进行样式设置。
  - 只有内联 SVG 图形才能完全接受 CSS 的样式控制。

## SVGO 优化

为了保留 SVG 图形的功能，需要正确配置 SVGO（一种 SVG 优化工具）：

```javascript
// svgo.config.mjs
export default {
  plugins: [{
    name: 'preset-default',
    params: {
      overrides: {
        removeViewBox: false,      // NEVER remove
        removeTitle: false,        // Keep for accessibility
        removeDesc: false,         // Keep for accessibility
        cleanupIds: false,         // Keep if CSS/JS references IDs
      }
    }
  }]
};
```

可以安全地删除的元素包括元数据、注释、空的 `<group>` 标签以及编辑器生成的多余内容。通过 SVGO 优化，Illustrator 或 Figma 导出的 SVG 文件通常可以减少 50% 到 80% 的文件大小。

## SVG 的嵌入方法

| 嵌入方法 | CSS 样式支持 | 缓存支持 | 适用场景 |
|--------|-------------|---------|----------|
| 内联 `<svg>` | ✅ 完全支持 | ❌ 不支持 | 需要动态样式或动画的 SVG 图形 |
| 使用 `<img src>` | ❌ 不支持 | ✅ 支持 | 静态图片 |
| 使用 `<use>` 标签引入符号精灵（Symbol Sprites） | ✅ 部分支持 | ✅ 适用于图标系统 |
| 作为 CSS 背景图片使用 | ❌ 不支持 | ✅ 支持 | 用于装饰性图案 |

## 性能测试

（以 1000 个 SVG 图标为例）：
- 使用 `<img>` 标签并设置 data URI：67 毫秒（最快）
- 优化后的内联 SVG：75 毫秒
- 使用符号精灵：99 毫秒
- 外部 SVG 文件（如外部 sprite）：126 毫秒（在 Chrome 浏览器中表现非常慢）

对于大量重复使用的图标，建议使用符号精灵；对于少量图标，内联 SVG 是一个合适的选择。

## 命名空间

外部 `.svg` 文件需要指定 `xmlns` 属性：

```svg
<!-- ✅ Works as external file -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">

<!-- ❌ May fail when loaded externally -->
<svg viewBox="0 0 24 24">
```

在 HTML5 中，内联 SVG 图形不需要指定 `xmlns`，但加上它也不会造成问题。

## 常见错误：
- 未设置 `viewBox`：SVG 图形会以固定大小显示，或者根本无法显示。
- 坐标超出 `viewBox` 范围：相关元素将无法被显示。
- 硬编码填充颜色（如 `fill="#000"`）：无法通过 CSS 进行颜色调整。
- 在需要应用 CSS 样式的场景中使用 `<img>` 标签：会导致 CSS 无法生效。
- 在部署前未检查 SVG 文件中的 `viewBox` 或 `title` 属性：可能导致样式问题。
- 在多个内联 SVG 中使用重复的 ID：会导致 CSS 或 JavaScript 代码出错。
- 误设置 `preserveAspectRatio="none"`：会导致图形失真。
- 使用错误的 `viewBox` 单位（如 `viewBox="0 0 100px 100px"`）：`viewBox` 应使用无单位的值。
- 编辑器生成的空 `<group>` 或路径：会无谓地增加文件大小。