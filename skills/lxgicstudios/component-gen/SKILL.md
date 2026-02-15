---
name: component-gen
description: 根据纯英文描述生成 React 组件。当您需要快速创建 UI 组件时，可以使用此方法。
---

# 组件生成器（Component Generator）

从零开始创建一个新的 React 组件非常繁琐。你可能已经明确了组件的需求——比如一个包含图片、标题和操作按钮的卡片——但设置所需的样板代码却花费了比预期更长的时间。这个工具可以根据简单的英文描述自动生成一个完整的 React 组件，支持 TypeScript、Tailwind 等技术。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-component "a pricing card with plan name, price, features list, and CTA button"
```

## 功能介绍

- 根据简单的英文描述生成完整的 React 组件
- 可选支持 TypeScript 语言，并提供正确的类型注释
- 通过 `--tailwind` 标志支持 Tailwind CSS 样式
- 可以直接将生成的代码写入文件或输出到标准输出（stdout）
- 生成的代码结构清晰，可直接用于生产环境

## 使用示例

```bash
# Generate a basic component
npx ai-component "a pricing card with plan name, price, features list, and CTA button"

# Generate with TypeScript
npx ai-component "a user profile dropdown with avatar, name, and logout" -t

# Generate with Tailwind and save to file
npx ai-component "a responsive navbar with logo, links, and mobile menu" --tailwind -o Navbar.tsx
```

## 最佳实践

- **详细描述布局**：对组件的位置和样式描述得越具体，组件的外观就越美观
- **在实际项目中使用 TypeScript**：`-t` 标志可以为代码提供正确的类型定义和接口
- **结合 Tailwind 使用**：`--tailwind` 标志生成的代码比内联样式更加简洁
- **逐步完善组件**：先生成基础组件，再根据需要进行调整。这样比从头开始编写代码更快。

## 适用场景

- 在进行新功能原型设计时，需要快速获取组件框架
- 在构建设计系统时，希望所有组件都有统一的起点
- 通过观察组件的结构来学习 React 开发模式
- 在速成项目（如 Hackathon）或最小可行产品（MVP）中，速度比完美更重要

## 属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-component --help
```

## 工作原理

该工具会将用户提供的描述发送给一个能够理解 React 开发模式和组件架构的 AI 模型，从而生成一个结构完整、功能齐全的组件，包括所需的样式和功能。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。