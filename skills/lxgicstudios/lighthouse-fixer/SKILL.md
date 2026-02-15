---
name: lighthouse-fixer
description: 运行 Lighthouse 审计工具，获取 AI 提供的修复建议。在提升网站性能时可以使用此方法。
---

# Lighthouse Fixer

Lighthouse 可以告诉你网站存在哪些问题，但其提供的修复建议通常较为笼统。这款工具会运行 Lighthouse 并针对你的具体问题给出切实可行的修复方案。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-lighthouse https://mysite.com
```

## 功能介绍

- 对任意网址执行全面的 Lighthouse 审计
- 通过人工智能分析审计结果
- 提供具体的修复建议，而非泛泛而谈的指导
- 根据问题的影响程度对问题进行优先级排序

## 使用示例

```bash
# Audit your site
npx ai-lighthouse https://mysite.com

# Specific page
npx ai-lighthouse https://example.com/page

# Focus on performance
npx ai-lighthouse https://mysite.com --category performance
```

## 最佳实践

- **优先修复性能问题**——这对用户体验影响最大
- **在网络连接较慢的环境中进行测试**——并非所有人都能使用千兆网络
- **单独检查移动设备版本**——移动设备的评分通常较低
- **逐步修复问题**——一次只修复一个方面

## 适用场景

- 当 Lighthouse 的评分急剧下降时
- 当 SEO 审计指出存在性能问题时
- 当 Core Web Vitals 指标未达标时
- 当你需要具体的修复建议而非仅仅文档链接时

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无需支付费用、无需注册，也无需 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-lighthouse --help
```

## 工作原理

该工具会使用 Lighthouse 对指定的网址进行审计，捕获完整的审计报告，并将其发送给 GPT-4o-mini。人工智能会解析这些报告内容，根据实际发现的问题提供具体的代码级修复建议。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。