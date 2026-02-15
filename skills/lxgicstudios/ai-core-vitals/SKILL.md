---
name: core-vitals-fixer
description: 利用人工智能（AI）的指导来修复 Core Web Vitals 相关的问题。当您的 Lighthouse 评分较低时，请使用此方法。
---

# 核心网页性能优化工具（Core Web Vitals Fixer）

您的页面加载时间（LCP）为4秒，页面重绘时间（CLS）波动较大，页面首次交互时间（FID）也显得很慢。这款工具会扫描您的代码，并明确指出需要修复的问题以及修复方法。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-core-vitals ./src/
```

## 功能介绍

- 分析您的代码中是否存在影响核心网页性能的问题
- 识别 LCP、CLS 和 FID 的问题
- 提供具体的修复方案及代码示例
- 根据问题的影响程度对问题进行优先级排序

## 使用示例

```bash
# Scan your source directory
npx ai-core-vitals ./src/

# Scan app directory
npx ai-core-vitals ./app/

# Focus on specific metric
npx ai-core-vitals ./src/ --metric lcp
```

## 最佳实践

- **优先修复 LCP**——这通常是提升页面性能的关键
- **对用户看不到的内容使用懒加载**——避免加载不必要的内容
- **为图片预留空间**——有助于减少页面重绘时间（CLS）
- **延迟加载非核心的 JavaScript 代码**——提升页面首次交互时间（FID）

## 适用场景

- 当 Lighthouse 的评分严重影响您的搜索引擎排名（SEO）时
- 当用户抱怨页面加载速度过慢时
- 当 Search Console 显示核心网页性能指标不佳时
- 在新建网站时，希望立即开始进行性能优化

## 该工具属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多款免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-core-vitals --help
```

## 工作原理

该工具会扫描您的代码文件，检测常见的性能问题，然后将问题数据发送给 GPT-4o-mini。AI 会识别出影响 LCP、CLS 和 FID 的问题，并提供带有优先级排序的修复建议。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-core-vitals](https://github.com/lxgicstudios/ai-core-vitals)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)