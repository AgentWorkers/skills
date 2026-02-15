---
name: airtable
description: 在 Airtable 数据库中创建、读取、更新和删除记录。当您需要管理 Airtable 表格/数据库中的数据、同步数据，或使用 Airtable 作为数据存储来自动化工作流程时，可以使用这些功能。
---

# Airtable API

通过 REST API 管理 Airtable 的数据库、表格和记录。

## 设置

1. 获取 API 密钥：https://airtable.com/create/tokens
2. 创建具有以下权限范围的 API 密钥：`datarecords:read`, `datarecords:write`
3. 存储 API 密钥：
```bash
mkdir -p ~/.config/airtable
echo "patXXXXXXXXXXXXXX" > ~/.config/airtable/api_key
```
4. 查找数据库 ID：打开数据库 → 帮助 → API 文档（以 `app` 开头）

## 列出记录

```bash
AIRTABLE_KEY=$(cat ~/.config/airtable/api_key)
BASE_ID="appXXXXXXXXXXXXXX"
TABLE_NAME="Table%20Name"  # URL-encoded

curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" | jq '.records'
```

## 获取单条记录

```bash
RECORD_ID="recXXXXXXXXXXXXXX"

curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}/${RECORD_ID}" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" | jq
```

## 创建记录

```bash
curl -s -X POST "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [{
      "fields": {
        "Name": "New Item",
        "Status": "Todo",
        "Notes": "Created via API"
      }
    }]
  }' | jq
```

## 创建多条记录

```bash
curl -s -X POST "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"fields": {"Name": "Item 1", "Status": "Todo"}},
      {"fields": {"Name": "Item 2", "Status": "Done"}}
    ]
  }'
```

每次请求最多可以创建 10 条记录。

## 更新记录

```bash
curl -s -X PATCH "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}/${RECORD_ID}" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "Status": "Done",
      "Notes": "Updated via API"
    }
  }' | jq
```

- `PATCH`：部分更新
- `PUT`：替换所有字段

## 删除记录

```bash
curl -s -X DELETE "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}/${RECORD_ID}" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" | jq
```

## 过滤记录

```bash
# filterByFormula parameter (URL-encoded)
FORMULA="Status%3D%27Todo%27"  # Status='Todo'

curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}?filterByFormula=${FORMULA}" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" | jq '.records'
```

常用过滤条件：
- `{Status}='Done'`：精确匹配
- `FIND('关键词', {Notes})`：包含指定文本
- `{Date} >= TODAY()`：日期比较
- `AND({Status}='Active', {Priority}='High')`：多个条件同时满足

## 对记录进行排序

```bash
curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}?sort%5B0%5D%5Bfield%5D=Created&sort%5B0%5D%5Bdirection%5D=desc" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" | jq '.records'
```

## 分页

```bash
# First page
RESPONSE=$(curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}?pageSize=100" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}")

OFFSET=$(echo $RESPONSE | jq -r '.offset // empty')

# Next page (if offset exists)
if [ -n "$OFFSET" ]; then
  curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}?pageSize=100&offset=${OFFSET}" \
    -H "Authorization: Bearer ${AIRTABLE_KEY}"
fi
```

## 选择特定字段

```bash
curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}?fields%5B%5D=Name&fields%5B%5D=Status" \
  -H "Authorization: Bearer ${AIRTABLE_KEY}" | jq '.records'
```

## 字段类型

- 文本：`"value"`
- 数字：`123`
- 复选框：`true` / `false`
- 日期：`"2024-01-15"`
- 单选：`"选项名称"`
- 多选：`["选项 1", "选项 2"]`
- 链接记录：`["recXXX", "recYYY"]`
- 附件：`[{"url": "https://..."}]`

## 速率限制

- 每个数据库每秒最多 5 次请求
- 使用批量操作（每次最多 10 条记录）以减少请求次数