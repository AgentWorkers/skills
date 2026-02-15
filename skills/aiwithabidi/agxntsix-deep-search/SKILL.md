---
name: Deep Search
version: 1.0.0
description: 三层复杂性AI搜索路由系统，具备自动模型选择功能
author: aiwithabidi
---
# 深度搜索 🔍

该搜索系统采用三层复杂性AI路由机制：  
- **快速搜索（sonar）**：适用于简单查询；  
- **深度研究（sonar-pro）**：适用于复杂查询；  
- **高级分析（sonar-reasoning-pro）**：适用于需要深入逻辑推理的查询。  
系统会根据查询的复杂性自动选择合适的搜索层级。  

**搜索模式**：  
- 互联网  
- 学术  
- 新闻  
- YouTube  
- Reddit  

## 使用方法  

```bash
# Quick lookup (sonar)
python3 scripts/deep_search.py quick "what is OpenClaw?"

# Research-grade (sonar-pro)
python3 scripts/deep_search.py pro "compare LangChain vs LlamaIndex"

# Deep analysis (sonar-reasoning-pro)
python3 scripts/deep_search.py deep "full market analysis of AI agent frameworks"

# Focus modes
python3 scripts/deep_search.py pro "query" --focus academic
python3 scripts/deep_search.py pro "query" --focus news
python3 scripts/deep_search.py pro "query" --focus youtube
python3 scripts/deep_search.py pro "query" --focus reddit
```  

## 系统要求**：  
- 必需设置 `PERPLEXITY_API_KEY` 环境变量；  
- 系统运行环境需支持 Python 3.10 及以上版本；  
- 需安装 `requests` 包。  

## 开发者信息**：  
该工具由 **AgxntSix** 开发，**AgxntSix** 是由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 创立的 AI 操作代理平台。  
🌐 [agxntsix.ai](https://www.agxntsix.ai) | 属于 OpenClaw 代理工具套件（AgxntSix Skill Suite）的一部分。