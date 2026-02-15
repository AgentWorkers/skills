---
name: prefetcher
description: AI 会推荐预加载的路线和数据，以提升用户体验（UX）。在优化导航性能时可以使用这一功能。
---

# 预加载建议器（Prefetch Advisor）

您的应用程序在页面切换时显得很慢。这个工具会分析用户的行为模式，并告诉您应该预加载哪些内容——包括路由信息、API调用结果以及图片等。这些资源会在用户点击之前就被加载到系统中。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-prefetch ./src
```

## 工作原理

- 分析您的路由结构和导航模式
- 识别出接下来最有可能被访问的页面
- 建议预加载相关的数据（如API调用结果）
- 提供链接预加载和资源预加载的策略
- 支持Next.js、React Router以及纯JavaScript应用程序

## 使用示例

```bash
# Analyze all routes
npx ai-prefetch ./src/pages

# Focus on specific user flow
npx ai-prefetch ./src --entry /dashboard

# Include API call analysis
npx ai-prefetch ./src --include-api

# Generate prefetch code
npx ai-prefetch ./src --generate

# Next.js Link prefetch optimization
npx ai-prefetch ./src --framework next
```

## 最佳实践

- **在用户悬停时进行预加载，而非在页面加载时**：这样可以避免浪费带宽
- **优先预加载常用路径**：例如登录后的仪表盘页面，而非设置页面
- **不要预加载所有内容**：只需预加载2-3个最有可能被访问的页面
- **利用空闲时间进行预加载**：对于非关键资源的预加载，可以使用`requestIdleCallback`函数

## 适用场景

- 页面切换时感觉卡顿
- 用户的导航行为具有规律性
- 您有足够的带宽资源可供使用
- 目的是提升用户的整体使用体验，而不仅仅是优化技术指标

## 属于LXGIC开发工具包（LXGIC Dev Toolkit）的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本完全免费，无需支付费用或注册账号，也不需要API密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub：https://github.com/LXGIC-Studios
- Twitter：https://x.com/lxgicstudios
- Substack：https://lxgicstudios.substack.com
- 官网：https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-prefetch --help
```

## 工作原理详解

该工具会映射您的应用程序的路由结构，并分析用户的导航行为。它会根据用户界面（UI）的模式来识别常见的访问路径，然后建议预加载哪些资源。在预加载决策过程中，人工智能会考虑多种因素，如链接的可见性、用户的操作意图以及资源的大小等。

## 许可证

采用MIT许可证，永久免费。您可以随心所欲地使用这个工具。