---
name: twenty-crm
description: 通过 REST/GraphQL 与 Twenty CRM（自托管版本）进行交互。
metadata: {"clawdbot":{"emoji":"🗂️","os":["darwin","linux"]}}
---

# Twenty CRM

您可以通过 REST 和 GraphQL 与自己托管的 Twenty 实例进行交互。

## 配置

创建 `config/twenty.env` 文件（示例文件位于 `config/twenty.env.example`）：

- `TWENTY_BASE_URL`（例如：`https://crm.example.com` 或 `http://localhost:3000`）
- `TWENTY_API_KEY`（Bearer 令牌）

脚本会自动加载此文件。

## 命令

### 低级辅助工具

- REST GET: `skills/twenty-crm/scripts/twenty-rest-get.sh "/companies" 'filter={"name":{"ilike":"%acme%"}}&limit=10'`
- REST POST: `skills/twenty-crm/scripts/twenty-rest-post.sh "/companies" '{"name":"Acme"}'`
- REST PATCH: `skills/twenty-crm/scripts/twenty-rest-patch.sh "/companies/<id>" '{"employees":550}'`
- REST DELETE: `skills/twenty-crm/scripts/twenty-rest-delete.sh "/companies/<id>"`

- GraphQL: `skills/twenty-crm/scripts/twenty-graphql.sh 'query { companies(limit: 5) { totalCount } }'`

### 常用操作（示例）

- 创建公司：`skills/twenty-crm/scripts/twenty-create-company.sh "Acme" "acme.com" 500`
- 按名称查找公司：`skills/twenty-crm/scripts/twenty-find-companies.sh "acme" 10`

## 注意事项

- Twenty 支持 REST（`/rest/...`）和 GraphQL（`/graphql`）两种接口。
- 对象名称和端点可能因您的工作区元数据和 Twenty 版本而有所不同。
- 根据您的设置，认证令牌的有效期可能较短；如果收到 401 错误，请刷新令牌。