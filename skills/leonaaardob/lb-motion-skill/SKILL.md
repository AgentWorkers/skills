---
name: motion
version: 1.0.0
description: 完成 Motion.dev 的文档编写——这是一个专为 React、JavaScript 和 Vue 设计的现代动画库（前身为 Framer Motion）
author: Leonardo Balland
tags:
  - motion
  - animation
  - react
  - javascript
  - vue
  - framer-motion
  - transitions
  - gestures
  - scroll
  - spring
  - keyframes
read_when:
  - Working with Motion animations or Framer Motion
  - Implementing animations in React, Vue, or vanilla JavaScript
  - Creating scroll-linked or scroll-triggered animations
  - Building gesture-based interactions
  - Optimizing animation performance
  - Migrating from Framer Motion to Motion
---

# Motion.dev 文档

Motion 是一个专为 React、JavaScript 和 Vue 设计的现代化动画库。它是 Framer Motion 的升级版本，具备以下特点：

- **体积小巧**：迷你 HTML/SVG 版本的体积仅为 2.3KB
- **高性能**：支持硬件加速的动画效果
- **灵活性**：可以动画化 HTML、SVG、WebGL 和 JavaScript 对象
- **易于使用**：提供直观的 API 和智能的默认设置
- **真实的物理效果**：实现自然、动态的动画效果
- **滚动动画**：可以将动画效果与滚动位置关联起来
- **手势支持**：支持拖拽、悬停、点击等多种手势操作

## 快速参考

### 安装

```bash
npm install motion
```

### 基本动画

```javascript
import { animate } from "motion"

// Animate elements
animate(".box", { rotate: 360, scale: 1.2 })

// Spring animation
animate(element, { x: 100 }, { type: "spring", stiffness: 300 })

// Stagger multiple elements
animate("li", { opacity: 1 }, { delay: stagger(0.1) })
```

### 在 React 中使用 Motion

```jsx
import { motion } from "motion/react"

<motion.div
  animate={{ rotate: 360 }}
  transition={{ duration: 2 }}
/>
```

### 滚动动画

```javascript
import { scroll } from "motion"

scroll(animate(".box", { scale: [1, 2, 1] }))
```

## 文档结构

- `quick-start.md`：安装指南及第一个动画示例
- 更多文档即将添加……

## 适用场景

- 在 Web 应用程序中实现动画效果
- 优化动画性能
- 创建基于滚动的交互式效果
- 从 Framer Motion 迁移到 Motion

## 外部资源

- 官方网站：https://motion.dev
- GitHub 仓库：https://github.com/motiondivision/motion
- 示例代码：https://motion.dev/examples