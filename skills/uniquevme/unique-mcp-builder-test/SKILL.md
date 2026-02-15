---
name: mcp-builder
description: **创建高质量MCP（Model Context Protocol）服务器的指南**  
本指南旨在帮助您构建能够支持大型语言模型（LLMs）通过精心设计的工具与外部服务交互的MCP服务器。无论您使用Python（FastMCP）还是Node/TypeScript（MCP SDK）来开发MCP服务器，本指南都适用于集成外部API或服务的场景。  

**MCP简介**  
MCP（Model Context Protocol）是一种用于在LLMs与外部系统之间传递模型上下文信息的标准化协议。通过使用MCP，您可以实现LLMs与各种第三方服务之间的无缝协作，从而扩展其功能和应用范围。  

**构建MCP服务器的关键步骤**：  
1. **定义MCP接口**：明确指定LLMs与外部服务之间需要交换的数据结构和格式。  
2. **实现协议通信**：确保您的服务器能够按照MCP协议正确地发送和接收数据。  
3. **处理安全性与可靠性**：考虑数据加密、身份验证和错误处理等方面的问题，以确保服务的安全性和稳定性。  
4. **集成外部服务**：将MCP服务器与目标外部服务进行集成，实现数据交换和功能调用。  
5. **测试与调试**：对MCP服务器进行全面的测试，确保其满足预期性能和稳定性要求。  

**示例代码与资源**：  
- [FastMCP示例代码](...)：基于Python的FastMCP实现示例。  
- [MCP SDK示例代码](...)：基于Node/TypeScript的MCP SDK实现示例。  
- [文档与教程](...)：详细的使用说明和参考资料。  

**注意事项**：  
- 请确保您的服务器兼容不同的LLMs和外部服务。  
- 遵循最佳实践，以优化性能和可维护性。  
- 定期更新MCP协议以适应新的技术和需求。  

**适用场景**：  
- 语言模型与数据库的集成  
- 语言模型与人工智能平台的集成  
- 语言模型与其他应用程序的交互  

**推荐阅读**：  
- [MCP官方文档](...)：了解MCP协议的详细规范和最新版本信息。  
- [相关技术博客文章](...)：获取关于构建高效MCP服务器的实用建议。  

通过遵循本指南，您可以轻松构建出高质量、可扩展的MCP服务器，从而提升您的语言模型系统的整体性能和用户体验。
license: Complete terms in LICENSE.txt
---

# MCP服务器开发指南

## 概述

本指南旨在帮助您开发MCP（Model Context Protocol）服务器，使大型语言模型（LLMs）能够通过设计良好的工具与外部服务进行交互。MCP服务器的质量体现在其能否有效帮助LLMs完成实际任务。

---

# 开发流程

## 🚀 高级工作流程

开发高质量的MCP服务器主要包括四个阶段：

### 第1阶段：深入研究与规划

#### 1.1 理解现代MCP设计

- **API覆盖范围与工作流工具**：
  在提供全面的API端点覆盖的同时，也要考虑使用专门的工作流工具。对于特定任务来说，工作流工具可能更为便捷；而全面的API覆盖范围则能赋予代理更强的灵活性，以便组合不同的操作。根据客户的需求选择合适的方案——有些客户更倾向于使用结合基本工具的代码执行方式，而另一些客户则更适合使用高级工作流。在不确定的情况下，优先考虑提供全面的API覆盖。

- **工具命名与可发现性**：
  明确、描述性的工具名称有助于代理快速找到所需的工具。使用一致的前缀（例如`github_create_issue`、`github_list_repos`），并采用以操作为导向的命名规则。

- **上下文管理**：
  代理需要简洁的工具描述以及过滤/分页结果的功能。设计工具时，应确保返回的数据具有针对性和相关性。部分客户支持代码执行，这有助于代理更高效地过滤和处理数据。

- **可操作的错误信息**：
  错误信息应提供具体的解决方案建议和下一步操作指导。

#### 1.2 学习MCP协议文档

- **浏览MCP规范**：
  首先通过站点地图（`https://modelcontextprotocol.io/sitemap.xml`）找到相关页面，然后使用`.md`后缀访问具体的markdown格式文档（例如`https://modelcontextprotocol.io/specification/draft.md`）。
  需要重点查看的页面包括：
  - 规范概述与架构
  - 传输机制（流式HTTP、标准输入输出）
  - 工具、资源及提示的定义

- **学习框架文档**：
  **推荐的技术栈**：
    - **语言**：TypeScript（支持高质量的SDK，并且在许多执行环境中具有良好的兼容性，例如MCPB。此外，AI模型擅长生成TypeScript代码，TypeScript的静态类型和强大的代码检查工具也非常有用）。
    - **传输方式**：对于远程服务器，使用流式HTTP和无状态的JSON（相比有状态的会话和流式响应，这种方式更易于扩展和维护）；对于本地服务器，则使用标准输入输出（stdio）。

- **加载框架文档**：
  - [📋 MCP最佳实践](./reference/mcp_best_practices.md) - 核心开发指南

  - **针对TypeScript的建议**：
    - **TypeScript SDK**：使用`WebFetch`加载`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
    - [⚡ TypeScript指南](./reference/node_mcp_server.md) - TypeScript相关模式和示例

  - **针对Python的建议**：
    - **Python SDK**：使用`WebFetch`加载`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
    - [🐍 Python指南](./reference/python_mcp_server.md) - Python相关模式和示例

