---
name: jb-docs
description: 您可以通过 REST API 或 MCP 服务器查询 Juicebox V5 的文档。可以搜索文档、获取合约地址以及查找实现指南。
---

# Juicebox V5 文档查询

您可以通过 REST API 或 MCP 服务器来查询 Juicebox 的文档。

## MCP 服务器（推荐使用）

请将以下代码添加到您的 Claude Code 或 MCP 客户端配置中：

```json
{
  "mcpServers": {
    "juice-docs": {
      "type": "http",
      "url": "https://docs.juicebox.money/api/mcp-sse"
    }
  }
}
```

### MCP 提供的工具
- `search_docs` - 按关键词搜索文档
- `get_doc` - 根据路径获取完整文档内容
- `list_docs_by_category` - 列出某个类别下的文档
- `get_doc_structure` - 获取文档结构

### 直接调用 MCP 的示例
```bash
curl -X POST https://docs.juicebox.money/api/mcp-sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_docs","arguments":{"query":"pay hook"}}}'
```

## REST API 端点

### 搜索文档
```bash
POST https://docs.juicebox.money/api/mcp/search
Content-Type: application/json

{
  "query": "pay hook",
  "category": "all",    # all, developer, user, dao, ecosystem
  "version": "v5",      # v3, v4, v5, all
  "limit": 10
}
```

### 获取特定文档
```bash
POST https://docs.juicebox.money/api/mcp/get-doc
Content-Type: application/json

{
  "path": "dev/v5/learn/overview.md"
}
```

### 按类别列出文档
```bash
GET https://docs.juicebox.money/api/mcp/list-docs?category=developer&version=v5
```

### 获取文档结构
```bash
GET https://docs.juicebox.money/api/mcp/structure
```

## 使用 WebFetch

您可以使用 WebFetch 直接查询 API 或获取文档页面：

### 搜索文档
```
WebFetch https://docs.juicebox.money/dev/v5/build/pay-hook/
"Extract how to implement a pay hook"
```

### 获取特定页面
```
WebFetch https://docs.juicebox.money/dev/v5/learn/overview/
"Summarize the V5 protocol overview"
```

## 文档结构
```
/dev/                    # Developer documentation root
/dev/v5/learn/           # Conceptual documentation
/dev/v5/build/           # Implementation guides
/dev/v5/api/             # API reference
/dev/v5/api/core/        # Core contract docs
```

## 可用的文档

### 协议文档
- **学习**：概念指南和协议概述
- **构建**：实现指南和教程
- **API**：技术规范和接口契约

### 合约地址
- 所有网络的部署地址（Ethereum、Optimism、Arbitrum、Base）
- 最新的 V5 合约地址
- Hook 部署器的地址

### 代码参考
- 接口定义
- 结构文档
- 事件签名

## 常见文档查询

### “主网上的 JBController 地址是多少？”
请使用 `/references` 文件夹获取离线合约地址，或从文档中查询。

### “如何实现支付 Hook？”
```
WebFetch https://docs.juicebox.money/dev/v5/build/pay-hook/
"Extract implementation steps for pay hooks"
```

### “JBMultiTerminal 发出了哪些事件？”
```
WebFetch https://docs.juicebox.money/dev/v5/api/core/jbmultiterminal/
"List all events emitted by JBMultiTerminal"
```

## 官方资源
- **文档**：https://docs.juicebox.money
- **GitHub**：https://github.com/jbx-protocol
- **V5 Core**：https://github.com/Bananapus/nana-core-v5
- **回购 Hook**：https://github.com/Bananapus/nana-buyback-hook-v5
- **721 Hook**：https://github.com/Bananapus/nana-721-hook-v5
- **Revnet**：https://github.com/rev-net/revnet-core-v5

## 文档生成指南

1. **使用 WebFetch** 直接查询文档页面。
2. **参考 `/references` 文件夹** 以获取离线接口/结构定义。
3. **提供相关文档的直接链接**。
4. **默认使用 V5 版本**，除非用户明确要求查看旧版本。

## 示例提示

- “Optimism 主网上的 JBController 地址是多少？”
- “显示支付 Hook 的文档。”
- “Terminal 发出了哪些事件？”
- “获取最新的 V5 合约地址。”