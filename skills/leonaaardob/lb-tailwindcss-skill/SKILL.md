---
name: tailwind
description: 完整的 Tailwind CSS 文档。适用于使用 Tailwind CSS 实用类、响应式设计、暗黑模式、动画、自定义配置、插件或遇到样式相关问题时的参考。涵盖了所有实用类、修饰符、配置选项以及最佳实践。
---

# Tailwind CSS 文档

本文档采用 Markdown 格式编写，完整地介绍了 Tailwind CSS 的各项功能。您可以通过阅读 `references/` 目录中的文件来了解关于实用类（utility classes）、响应式设计（responsive design）、自定义（customization）以及最佳实践（best practices）的相关信息。

## 文档结构

所有文档都存储在 `references/` 目录下，每个实用功能或概念都有一个对应的单独文件：

### 核心概念（Core Concepts）
- `installation.mdx`：安装与配置
- `editor-setup.mdx`：集成开发环境（IDE）的配置
- `using-with-preprocessors.mdx`：SCSS 与 PostCSS 的集成方式
- `optimizing-for-production.mdx`：针对生产环境的优化设置
- `browser-support.mdx`：浏览器兼容性说明

### 布局与间距（Layout & Spacing）
- `container.mdx`、`columns.mdx`：布局相关实用类
- `aspect-ratio.mdx`：宽高比控制
- `box-sizing.mdx`：盒模型（box model）
- `display.mdx`：显示属性（display properties）
- `float.mdx`、`clear.mdx`：浮动（floats）效果
- `position.mdx`：定位（positioning）
- `top-right-bottom-left.mdx`：内边距（inset）实用类
- `visibility.mdx`、`z-index.mdx`：Z 层次与可见性（Z-index and visibility）
- `padding.mdx`、`margin.mdx`：间距设置（spacing）
- `space-between.mdx`：元素间的间距调整（gap utilities）

### Flexbox 与 Grid
- `flex-direction.mdx`、`flex-wrap.mdx`、`flex.mdx`：Flexbox 布局
- `flex-grow.mdx`、`flex-shrink.mdx`、`flex-basis.mdx`：弹性盒子大小调整（flex sizing）
- `order.mdx`：Flexbox 或 Grid 中元素的排列顺序（flex/grid order）
- `grid-template-columns.mdx`、`grid-template-rows.mdx`：网格布局（grid layout）
- `grid-column.mdx`、`grid-row.mdx`：网格单元格的定位（grid placement）
- `gap.mdx`：网格或 Flexbox 中的间距（grid/flex gap）
- `justify-content.mdx`、`justify-items.mdx`、`justify-self.mdx`：内容对齐方式（justify）
- `align-content.mdx`、`align-items.mdx`、`align-self.mdx`：元素对齐方式（align）
- `place-content.mdx`、`place-items.mdx`、`place-self.mdx`：元素放置位置（place）

### 字体样式（Typography）
- `font-family.mdx`、`font-size.mdx`、`font-weight.mdx`：字体设置
- `font-smoothing.mdx`、`font-style.mdx`、`font-variant-numeric.mdx`：字体平滑效果、样式与数字显示
- `letter-spacing.mdx`、`line-height.mdx`、`line-clamp.mdx`：字符间距与行高
- `list-style-type.mdx`、`list-style-position.mdx`：列表样式
- `text-align.mdx`、`text-color.mdx`、`text-decoration.mdx`：文本对齐与颜色
- `text-transform.mdx`、`text-overflow.mdx`、`text-wrap.mdx`：文本转换与换行
- `text-indent.mdx`、`vertical-align.mdx`、`whitespace.mdx`：文本缩进与空白符处理
- `word-break.mdx`、`hyphens.mdx`：单词断行与连字符使用

### 背景（Backgrounds）
- `background-attachment.mdx`、`background-clip.mdx`：背景属性
- `background-color.mdx`、`background-origin.mdx`：背景颜色与来源
- `background-position.mdx`、`background-repeat.mdx`：背景位置与重复方式
- `background-size.mdx`、`background-image.mdx`：背景图片设置
- `gradient-color-stops.mdx`：渐变效果设置

### 边框（Borders）
- `border-radius.mdx`、`border-width.mdx`、`border-color.mdx`：边框样式
- `border-style.mdx`、`divide-width.mdx`、`divide-color.mdx`：边框与分割线样式
- `divide-style.mdx`、`outline-width.mdx`、`outline-color.mdx`：轮廓线样式
- `outline-style.mdx`、`outline-offset.mdx`、`ring-width.mdx`：轮廓线偏移与宽度
- `ring-color.mdx`、`ring-offset-width.mdx`、`ring-offset-color.mdx`：边框内环的样式与偏移

