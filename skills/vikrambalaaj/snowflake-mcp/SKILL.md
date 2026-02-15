---
name: snowflake-mcp
description: 使用 Clawdbot 或其他 MCP 客户端连接到 Snowflake 托管的中间件服务器（MCP）。该功能适用于连接 Snowflake MCP 端点、验证连接性或配置 Cortex AI 服务。
---

# Snowflake MCP 连接

使用此技能将 Snowflake 的 Managed MCP 服务器与 Clawdbot 集成。该指南涵盖了端点创建、身份验证以及工具验证等内容，从而可以通过 MCP 访问 Snowflake 数据。

## 快速入门

### 先决条件

- 拥有 ACCOUNTADMIN 角色的 Snowflake 账户
- 从 Snowflake 获取的程序化访问令牌（Programmatic Access Token，简称 PAT）
- Clawdbot 或任何兼容 MCP 的客户端

### 第 1 步：创建程序化访问令牌（PAT）

1. 在 Snowsight 中，进入用户菜单 → **我的个人资料**（My Profile）
2. 选择 **程序化访问令牌**（Programmatic Access Tokens）
3. 为你的角色点击 **创建令牌**（Create Token）
4. 安全地复制并保存令牌

### 第 2 步：在 Snowflake 中创建 MCP 服务器

在 Snowsight 的工作表中运行以下 SQL 语句以创建你的 MCP 服务器：

```sql
CREATE OR REPLACE MCP SERVER my_mcp_server FROM SPECIFICATION
$$
tools:
  - name: "SQL Execution Tool"
    type: "SYSTEM_EXECUTE_SQL"
    description: "Execute SQL queries against the Snowflake database."
    title: "SQL Execution Tool"
$$;
```

### 第 3 步：测试连接

使用 curl 进行测试（请替换占位符）：

```bash
curl -X POST "https://YOUR-ORG-YOUR-ACCOUNT.snowflakecomputing.com/api/v2/databases/YOUR_DB/schemas/YOUR_SCHEMA/mcp-servers/my_mcp_server" \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --header "Authorization: Bearer YOUR-PAT-TOKEN" \
  --data '{
    "jsonrpc": "2.0",
    "id": 12345,
    "method": "tools/list",
    "params": {}
  }'
```

### 第 4 步：配置 Clawdbot

在项目根目录下创建 `mcp.json` 文件（这是 Clawdbot 在会话中可以加载的 MCP 配置文件）：

```json
{
  "mcpServers": {
    "Snowflake MCP Server": {
      "url": "https://YOUR-ORG-YOUR-ACCOUNT.snowflakecomputing.com/api/v2/databases/YOUR_DB/schemas/YOUR_SCHEMA/mcp-servers/my_mcp_server",
      "headers": {
        "Authorization": "Bearer YOUR-PAT-TOKEN"
      }
    }
  }
}
```

启动一个新的 Clawdbot 会话，并加载 `mcp.json` 文件，以使 MCP 连接生效。此时，Snowflake 工具应该会出现在你的会话中。

### 第 5 步：在 Clawdbot 中进行验证

1. 启动一个新的 Clawdbot 会话
2. 为该会话加载 `mcp.json` 文件
3. 提出一个能够触发 Snowflake 工具的请求（例如，执行 SQL 查询）

## MCP 服务器示例

### 仅执行基本 SQL 语句

```sql
CREATE OR REPLACE MCP SERVER sql_mcp_server FROM SPECIFICATION
$$
tools:
  - name: "SQL Execution Tool"
    type: "SYSTEM_EXECUTE_SQL"
    description: "Execute SQL queries against Snowflake."
    title: "SQL Execution"
$$;
```

### 使用 Cortex Search（RAG）

首先在 Snowsight 中创建一个 Cortex Search 服务（AI & ML → Cortex Search），然后：

```sql
CREATE OR REPLACE MCP SERVER search_mcp_server FROM SPECIFICATION
$$
tools:
  - name: "Document Search"
    identifier: "MY_DB.MY_SCHEMA.MY_SEARCH_SERVICE"
    type: "CORTEX_SEARCH_SERVICE_QUERY"
    description: "Search and retrieve information from documents using vector search."
    title: "Document Search"
  - name: "SQL Execution Tool"
    type: "SYSTEM_EXECUTE_SQL"
    description: "Execute SQL queries."
    title: "SQL Execution"
$$;
```

### 使用 Cortex Analyst（语义视图）

首先上传一个语义 YAML 文件或创建一个语义视图，然后：

