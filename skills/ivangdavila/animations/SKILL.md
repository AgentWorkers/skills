---
name: Animations
description: 创建性能优异的网页动画，同时确保良好的可访问性和精确的动画时机控制。
metadata: {"clawdbot":{"emoji":"✨","requires":{},"os":["linux","darwin","win32"]}}
---

## GPU加速相关的属性

只有以下属性会在合成器线程上被动画化（60帧每秒）：

| 属性 | 用途 |
|----------|-----|
| `transform` | 移动、旋转、缩放（translateX、rotate、scale） |
| `opacity` | 显示/隐藏（淡入/淡出） |

其他所有属性都会触发布局更新或重绘。请避免对以下属性进行动画化：
- `width`、`height`、`margin`、`padding`（这些操作会导致布局频繁更新） |
- `top`、`left`、`right`、`bottom`（使用 `transform` 代替） |
- `border-width`、`font-size`（这些操作会导致页面重新布局，性能开销较大） |

```css
/* ❌ Triggers layout every frame */
.slide { left: 100px; transition: left 0.3s; }

/* ✅ GPU accelerated */
.slide { transform: translateX(100px); transition: transform 0.3s; }
```

## 降低运动效果（Reduced Motion）

大约5%的用户会出现前庭功能障碍（如运动引起的头晕、恶心）。

```css
/* Only animate if user hasn't requested reduced motion */
@media (prefers-reduced-motion: no-preference) {
  .animated { animation: slide-in 0.5s ease-out; }
}

/* Or disable for those who requested it */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

即使降低了运动效果，也要保持微妙的淡入/淡出效果和颜色变化。请避免使用视差效果、抖动效果以及无限循环动画。

## 时间控制函数

| 动画效果类型 | 适用场景 |
|--------|----------|
| `ease-out` | 元素进入视野时（使动画看起来更自然） |
| `ease-in` | 元素离开视野时（使动画逐渐消失） |
| `ease-in-out` | 元素在视野内移动时 |
| `linear` | 仅用于旋转图标、进度条、颜色循环等简单动画 |

```css
/* Custom bounce */
transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Material Design standard */
transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

## 动画持续时间指南

| 动画类型 | 最佳持续时间 |
|------|----------|
| 微交互（悬停、聚焦） | 100-200毫秒 |
| 过渡效果（模态框、下拉菜单） | 200-300毫秒 |
| 页面切换 | 300-500毫秒 |
| 复杂动画 | 最长500毫秒 |

持续时间超过500毫秒的动画会显得很卡顿。通常来说，动画时间越短越好。

## CSS过渡效果与动画效果的区别

**CSS过渡效果：** 用于实现从状态A到状态B的简单变化。  
**动画效果：** 包含多个步骤，可以自动播放，并且可以循环播放。  

**使用建议：**  
- 对于悬停或聚焦等微交互，使用CSS过渡效果。  
- 对于加载时的视觉效果或序列动画，使用动画效果。  

## `will-change`属性的使用

只有在遇到特定的性能问题时，才应使用 `will-change` 属性进行优化。  

## `transition`属性的注意事项

`all` 选项可能会导致颜色、背景、边框等属性的意外动画化。  

## React/框架相关注意事项

- 退出动画需要使用 `AnimatePresence` 功能来确保动画正确执行。  
- 列表元素的动画需要使用稳定的动画关键帧（stable keys）。  
- 父元素的自动动画化（AutoAnimate）必须是无条件的（unconditional）。  

## 库选择

| 库名 | 大小（KB） | 适用场景 |
|---------|------|----------|
| CSS only | 0KB | 仅用于悬停效果和简单过渡效果 |
| AutoAnimate | 3KB | 适用于列表、折叠菜单、提示框等90%的UI动画需求 |
| Motion | 22KB | 适用于手势识别、物理效果、滚动动画以及复杂的动画效果 |
| GSAP | 60KB | 适用于时间轴控制、创意动画以及滚动触发的动画序列 |

**推荐步骤：**  
- 先使用CSS实现基本动画效果。  
- 对于列表动画，优先使用 `AutoAnimate` 库。  
- 只有在需要复杂动画效果时，才引入 `Motion` 或 `GSAP` 库。  

## 常见错误：

- 使用 `width`/`height` 进行动画化，而不是 `scale`——会导致布局频繁更新。  
- 使用无限循环的动画且没有暂停控制——无法停止动画。  
- 进入和离开视场的动画使用相同的缓动效果——进入时使用 `ease-out`，离开时使用 `ease-in`。  
- 忽略了“降低运动效果”的设置——会导致用户不适。  
- 动画持续时间超过500毫秒——会显得卡顿。  
- 使用 `transition: all` 会导致不必要的动画效果。  
- 在React中，退出动画时未使用 `AnimatePresence` 功能。