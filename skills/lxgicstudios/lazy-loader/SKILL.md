---
name: lazy-loader
description: 使用人工智能来识别应该延迟加载的组件。在优化包大小和初始加载速度时，这些信息非常有用。
---

# 懒加载分析器（Lazy Load Analyzer）

你的应用程序包文件体积庞大，导致初始加载速度较慢。这款工具可以识别出那些应该通过懒加载方式引入的组件，并告诉你如何合理地分割这些组件，从而避免在首次加载时加载整个应用程序。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-lazy-load ./src
```

## 功能介绍

- 分析你的组件结构，寻找适合使用懒加载的时机；
- 识别那些不需要立即加载的组件；
- 为 Next.js 和 React Router 提供基于路由的组件分割方案；
- 建议使用 `React.lazy()` 结合 `Suspense` 来实现懒加载功能；
- 评估每种分割方案对应用程序包大小的影响。

## 使用示例

```bash
# Analyze all components
npx ai-lazy-load ./src/components

# Focus on pages/routes
npx ai-lazy-load ./src/pages --routes-only

# Show bundle impact estimates
npx ai-lazy-load ./src --with-sizes

# Generate ready-to-use code
npx ai-lazy-load ./src --generate-code

# Next.js specific analysis
npx ai-lazy-load ./src --framework next
```

## 最佳实践

- **不要对所有组件都使用懒加载**：那些在页面初始渲染时就需要的组件应该立即加载；
- **将相关组件分组**：应该按功能模块进行懒加载，而不是单独的按钮；
- **为每个懒加载部分添加适当的加载状态**：每个使用 `Suspense` 的部分都需要提供默认显示内容（fallback）；
- **对比效果**：在使用懒加载前后，使用该工具检查应用程序包的大小变化。

## 适用场景

- 应用程序的压缩后初始包大小超过 200KB；
- Lighthouse 工具提示“减少未使用的 JavaScript 代码”；
- 在添加新功能时担心应用程序包膨胀；
- 为提升页面初始加载时间（TTI, Time To Interactive）而进行应用重构。

## 该工具属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-lazy-load --help
```

## 工作原理

该工具会解析你的组件导入语句，并构建一个依赖关系图。它会识别出那些条件性渲染的组件、那些位于视口之外的组件，以及那些需要根据用户操作才加载的组件。通过人工智能技术，该工具会评估哪种分割方式能够在保持最低复杂度的同时带来最佳的性能提升。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。