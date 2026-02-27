---
name: cerebrun
description: "**MCP客户端（适用于Cerebrun）**  
Cerebrun是一款全面性的个人上下文与记忆管理系统。该客户端支持以下功能：  
1. **检索用户上下文信息**（语言设置、参与的项目、身份信息、存储的数据等）；  
2. **执行语义搜索**；  
3. **管理知识库内容**；  
4. **与LLM（大型语言模型）网关进行交互**。  
**适用场景：**  
- **检索用户偏好或相关上下文数据**；  
- **查询用户存储的知识库内容**；  
- **管理和调整用户的项目及目标**；  
- **存储或查询个人信息**；  
- **通过LLM网关访问对话历史记录**。"
---
# Cerebrun MCP 客户端

Cerebrun（cereb.run）是一个 Model Context Protocol（MCP）服务器，能够实现跨会话的持久化个人上下文管理。

## 快速入门

所有请求都需要以下参数：
- `api_key`：Cerebrun API 密钥（Bearer 令牌）
- `base_url`：https://cereb.run/mcp

## 上下文层次结构

**第0层** - 语言、时区、通信偏好设置
**第1层** - 项目、目标、固定保存的记忆内容
**第2层** - 个人身份信息、API 密钥等
**第3层** - 加密存储空间（需要用户同意）

## 使用方法

### 获取上下文信息
```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_context","arguments":{"layer":0}}}' \
  https://cereb.run/mcp
```

### 搜索上下文信息
```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_context","arguments":{"query":"Rust authentication","limit":5}}}' \
  https://cereb.run/mcp
```

### 添加知识内容
```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"push_knowledge","arguments":{"content":"Important insight","category":"learning","tags":["rust","performance"]}}}' \
  https://cereb.run/mcp
```

### 通过 Gateway 进行聊天
```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"chat_with_llm","arguments":{"message":"Hello","provider":"openai","model":"gpt-4"}}}' \
  https://cereb.run/mcp
```

## 工具参考

请参阅 [REFERENCES.md](references/REFERENCES.md) 以获取完整的 API 文档。

## 脚本使用示例
（此处为示例代码块，实际使用时需替换为具体的脚本内容）

## 配置

将 API 密钥存储在环境变量 `CEREBRUN_API_KEY` 中，或通过 `--api-key` 参数传递。