---
name: storybook-gen
description: **将 React 组件转换为 Storybook 故事（Generate Storybook stories from React components）**  
这种方法适用于为组件编写文档或构建设计系统时。通过将 React 组件转换为 Storybook 故事，可以更直观地展示组件的使用方式、功能以及交互逻辑，从而提高文档的可读性和可维护性。
---

# Storybook 生成器

只需将此工具指向一个 React 组件，即可自动生成包含所有变体、控件和边缘情况的完整 Storybook 故事。再也不用手动编写冗长的故事模板了。

**一个命令，零配置，即可使用。**

## 快速入门

```bash
npx ai-storybook ./src/components/Button.tsx
```

## 功能介绍

- 分析组件的属性（props），并生成相应的控件
- 为常见的组件状态（默认值、禁用状态、加载状态、错误状态）创建故事
- 支持处理复杂的属性类型（包括对象和回调函数）
- 为故事参数生成正确的 TypeScript 类型
- 提供真实的示例数据，而不仅仅是占位符文本

## 使用示例

```bash
# Generate stories for a single component
npx ai-storybook ./src/components/Card.tsx

# Process entire components directory
npx ai-storybook ./src/components/ --recursive

# Output CSF3 format
npx ai-storybook ./src/Button.tsx --format csf3

# Include interaction tests
npx ai-storybook ./src/Modal.tsx --with-interactions

# Specify output directory
npx ai-storybook ./src/Input.tsx -o ./stories/
```

## 最佳实践

- **先编写良好的属性类型**：准确的 TypeScript 类型有助于生成更高质量的故事内容
- **添加 JSDoc 注释**：AI 会利用这些注释来生成有意义的描述
- **先生成故事，再自定义**：先使用该工具生成基础内容，再手动添加特定的边缘情况
- **保持组件职责清晰**：职责明确的组件会生成更简洁的故事模板

## 适用场景

- 为现有代码库设置 Storybook
- 新增组件时需要快速生成相关故事
- 为团队文档化组件库
- 创建具有统一故事格式的设计系统

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-storybook --help
```

## 工作原理

该工具会解析你的 React 组件，提取其属性类型、默认值和组件结构，然后生成相应的 Storybook 故事。它会根据属性名称和类型来创建各种组合的测试用例，从而生成有意义的示例代码。

## 许可证

MIT 许可证。永久免费使用，你可以随意使用该工具。