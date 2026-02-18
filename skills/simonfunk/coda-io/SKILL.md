---
name: coda
description: 通过 Coda REST API v1 与 Coda.io 的文档、表格、行、页面以及自动化功能进行交互。当用户需要读取、写入、更新或删除 Coda 文档中的数据时，可以使用该 API。此外，在以下情况下也会用到该 API：提到“Coda”、“Coda 文档”、“Coda 表格”、“Coda 行”、“Coda API”、“同步到 Coda”、“从 Coda 读取数据”、“写入 Coda 数据”、“Coda 自动化”、“Coda 页面”、“Coda 公式”、“共享 Coda 文档”或“Coda 权限”时。该 API 支持对文档、页面、表格、列、行、公式、控件、文件夹、权限、发布功能以及分析数据的操作。
metadata:
  env:
    - CODA_API_TOKEN (required): "Coda API token — get at https://coda.io/account → API settings"
---
# Coda API 技能

通过 Coda.io 的 REST API v1 与其进行交互。基础 URL：`https://coda.io/apis/v1`

## 设置

1. 在 `https://coda.io/account` 的 “API 设置” → “生成 API 令牌” 中获取 API 令牌。
2. 设置环境变量：`export CODA_API_TOKEN="<token>"`
3. 验证：`bash scripts/coda.sh whoami`

## 辅助脚本

`scripts/coda.sh` 负责封装常见的操作。运行 `bash scripts/coda.sh help` 可以查看使用方法。

示例：
```bash
# List docs
bash scripts/coda.sh list-docs | jq '.items[].name'

# List tables in a doc
bash scripts/coda.sh list-tables AbCDeFGH | jq '.items[] | {id, name}'

# List columns (discover IDs before writing)
bash scripts/coda.sh list-columns AbCDeFGH grid-abc | jq '.items[] | {id, name}'

# Read rows with column names
bash scripts/coda.sh list-rows AbCDeFGH grid-abc 10 true | jq '.items'

# Insert rows
echo '{"rows":[{"cells":[{"column":"c-abc","value":"Hello"}]}]}' | \
  bash scripts/coda.sh insert-rows AbCDeFGH grid-abc

# Upsert rows (match on key column)
echo '{"rows":[{"cells":[{"column":"c-abc","value":"Hello"},{"column":"c-def","value":42}]}],"keyColumns":["c-abc"]}' | \
  bash scripts/coda.sh upsert-rows AbCDeFGH grid-abc

# Share doc
bash scripts/coda.sh share-doc AbCDeFGH user@example.com write
```

## 工作流程：读取数据

1. `list-docs` → 查找文档 ID
2. `list-tables <docId>` → 查找表格 ID
3. `list-columns <docId> <tableId>` → 获取列 ID/名称
4. `list-rows <docId> <tableId>` → 读取数据

## 工作流程：写入数据

1. 首先获取列 ID（参见上述步骤 3）
2. 使用列 ID 构建包含数据的 JSON 数组
3. 使用 `insert-rows`（插入新数据）或 `upsert-rows`（具有 `keyColumns` 以实现幂等写入）
4. 写入操作返回 HTTP 202 状态码及 `requestId`；如需确认写入结果，可以使用 `mutation-status` 进行轮询

## 关键概念

- **使用资源 ID 而非名称**：使用稳定的资源 ID 而不是用户可编辑的名称。
- **最终一致性**：写入操作是异步的（返回 HTTP 202 状态码），需要通过 `mutation-status` 进行轮询以确认写入结果。
- **分页**：列表接口会返回 `nextPageToken`，将其作为参数传递以获取下一页数据。
- **速率限制**：读取操作每 6 秒最多 100 次；写入操作每 6 秒最多 10 次；文档内容写入操作每 10 秒最多 5 次。违反限制时会收到 429 错误并自动重试。
- **获取最新数据**：在请求头中添加 `X-Coda-Doc-Version: latest` 以确保获取到最新数据（可能会收到 400 错误）。
- **数据格式**：支持 `simple`（默认）、`simpleWithArrays` 和 `rich`（用于结构化数据）。
- **从 URL 获取文档 ID**：`https://coda.io/d/Title_d<DOC_ID>`，其中 `_d` 后的部分即为文档 ID。

## 直接使用 curl（当脚本未涵盖相关操作时）

```bash
curl -s -H "Authorization: Bearer $CODA_API_TOKEN" \
  "https://coda.io/apis/v1/docs/{docId}/tables/{tableId}/rows?useColumnNames=true&limit=50"
```

## 写入操作的相关命令

```bash
curl -s -H "Authorization: Bearer $CODA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST -d '{"rows":[...]}' \
  "https://coda.io/apis/v1/docs/{docId}/tables/{tableId}/rows"
```

## 完整的 API 参考文档

请参阅 [references/api-endpoints.md](references/api-endpoints.md)，以获取完整的 API 端点列表，包括参数、请求体格式和响应详情。

可按以下类别搜索：账户（Account）、文件夹（Folders）、文档（Docs）、页面（Pages）、表格（Tables）、列（Columns）、行（Rows）、公式（Formulas）、控件（Controls）、权限（Permissions）、发布（Publishing）、自动化（Automations）、分析（Analytics）和其他（Miscellaneous）。