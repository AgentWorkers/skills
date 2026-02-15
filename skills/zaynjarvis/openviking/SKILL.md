---
name: openviking
description: 通过 OpenViking Context Database MCP 服务器实现 RAG（Retrieval with Annotation and Graph）和语义搜索功能。可以查询文档、搜索知识库，并将文件/URL 添加到向量内存中。该系统可用于文档问答、知识管理、AI 代理的记忆存储、文件搜索以及语义信息检索等场景。相关操作可通过以下命令触发：`openviking`、`search documents`、`semantic search`、`knowledge base`、`vector database`、`RAG`、`query pdf`、`document query`、`add resource`。
---

# OpenViking – 专为AI代理设计的上下文数据库

OpenViking 是字节跳动（ByteDance）开发的开源**上下文数据库**，专为AI代理设计。它是一种新一代的RAG（Retrieval-Augmentation）系统，通过文件系统范式替代了传统的扁平向量存储方式，用于管理记忆、资源和技能。

**主要特性：**
- **文件系统范式**：使用URI（如 `viking://resources/...`）来组织上下文数据。
- **分层上下文结构（L0/L1/L2）**：数据从抽象层逐步细化到详细内容，按需加载。
- **目录递归检索**：比扁平向量搜索具有更高的准确性。
- **内置MCP服务器**：通过Model Context Protocol提供完整的RAG处理流程。

---

## 快速检查：是否已安装？

```bash
test -f ~/code/openviking/examples/mcp-query/ov.conf && echo "Ready" || echo "Needs setup"
curl -s http://localhost:2033/mcp && echo "Running" || echo "Not running"
```

## 如果未安装 → 初始化

运行初始化脚本（仅需执行一次）：

```bash
bash ~/.openclaw/skills/openviking-mcp/scripts/init.sh
```

该脚本将：
1. 从 `https://github.com/volcengine/OpenViking` 克隆OpenViking代码。
2. 使用 `uv sync` 安装所需依赖项。
3. 创建 `ov.conf` 配置文件。
4. **提示您输入API密钥**（`embeddingdense.api_key` 和 `vlm.api_key`）。

**所需密钥：Volcengine/Ark API密钥**

| 配置键 | 用途 |
|------------|---------|
| `embeddingdense.api_key` | 用于语义搜索的嵌入模型 |
| `vlm.api_key` | 用于生成答案的LLM（Large Language Model） |

请在 [https://console.volcengine.com/ark] 获取API密钥。

## 启动服务器

```bash
cd ~/code/openviking/examples/mcp-query
uv run server.py
```

可选参数：
- `--port 2033`：指定服务器监听端口。
- `--host 127.0.0.1`：设置服务器绑定地址。
- `--data ./data`：指定数据目录。

服务器地址为：`http://127.0.0.1:2033/mcp`

## 连接到Claude

```bash
claude mcp add --transport http openviking http://localhost:2033/mcp
```

或者，您也可以将服务器配置信息添加到 `~/.mcp.json` 文件中：

```json
{
  "mcpServers": {
    "openviking": {
      "type": "http",
      "url": "http://localhost:2033/mcp"
    }
  }
}
```

## 可用工具

| 工具 | 功能描述 |
|------|-------------|
| `query` | 完整的RAG处理流程：同时支持搜索和LLM生成答案。 |
| `search` | 仅支持语义搜索，返回文档内容。 |
| `add_resource` | 用于添加文件、目录或URL。 |

## 示例用法

连接成功后，您可以按照以下步骤使用OpenViking：

```
"Query: What is OpenViking?"
"Search: machine learning papers"
"Add https://example.com/article to knowledge base"
"Add ~/documents/report.pdf"
```

## 故障排除

| 问题 | 解决方案 |
|-------|-----|
| 端口已被占用 | 使用 `uv run server.py --port 2034` 重新启动服务器。 |
| 认证错误 | 检查 `ov.conf` 文件中的API密钥是否正确。 |
| 服务器未启动 | 确保服务器正在运行：`curl localhost:2033/mcp`。

## 相关文件

- `ov.conf`：配置文件（包含API密钥和模型信息）。 |
- `data/`：用于存储向量数据的目录。 |
- `server.py`：MCP服务器的实现代码。