---
name: perf-auditor
description: 运行 Lighthouse 性能审计，并获得 AI 提供的修复建议。当您的网站运行缓慢且需要具体的修复措施时，可以使用此方法。
---

# 性能审计工具

您的网站在 Lighthouse 评估中的得分为 43 分，但您不知道从哪里开始优化。这款工具会进行性能审计，并提供具体、有优先级的优化建议，而不是模糊的指导。它会明确指出哪些环节导致了性能下降以及如何改进。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-lighthouse https://mysite.com
```

## 工具功能

- 对任意 URL 运行 Lighthouse 性能审计
- 通过具体指标识别性能瓶颈
- 生成基于人工智能的优化建议，并提供相应的代码修改方案
- 根据影响程度对优化建议进行优先级排序，帮助您先解决最关键的问题
- 支持核心网页健康指标（Core Web Vitals）、渲染阻塞资源（render-blocking resources）和图片优化（image optimization）的检测

## 使用示例

```bash
# Audit a production URL
npx ai-lighthouse https://mysite.com

# Audit a local dev server
npx ai-lighthouse http://localhost:3000

# Audit a specific page
npx ai-lighthouse https://mysite.com/products
```

## 最佳实践

- **测试生产环境，而非开发环境**：开发环境的代码通常未经优化。请始终使用生产环境的 URL 进行审计，以获取真实的数据。
- **优先解决前 3 个问题**：不要试图一次性解决所有问题，前 3 个问题通常占据了性能问题的 80%。
- **审计前后对比**：先进行一次审计以获取基准数据，进行修改后再次审计，查看优化效果。
- **分别检测移动设备和桌面设备**：移动设备的性能通常更差，而大多数用户使用的是移动设备。

## 适用场景

- 当您的 Lighthouse 评分下降，需要找出原因时
- 客户抱怨页面加载速度慢时
- 在产品发布前进行优化时
- 需要满足搜索引擎优化（SEO）的核心网页健康指标要求时

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-lighthouse --help
```

## 工作原理

该工具会通过编程方式对您的 URL 运行 Lighthouse 测试，收集性能数据。随后分析审计结果，并将瓶颈信息发送给人工智能模型，模型会根据分析结果生成具体的优化建议。每个建议都会说明预期的优化效果及所需的代码修改内容。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。