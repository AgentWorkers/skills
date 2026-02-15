---
name: baml-codegen
description: "**使用说明：**  
本工具适用于生成用于类型安全的 Large Language Model（LLM）提取、分类、RAG（Retrieval with Aggregation）或代理工作流的 BAML（Binary Application Markup Language）代码。它能够根据自然语言需求自动生成包含类型、函数、客户端、测试以及框架集成的完整 .baml 文件。用户可通过 MCP（BoundaryML Command Prompt）查询官方 BoundaryML 仓库中的实时模式。该工具支持多模态输入（图像、音频），兼容 Python、TypeScript、Ruby、Go 等编程语言，以及 10 多种开发框架。在代码编译过程中，可实现 50-70% 的token优化，并保证 95% 以上的编译成功率。"
license: "Apache-2.0"
compatibility: "Requires MCP servers: baml_Docs (required), baml_Examples (optional). Works offline with 80% functionality using cached patterns."
---

# BAML代码生成

用于生成类型安全的LLM（大型语言模型）提取代码。适用于创建结构化输出、分类、RAG（检索、聚合和生成）或代理工作流。

## 重要规则

- **切勿编辑`baml_client/`目录**：该目录中的代码完全由工具自动生成，在每次运行`baml-cli generate`时都会被覆盖。请查看`baml_src/generators.baml`文件以确定输出语言（python、typescript、ruby或go）。
- **务必编辑`baml_src/`目录**：该目录是所有BAML代码的来源。
- **在修改代码后运行`baml-cli generate`：工具会重新生成目标语言的客户端代码。

## 设计理念（简而言之）

- **数据模型先行**：首先定义数据模型，编译器会根据模型自动添加类型信息。
- **优先使用类型而非字符串**：应使用枚举（enum）、类（class）或联合类型（union），避免字符串解析。
- **BAML负责处理复杂的输入数据**：BAML能够从格式混乱的LLM输出中提取有效的JSON数据。
- **BAML是一个转换工具，而非库**：用户只需编写`.baml`文件，工具会自动生成Python、TypeScript、Ruby或Go等目标语言的代码，无需额外的运行时依赖。
- **基于测试的迭代开发**：可以使用VS Code的Playground功能或`baml-cli test`命令进行代码测试和迭代。

## 工作流程

```
Analyze → Pattern Match (MCP) → Validate → Generate → Test → Deliver
         ↓ [IF ERRORS] Error Recovery (MCP) → Retry
```

## BAML语法

| 元素        | 例子                                      |
|-------------|-----------------------------------------|
| 类（Class）      | `class Invoice { total float @description("金额") @assert(this > 0) @alias("amt") }` |
| 枚举（Enum）     | `enum Category { Tech @alias("技术领域") @description("科技行业"), Finance, Other }` |
| 函数（Function）    | `function Extract(text: string, img: image?) -> Invoice { client GPT5 prompt ## "{{ text }} {{ img }} {{ ctx.output_format }}" # }` |
| 客户端（Client）    | `client<llm> GPT5 { provider openai options { model: gpt-5 } retry_policy: Exponential }` |
| 回退策略（Fallback） | `client<llm> Resilient { provider: fallback options { strategy: [FastModel, SlowModel] } }` |

## 数据类型

- **基本类型**：`string`, `int`, `float`, `bool`
- **多模态类型**：`image`, `audio`
- **容器类型**：`Type[]`（数组）、`Type?`（可选）、`map<string, Type>`（键值对）
- **复合类型**：`Type1 | Type2`（联合类型）、嵌套类
- **注释**：`@description("...")`, `@assert(condition)`, `@alias("json_name")`, `@check(name, condition)`

## 提供者（Providers）

- `openai`, `anthropic`, `gemini`, `vertex`, `bedrock`, `ollama`；以及通过`openai-generic`兼容的其他OpenAI提供商

## 模式分类

| 模式          | 使用场景                                      | 模型                          | 框架标记                          |
|------------------|----------------------------------|----------------------------------------|-------------------------------------------|
| 提取（Extraction）   | 将非结构化数据转换为结构化数据           | GPT-5                         | fastapi, next.js                         |
| 分类（Classification） | 对输入内容进行分类                         | GPT-5-mini                         | 任意框架                         |
| RAG（Retrieval, Aggregation, and Generation） | 从文本中提取信息并生成答案           | GPT-5                         | langgraph                         |
| 代理（Agents）      | 执行多步骤推理                             | GPT-5                         | langgraph                         |
| 视觉处理（Vision）    | 从图像/音频数据中提取信息                   | GPT-5-Vision                     | multimodal                         |

## 容错机制（Resilience）

- **重试策略（Retry Policy）**：`retry_policy: Exponential { max_retries: 3, strategy: exponential_backoff }`
- **回退机制（Fallback）**：根据成本和可靠性需求，依次使用不同的模型（如`FastModel`、`SlowModel`）

## MCP（Model Compatibility Protocol）指标

- **模式验证**：根据`baml-examples`中的模式进行验证。
- **错误处理**：使用文档修复潜在问题。
- **MCP不可用时**：启用回退机制以继续执行。

## 输出成果

- **BAML代码**：完整的`.baml`文件（包含类型定义、函数、客户端代码及重试策略）
- **测试**：使用pytest/Jest进行100%的函数覆盖率测试。
- **集成**：针对特定框架生成的客户端代码（如LangGraph节点、FastAPI接口、Next.js API路由）。
- **元数据**：使用的模式、生成的token数量、成本估算等信息。

## 参考资料

- [providers.md](referencesproviders.md)：OpenAI、Anthropic、Google、Ollama、Azure、Bedrock、openai-generic等提供商的详细信息。
- [types-and-schemas.md](references/types-and-schemas.md)：完整的类型系统、枚举、联合类型、映射结构、图像/音频类型。
- [validation.md](references/validation.md)：类型验证相关注释和函数。
- [patterns.md](references/patterns.md)：包含代码示例的模式库。
- [philosophy.md](references/philosophy.md)：BAML的设计理念和重要规则。
- [mcp-interface.md](references/mcp-interface.md)：查询工作流程和缓存机制。
- [languages-python.md](references/languages-python.md)：Python语言及Pydantic库的使用。
- [languages-typescript.md](references/languages-typescript.md)：TypeScript语言及React/Next.js框架的集成。
- [frameworks-langgraph.md](references/frameworks-langgraph.md)：LangGraph框架的集成方式。