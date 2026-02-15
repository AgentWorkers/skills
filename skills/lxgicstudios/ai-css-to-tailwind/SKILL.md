---
name: css-to-tailwind
description: 将 CSS 文件转换为 Tailwind CSS 的实用类
---

# 将CSS转换为Tailwind

如果你有旧的CSS代码，可以将其转换为Tailwind样式。该工具能够处理复杂的CSS选择器和媒体查询。

## 快速入门

```bash
npx ai-css-to-tailwind ./src/styles/button.css
```

## 功能介绍

- 将CSS规则转换为Tailwind实用函数（utils）
- 支持响应式设计（处理不同的屏幕分辨率）
- 将自定义CSS属性转换为主题（theme）中的变量
- 保留复杂的悬停（hover）和聚焦（focus）状态效果

## 使用示例

```bash
# Convert a CSS file
npx ai-css-to-tailwind ./styles/header.css

# Convert and update component
npx ai-css-to-tailwind ./styles/card.css --update ./components/Card.tsx

# Batch convert
npx ai-css-to-tailwind ./styles/*.css
```

## 支持的内容

- 媒体查询（media queries） → 响应式前缀（responsive prefixes）
- 伪类（pseudo-classes） → 状态变体（state variants）
- CSS变量（CSS variables） → 主题变量（theme variables）
- 复杂的选择器（complex selectors） → 组件模式（component patterns）

## 系统要求

- Node.js 18.0及以上版本
- 需要OPENAI_API_KEY

## 许可证

MIT许可证。永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub仓库：[github.com/lxgicstudios/ai-css-to-tailwind](https://github.com/lxgicstudios/ai-css-to-tailwind)
- Twitter账号：[@lxgicstudios](https://x.com/lxgicstudios)