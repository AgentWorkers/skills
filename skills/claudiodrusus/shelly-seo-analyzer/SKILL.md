---
name: seo-analyzer
description: 分析任何网页的URL，以检测SEO问题并提供可操作的改进建议。该工具会检查标题标签、元描述、标题结构、关键词密度、图片的alt标签、Open Graph信息等。
triggers:
  - analyze seo
  - check seo
  - seo audit
---
# seo-analyzer

该工具可分析任何网页URL，检测其中的SEO问题，并提供可行的改进建议。

## 使用方法

```bash
./seo-analyze.sh <URL>
```

或者使用 `web_fetch` 获取页面内容，然后将其传递给该工具进行处理：

```bash
curl -sL <URL> | ./seo-analyze.sh -
```

## 检查内容

- **标题标签** — 是否存在，长度（50-60个字符为宜）
- **元描述** — 是否存在，长度（150-160个字符为宜）
- **标题结构** — H1标题的数量及层级结构
- **关键词密度** — 最常见的10个关键词（每个关键词至少包含3个字符）
- **图片的alt标签** — 是否缺少alt属性
- **Open Graph/Twitter卡片** — 用于社交分享的元数据
- **规范URL** — 防止内容重复
- **字数** — 检测内容是否过于简短

## 输出结果

以纯文本形式生成报告，列出检测结果及优先级较高的改进建议。

## 所需工具

- `curl`（或在OpenClaw中使用`web_fetch`）
- `grep`、`sed`、`awk`（标准Unix工具）

## 开发者

Shelly 🦞 (@ShellyToMillion)