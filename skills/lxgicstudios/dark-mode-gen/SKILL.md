---
name: dark-mode-gen
description: 为组件添加深色模式（dark mode）支持。在实现深色主题时可以使用该功能。
---

# 暗模式生成器

启用暗模式意味着需要使用CSS变量或Tailwind的`dark:`前缀来更新所有组件。这个工具可以自动为单个文件或整个目录完成这项工作。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-dark-mode ./src/components/Card.tsx
```

## 功能介绍

- 为React组件添加暗模式样式
- 支持CSS变量、Tailwind或`styled-components`
- 处理` prefers-color-scheme`媒体查询
- 保留现有的样式和结构

## 使用示例

```bash
# Single component
npx ai-dark-mode ./src/components/Card.tsx

# Entire directory
npx ai-dark-mode ./src/components/

# Preview before writing
npx ai-dark-mode ./src/components/Card.tsx --dry-run
```

## 最佳实践

- **使用CSS变量**：比硬编码的颜色更易于维护
- **测试两种模式**：确保两种模式下的对比度都良好
- **不要忽略图片**：某些图形需要 light/dark 版本
- **尊重系统设置**：使用` prefers-color-scheme`来决定显示模式

## 适用场景

- 为现有项目添加暗模式功能
- 将仅支持亮模式的组件转换为支持暗模式的组件
- 在多个文件中统一暗模式的实现方式
- 快速原型设计时添加暗模式支持

## 属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要API密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用`npx`命令运行。建议使用Node.js 18及以上版本。需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-dark-mode --help
```

## 工作原理

该工具会读取你的组件文件，识别其中的颜色定义和样式，然后添加相应的暗模式版本。对于Tailwind样式，它会添加`dark:`前缀；对于CSS样式，则会使用` prefers-color-scheme`来处理暗模式切换。

## 许可证

采用MIT许可证。永久免费，你可以随意使用这个工具。