---
name: openviking-mcp
description: **配置并运行 OpenViking MCP 服务器以支持 RAG（问答生成）功能**  
当用户需要通过 Model Context Protocol 在 Claude Desktop/CLI 或其他 MCP 客户端进行语义搜索或文档问答时，可使用该服务器。该服务器会在收到关于 OpenViking MCP、RAG 服务器或语义搜索相关配置的请求时被触发。
---

# OpenViking MCP 服务器

这是一个 HTTP 基本的 MCP（Media Center Protocol）服务器，它将 OpenViking 的 RAG（Retrieval, Augmentation, and Generation）功能作为工具提供给 Claude 以及其他 MCP 客户端使用。

## 提供的功能

| 工具 | 功能 |
|------|---------|
| `query` | 完整的 RAG 流程——语义搜索 + 大语言模型（LLM）答案生成 |
| `search` | 仅提供语义搜索，返回匹配的文档及其分数 |
| `add_resource` | 将文件、目录或 URL 添加到数据库中 |

## 先决条件

- Python 3.13 或更高版本 |
- 已安装 `uv`（通过运行 `curl -LsSf https://astral.sh/uv/install.sh | sh` 安装） |
- OpenAI API 密钥（用于 LLM 和嵌入功能）

## 设置步骤

### 第 1 步：获取代码

克隆 OpenViking 仓库：

```bash
git clone https://github.com/ZaynJarvis/openviking.git
# Or your fork/organization's repo
cd openviking/examples/mcp-query
```

### 第 2 步：安装依赖项

```bash
uv sync
```

### 第 3 步：配置 API 密钥（需要用户手动操作）

复制示例配置文件：

```bash
cp ov.conf.example ov.conf
```

**请编辑 `ov.conf` 文件并添加您的 API 密钥。** 关键字段包括：

| 字段 | 用途 | 示例 |
|-------|---------|---------|
| `vlm.token` | 用于生成答案的 LLM | `sk-...`（OpenAI） |
| `embedding.token` | 用于语义搜索的嵌入模型 | `sk-...`（OpenAI） |

**等待用户确认：** 在继续之前，请用户粘贴他们的 `ov.conf` 文件（如果需要共享日志，请将 API 密钥隐藏），或确认他们已经完成了配置。

示例最小配置文件：

```json
{
  "vlm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "token": "YOUR_OPENAI_API_KEY"
  },
  "embedding": {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "token": "YOUR_OPENAI_API_KEY"
  }
}
```

### 第 4 步：启动服务器

```bash
uv run server.py
```

服务器默认运行在 `http://127.0.0.1:8000/mcp` 上。

### 第 5 步：连接到 Claude

**Claude 命令行界面：**
```bash
claude mcp add --transport http openviking http://localhost:8000/mcp
```

**Claude 桌面应用：** 将以下配置添加到 `~/.mcp.json` 文件中：

```json
{
  "mcpServers": {
    "openviking": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 服务器选项

```
uv run server.py [OPTIONS]

  --config PATH       Config file path (default: ./ov.conf)
  --data PATH         Data directory path (default: ./data)
  --host HOST         Bind address (default: 127.0.0.1)
  --port PORT         Listen port (default: 8000)
  --transport TYPE    streamable-http | stdio (default: streamable-http)
```

环境变量：`OV_CONFIG`, `OV_DATA`, `OV_PORT`, `OV_DEBUG`

## 使用示例

连接成功后，Claude 可以使用以下功能：

**使用 RAG 进行查询：**
```
"Search my documents for information about Q3 revenue and summarize the findings"
```

**仅进行语义搜索：**
```
"Find documents related to machine learning architecture"
```

**添加文档：**
```
"Index the PDF at ~/documents/report.pdf"
"Add https://example.com/article to my knowledge base"
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 端口已被占用 | 使用 `--port 9000` 更改端口 |
| 配置文件未找到 | 确保 `ov.conf` 文件存在，或设置正确的 `OV_CONFIG` 路径 |
| 依赖项缺失 | 在 `mcp-query` 目录中运行 `uv sync` 命令 |
| 认证错误 | 检查 `ov.conf` 文件中的 API 密钥是否正确 |

## 资源

- OpenViking 仓库：`code/openviking/` 或 https://github.com/ZaynJarvis/openviking