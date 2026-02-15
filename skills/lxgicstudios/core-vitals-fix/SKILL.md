---
name: core-vitals-fixer
description: 利用人工智能技术来解决 Core Web Vitals 相关的问题。当您的 Lighthouse 评分较低时，可以使用此方法进行优化。
---

# 核心网页性能优化工具（Core Web Vitals Fixer）

您的页面加载时间（LCP）为4秒，CLS（Cumulative Layout Shift）值波动较大，FID（First Input Delay）也显得较慢。该工具会扫描您的代码，并明确指出需要修复的问题以及相应的解决方法。

**仅需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-core-vitals ./src/
```

## 功能介绍

- 分析您的代码中存在的核心网页性能问题
- 识别LCP、FID和CLS方面的问题
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

- **优先修复LCP**：这通常是提升页面性能的关键步骤
- **对用户看不到的内容使用懒加载（Lazy Load）**：避免加载用户无法看到的内容
- **为图片预留显示空间**：有助于减少CLS值
- **延迟加载非关键JavaScript代码**：有助于提升FID值

## 适用场景

- Lighthouse评分严重影响您的搜索引擎排名（SEO）
- 用户抱怨页面加载速度过慢
- 在Search Console中检测到核心网页性能指标不达标
- 正在构建新网站并希望从优化开始

## 该工具属于LXGIC开发工具包（LXGIC Dev Toolkit）的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本完全无需支付费用、注册或使用API密钥，只需简单运行即可使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行该工具需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-core-vitals --help
```

## 工作原理

该工具会扫描您的代码文件，检测常见的性能问题，然后将这些问题发送给GPT-4o-mini模型进行处理。AI模型会识别出影响LCP、CLS和FID的问题，并提供带有优先级排序的修复建议。

## 许可证

采用MIT许可证，永久免费。您可以随意使用该工具。