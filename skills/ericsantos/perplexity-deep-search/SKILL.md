---
name: perplexity
description: "通过 Perplexity API 进行深度搜索。提供三种模式：搜索（快速获取事实）、分析（复杂问题研究）和调研（生成深度报告）。返回基于人工智能的答案，并附有引用来源。"
homepage: https://docs.perplexity.ai
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":["curl","jq"]},"primaryEnv":"PERPLEXITY_API_KEY"}}
---

# Perplexity 深度搜索

这是一个基于人工智能的网页搜索工具，提供三种不同深度级别的搜索模式。

## 快速入门

```bash
# Quick search (sonar) - facts, summaries, current events
{baseDir}/scripts/search.sh "latest AI news"

# Reasoning (sonar-reasoning-pro) - complex analysis, multi-step
{baseDir}/scripts/search.sh --mode reason "compare React vs Vue for enterprise apps"

# Deep Research (sonar-deep-research) - full reports, exhaustive analysis
{baseDir}/scripts/search.sh --mode research "market analysis of AI in healthcare 2025"
```

## 模式

| 模式 | 模型 | 适用场景 | 成本 |
|------|-------|----------|------|
| `search`（默认） | `sonar-pro` | 快速获取事实、摘要、时事信息 | 低成本 |
| `reason` | `sonar-reasoning-pro` | 复杂分析、比较、问题解决 | 中等成本 |
| `research` | `sonar-deep-research` | 深度报告、市场分析、文献综述 | 高成本 |

## 选项

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--mode` | `search`、`reason`、`research` | `search` |
| `--recency` | `小时`、`天`、`周`、`月` | — |
| `--domains` | 用逗号分隔的域名过滤器 | — |
| `--lang` | 语言代码（`pt`、`en`、`es`等） | — |
| `--json` | 原始 JSON 输出 | 关闭 |

## 示例

```bash
# Search with recency filter
{baseDir}/scripts/search.sh --recency week "OpenAI latest announcements"

# Search restricted to specific domains
{baseDir}/scripts/search.sh --domains "arxiv.org,nature.com" "transformer architecture advances"

# Search in Portuguese
{baseDir}/scripts/search.sh --lang pt "inteligência artificial no Brasil"

# Deep research with JSON output
{baseDir}/scripts/search.sh --mode research --json "enterprise AI adoption trends"
```

## API 密钥

设置 `PERPLEXITY_API_KEY` 环境变量：
```bash
export PERPLEXITY_API_KEY="pplx-..."
```

## 定价参考

- **搜索（sonar-pro）：** 每次查询约 0.01 美元 |
- **推理（sonar-reasoning-pro）：** 每次查询约 0.02 美元 |
- **深度研究（sonar-deep-research）：** 每次查询约 0.40 美元（包含多次搜索和推理）

建议日常查询使用 `search` 模式；只有在需要详尽分析时才使用 `research` 模式。