```sql
CREATE OR REPLACE MCP SERVER analyst_mcp_server FROM SPECIFICATION
$$
tools:
  - name: "Sales Analytics"
    identifier: "MY_DB.MY_SCHEMA.SALES_SEMANTIC_VIEW"
    type: "CORTEX_ANALYST_MESSAGE"
    description: "Query sales metrics and KPIs using natural language."
    title: "Sales Analytics"
  - name: "SQL Execution Tool"
    type: "SYSTEM_EXECUTE_SQL"
    description: "Execute SQL queries."
    title: "SQL Execution"
$$;
```

### 使用 Cortex Agent

```sql
CREATE OR REPLACE MCP SERVER agent_mcp_server FROM SPECIFICATION
$$
tools:
  - name: "Documentation Agent"
    identifier: "MY_DB.MY_SCHEMA.MY_AGENT"
    type: "CORTEX_AGENT_RUN"
    description: "An agent that answers questions using documentation."
    title: "Documentation Agent"
$$;
```

### 全功能服务器

```sql
CREATE OR REPLACE MCP SERVER full_mcp_server FROM SPECIFICATION
$$
tools:
  - name: "Analytics Semantic View"
    identifier: "ANALYTICS_DB.DATA.FINANCIAL_ANALYTICS"
    type: "CORTEX_ANALYST_MESSAGE"
    description: "Query financial metrics, customer data, and business KPIs."
    title: "Financial Analytics"
  - name: "Support Tickets Search"
    identifier: "SUPPORT_DB.DATA.TICKETS_SEARCH"
    type: "CORTEX_SEARCH_SERVICE_QUERY"
    description: "Search support tickets and customer interactions."
    title: "Support Search"
  - name: "SQL Execution Tool"
    type: "SYSTEM_EXECUTE_SQL"
    description: "Execute SQL queries against Snowflake."
    title: "SQL Execution"
  - name: "Send_Email"
    identifier: "MY_DB.DATA.SEND_EMAIL"
    type: "GENERIC"
    description: "Send emails to verified addresses."
    title: "Send Email"
    config:
      type: "procedure"
      warehouse: "COMPUTE_WH"
      input_schema:
        type: "object"
        properties:
          body:
            description: "Email body in HTML format."
            type: "string"
          recipient_email:
            description: "Recipient email address."
            type: "string"
          subject:
            description: "Email subject line."
            type: "string"
$$;
```

## 工具类型参考

| 类型 | 用途 |
|------|---------|
| `SYSTEM_EXECUTE_SQL` | 执行任意 SQL 查询 |
| `CORTEX_SEARCH_SERVICE_QUERY` | 对非结构化数据进行 RAG（检索、聚合和生成）操作 |
| `CORTEX_ANALYST_MESSAGE` | 对语义模型进行自然语言查询 |
| `CORTEX_AGENT_RUN` | 调用 Cortex Agent |
| `GENERIC` | 自定义工具（过程/函数） |

## 好处

- **基于设计进行管理**：与你的数据相同的 RBAC（角色基于权限控制）策略适用 |
- **无需基础设施**：无需部署本地服务器 |
- **简化集成**：可以连接到任何兼容 MCP 的客户端 |
- **可扩展**：可以通过过程/函数添加自定义工具 |

## 故障排除

### 连接问题

- **SSL 错误**：在账户名称中使用连字符（-）而不是下划线（_） |
- **401 未授权**：确认 PAT 令牌有效且未过期 |
- **404 未找到**：检查数据库、模式和 MCP 服务器的名称

### 测试工具

列出可用的工具：

```bash
curl -X POST "https://YOUR-ACCOUNT.snowflakecomputing.com/api/v2/databases/DB/schemas/SCHEMA/mcp-servers/SERVER" \
  -H "Authorization: Bearer PAT" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### PAT 令牌注意事项

- PAT 不会评估次要角色 |
- 创建令牌时，请选择具有所有所需权限的单一角色 |
- 如需更改角色，请创建新的 PAT

## 替代方案：本地 MCP 服务器

有关使用 `snowflake-labs-mcp` 包进行本地部署的详细信息，请参阅 [mcp-client-setup.md](mcp-client-setup.md)。

## 资源

- [Snowflake MCP 服务器指南](https://www.snowflake.com/en/developers/guides/getting-started-with-snowflake-mcp-server/) |
- [Snowflake MCP 文档](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp) |
- [GitHub: sfguide-getting-started-with-snowflake-mcp-server](https://github.com/Snowflake-Labs/sfguide-getting-started-with-snowflake-mcp-server) |
- [MCP 协议](https://modelcontextprotocol.io)