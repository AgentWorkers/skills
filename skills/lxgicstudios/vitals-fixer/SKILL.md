---
name: vitals-fixer
description: 使用 AI 指导来解决 Core Web Vitals 相关的问题。当您的 Lighthouse 评分需要提升时，请采用此方法。
---

# 核心网页健康指标修复工具（Core Web Vitals Fixer）

您的 Lighthouse 评估结果显示为红色（表示存在性能问题）。该工具会详细说明问题原因及修复方法，涵盖 LCP（加载时间）、FID（首次交互时间）、CLS（内容加载完成时间）等关键指标，并提供具体的解决方案。再也不用对性能问题进行猜测了。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-core-vitals ./src
```

## 工具功能

- 分析您的代码，找出影响网页健康指标的问题；
- 识别导致 LCP 延迟的瓶颈（如阻塞页面渲染的资源）；
- 找出导致 CLS 问题的原因（如缺少尺寸信息的图片）；
- 发现由于 JavaScript 执行缓慢而引起的 FID 问题；
- 提供具体的代码修改建议，而不仅仅是泛泛而谈的优化建议。

## 使用示例

```bash
# Full project analysis
npx ai-core-vitals ./

# Focus on specific metric
npx ai-core-vitals ./src --metric lcp

# Analyze with a URL for real data
npx ai-core-vitals ./src --url https://yoursite.com

# Prioritized fix list
npx ai-core-vitals ./src --prioritize

# Output detailed report
npx ai-core-vitals ./src -o vitals-report.md
```

## 最佳实践

- **优先修复 LCP**：它对用户感知的性能影响最大；
- **修复前后进行测试**：使用 Lighthouse 验证修复效果；
- **不要依赖开发模式（dev mode）**：生产环境的代码运行方式可能与开发环境不同，务必进行双重测试；
- **专注于能带来显著提升的优化**：修复一张大图片的效果可能比进行十次微调更好。

## 适用场景

- 在 Search Console 的核心网页健康指标评估中未通过；
- 准备接受 Lighthouse 的性能审计；
- 客户反馈网站加载速度较慢；
- 需要构建性能回归测试。

## 该工具属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本完全无付费门槛、无需注册，也无需使用 API 密钥，只需使用命令行工具即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-core-vitals --help
```

## 工作原理

该工具会扫描您的源代码，查找可能影响网页健康指标的问题（如未优化的图片、缺失的预加载资源、导致布局变化的元素以及体积过大的代码包）。通过人工智能技术，将这些问题与实际代码关联起来，从而提出针对性的修复建议。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。