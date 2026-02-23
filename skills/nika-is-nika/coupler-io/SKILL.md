# Coupler.io

通过 Coupler.io 的 MCP 服务器实现只读数据访问。

**作者：** Coupler.io 团队  
**官网：** [coupler.io](https://coupler.io)

## 前提条件

- 已安装 [mcporter](https://github.com/openclaw/mcporter) CLI 并将其添加到 PATH 环境变量中  
- 拥有 Coupler.io 账户，并且至少配置了一个指向 OpenClaw 目标的数据流  

## 快速参考

```bash
mcporter call coupler.list-dataflows
mcporter call coupler.get-dataflow dataflowId=<uuid>
mcporter call coupler.get-schema executionId=<exec-id>
mcporter call coupler.get-data executionId=<exec-id> query="SELECT * FROM data LIMIT 10"
```

---

## 连接设置

> **端点验证：** 该功能会连接到 `auth.coupler.io`（用于 OAuth 验证）和 `mcp.coupler.io`（用于数据传输）。这些是 Coupler.io 的官方端点。您可以通过自己的 Coupler.io 账户（“AI 集成”页面）来验证这些端点的有效性。  

### 1. 将服务器添加到 mcporter 配置中  

```bash
mcporter config add coupler --url https://mcp.coupler.io/mcp
```

### 2. 通过 OAuth 进行身份验证  

```bash
mcporter auth --http-url https://mcp.coupler.io/mcp --persist config/mcporter.json         
```

系统会自动打开浏览器，引导您完成 Coupler.io 的登录流程（使用 PKCE 协议进行 OAuth 验证）。验证通过后，令牌会存储在 mcporter 的配置文件中。  

**重新认证方法：**（例如，在权限被撤销后）  
```bash
mcporter auth coupler --reset
```

### 3. 验证连接是否成功  

```bash
mcporter list coupler --schema
```

---

## 令牌刷新

当遇到 401 错误时，mcporter 会自动刷新令牌，无需用户手动操作。  
如需强制刷新令牌，可执行：`mcporter auth coupler --reset`  

---

## MCP 工具  

### list-dataflows  
列出所有以 OpenClaw 为目标的数据流。  

```bash
mcporter call coupler.list-dataflows --output json
```

### get-dataflow  
获取数据流的详细信息，包括 `lastSuccessfulExecutionId`（最后一次成功执行的 ID）。  

```bash
mcporter call coupler.get-dataflow dataflowId=<uuid> --output json
```

### get-schema  
获取列的定义。列名存储在 `columnName` 变量中（例如：`col_0`、`col_1`）。  

```bash
mcporter call coupler.get-schema executionId=<exec-id>
```

### get-data  
在数据流上执行 SQL 查询；查询结果存储在 `data` 表中。  

**建议操作：** 在执行大规模查询前，先使用 `LIMIT 5` 来获取样本数据，以便了解数据结构。  

---

## 典型工作流程  

```bash
# 1. List flows, find ID
mcporter call coupler.list-dataflows --output json | jq '.[] | {name, id}'

# 2. Get execution ID
mcporter call coupler.get-dataflow dataflowId=<id> --output json | jq '.lastSuccessfulExecutionId'

# 3. Check schema
mcporter call coupler.get-schema executionId=<exec-id>

# 4. Query
mcporter call coupler.get-data executionId=<exec-id> query="SELECT * FROM data LIMIT 10"
```

---

## 限制条款  

- 仅支持只读操作，无法修改数据流、数据源或数据内容。  
- 只能查看以 OpenClaw 为目标的数据流。  
- 令牌的有效期为 2 小时，mcporter 会自动刷新令牌。