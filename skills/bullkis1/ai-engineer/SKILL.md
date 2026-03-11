---
name: ai-engineer
description: AI/机器学习（ML）工程专家，专注于构建智能功能、检索与建议（RAG）系统、大型语言模型（LLM）集成、数据管道、向量搜索以及基于AI的应用程序。适用于涉及以下领域的开发工作：大型语言模型、嵌入技术、向量数据库、检索与建议系统、模型微调、提示工程（prompt engineering）、AI代理、机器学习管道，以及将模型部署到生产环境。不适用于一般的Web开发（请使用快速原型工具）或简单的API调用。
  AI/ML engineering specialist for building intelligent features, RAG systems,
  LLM integrations, data pipelines, vector search, and AI-powered applications.
  Use when building anything involving: LLMs, embeddings, vector databases, RAG,
  fine-tuning, prompt engineering, AI agents, ML pipelines, or deploying models
  to production. NOT for general web dev (use rapid-prototyper) or simple API calls.
---
# 人工智能工程师

构建能够在生产环境中运行的实用人工智能系统。这些系统以数据驱动、系统化且注重性能为特点。

## 核心能力

- **大语言模型（LLM）集成**：OpenAI、Anthropic，以及本地模型（Ollama、llama.cpp、LiteLLM）
- **检索与生成（RAG）系统**：数据分块、嵌入处理、向量搜索、信息检索、结果重排序
- **向量数据库**：Chroma（本地部署）、Pinecone（托管型）、Weaviate、FAISS、Qdrant
- **代理与工具**：调用外部工具、多步骤任务处理、OpenClaw子代理
- **数据管道**：数据导入、清洗、转换、特征工程
- **机器学习运维（MLOps）**：模型版本管理（MLflow）、监控、模型漂移检测、A/B测试
- **评估**：构建基准测试集、检测偏见、评估性能指标

## 决策框架

### 选择哪种大语言模型？
- **原型开发/速度要求**：OpenAI GPT-4o 或 Anthropic Claude Sonnet
- **本地部署/私有环境**：Ollama + Qwen 2.5 32B 或 Llama 3.3 70B
- **多模型集成**：LiteLLM（无需修改代码即可切换模型）
- **嵌入算法**：text-embedding-3-small（OpenAI）或 nomic-embed-text（本地实现）

### 选择哪种向量数据库？
- **本地开发/测试环境**：Chroma（无需额外配置）
- **生产环境**：Pinecone
- **自托管的生产环境**：Qdrant 或 Weaviate
- **如果系统已使用 PostgreSQL**：可使用 pgvector 扩展

### 应该先使用 RAG 还是微调模型？
- **优先使用 RAG**：在大多数情况下，先尝试 RAG 即可；90% 的场景下 RAG 已能满足需求。
- 仅在需要改变模型风格/语气、领域词汇高度专业化、或对延迟有严格要求时才进行微调

## RAG 工作流程

### 1. 数据导入
```python
# Chunk documents (rule of thumb: 512 tokens, 50 overlap)
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
chunks = splitter.split_documents(docs)
```

### 2. 数据嵌入与存储
```python
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

client = chromadb.PersistentClient(path="./chroma_db")
ef = OpenAIEmbeddingFunction(api_key=os.environ["OPENAI_API_KEY"], model_name="text-embedding-3-small")
collection = client.get_or_create_collection("docs", embedding_function=ef)
collection.add(documents=[c.page_content for c in chunks], ids=[str(i) for i in range(len(chunks))])
```

### 3. 信息检索与内容生成
```python
results = collection.query(query_texts=[user_query], n_results=5)
context = "\n\n".join(results["documents"][0])

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"Answer based on this context:\n{context}"},
        {"role": "user", "content": user_query},
    ]
)
```

有关高级技术模式（如结果重排序、混合搜索、HyDE、评估方法），请参阅 `references/rag-patterns.md`。

## 大语言模型的工具调用（代理机制）

```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_docs",
        "description": "Search internal documentation",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

response = openai.chat.completions.create(model="gpt-4o", messages=messages, tools=tools)
```

有关多步骤任务处理、错误处理及工具使用规范，请参阅 `references/agent-patterns.md`。

## 重要规则

- **尽早进行评估**：在构建系统之前先建立评估数据集。
- **务必先使用 RAG**：在微调之前必须先应用 RAG 技术。
- **记录所有操作**：从项目开始就记录提示内容、模型输出结果、执行耗时以及令牌使用情况。
- **检测偏见**：尤其是对于面向用户的分类或评分系统，必须进行偏见检测。
- **切勿硬编码 API 密钥**：应使用环境变量或密钥管理工具来存储 API 密钥。

## 参考资料

- `references/rag-patterns.md`：数据分块策略、结果重排序、HyDE 技术、混合搜索方法、评估流程
- `references/agent-patterns.md`：工具调用机制、多步骤任务处理流程、内存管理策略、错误处理方法