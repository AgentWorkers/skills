---
name: LangChain
description: 避免常见的 LangChain 错误——LCEL 潜在问题、内存持久化、RAG 分块处理以及输出解析器相关的问题。
metadata: {"clawdbot":{"emoji":"🦜","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## LCEL基础
- `|` 管道将输出传递给下一个处理步骤（例如：`prompt | llm | parser`）
- `RunnablePassthrough()` 会原样传递输入数据，适用于并行处理的分支
- `RunnableParallel` 可以同时运行多个分支（例如：`{"a": chain1, "b": chain2}`）
- `.invoke()` 用于单个请求，`.batch()` 用于批量请求，`.stream()` 用于处理多个令牌
- 输入数据必须与预期的键匹配（例如：如果提示要求 `{question}`，则输入必须是 `{"question": x}` 而不是简单的 `x`）

## 关于内存的使用
- 内存数据不会在会话之间自动保存，需要手动进行保存/加载
- `ConversationBufferMemory` 的使用可能导致内存占用无限增长，建议使用 `ConversationSummaryMemory` 来处理长时间的对话
- 内存键必须与提示中的变量相匹配（例如：如果提示中使用了 `{chat_history}`，则内存键也应为 `memory_key="chat_history"`）
- 对于聊天模型，设置 `return_messages=True` 可以输出完整的对话内容；对于完成型模型，设置 `return_messages=False` 可以仅返回字符串结果

## RAG（Retrieval with Aggregation）分块技术
- 分块的大小会影响检索质量：过小会导致上下文丢失，过大则会影响检索的准确性
- 分块之间应有一定的重叠（通常为 10-20%），以避免在句子中间中断检索
- `RecursiveCharacterTextSplitter` 会保留文本的结构，先按段落分割再按句子分割
- 嵌入层的维度必须与向量存储的维度相匹配，否则可能导致运行失败

## 输出解析器
- `PydanticOutputParser` 需要在提示中提供格式化指令（通过调用 `.get_formatinstructions()` 来设置）
- 解析器可能会出现错误，但错误可能不会明显显示；格式错误的 JSON 数据仍可能被部分解析
- `OutputFixingParser` 会尝试使用 LLM 重新解析数据，并修复错误
- 对于支持结构化输出的模型，可以使用 `with_structured_output()` 来提高解析的准确性

## 数据检索
- `similarity_search` 可以返回相关文档；`.page_content` 可以获取文档的内容
- `k` 参数用于控制返回的结果数量：过多的结果可能反而降低检索效果，因为会增加噪声
- 在进行相似性检索之前，可以对元数据进行过滤（例如：在大多数向量存储中，可以使用 `filter={"source": "docs"}`）
- `max_marginal_relevance_search` 可以提高检索结果的多样性，避免重复出现相似的内容

## 代理（Agents）
- 代理会动态决定工具的使用顺序；工具的顺序是固定的
- 工具的描述非常重要，代理会根据这些描述来决定何时使用某个工具
- 设置 `handle_parsing_errors=True` 可以防止因代理输出格式错误而导致程序崩溃
- 设置 `max_iterations` 可以避免无限循环；默认值 `max_iterations=10` 可能较低，需要根据实际情况进行调整

## 常见错误
- 提示模板中的变量是区分大小写的（例如：`{Question}` 和 `{question}` 是不同的）
- 聊天模型需要特定的消息格式，请使用 `ChatPromptTemplate` 而不是 `PromptTemplate`
- 回调函数可能无法正确传递；请通过 `config={"callbacks": [...]}` 将回调函数传递给代理
- 有时速率限制会导致程序异常退出，可以使用重试逻辑来处理这种情况
- 如果令牌数量过多，可能会导致上下文丢失；对于较长的对话记录，可以使用 `trim_messages` 或摘要功能来处理数据