#### 1.4 规划实现方案

- **理解API**：
  查阅服务的API文档，明确关键端点、认证要求及数据模型。如有需要，可以使用网络搜索和`WebFetch`来获取更多信息。

- **工具选择**：
  优先选择能够提供全面API覆盖的工具。列出需要实现的端点，从最常见的操作开始。

---

### 第2阶段：实现

#### 2.1 设置项目结构

请参考相应语言的指南来设置项目结构：
- [⚡ TypeScript指南](./reference/node_mcp_server.md) - 项目结构、`package.json`、`tsconfig.json`的配置
- [🐍 Python指南](./reference/python_mcp_server.md) - 模块组织方式及依赖管理

#### 2.2 实现核心基础设施

- 创建通用工具：
  - 带有认证功能的API客户端
  - 错误处理辅助函数
  - 响应格式化功能（JSON/Markdown）
  - 分页支持

#### 2.3 实现具体工具

对于每个工具：
- **输入数据结构**：
  使用Zod（TypeScript）或Pydantic（Python）来定义输入数据结构，包括约束条件和清晰的描述，并在字段描述中提供示例。
- **输出数据结构**：
  在可能的情况下，为结构化数据定义`outputSchema`；在工具响应中使用`structuredContent`（TypeScript SDK提供的功能），以便客户端能够理解和处理数据。
- **工具描述**：
  提供功能的简洁总结、参数说明以及返回的数据结构。
- **实现细节**：
  对I/O操作使用异步/await机制；进行适当的错误处理，并提供可操作的错误信息；在适用的情况下支持分页；使用现代SDK时，同时返回文本内容和结构化数据。
- **注释**：
  添加以下属性注释：
    - `readOnlyHint`：true/false（表示数据是否只读）
    - `destructiveHint`：true/false（表示操作是否具有破坏性）
    - `idempotentHint`：true/false（表示操作是否具有幂等性）
    - `openWorldHint`：true/false（表示操作是否可以修改外部状态）

---

### 第3阶段：审查与测试

#### 3.1 代码质量检查

检查代码是否存在以下问题：
- 无重复代码（遵循DRY原则）
- 一致的错误处理方式
- 完整的类型覆盖
- 清晰的工具描述

#### 3.2 构建与测试

- **TypeScript**：
  运行`npm run build`来验证代码编译是否正确。
  使用`npx @modelcontextprotocol/inspector`工具进行测试。

- **Python**：
  使用`python -m py_compile your_server.py`来检查语法是否正确；然后使用MCP Inspector进行测试。
  请参考相应语言的指南以获取详细的测试方法和质量检查清单。

---

### 第4阶段：创建评估方案

在实现MCP服务器后，需要创建全面的评估方案来测试其有效性。

- [✅ 评估指南](./reference/evaluation.md)提供了完整的评估指南。

#### 4.1 明确评估目的

通过评估来验证LLMs是否能够有效地利用您的MCP服务器来回答现实、复杂的问题。

#### 4.2 创建10个评估问题

为了创建有效的评估问题，请按照评估指南中的步骤进行：
1. **工具检查**：列出所有可用的工具并了解它们的功能。
2. **内容探索**：使用只读操作来探索可用的数据。
3. **问题生成**：创建10个复杂且具有现实意义的问题。
4. **答案验证**：亲自尝试回答这些问题以验证答案的正确性。

#### 4.3 评估要求

确保每个问题满足以下条件：
- **独立性**：不依赖于其他问题。
- **只读性**：仅需要执行非破坏性操作。
- **复杂性**：需要调用多个工具并进行深入的数据探索。
- **现实性**：基于人类实际会关心的使用场景。
- **可验证性**：答案应该是明确的，可以通过字符串比较来验证。
- **稳定性**：答案不会随时间变化。

#### 4.4 输出格式

创建一个符合以下结构的XML文件：

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

在开发过程中，请根据需要加载以下资源：

### 核心MCP文档（优先加载）
- **MCP协议**：首先通过站点地图`https://modelcontextprotocol.io/sitemap.xml`找到相关页面，然后使用`.md`后缀获取具体文档。
- [📋 MCP最佳实践](./reference/mcp_best_practices.md) - 包括以下内容的通用指南：
  - 服务器和工具的命名规范
  - 响应格式规范（JSON vs Markdown）
  - 分页最佳实践
  - 传输方式选择（流式HTTP vs 标准输入输出）
  - 安全性和错误处理标准

### SDK文档（在第1/2阶段加载）
- **Python SDK**：从`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`下载。
- **TypeScript SDK**：从`https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`下载。

### 语言特定的实现指南（在第2阶段加载）
- [🐍 Python实现指南](./reference/python_mcp_server.md) - 完整的Python/FastMCP实现指南，包括：
  - 服务器初始化示例
  - 使用`@mcp.tool`注册工具的示例
  - 完整的示例代码
  - 质量检查清单

- [⚡ TypeScript实现指南](./reference/node_mcp_server.md) - 完整的TypeScript实现指南，包括：
  - 项目结构
  - 使用Zod定义数据结构的示例
  - 使用`server.registerTool`注册工具的示例
  - 完整的示例代码
  - 质量检查清单

### 评估指南（在第4阶段加载）
- [✅ 评估指南](./reference/evaluation.md) - 包括问题创建方法、答案验证策略、XML格式规范、示例问题及答案的完整指南；以及如何使用提供的脚本运行评估的说明。