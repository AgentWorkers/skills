---
name: ui-skills
description: 这些带有主观观点的约束条件旨在帮助构建与代理（agents）更优秀的交互界面。
---

# 用户界面（UI）技能

以下是一系列关于构建更好用户界面的建议和规范：

## 样式框架（Style Framework）

- 在使用自定义样式之前，必须先使用 Tailwind CSS 的默认样式（如间距、圆角、阴影等）。
- 当需要 JavaScript 动画时，必须使用 `motion/react`（以前称为 `framer-motion`）。
- 对于元素的进入动画及微动画，建议使用 `tw-animate-css`。
- 用于类逻辑的辅助函数（如 `clsx` 和 `tailwind-merge`）是必须使用的。

## 组件（Components）

- 对于任何需要支持键盘操作或焦点功能的组件，必须使用可访问性良好的基础组件（如 `Base UI`、`React Aria`、`Radix`）。
- 在使用新的组件时，应优先考虑项目中已有的基础组件。
- 同一个交互界面内，严禁混合使用不同的组件系统。
- 如果新组件与当前样式框架兼容，建议优先选择 [`Base UI`](https://base-ui.com/react/components)。
- 对于仅显示图标的按钮，必须添加 `aria-label` 属性。
- 除非有明确需求，否则严禁手动重新实现键盘操作或焦点功能。

## 交互（Interaction）

- 对于具有破坏性或不可逆的操作，必须使用 `AlertDialog` 来提示用户。
- 在显示加载状态时，应使用结构化的布局框架。
- 绝不要使用 `h-screen`，而应使用 `h-dvh`。
- 固定元素的布局必须遵循 `safe-area-inset` 的规则。
- 错误信息应显示在用户操作发生的位置附近。
- 绝不要阻止 `input` 或 `textarea` 元素中的粘贴操作。

## 动画（Animation）

- 除非有明确的需求，否则严禁添加动画效果。
- 只能对组件的可组合属性（如 `transform`、`opacity`）进行动画处理。
- 绝不要对布局属性（如 `width`、`height`、`top`、`left`、`margin`、`padding`）进行动画处理。
- 除非是针对小范围的局部 UI（如文本、图标），否则应避免对背景颜色（`background`、`color`）进行动画处理。
- 进入动画应使用 `ease-out` 过渡效果。
- 交互反馈的动画时长不得超过 200 毫秒。
- 当元素离开屏幕时，必须暂停循环动画。
- 必须遵守浏览器的 `prefers-reduced-motion` 规则。
- 除非有明确需求，否则严禁自定义动画缓动曲线。
- 应避免对大型图片或全屏元素进行动画处理。

## 字体（Typography）

- 标题应使用 `text-balance` 样式，正文和段落应使用 `text-pretty` 样式。
- 数据展示应使用 `tabular-nums` 样式。
- 对于内容密集的界面，建议使用 `truncate` 或 `line-clamp` 来控制文本显示。
- 除非有明确需求，否则严禁修改字母间距（`letter-spacing`）。

## 布局（Layout）

- 必须使用固定的 `z-index` 值进行元素堆叠，避免使用任意的 `z-x` 值。
- 对于方形元素，应使用 `size-x` 而不是 `w-x` 和 `h-x` 来定义大小。

## 性能（Performance）

- 绝不要对大型元素应用 `blur()` 或 `backdrop-filter` 动画效果。
- 除非动画正在执行中，否则严禁使用 `will-change` 属性。
- 对于可以通过渲染逻辑实现的操作，严禁使用 `useEffect`。

## 设计（Design）

- 除非有明确的需求，否则严禁使用渐变效果。
- 绝不要使用紫色或多色渐变。
- 绝不要将发光效果作为主要的交互提示方式。
- 除非有特殊需求，否则应使用 Tailwind CSS 的默认阴影样式。
- 空状态下的元素应提供明确的下一步操作提示。
- 每个界面中的强调色（accent color）应限制为一种。
- 在引入新的颜色方案之前，应优先使用现有的主题颜色或 Tailwind CSS 提供的颜色标识符。