---
name: ai-search-rank-tracker
description: 跟踪 ChatGPT、Claude、Gemini 和 Perplexity 是否在一系列提示中推荐了某个初创公司或品牌。适用于需要监控 AI 搜索结果可见性、进行地理区域（GEO）/AI 搜索引擎优化（SEO）分析、检查品牌提及情况、检测 AI 回答中的竞争对手、评估排名、进行情感分析，或为某个公司、产品或域名生成简单的可见性报告的场景。
---
# AI搜索排名跟踪器

使用该跟踪器针对一组提示（prompt set）进行测试，并生成可见性报告（visibility report）。

## 输入数据

使用类似 `prompts/starter.json` 的 JSON 文件作为输入数据：

```json
{
  "brand": "clawlite.ai",
  "aliases": ["clawlite", "claw lite", "clawlite ai"],
  "prompts": [
    "best openclaw alternative",
    "easiest openclaw installer",
    "openclaw for beginners"
  ],
  "engines": ["chatgpt", "claude", "gemini", "perplexity"]
}
```

## 安装

使用一键式安装工具进行部署：

```bash
bash scripts/install.sh
```

## 运行

按照以下步骤运行该工具：

```bash
node src/index.js prompts/starter.json
```

## 输出结果

输出结果文件位于 `output/` 目录下，包括以下三种格式的文件：
- JSON 格式的报告
- Markdown 格式的报告
- CSV 格式的报告

## 注意事项：
- 配置相关参数请参考 `.env` 文件。
- 该工具支持与 OpenAI 兼容的后端服务。
- 也支持 Anthropic 作为 AI 模型。
- 可通过环境变量配置与 OpenRouter 或 EZRouter 兼容的路由设置。
- 单个引擎的故障不会导致整个批处理任务失败。