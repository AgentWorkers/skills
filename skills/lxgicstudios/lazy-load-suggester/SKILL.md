---
name: lazy-load-suggester
description: 识别应该延迟加载的组件。在优化应用程序包大小时可以使用这一方法。
---

# 懒加载建议工具（Lazy Load Suggester）

并非所有内容都需要在页面首次加载时就被加载。该工具会分析你的组件结构，并告诉你哪些组件应该采用懒加载方式，从而提升页面性能。

**只需一条命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-lazy-load ./src/
```

## 工作原理

- 分析组件的使用模式
- 识别那些会占用大量资源的组件（这些组件通常会在页面加载时立即被加载）
- 提出适合采用懒加载的组件建议
- 提供相应的代码示例供你参考实现

## 使用示例

```bash
# Analyze all components
npx ai-lazy-load ./src/

# Focus on specific directory
npx ai-lazy-load ./src/components/

# Include pages
npx ai-lazy-load ./src/pages/
```

## 最佳实践

- **懒加载特定路由**：用户并不需要一次性看到所有页面内容。
- **占用大量资源的组件**：如模态框（modal）、图表（charts）、编辑器（editors）等。
- **用户需要滚动才能看到的内容**：这些内容可以延迟加载。
- **保持关键路径的简洁性**：优先加载用户当前可见的内容。

## 适用场景

- 初始应用程序包文件过大，导致加载速度缓慢。
- 用户与应用程序的交互时间过长。
- 需要在现有应用程序中加入代码分割（code splitting）功能。
- 需要优化特定的用户使用流程。

## 属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本完全开放，无需支付费用、无需注册账号，也无需使用 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。此外，系统需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-lazy-load --help
```

## 工作原理详解

该工具会扫描你的组件结构，了解各个组件之间的依赖关系以及它们的大小。通过人工智能技术，它会识别出那些不立即需要加载、但适合采用懒加载方式的组件。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具，无需遵守任何额外的使用限制。