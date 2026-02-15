---
name: research-logger
version: 1.0.0
description: 自动将深度搜索结果保存到 SQLite 和 Langfuse 数据库中。同时，该系统将搜索功能与持久化日志记录功能相结合：每次搜索都会记录下相关主题标签、时间戳以及完整的搜索结果。用户可以查看以往的搜索记录，也可以查看最近进行的搜索操作。触发事件包括：记录搜索内容、保存搜索结果、查询搜索历史记录、查找之前的研究内容等。
license: MIT
compatibility:
  openclaw: ">=0.10"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["PERPLEXITY_API_KEY"]
---
# Research Logger 📝🔬  
搜索 + 自动保存功能：每次研究查询都会通过 Langfuse 追踪工具被记录到 SQLite 数据库中。  

## 使用场景  
- 需要保存以便后续查阅的研究结果  
- 从重复的搜索中构建知识库  
- 回顾某个主题的过往研究内容  
- 创建研究决策的审计记录  

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
该工具是 OpenClaw 代理的 **AgxntSix Skill Suite** 的组成部分。  

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)