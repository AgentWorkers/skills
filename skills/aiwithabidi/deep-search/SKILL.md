---
name: deep-search
description: Three-tier AI search routing — quick facts (sonar), research comparisons (sonar-pro), and deep analysis (sonar-reasoning-pro). Auto-selects model tier based on query complexity. Focus modes: internet, academic, news, youtube, reddit. Use for research, fact-checking, competitive analysis, or any web search task.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Perplexity API key
metadata: {"openclaw": {"emoji": "\ud83d\udd0e", "requires": {"env": ["PERPLEXITY_API_KEY"]}, "primaryEnv": "PERPLEXITY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 深度搜索 🔍

基于多层Perplexity算法的搜索系统，支持自动的Langfuse追踪功能。

## 使用场景

- 快速获取事实或简单查询 → 使用“quick”层级  
- 标准研究、对比分析、操作指南 → 使用“pro”层级  
- 深度分析、市场调研、复杂问题 → 使用“deep”层级  
- 学术论文搜索、新闻监控、Reddit/YouTube内容分析 → 使用“deep”层级  

## 使用方法  

```bash
# Quick search (sonar, ~2s)
python3 {baseDir}/scripts/deep_search.py quick "what is OpenClaw"

# Pro search (sonar-pro, ~5-8s)
python3 {baseDir}/scripts/deep_search.py pro "compare Claude vs GPT-4o for coding"

# Deep research (sonar-reasoning-pro, ~10-20s)
python3 {baseDir}/scripts/deep_search.py deep "full market analysis of AI agent frameworks"

# Focus modes
python3 {baseDir}/scripts/deep_search.py pro "query" --focus academic
python3 {baseDir}/scripts/deep_search.py pro "query" --focus news
python3 {baseDir}/scripts/deep_search.py pro "query" --focus youtube
python3 {baseDir}/scripts/deep_search.py pro "query" --focus reddit
```  

## 级别划分  

| 级别 | 模型 | 执行速度 | 适用场景 |
|------|-------|-------|----------|
| quick | sonar | 约2秒 | 简单事实查询、快速查找 |
| pro | sonar-pro | 约5-8秒 | 研究、对比分析 |
| deep | sonar-reasoning-pro | 约10-20秒 | 深度分析、复杂问题 |

## 环境要求  

- `PERPLEXITY_API_KEY` — 必需项：Perplexity API密钥  
- `OPENROUTER_API_KEY` — 可选项：用于Langfuse追踪功能的定价信息  

## 开发者信息  
由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)和[agxntsix.ai](https://www.agxntsix.ai)共同开发  
[YouTube频道](https://youtube.com/@aiwithabidi) | [GitHub仓库](https://github.com/aiwithabidi)  
该功能是**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。  

📅 **需要帮助为您的企业配置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)