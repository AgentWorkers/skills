---
name: dark-mode
description: 使用 AI 为组件添加暗黑模式支持。在构建主题切换功能或对现有系统进行暗黑模式改造时可以使用此方法。
---

# 暗模式生成器

厌倦了手动编写各种暗模式样式吗？这款工具会扫描你的组件，并自动生成所需的CSS或Tailwind样式类。只需将文件指向该工具，即可快速实现暗模式支持，无需额外配置。

**一个命令，零配置，立即生效。**

## 快速入门

```bash
npx ai-dark-mode ./src/components/Button.tsx
```

## 功能介绍

- 分析组件的现有样式和颜色使用情况
- 生成视觉效果良好的暗模式样式
- 支持纯CSS、Tailwind或CSS-in-JS格式
- 输出格式清晰、可直接复用的代码
- 保留你现有的设计系统颜色设置

## 使用示例

```bash
# Generate dark mode for a single component
npx ai-dark-mode ./src/components/Card.tsx

# Process an entire directory
npx ai-dark-mode ./src/components/ --recursive

# Output Tailwind dark: classes
npx ai-dark-mode ./src/Button.tsx --format tailwind

# Generate CSS custom properties
npx ai-dark-mode ./src/styles/main.css --format css-vars
```

## 最佳实践

- **使用设计系统中的颜色规范**：如果你有定义好的颜色调色板，AI会参考这些规范以确保一致性
- **检查对比度**：工具会尽力保持文本的可读性，但仍需手动检查可访问性
- **在两种模式下进行测试**：生成的样式虽然智能，但并非完美无缺，切换模式可发现潜在问题
- **考虑背景效果**：暗模式不仅仅是简单的颜色反转，还需要考虑元素的层次感和深度效果

## 适用场景

- 继承了没有暗模式的代码库，需要快速添加暗模式功能
- 新建组件时希望从一开始就支持暗模式
- 将设计系统转换为支持主题切换的形式
- 需要在两种模式下快速原型设计，而无需手动修改代码

## 属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本无需支付费用、注册或使用API密钥，只需使用npx命令即可运行。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，直接使用npx命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-dark-mode --help
```

## 工作原理

该工具会解析你的组件文件，提取颜色值和样式定义，然后利用AI生成语义上合适的暗模式样式。它理解浅色背景会变为深色、文本颜色需要反转以增强对比度，以及细微的灰色调需要仔细调整。

## 许可证

MIT许可证。永久免费使用，可自由支配。