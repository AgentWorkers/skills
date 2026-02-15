---
name: prefetch-suggester
description: 获取有关路线和数据预取的建议，这些建议可用于优化导航体验。
---

# 预加载建议器（Prefetch Suggester）

用户讨厌等待页面加载。该工具会分析您的页面导航路径，并建议预先加载哪些内容，以实现更流畅的导航体验。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-prefetch ./src/pages/
```

## 功能介绍

- 分析您的页面导航路径和用户行为模式
- 识别用户接下来可能访问的页面
- 建议需要预先加载的数据
- 提供相应的实现代码

## 使用示例

```bash
# Analyze pages directory
npx ai-prefetch ./src/pages/

# Analyze app routes
npx ai-prefetch ./app/routes/
```

## 最佳实践

- **悬停时预加载**：在用户点击之前预先加载相关内容
- **不要预加载所有内容**：避免浪费带宽
- **优先预加载常用路径**：如结账流程、导航路径等关键路径
- **使用Intersection Observer**：仅在页面可见时才进行预加载

## 适用场景

- 当导航体验显得缓慢时
- 优化用户操作流程
- 为现有应用程序添加预加载功能
- 学习页面预加载的最佳实践

## 该工具属于LXGIC开发工具包（LXGIC Dev Toolkit）的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无需支付费用、无需注册，也无需使用API密钥。这些工具都能直接使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-prefetch --help
```

## 工作原理

该工具通过分析页面的路由结构和链接模式，判断用户可能的导航路径，然后根据数据的重要性和访问概率来建议需要预先加载的页面和数据。

## 许可协议

采用MIT许可证，永久免费。您可以自由使用该工具。