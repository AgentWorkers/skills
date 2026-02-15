---
name: mcp-builder
description: **创建高质量MCP（Model Context Protocol）服务器的指南**  
本指南旨在帮助您构建能够支持大型语言模型（LLMs）通过设计良好的工具与外部服务交互的MCP服务器。无论您使用Python（FastMCP）还是Node/TypeScript（MCP SDK）来开发MCP服务器，本指南都适用于集成外部API或服务的场景。  

**MCP简介**  
MCP（Model Context Protocol）是一种用于在大型语言模型（LLMs）与外部系统之间传递上下文信息的协议。通过MCP，LLMs可以获取必要的数据或执行特定操作，从而实现更高效、更灵活的交互。  

**构建MCP服务器的关键步骤**：  
1. **设计数据结构**：明确需要传递给LLMs的数据格式和结构。  
2. **实现通信接口**：编写代码以实现与外部服务的通信，确保数据能够正确地发送和接收。  
3. **处理错误和异常**：确保系统能够优雅地处理可能出现的错误和异常情况。  
4. **测试和调试**：对MCP服务器进行彻底的测试，确保其稳定性和可靠性。  

**示例代码**：  
- **Python（FastMCP）示例**：提供使用FastMCP框架构建MCP服务器的代码示例。  
- **Node/TypeScript（MCP SDK）示例**：提供使用MCP SDK构建MCP服务器的代码示例。  

**注意事项**：  
- 请确保遵循相关编程语言和框架的最佳实践。  
- 根据实际需求调整代码示例以适应您的具体应用场景。  
- 定期更新和优化MCP服务器，以适应新的技术和需求变化。  

