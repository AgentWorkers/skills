---
name: Research Logger
version: 1.0.0
description: 具备自动 SQLite 日志记录和 Langfuse 跟踪功能的人工智能研究流程
author: aiwithabidi
---
# Research Logger 📚

这是一个用于AI研究的自动化日志记录工具。它支持通过“Perplexity”指标进行搜索，并将搜索结果连同主题/项目元数据一起自动保存到SQLite数据库中，同时提供完整的Langfuse追踪功能。从此，您再也不会丢失任何研究记录了。

## 使用方法

```bash
# Search and auto-save to SQLite
python3 scripts/research_logger.py log quick "what is RAG?"

# Research with topic tagging
python3 scripts/research_logger.py log pro "compare vector databases" --topic "AI infrastructure"

# Search past research entries
python3 scripts/research_logger.py search "AI"

# View recent entries
python3 scripts/research_logger.py recent --limit 5
```

## 系统要求

- 必需的环境变量：`PERPLEXITY_API_KEY`
- 可选的环境变量：`LANGFUSE_PUBLIC_KEY`、`LANGFUSE_SECRET_KEY`、`LANGFUSE_HOST`（用于追踪功能）
- Python 3.10及以上版本
- 必需安装的软件包：`requests`、`langfuse`
- SQLite（Python内置支持）

## 致谢

该工具由**AgxntSix**开发——这是一个由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)开发的AI操作代理工具。
🌐 [agxntsix.ai](https://www.agxntsix.ai) | 属于OpenClaw代理的**AgxntSix Skill Suite**系列产品之一