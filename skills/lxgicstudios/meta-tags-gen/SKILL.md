---
name: meta-tags-gen
description: 扫描页面并生成缺失的元标签。适用于提升搜索引擎优化（SEO）的效果。
---

# 元标签生成器

您的页面缺少 Open Graph 标签和 Twitter 卡片信息。该工具会扫描您的内容，并生成与页面实际内容相匹配的元标签。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-meta-tags --url https://mysite.com
```

## 功能介绍

- 扫描 URL 或本地 HTML 文件
- 识别缺失的元标签
- 生成 SEO、Open Graph 和 Twitter 卡片标签
- 根据页面实际内容生成描述性文字

## 使用示例

```bash
# Scan a URL
npx ai-meta-tags --url https://mysite.com

# Scan local file
npx ai-meta-tags --file index.html

# Generate for blog post
npx ai-meta-tags --url https://mysite.com/blog/my-post
```

## 最佳实践

- **每个页面使用独特的描述**：不要在所有地方使用相同的描述
- **标题长度控制在 60 个字符以内**：过长的标题会被截断
- **使用真实的图片**：og-image 标签对分享效果至关重要
- **使用验证工具进行测试**：Facebook 和 Twitter 都有相应的验证工具

## 适用场景

- 在社交媒体上分享时链接显示效果不佳
- SEO 审计发现缺少元标签
- 新建网站时需要所有元标签
- 为旧页面添加现代 SEO 功能

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无付费门槛、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-meta-tags --help
```

## 工作原理

该工具会获取页面内容，分析文本和结构，然后生成相应的元标签。AI 会根据页面内容生成具有描述性的文字，而非简单的填充文本。

## 许可证

遵循 MIT 许可协议，永久免费。您可以随意使用该工具。