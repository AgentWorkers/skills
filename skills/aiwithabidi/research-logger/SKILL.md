---
name: research-logger
description: AI research pipeline with automatic logging. Search via Perplexity, auto-save results to SQLite with topic and project metadata, full Langfuse tracing. Never lose a research session again. Use when conducting research, competitive analysis, or building a knowledge base.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Perplexity API key
metadata: {"openclaw": {"emoji": "\ud83d\udcdd", "requires": {"env": ["PERPLEXITY_API_KEY"]}, "primaryEnv": "PERPLEXITY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 研究日志记录器 📝🔬  
具备搜索和自动保存功能：每次研究查询都会通过 Langfuse 追踪工具被记录到 SQLite 数据库中。  

## 使用场景  
- 需要保存以便日后查阅的研究内容  
- 从重复的搜索中构建知识库  
- 回顾某个主题的过往研究记录  
- 创建研究决策的审计追踪记录  

## 使用方法  
```bash
# Search and auto-log
python3 {baseDir}/scripts/research_logger.py log quick "what is RAG"
python3 {baseDir}/scripts/research_logger.py log pro "compare vector databases" --topic "databases"

# Search past research
python3 {baseDir}/scripts/research_logger.py search "vector databases"

# View recent entries
python3 {baseDir}/scripts/research_logger.py recent --limit 5
```  

## 致谢  
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)