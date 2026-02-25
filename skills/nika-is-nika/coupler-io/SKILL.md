# Coupler.io

通过 Coupler.io 的 MCP 服务器实现只读数据访问。

**作者：** Coupler.io 团队  
**官网：** [coupler.io](https://coupler.io)

## 前提条件

- 已安装 [mcporter](https://github.com/openclaw/mcporter) CLI 并将其添加到系统路径中  
- 拥有 Coupler.io 账户，并且至少配置了一个指向 OpenClaw 目标的数据流  

## 快速参考  

```bash
mcporter call mcp-coupler-io-mcp.list-dataflows
mcporter call mcp-coupler-io-mcp.get-dataflow dataflowId=<uuid>
mcporter call mcp-coupler-io-mcp.get-schema executionId=<exec-id>
mcporter call mcp-coupler-io-mcp.get-data executionId=<exec-id> query="SELECT * FROM data LIMIT 10"
```

---

## 连接设置  

> **端点验证：** 该功能会连接到 `auth.coupler.io`（用于 OAuth 认证）和 `mcp.coupler.io`（用于数据传输）。这些是 Coupler.io 的官方端点。您可以通过 Coupler.io 账户的“AI 集成”页面进行验证。  

> **传输方式：** 该 MCP 使用的是 **streamable HTTP**，而非 SSE。如果在输出中看到“SSE 错误”，请忽略这个误导性的提示——实际上仍然是 HTTP 协议。  

### 1. 一步完成认证和服务器添加  

**请勿** 分别使用 `mcporter config add` 和 `mcporter auth` 命令——这样会导致创建没有认证元数据的配置项，并引发 401 错误。正确的操作是使用以下命令一次性完成认证和服务器添加：  

```bash
mcporter auth --http-url https://mcp.coupler.io/mcp --persist config/mcporter.json
```

该命令会自动检测 OAuth 认证流程，打开浏览器进行 Coupler.io 登录（采用 PKCE 认证方式），并在成功后保存服务器配置及访问令牌。  

若需要重新认证或清除过期的令牌，请使用：  
```bash
mcporter auth --http-url https://mcp.coupler.io/mcp --persist config/mcporter.json --reset
```

### 2. 确保配置中包含 `"auth": "oauth"`  

认证完成后，请检查 `config/mcporter.json` 文件。除非配置中包含 `"auth": "oauth"`，否则 mcporter 会使用缓存的令牌。配置文件应如下所示：  
```json
{
  "mcpServers": {
    "mcp-coupler-io-mcp": {
      "baseUrl": "https://mcp.coupler.io/mcp",
      "auth": "oauth"
    }
  }
}
```

如果配置中缺少 `"auth": "oauth"`，请手动添加该字段。  

### 3. 验证连接是否成功  

执行上述操作后，系统应返回 4 个可用工具：`get-data`、`get-schema`、`list-dataflows` 和 `get-dataflow`。  

> **注意：** 服务器名称会自动从 URL 中生成（例如 `mcp-coupler-io-mcp`），请在后续命令中始终使用该名称。  

---

## 令牌刷新  

mcporter 会在遇到 401 错误时自动刷新令牌，无需手动操作。  
如需强制刷新令牌，可执行：  
`mcporter auth mcp-coupler-io-mcp --reset`  

---

## MCP 工具  

### list-dataflows  

列出所有以 OpenClaw 为目标的数据流。  
```bash
mcporter call mcp-coupler-io-mcp.list-dataflows --output json
```

### get-dataflow  

获取数据流的详细信息，包括 `lastSuccessfulExecutionId`。  
```bash
mcporter call mcp-coupler-io-mcp.get-dataflow dataflowId=<uuid> --output json
```

### get-schema  

获取列的定义。列名存储在 `columnName` 中（例如 `col_0`、`col_1`）。  
```bash
mcporter call mcp-coupler-io-mcp.get-schema executionId=<exec-id>
```

### get-data  

对数据流中的数据执行 SQL 查询。查询的表名始终为 `data`。  
```bash
mcporter call mcp-coupler-io-mcp.get-data executionId=<exec-id> query="SELECT col_0, col_1 FROM data WHERE col_2 > 100 LIMIT 50"
```

**建议先进行少量数据查询（例如 `LIMIT 5`）**，以了解数据结构后再执行大规模查询。  

---

## 典型工作流程  

```bash
# 1. List flows, find ID
mcporter call mcp-coupler-io-mcp.list-dataflows --output json

# 2. Get execution ID
mcporter call mcp-coupler-io-mcp.get-dataflow dataflowId=<id> --output json

# 3. Check schema
mcporter call mcp-coupler-io-mcp.get-schema executionId=<exec-id>

# 4. Query
mcporter call mcp-coupler-io-mcp.get-data executionId=<exec-id> query="SELECT * FROM data LIMIT 10"
```

---

## 限制条件  

- 仅支持只读操作，无法修改数据流、数据源或数据内容。  
- 只显示以 OpenClaw 为目标的数据流。  
- 令牌的有效期为 2 小时，mcporter 会自动刷新令牌。