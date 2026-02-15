---
name: deep-search
version: 1.0.0
description: >
  **多层复杂性搜索功能（Multi-tier Perplexity Search）与 Langfuse 跟踪技术**  
  该搜索系统提供三种搜索深度级别：  
  - **快速搜索（Quick Search, Sonar）**  
  - **高级搜索（Advanced Search, Sonar-Pro）**  
  - **深度搜索（Deep Search, Sonar-Reasoning-Pro）**  
  支持多种搜索焦点模式：  
  - **互联网（Internet）**  
  - **学术（Academic）**  
  - **新闻（News）**  
  - **YouTube**  
  - **Reddit**  
  搜索结果会附带 AI 合成的答案及相关引用。  
  适用于研究、比较、市场分析及事实核查等场景。  
  **可使用的搜索指令/功能：**  
  - **search**  
  - **research**  
  - **look up**  
  - **find out**  
  - **compare**  
  - **what is**  
  - **deep search**  
  - **web research**
license: MIT
compatibility:
  openclaw: ">=0.10"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["PERPLEXITY_API_KEY"]
---
# 深度搜索 🔍

基于多层Perplexity算法的搜索系统，支持自动Langfuse追踪功能。

## 使用场景

- 快速获取事实信息或简单查询 → 使用“quick”层级
- 标准研究、对比分析、操作指南 → 使用“pro”层级
- 深度分析、市场调研、复杂问题 → 使用“deep”层级
- 学术论文搜索、新闻监测、Reddit/YouTube内容分析 → 使用“deep”层级

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

## 系统层级

| 层级 | 模型 | 执行速度 | 适用场景 |
|------|-------|-------|----------|
| quick | sonar | 约2秒 | 简单事实查询、快速查找 |
| pro | sonar-pro | 约5-8秒 | 研究、对比分析 |
| deep | sonar-reasoning-pro | 约10-20秒 | 深度分析、复杂问题 |

## 系统要求

- `PERPLEXITY_API_KEY`：必需的Perplexity API密钥。
- `OPENROUTER_API_KEY`：可选，用于Langfuse追踪功能的定价。

## 开发者信息

由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)和[agxntsix.ai](https://www.agxntsix.ai)共同开发。
相关视频：[YouTube](https://youtube.com/@aiwithabidi)
代码仓库：[GitHub](https://github.com/aiwithabidi)
该功能属于**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。

📅 **需要帮助为您的企业配置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)