**资源链接**：  
- [FastMCP官方文档](https://fastmcp.readthedocs.io/)  
- [MCP SDK官方文档](https://clawhub.com/docs/mcp-sdk/)  

**使用建议**：  
- 在构建集成外部服务的LLM应用时，优先考虑使用MCP协议。  
- 通过参考本指南和示例代码，您可以快速、高效地实现MCP服务器的功能。  

希望本指南能对您有所帮助！如有任何疑问，请随时联系我们。
license: Complete terms in LICENSE.txt
---

# MCP服务器开发指南

## 概述

要创建高质量的中模型上下文协议（MCP）服务器，以帮助大语言模型（LLMs）有效地与外部服务进行交互，请使用本指南。MCP服务器提供了工具，使LLMs能够访问外部服务和API。MCP服务器的质量体现在它能够多好地帮助LLMs利用这些工具完成实际任务。

---

# 开发流程

## 🚀 高级工作流程

创建高质量MCP服务器涉及四个主要阶段：

### 第1阶段：深入研究与规划

#### 1.1 理解以代理为中心的设计原则

在开始实现之前，通过以下原则来了解如何为AI代理设计工具：

**为工作流程而设计，而不仅仅是API端点：**
- 不要仅仅封装现有的API端点——而是构建有意义、影响深远的工作流程工具
- 整合相关操作（例如，`schedule_event`函数既检查可用性又创建事件）
- 专注于能够完成完整任务的工具，而不仅仅是单个API调用
- 考虑代理实际需要完成的工作流程

**针对有限的上下文进行优化：**
- 代理的上下文窗口是有限的——每个标记都至关重要
- 返回高信号信息，而不是详尽的数据转储
- 提供“简洁”与“详细”的响应格式选项
- 默认使用人类可读的标识符，而不是技术代码（名称而非ID）
- 将代理的上下文预算视为稀缺资源

**设计可操作的错误信息：**
- 错误信息应引导代理使用正确的模式
- 建议具体的下一步操作：“尝试使用`filter='active_only'来减少结果”
- 使错误具有教育意义，而不仅仅是诊断信息
- 通过清晰的反馈帮助代理学习正确的工具使用方法

**遵循自然的任务划分：**
- 工具名称应反映人类的思维方式
- 使用一致的前缀对相关工具进行分组，以便于发现
- 围绕自然的工作流程设计工具，而不仅仅是API结构

**采用评估驱动的开发方式：**
- 尽早创建现实的评估场景
- 让代理的反馈推动工具的改进
- 快速原型设计，并根据代理的实际表现进行迭代

#### 1.3 学习MCP协议文档

**获取最新的MCP协议文档：**

使用WebFetch加载：`https://modelcontextprotocol.io/llms-full.txt`

这份全面的文档包含了完整的MCP规范和指南。

#### 1.4 学习框架文档

**加载并阅读以下参考文件：**

- **MCP最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 所有MCP服务器的核心指南

**对于Python实现，还需加载：**
- **Python SDK文档**：使用WebFetch加载`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python实现指南](./reference/python_mcp_server.md) - Python特定的最佳实践和示例

**对于Node/TypeScript实现，还需加载：**
- **TypeScript SDK文档**：使用WebFetch加载`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript实现指南](./reference/node_mcp_server.md) - Node/TypeScript特定的最佳实践和示例

#### 1.5 彻底研究API文档**

为了集成某个服务，请阅读所有可用的API文档：
- 官方API参考文档
- 认证和授权要求
- 速率限制和分页模式
- 错误响应和状态码
- 可用的端点及其参数
- 数据模型和模式

**根据需要使用网络搜索和WebFetch工具来收集全面的信息。**

#### 1.6 制定详细的实施计划**

基于你的研究，制定一个详细的计划，包括：

**工具选择：**
- 列出最值得实现的端点/操作
- 优先考虑能够实现最常见和最重要用例的工具
- 考虑哪些工具可以协同工作以完成复杂的工作流程

**共享实用工具和辅助函数：**
- 识别常见的API请求模式
- 规划分页辅助函数
- 设计过滤和格式化工具
- 规划错误处理策略

**输入/输出设计：**
- 定义输入验证模型（Python使用Pydantic，TypeScript使用Zod）
- 设计一致的响应格式（例如JSON或Markdown），并配置详细的程度（例如详细或简洁）
- 规划大规模使用（数千用户/资源）
- 实现字符限制和截断策略（例如25,000个标记）

**错误处理策略：**
- 规划优雅的失败模式
- 设计清晰、可操作、对LLM友好的自然语言错误信息，提示进一步的操作
- 考虑速率限制和超时情况
- 处理认证和授权错误

---

### 第2阶段：实现

现在你有了一个全面的计划，按照语言特定的最佳实践开始实现。

#### 2.1 设置项目结构

**对于Python：**
- 创建一个单独的`.py`文件，如果复杂可以组织成模块（参见[🐍 Python指南](./reference/python_mcp_server.md)）
- 使用MCP Python SDK进行工具注册
- 定义Pydantic模型进行输入验证

**对于Node/TypeScript：**
- 创建适当的项目结构（参见[⚡ TypeScript指南](./reference/node_mcp_server.md)）
- 设置`package.json`和`tsconfig.json`
- 使用MCP TypeScript SDK
- 定义Zod模式进行输入验证

#### 2.2 首先实现核心基础设施

**在实现工具之前，先创建共享实用工具：**
- API请求辅助函数
- 错误处理辅助函数
- 响应格式化函数（JSON和Markdown）
- 分页辅助函数
- 认证/令牌管理

#### 2.3 系统地实现工具

对于计划中的每个工具：

**定义输入模式：**
- 使用Pydantic（Python）或Zod（TypeScript）进行验证
- 包含适当的约束（最小/最大长度、正则表达式模式、最小/最大值、范围）
- 提供清晰的字段描述
- 在字段描述中包含多样化的示例

**编写全面的文档字符串/描述：**
- 一句话总结工具的功能
- 详细解释用途和功能
- 明确的参数类型及示例
- 完整的返回类型模式
- 使用示例（何时使用，何时不使用）
- 错误处理文档，说明在遇到特定错误时应如何处理

**实现工具逻辑：**
- 使用共享实用工具避免代码重复
- 遵循异步/await模式进行所有I/O操作
- 实现适当的错误处理
- 支持多种响应格式（JSON和Markdown）
- 遵循分页参数
- 检查字符限制并进行适当的截断

**添加工具注释：**
- `readOnlyHint`：true（对于只读操作）
- `destructiveHint`：false（对于非破坏性操作）
- `idempotentHint`：true（如果重复调用有相同的效果）
- `openWorldHint`：true（如果与外部系统交互）

#### 2.4 遵循语言特定的最佳实践**

**此时，加载相应的语言指南：**

**对于Python：加载[🐍 Python实现指南](./reference/python_mcp_server.md)，并确保以下内容：**
- 使用MCP Python SDK进行正确的工具注册
- 使用`model_config`的Pydantic v2模型
- 全程使用类型提示
- 所有I/O操作都使用异步/await
- 适当的导入组织
- 模块级别的常量（CHARACTER_LIMIT, API_BASE_URL）

**对于Node/TypeScript：加载[⚡ TypeScript实现指南](./reference/node_mcp_server.md)，并确保以下内容：**
- 正确使用`server.registerTool`
- 使用`.strict()`的Zod模式
- 启用TypeScript严格模式
- 不使用`any`类型——使用适当的类型
- 明确的Promise<T>返回类型
- 构建构建过程（`npm run build`）

---

### 第3阶段：审查与优化

初步实现完成后：

#### 3.1 代码质量审查

为了确保质量，审查代码是否满足以下要求：
- **DRY原则**：工具之间没有重复代码
- **可组合性**：将共享逻辑提取到函数中
- **一致性**：类似的操作返回相似的格式
- **错误处理**：所有外部调用都有错误处理
- **类型安全**：完整的类型覆盖（Python类型提示，TypeScript类型）
- **文档**：每个工具都有全面的文档字符串/描述

#### 3.2 测试与构建

**重要提示：**MCP服务器是长时间运行的进程，它们通过标准输入/输出或sse/http等待请求。直接在主进程中运行它们（例如`python server.py`或`node dist/index.js`）会导致进程无限期挂起。

**安全的测试服务器的方法：**
- 使用评估框架（见第4阶段）——推荐的方法
- 在tmux中运行服务器，使其不在主进程中
- 在测试时设置超时：`timeout 5s python server.py`

**对于Python：**
- 验证Python语法：`python -m py_compile your_server.py`
- 通过检查文件来验证导入是否正确
- 手动测试：在tmux中运行服务器，然后在主进程中使用评估框架进行测试
- 或者直接使用评估框架（它负责标准输入/输出的传输）

**对于Node/TypeScript：**
- 运行`npm run build`并确保没有错误
- 验证是否生成了dist/index.js
- 手动测试：在tmux中运行服务器，然后在主进程中使用评估框架进行测试
- 或者直接使用评估框架（它负责标准输入/输出的传输）

#### 3.3 使用质量检查表

为了验证实现的质量，请从语言特定的指南中加载相应的检查表：
- Python：参见[🐍 Python指南](./reference/python_mcp_server.md)中的“质量检查表”
- Node/TypeScript：参见[⚡ TypeScript指南](./reference/node_mcp_server.md)中的“质量检查表”

---

### 第4阶段：创建评估

实现MCP服务器后，创建全面的评估来测试其有效性。

**加载[✅ 评估指南](./reference/evaluation.md)以获取完整的评估指南。**

#### 4.1 理解评估目的

评估用于测试LLMs是否能够有效地使用你的MCP服务器来回答现实、复杂的问题。

#### 4.2 创建10个评估问题

为了创建有效的评估，请按照评估指南中概述的流程进行：

1. **工具检查**：列出可用的工具并了解它们的功能
2. **内容探索**：使用只读操作来探索可用的数据
3. **问题生成**：创建10个复杂、现实的问题
4. **答案验证**：自己解决每个问题以验证答案

#### 4.3 评估要求

每个问题必须满足以下条件：
- **独立性**：不依赖于其他问题
- **只读**：只需要非破坏性操作
- **复杂性**：需要多次工具调用和深入探索
- **现实性**：基于人类关心的实际用例
- **可验证性**：答案可以通过字符串比较来验证
- **稳定性**：答案不会随时间改变

#### 4.4 输出格式

创建一个具有以下结构的XML文件：

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载这些资源：

### 核心MCP文档（首先加载）
- **MCP协议**：从`https://modelcontextprotocol.io/llms-full.txt`获取 - 完整的MCP规范
- [📋 MCP最佳实践](./reference/mcp_best_practices.md) - 包括以下内容的通用MCP指南：
  - 服务器和工具命名规范
  - 响应格式指南（JSON vs Markdown）
  - 分页最佳实践
  - 字符限制和截断策略
  - 工具开发指南
  - 安全性和错误处理标准

### SDK文档（在第1/2阶段加载）
- **Python SDK**：从`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`获取
- **TypeScript SDK**：从`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`获取

### 语言特定的实现指南（在第2阶段加载）
- [🐍 Python实现指南](./reference/python_mcp_server.md) - 完整的Python/FastMCP指南，包括：
  - 服务器初始化模式
  - Pydantic模型示例
  - 使用`@mcp.tool`进行工具注册
  - 完整的工作示例
  - 质量检查表

- [⚡ TypeScript实现指南](./reference/node_mcp_server.md) - 完整的TypeScript指南，包括：
  - 项目结构
  - Zod模式
  - 使用`server.registerTool`进行工具注册
  - 完整的工作示例
  - 质量检查表

### 评估指南（在第4阶段加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南，包括：
  - 问题创建指南
  - 答案验证策略
  - XML格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估