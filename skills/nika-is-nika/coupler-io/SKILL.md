# Coupler.io

通过 Coupler.io 的 MCP 服务器实现只读数据访问。

**作者：** Coupler.io 团队  
**官网：** [coupler.io](https://coupler.io)

## 先决条件

- 已安装 [mcporter](https://github.com/openclaw/mcporter) CLI 并将其添加到 PATH 环境变量中  
- 确保系统中已安装 `curl`、`jq` 和 `openssl`；如果未安装，请通过相应的包管理器进行安装  
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

> **端点验证：** 该功能会连接到 `auth.coupler.io`（用于 OAuth 认证）和 `mcp.coupler.io`（用于数据传输）。这些是 Coupler.io 的官方端点。您可以通过 Coupler.io 账户的“AI 集成”页面来验证这些端点的有效性。  

### 自动化设置

运行设置脚本，所有步骤都将自动完成（无需手动操作）：  
```bash
bash CPL/setup.sh
```

该脚本会自动注册 OAuth 客户端、打开浏览器进行登录、通过本地 HTTP 服务器（端口 8976）捕获回调代码、交换令牌并保存配置信息——全程无需人工干预。  

**注意：** OAuth 凭据会保存在 `coupler-io/oauth-state.json` 文件中。  

### 手动 OAuth 流程（仅适用于首次使用）

1. **注册客户端：**  
   ```bash
   curl -X POST https://auth.coupler.io/oauth2/register \
     -H "Content-Type: application/json" \
     -d '{
       "client_name": "OpenClaw",
       "redirect_uris": ["http://127.0.0.1:8976/callback"],
       "grant_types": ["authorization_code"],
       "response_types": ["code"],
       "token_endpoint_auth_method": "none"
     }'
   ```

   从响应中保存 `client_id`。  

2. **生成 PKCE（Proof Key Exchange）令牌：**  
   ```bash
   CODE_VERIFIER=$(openssl rand -base64 32 | tr -d '=/+' | cut -c1-43)
   CODE_CHALLENGE=$(echo -n "$CODE_VERIFIER" | openssl dgst -sha256 -binary | base64 | tr -d '=' | tr '+/' '-_')
   ```

3. **在浏览器中完成认证：** 打开指定 URL，用户登录后：  
   ```text
   https://auth.coupler.io/oauth2/authorize?client_id=<client_id>&redirect_uri=http://127.0.0.1:8976/callback&response_type=code&scope=mcp&code_challenge=<code_challenge>&code_challenge_method=S256
   ```

4. **获取回调代码：**  
   ```bash
   curl -X POST https://auth.coupler.io/oauth2/token \
     -d "grant_type=authorization_code&client_id=<client_id>&code=<auth_code>&redirect_uri=http://127.0.0.1:8976/callback&code_verifier=<code_verifier>"
   ```

5. **保存令牌：**  
   - `access_token` 保存到 `config/mcporter.json`  
   - `refresh_token` 保存到 `coupler-io/oauth-state.json`（用于自动刷新令牌）  

6. **保护令牌文件：**  
   ```bash
   chmod 600 config/mcporter.json CPL/oauth-state.json
   ```

   > ⚠️ 令牌文件包含敏感信息，请勿将其提交到版本控制系统中（已通过 `.gitignore` 文件排除）。为提高安全性，可以考虑将令牌存储在系统的密钥链中（macOS：`security add-generic-password`）。  

### mcporter 配置文件

`config/mcporter.json` 的内容如下：  
```json
{
  "mcpServers": {
    "coupler": {
      "baseUrl": "https://mcp.coupler.io/mcp",
      "headers": {
        "Authorization": "Bearer <access_token>"
      }
    }
  }
}
```

### OAuth 状态信息

`coupler-io/oauth-state.json` 的内容如下：  
```json
{
  "authServer": "https://auth.coupler.io",
  "clientId": "<client_id>",
  "refreshToken": "<refresh_token>"
}
```

---

## 令牌刷新

访问令牌的有效期为 2 小时。可以通过以下方式自动刷新令牌：  
```bash
CLIENT_ID=$(jq -r '.clientId' coupler-io/oauth-state.json)
REFRESH_TOKEN=$(jq -r '.refreshToken' coupler-io/oauth-state.json)
AUTH_SERVER=$(jq -r '.authServer' coupler-io/oauth-state.json)

curl -s -X POST "$AUTH_SERVER/oauth2/token" \
  -d "grant_type=refresh_token&client_id=$CLIENT_ID&refresh_token=$REFRESH_TOKEN"
```

更新 `config/mcporter.json` 文件中的 `access_token`，并更新 `coupler-io/oauth-state.json` 文件中的 `refresh_token`。  

**何时需要刷新令牌？**  
- 当遇到 401 错误时；  
- 或者在令牌即将过期之前，为了确保数据传输的连续性，可以主动进行刷新。  

---

## MCP 工具

### `list-dataflows`  
列出所有以 OpenClaw 为目标的数据流。  
```bash
mcporter call coupler.list-dataflows --output json
```

### `get-dataflow`  
获取数据流的详细信息，包括 `lastSuccessfulExecutionId`。  
```bash
mcporter call coupler.get-dataflow dataflowId=<uuid> --output json
```

### `get-schema`  
获取列的定义。列名存储在 `columnName` 中（例如 `col_0`、`col_1`）。  
```bash
mcporter call coupler.get-schema executionId=<exec-id>
```

### `get-data`  
对数据流中的数据执行 SQL 查询。查询的目标表始终为 `data`。  
```bash
mcporter call coupler.get-data executionId=<exec-id> query="SELECT col_0, col_1 FROM data WHERE col_2 > 100 LIMIT 50"
```

**建议操作：** 在执行大规模查询之前，先使用 `LIMIT 5` 来获取数据样本，以了解数据结构。  

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

## 限制事项

- 仅支持只读操作，无法修改数据流、数据源或数据内容。  
- 只能查看以 OpenClaw 为目标的数据流。  
- 令牌的有效期为 2 小时，需使用 `refresh_token` 进行自动刷新。