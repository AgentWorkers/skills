---
name: web-designer
description: 这款由人工智能驱动的网页设计服务能够生成专业的 Next.js + Tailwind CSS 网页、SaaS 网站、作品集等。
version: 1.0.0
author: bobdevibecoder
commands:
  - generate: Generate a new website design from a brief
  - templates: List available design templates
  - preview: Generate a preview description of a design
  - quote: Generate a price quote for a client request
---

# 网页设计师技能

我们提供由 AI 支持的专业网站设计服务，能够生成可用于实际开发的 Next.js + Tailwind CSS 代码。

## 命令

### `generate <template> <brief>`
根据提供的模板和客户需求生成一个完整的网站。

**可用模板：**
- `landing`：SaaS/产品登录页面（采用暗色调的 Glassmorphism 设计风格）
- `portfolio`：个人/机构作品集网站
- `blog`：带有文章布局的博客网站
- `docs`：文档网站
- `pricing`：包含价格等级信息的定价页面
- `saas`：完整的 SaaS 营销网站（包含首页、功能介绍、呼叫行动按钮和页脚）

**示例：**
```
web-designer generate saas "A crypto portfolio tracker called CoinView with purple/blue theme. Features: real-time prices, portfolio tracking, alerts, API access."
```

### `templates`
列出所有可用模板，并附上描述和价格信息。

### `preview <template> <brief>`
仅生成设计的文字描述，不生成实际代码。

### `quote <brief>`
根据客户的需求生成专业的报价。

## 价格指南
- 单个登录页面：75 美元至 150 美元
- 作品集网站（3-5 页）：150 美元至 300 美元
- 完整的 SaaS 营销网站：200 美元至 500 美元
- 博客模板：100 美元至 200 美元
- 文档网站：150 美元至 300 美元
- 定制设计：300 美元至 750 美元

## 我们的作品集示例：
- ConvertFlow：https://micro-saas-template-omega.vercel.app
- MarkdownMagic：https://markdown-magic-chi.vercel.app
- QRForge：https://qr-forge-48x79aots-milad12bands-projects.vercel.app
- Base64Pro：https://base64pro-18fhuiuve-milad12bands-projects.vercel.app