---
name: local-rag-search
description: 如何高效地使用 mcp-local-rag 服务器进行带有语义相似性排序的网页搜索？当您需要从互联网上搜索最新信息、跨多个来源研究特定主题，或在不依赖外部 API 的情况下获取所需内容时，可以运用这项技能。该技能将指导您如何有效地利用基于 RAG（Retrieval, Augmentation, and Generation）的搜索技术，结合 DuckDuckGo、Google 等搜索引擎以及多引擎深度搜索功能来提升搜索效果。
---

# 本地RAG搜索技能

该技能允许您高效地使用mcp-local-rag MCP服务器进行智能网页搜索，并具备语义排名功能。该服务器通过类似RAG（Retrieval, Augmentation, and Generation）的相似性评分机制来优先显示最相关的结果，而无需依赖任何外部API。

## 可用工具

### 1. `rag_search_ddgs` - DuckDuckGo搜索
适用于注重隐私的通用网页搜索。

**使用场景：**
- 用户偏好注重隐私的搜索方式
- 查找通用信息
- 大多数查询的默认选择

**参数：**
- `query`：自然语言搜索查询
- `num_results`：返回的初始结果数量（默认：10）
- `top_k`：返回的最相关结果数量（默认：5）
- `include_urls`：是否包含源URL（默认：true）

### 2. `rag_search_google` - Google搜索
适用于进行综合性、技术性或详细内容的搜索。

**使用场景：**
- 技术或科学类查询
- 需要全面的信息覆盖
- 搜索特定文档

### 3. `deep_research` - 多引擎深度搜索
适用于跨多个搜索引擎进行综合性研究。

**使用场景：**
- 研究需要广泛覆盖范围的复杂主题
- 需要从多个来源获取多样化的观点
- 收集关于某个主题的全面信息

**可用的后端：**
- `duckduckgo`：注重隐私的通用搜索
- `google`：全面的科技搜索结果
- `bing`：微软的搜索引擎
- `brave`：以隐私为先的搜索引擎
- `wikipedia`：百科全书/事实性内容
- `yahoo`, `yandex`, `mojeek`, `grokipedia`：其他替代搜索引擎

**默认设置：`["duckduckgo", "google"]`

### 4. `deep_research_google` - 仅使用Google的深度搜索
仅使用Google进行深度搜索的快捷方式。

### 5. `deep_research_ddgs` - 仅使用DuckDuckGo的深度搜索
仅使用DuckDuckGo进行深度搜索的快捷方式。

## 最佳实践

### 查询构建
1. **使用自然语言**：将查询写成问题或描述性短语
   - 例如：`最新的量子计算发展`
   - 例如：`如何在Python中实现二分搜索`
   - 避免使用单独的关键词（如“quantum”或“Python”）

2. **具体化**：包含上下文和细节
   - 例如：`2024年React钩子的最佳实践`
   - 更好的示例：`React useEffect清理函数的最佳实践`

### 工具选择策略

1. **单一主题，快速回答** → 使用`rag_search_ddgs`或`rag_search_google`
   ```
   rag_search_ddgs(
       query="What is the capital of France?",
       top_k=3
   )
   ```

2. **技术/科学类查询** → 使用`rag_search_google`
   ```
   rag_search_google(
       query="Docker multi-stage build optimization techniques",
       num_results=15,
       top_k=7
   )
   ```

3. **综合性研究** → 使用`deep_research`并结合多个搜索词
   ```
   deep_research(
       search_terms=[
           "machine learning fundamentals",
           "neural networks architecture",
           "deep learning best practices 2024"
       ],
       backends=["google", "duckduckgo"],
       top_k_per_term=5
   )
   ```

4. **事实/百科内容** → 使用`deep_research`并结合Wikipedia
   ```
   deep_research(
       search_terms=["World War II timeline", "WWII key battles"],
       backends=["wikipedia"],
       num_results_per_term=5
   )
   ```

### 参数调整

**快速获取答案时：**
- `num_results=5-10`, `top_k=3-5`

**进行综合性研究时：**
- `num_results=15-20`, `top_k=7-10`

**进行深度研究时：**
- `num_results_per_term=10-15`, `top_k_per_term=3-5`
- 使用2-5个相关的搜索词
- 使用2-5个后端（越多后端，信息越全面，但搜索速度越慢）

## 工作流程示例

### 示例1：当前事件
```
Task: "What happened at the UN climate summit last week?"

1. Use rag_search_google for recent news coverage
2. Set top_k=7 for comprehensive view
3. Present findings with source URLs
```

### 示例2：技术深度研究
```
Task: "How do I optimize PostgreSQL queries?"

1. Use deep_research with multiple specific terms:
   - "PostgreSQL query optimization techniques"
   - "PostgreSQL index best practices"
   - "PostgreSQL EXPLAIN ANALYZE tutorial"
2. Use backends=["google", "stackoverflow"] if available
3. Synthesize findings into actionable guide
```

### 示例3：多角度研究
```
Task: "Research the impact of remote work on productivity"

1. Use deep_research with diverse search terms:
   - "remote work productivity statistics 2024"
   - "hybrid work model effectiveness studies"
   - "work from home challenges research"
2. Use backends=["google", "duckduckgo"] for broad coverage
3. Synthesize different perspectives and studies
```

## 指导原则

1. **始终引用来源**：当`include_urls=True`时，在回答中引用源URL
2. **验证时效性**：检查内容是否最新且相关
3. **交叉验证**：对于重要事实，使用多个搜索词或搜索引擎
4. **尊重隐私**：除非有特殊需求，否则使用DuckDuckGo进行通用搜索
5. **批量相关查询**：在研究某个主题时，为`deep_research`创建多个相关搜索词
6. **语义相关性**：信任RAG评分机制——排名靠前的结果在语义上与查询最为接近
7. **解释选择理由**：简要说明使用的是哪个工具及其原因

## 错误处理

如果搜索结果不足：
1. 尝试用不同的关键词重新构建查询
2. 更换后端
3. 增加`num_results`参数
4. 使用`deep_research`并结合多个相关搜索词

## 隐私考虑

- DuckDuckGo：注重隐私，不追踪用户行为
- Google：信息最全面，但会记录搜索记录
- 除非用户有特定需求，否则建议默认使用DuckDuckGo

## 性能说明

- 第一次搜索可能较慢（模型加载）
- 后续搜索速度更快（模型已缓存）
- 使用的后端越多，信息越全面，但搜索速度越慢
- 根据实际需求调整`num_results`和`top_k`参数