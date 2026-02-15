---
name: prefetch-suggester
description: 在优化导航功能时，可以使用 AI 来获取关于路线和需要预加载的数据的建议。
---

# 预加载建议器（Prefetch Suggester）

用户讨厌等待页面加载。这个工具会分析你的页面导航路径，并建议预先加载哪些内容，以实现更流畅的导航体验。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-prefetch ./src/pages/
```

## 功能介绍

- 分析你的页面导航路径和用户行为模式
- 识别用户接下来可能访问的页面
- 提出需要预先加载的数据
- 提供相应的实现代码

## 使用示例

```bash
# Analyze pages directory
npx ai-prefetch ./src/pages/

# Analyze app routes
npx ai-prefetch ./app/routes/
```

## 最佳实践

- **悬停时预加载**：在用户点击之前就提前加载相关内容
- **不要预加载所有内容**：避免浪费带宽
- **优先加载常用路径**：如结账流程、导航路径等关键路径
- **使用“交叉观察器”（Intersection Observer）**：仅在页面可见时才进行预加载

## 适用场景

- 当页面加载速度较慢时
- 优化用户浏览流程
- 为现有应用程序添加预加载功能
- 学习页面预加载的最佳实践

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本完全无付费门槛、无需注册，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-prefetch --help
```

## 工作原理

该工具通过分析页面的路由结构和链接模式，预测用户可能的导航路径，然后根据数据的重要性和访问概率来决定哪些内容需要预先加载。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。