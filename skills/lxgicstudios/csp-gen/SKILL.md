---
name: csp-gen
description: 为您的网站生成内容安全策略（Content Security Policy, CSP）头部。当您需要添加CSP头部时，无需花费数小时阅读相关规范，只需使用此方法即可。
---

# CSP生成器

内容安全策略（CSP）头部是防范跨站脚本攻击（XSS攻击）的最佳手段之一。然而，手动编写这些头部内容往往令人困惑。这款工具会自动分析您的网站，并生成正确的CSP头部信息，让您再也不用猜测需要哪些指令，也不用担心意外地阻止自己的脚本运行了。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-csp https://mysite.com
```

## 功能介绍

- 分析您的网站，确定加载了哪些资源以及这些资源的来源；
- 生成完整的内容安全策略头部字符串；
- 处理`script-src`、`style-src`、`img-src`、`connect-src`等所有相关指令；
- 提供用于监控违规行为的`report-uri`配置建议；
- 提供严格和宽松两种策略选项供您选择。

## 使用示例

```bash
# Generate CSP for a production site
npx ai-csp https://mysite.com

# Generate CSP for local development
npx ai-csp http://localhost:3000

# Analyze a specific page
npx ai-csp https://mysite.com/dashboard
```

## 最佳实践

- **先使用“仅报告”模式**：先部署`Content-Security-Policy-Report-Only`模式，查看哪些功能会受到影响；
- **避免使用`unsafe-inline`指令**：如果您的CSP策略中包含`unsafe-inline`，那么它的安全性几乎等于零；
- **为内联脚本使用随机数（nonces）**：这比使用`unsafe-inline`安全得多，并且适用于大多数开发框架；
- **在所有页面上进行测试**：不同页面可能加载不同的资源，因此需要生成并合并相应的CSP策略。

## 适用场景

- 首次为网站添加CSP头部时，不知道从何开始；
- 当现有的CSP策略过于宽松，需要加强安全性时；
- 添加了新的第三方脚本后，需要更新CSP策略；
- 安全审计指出缺少或存在漏洞的CSP头部时。

## 作为LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多种免费开发工具之一。免费版本无需支付费用、无需注册，也无需API密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-csp --help
```

## 工作原理

该工具通过检查网站中加载的脚本、样式文件、图片和API来分析资源的使用情况，并将这些资源与相应的CSP指令关联起来，从而生成完整的CSP策略字符串。工具会利用人工智能来帮助您在安全性和功能性之间找到最佳平衡。

## 许可证

采用MIT许可证，永久免费。您可以随心所欲地使用该工具。