### 效果与滤镜（Effects & Filters）
- `box-shadow.mdx`、`box-shadow-color.mdx`：阴影效果
- `opacity.mdx`、`mix-blend-mode.mdx`、`background-blend-mode.mdx`：透明度与混合模式
- `filter.mdx`：滤镜应用
- `blur.mdx`、`brightness.mdx`、`contrast.mdx`、`grayscale.mdx`：模糊、亮度、对比度与灰度效果
- `hue-rotate.mdx`、`invert.mdx`、`saturate.mdx`、`sepia.mdx`：色调变换与饱和度调整
- `backdrop-filter.mdx`：背景滤镜
- `backdrop-blur.mdx`、`backdrop-brightness.mdx`：背景模糊与亮度调整

### 过渡与动画（Transitions & Animations）
- `transition-property.mdx`、`transition-duration.mdx`：过渡属性与持续时间
- `transition-timing-function.mdx`、`transition-delay.mdx`：过渡效果的时间函数与延迟
- `animation.mdx`：动画效果的定义与应用

### 变形（Transforms）
- `scale.mdx`、`rotate.mdx`、`translate.mdx`、`skew.mdx`：元素变形方式
- `transform-origin.mdx`：变形原点设置

### 交互性（Interactivity）
- `accent-color.mdx`、`appearance.mdx`、`cursor.mdx`：强调色与鼠标指针样式
- `caret-color.mdx`、`pointer-events.mdx`：光标样式与事件处理
- `resize.mdx`：元素大小调整
- `scroll-behavior.mdx`、`scroll-margin.mdx`、`scroll-padding.mdx`：滚动行为与内边距
- `scroll-snap-align.mdx`、`scroll-snap-stop.mdx`、`scroll-snap-type.mdx`：滚动定位与停止方式
- `touch-action.mdx`、`user-select.mdx`、`will-change.mdx`：触摸交互与选择事件

### 自定义（Customization）
- `adding-custom-styles.mdx`：自定义 CSS 样式
- `configuration.mdx`：`tailwind.config.js` 配置文件
- `content-configuration.mdx`：内容样式配置
- `theme.mdx`：主题样式定制
- `screens.mdx`：屏幕分辨率适配
- `colors.mdx`：颜色调色板
- `spacing.mdx`：间距调整规则
- `plugins.mdx`：插件系统
- `presets.mdx`：预设样式配置

### 高级功能（Advanced Features）
- `dark-mode.mdx`：暗黑模式设置
- `reusing-styles.mdx`：组件样式复用
- `functions-and-directives.mdx`：`@apply`、`@layer` 等辅助函数与指令

## 快速参考

### 常见任务（Common Tasks）
- 设置 Tailwind CSS：`installation.mdx`
- 实现响应式设计：`responsive-design.mdx`、`screens.mdx`
- 开启暗黑模式：`dark-mode.mdx`
- 自定义颜色：`customizing-colors.mdx`、`colors.mdx`
- 使用布局实用类：`container.mdx`、`display.mdx`、`position.mdx`
- 使用 Flexbox：`flex-direction.mdx`、`justify-content.mdx`、`align-items.mdx`
- 使用 Grid：`grid-template-columns.mdx`、`gap.mdx`
- 调整字体样式：`font-size.mdx`、`font-weight.mdx`、`text-color.mdx`
- 调整间距：`padding.mdx`、`margin.mdx`、`space-between.mdx`
- 设置背景：`background-color.mdx`、`background-image.mdx`
- 设定边框：`border-width.mdx`、`border-color.mdx`、`border-radius.mdx`
- 应用阴影效果：`box-shadow.mdx`
- 定义过渡效果：`transition-property.mdx`
- 自定义配置：`configuration.mdx`、`theme.mdx`
- 开发插件：`plugins.mdx`

### 使用建议

- 当需要使用 Tailwind CSS 的实用类时，请参考相关文件。
- 遇到响应式设计相关问题时，可查阅 `responsive-design.mdx` 和 `screens.mdx`。
- 如需启用暗黑模式，请参考 `dark-mode.mdx`。
- 如需自定义 Tailwind 的配置，请查看 `configuration.mdx` 和 `theme.mdx`。
- 如需开发插件或进行样式迁移，请参考 `plugins.mdx`。

### 查找文档的方法

1. **查找特定实用类**：直接通过文件名（如 `flex.mdx`、`text-color.mdx`）查找相关文档。
2. **了解概念**：查阅对应的概念文件（如 `installation`、`dark-mode`、`responsive-design`）。
3. **进行自定义设置**：查看配置文件（`configuration`、`theme`、`plugins`）。
4. **学习最佳实践**：阅读 `reusing-styles`、`adding-custom-styles` 等相关文档。

所有文档均为 `.mdx` 格式（Markdown + JSX），但也可以直接以纯 Markdown 格式阅读。