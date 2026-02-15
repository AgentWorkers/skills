---
name: component-gen
description: 根据描述生成 React/Vue/Svelte 组件
---

# 组件生成器

只需描述您的需求，即可获得一个可直接用于生产的组件。支持 React、Vue 和 Svelte。

## 快速入门

```bash
npx ai-component "A pricing card with monthly/yearly toggle"
```

## 功能概述

- 根据描述生成完整的组件
- 支持 React、Vue 和 Svelte
- 包含 TypeScript 类型定义
- 优化可访问性（accessibility）
- 集成 Tailwind CSS 样式

## 使用示例

```bash
# Generate React component
npx ai-component "user profile card with avatar"

# Specify framework
npx ai-component "dropdown menu" --framework vue

# With specific styling
npx ai-component "modal dialog" --css tailwind
```

## 输出内容

- 具有正确结构的组件文件
- TypeScript 接口
- 默认属性
- 基本测试框架
- 可选的 Storybook 示例（Storybook 是一个用于编写和展示组件的工具）

## 系统要求

- Node.js 18.0 或更高版本
- 需要 OPENAI_API_KEY

## 许可证

MIT 许可证。永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub: [github.com/lxgicstudios/ai-component](https://github.com/lxgicstudios/ai-component)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)