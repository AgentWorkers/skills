---
name: aeo-prompt-frequency-analyzer
description: 通过多次使用 Google Search 进行搜索，并统计查询的频率分布，来分析 Gemini 在回答用户问题时所使用的搜索查询。这种方法可用于研究 AEO（Automatic Emergency Operations）查询模式、了解 AI 模型如何在网上搜索特定主题，或探讨 AI 引发的搜索查询的随机性（概率特性）。
---
# 提示频率分析器

使用启用了Google搜索功能的Gemini，运行N次提示请求。收集并报告Gemini在所有运行中生成的搜索查询的频率。

## 使用方法

```bash
GEMINI_API_KEY=$(security find-generic-password -s "nano-banana-pro" -w) \
  python3 scripts/analyze.py "your prompt here" [--runs 10] [--model gemini-2.5-pro] [--concurrency 5] [--output text|json]
```

从技能目录中运行该脚本。请使用相对于此SKILL.md文件的`scripts/analyze.py`文件。

## 参数选项

- `--runs N` — 运行提示请求的次数（默认值：10）
- `--model NAME` — 要使用的Gemini模型（默认值：gemini-2.5-pro）
- `--concurrency N` — 最大并行API调用次数（默认值：5；建议不超过5以避免触发速率限制）
- `--output text|json` — 输出格式（默认值：text）

## 输出结果

为每个独特的搜索查询生成以下报告：
- 频率百分比（该查询被使用的次数占总次数的百分比）
- 原始查询次数
- 被引用的主要网页来源

## 注意事项

- Gemini API密钥必须存储在`GEMINI_API_KEY`环境变量中（在macOS的Keychain中，文件名为`nano-banana-pro`）
- 每次运行都是独立的——Gemini每次可能会使用不同的搜索查询
- 失败的请求会尝试重试最多3次，并采用指数级退避策略
- 使用`--output json`选项可获取可用于程序化处理的输出数据