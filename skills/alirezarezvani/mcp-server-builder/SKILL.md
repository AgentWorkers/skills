---
name: "mcp-server-builder"
description: "MCP Server Builder"
---
# MCP 服务器构建器

**级别：** 高级  
**类别：** 工程技术  
**领域：** 人工智能 / API 集成  

## 概述  

使用此技能，您可以根据 API 合同设计和部署可投入生产的 MCP 服务器，而无需手动编写一次性的工具封装代码。该工具专注于快速搭建服务器框架、确保数据结构的质量、进行验证以及实现安全的代码演进。  

该工具支持 Python 和 TypeScript 两种语言的实现，并以 OpenAPI 作为数据来源的权威标准。  

## 核心功能  

- 将 OpenAPI 的路径和操作转换为 MCP 工具定义  
- 生成服务器框架代码（Python 或 TypeScript）  
- 强制执行命名规范、描述规范以及数据结构的一致性检查  
- 验证 MCP 工具的配置文件，以防止常见生产环境中的问题  
- 实施版本控制及向后兼容性检查  
- 将传输层/运行时层的实现与工具合同设计分离  

## 适用场景  

- 需要将内部/外部 REST API 提供给大型语言模型（LLM）代理  
- 希望用类型化工具替换易出错的浏览器自动化脚本  
- 需要一个可供多个团队和辅助工具共享的 MCP 服务器  
- 在发布 MCP 工具之前需要进行可重复的质量检查  
- 希望根据现有的 OpenAPI 规范快速搭建 MCP 服务器  

## 主要工作流程  

### 1. 从 OpenAPI 创建 MCP 服务器框架  

1. 从有效的 OpenAPI 规范文件开始。  
2. 生成工具配置文件及服务器框架代码。  
3. 审查命名规则和认证策略。  
4. 为特定端点添加运行时逻辑。  

```bash
python3 scripts/openapi_to_mcp.py \
  --input openapi.json \
  --server-name billing-mcp \
  --language python \
  --output-dir ./out \
  --format text
```  

该工具也支持通过标准输入（stdin）进行操作：  
```bash
cat openapi.json | python3 scripts/openapi_to_mcp.py --server-name billing-mcp --language typescript
```  

### 2. 验证 MCP 工具定义  

在集成测试之前运行验证工具：  
```bash
python3 scripts/mcp_validator.py --input out/tool_manifest.json --strict --format text
```  

验证内容包括：重复的名称、无效的数据结构、缺失的描述信息、必填字段为空以及命名不规范等问题。  

### 3. 选择运行时语言  

- **Python**：适用于需要快速迭代和处理大量数据的后端场景。  
- **TypeScript**：适用于前端和后端代码共享的场景，有助于提高代码的一致性。  
- 即使传输层或运行时层发生变化，工具合同也能保持稳定。  

### 4. 认证与安全设计  

- 将敏感信息（如密钥）存储在环境变量中，而非工具配置文件中。  
- 对出站连接使用明确的允许列表进行控制。  
- 返回结构化的错误信息（包含 `code`、`message` 和 `details`），以便代理程序能够正确处理错误。  
- 避免在未经明确确认的情况下执行破坏性操作。  

### 5. 版本控制策略  

- 仅在非破坏性更新时添加新字段。  
- 绝不要直接修改工具的名称。  
- 对涉及功能变更的工具使用新的唯一标识符。  
- 为每次版本更新维护工具合同的变更日志。  

## 脚本接口  

- `python3 scripts/openapi_to_mcp.py --help`  
  - 从标准输入或指定文件读取 OpenAPI 规范  
  - 生成工具配置文件及服务器框架代码  
  - 输出 JSON 总结或文本报告  

- `python3 scripts/mcp-validator.py --help`  
  - 验证工具配置文件及可选的运行时配置  
  - 在检测到错误时以非零退出码结束程序  

## 常见问题  

- 工具名称直接来源于原始 API 路径（例如 `get__v1__users___id`）  
- 缺少操作描述（导致代理程序无法正确选择工具）  
- 参数结构不明确或缺少必填字段  
- 将传输层错误与业务逻辑错误混在一起  
- 在不进行版本控制的情况下修改数据结构，导致客户端出现故障  

## 最佳实践  

- 如有 `operationId`，请使用它作为工具的规范名称。  
- 每个工具应仅实现单一功能，避免创建功能过于复杂的工具。  
- 为每个工具添加简洁的描述，并使用明确的动词来描述其功能。  
- 在持续集成（CI）过程中使用严格模式验证工具配置文件。  
- 将生成的服务器框架代码提交到版本控制系统后，再逐步进行定制。  
- 将工具配置的变更与相应的变更日志记录关联起来。  

## 参考资料  

- [references/openapi-extraction-guide.md](references/openapi-extraction-guide.md)  
- [references/python-server-template.md](references/python-server-template.md)  
- [references/typescript-server-template.md](references/typescript-server-template.md)  
- [references/validation-checklist.md](references/validation-checklist.md)  
- [README.md](README.md)  

## 架构选择建议  

根据实际需求选择合适的服务器实现方式：  
- **Python 运行时**：适用于迭代速度快、处理大量数据的团队。  
- **TypeScript 运行时**：适用于前端代码与后端代码共享的团队。  
- **单一 MCP 服务器**：适用于操作简单、影响范围广的场景。  
- **分离的领域服务器**：有助于明确职责划分和降低代码变更的风险。  

## 配置文件质量标准  

在发布工具配置文件之前，需满足以下要求：  
- 每个工具的名称都应首先包含明确的操作动词。  
- 每个工具的描述都应清晰说明其功能及预期结果。  
- 所有必填字段都应有明确的类型定义。  
- 执行破坏性操作时需要用户确认。  
- 所有工具的错误响应格式应保持一致。  
- 在严格模式下，验证工具配置文件时不应返回任何错误。  

## 测试策略  

- **单元测试**：验证 OpenAPI 操作到 MCP 工具配置文件的转换过程。  
- **合同验证**：通过代码审查（CI）检查工具配置文件的变化。  
- **集成测试**：使用测试环境中的 API 调用生成的工具代码。  
- **弹性测试**：模拟上游的 4xx/5xx 错误，并验证工具的响应是否符合预期。  

## 部署规范  

- 根据不同的环境配置相应的 MCP 运行时依赖项。  
- 在发布新版本时逐步推送服务器更新。  
- 确保至少在一个版本发布周期内保持向后兼容性。  
- 为新增、删除或修改的工具配置文件添加详细的变更日志。  

## 安全控制措施  

- 明确指定允许的出站连接地址。  
- 不要代理用户提供的任意 URL。  
- 从日志中屏蔽敏感信息和认证相关的数据。  
- 对高负载工具实施速率限制，并设置请求超时机制。