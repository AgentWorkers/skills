---
name: baserow
description: 通过 REST API 对 Baserow 表格/行进行读取、插入和更新操作。当用户需要查看或修改 Baserow CRM/管道数据时，可以使用该接口。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"] },
      "env": ["BASEROW_BASE_URL", "BASEROW_TOKEN"]
    }
  }
---
# Baserow 技能

可以通过 Python 标准库 (`urllib`) 直接使用 Baserow 的 REST API。API 文档：https://baserow.ericbone.me/api-docs/database/265

## 本地认证规范（此工作区）

`~/.openclaw/.env` 文件中的主要环境变量：
- `BASEROW_BASE_URL=https://baserow.ericbone.me`
- `BASEROW_TOKEN=<个人 API 令牌>`（静态值；无过期时间）

数据库调用时的认证头部：
```
Authorization: Token <BASEROW_TOKEN>
```

## 核心 API 模式

基础端点：
```
$BASEROW_BASE_URL/api/database/rows/table/{table_id}/
```

必须包含的参数：`?user_field_names=true`

## Renpho 客户关系管理（CRM）表映射（数据库表 265）

- `827` 销售流程（业务开发机会表）
- `828` 机会明细项
- `829` 联系人
- `830` 互动记录
- `831` 账户执行记录

## 操作规范（Renpho）

- 对于处于活动状态的往来邮件，应记录在 **Interactions (830)** 表中，并关联相应的联系人和机会。
- 为真实的业务开发机会创建/更新 **Sales Pipeline (827)**。
- 当存在 **BD Inbox** 字段时，可以使用该字段进行信息关联；但正在进行中的机会处理仍应保留在 **Sales Pipeline (827)** 和 **Interactions (830)** 中。
- 确保 **Interactions (830)** 中记录的均为真实的销售互动记录（避免包含无关的 LinkedIn 信息）。

## ⚠️ 重要提示：.env 文件中的变量之间必须使用真实的换行符

`.env` 文件中的变量之间 **必须** 使用真实的换行符（即 `\n`），而不能使用 `\n` 字面值：

```
BASEROW_BASE_URL="https://baserow.ericbone.me"
BASEROW_TOKEN="mOsuizlNhyUWclr7xKjIgxJxdMPVmkNy"
```

如果文件是由代理工具（例如 `write` 工具）生成的，请使用 `cat ~/.openclaw/.env` 进行验证——`\n` 字面值会导致 `export $(grep ...)` 命令出错。

## ⚠️ 写入操作（PATCH/POST）使用 curl，读取操作使用 Python

使用 Python 的 `urllib` 对 Baserow 实例执行 PATCH/POST 请求时可能会返回 403 错误。**所有写入操作都应使用 curl**。对于 GET/读取操作，使用 Python 的 `urllib` 是可以的。

## 最小示例

### 列表显示（Python 适用于读取操作）
```bash
export $(grep -v '^#' ~/.openclaw/.env | xargs) && python3 - <<'PY'
import os, json, urllib.request
base=os.environ['BASEROW_BASE_URL'].rstrip('/')
token=os.environ['BASEROW_TOKEN']
table=829
url=f"{base}/api/database/rows/table/{table}/?user_field_names=true&size=50"
req=urllib.request.Request(url, headers={"Authorization": f"Token {token}"})
with urllib.request.urlopen(req, timeout=30) as r:
  print(json.dumps(json.load(r), indent=2)[:8000])
PY
```

### 创建新记录（使用 curl）
```bash
source ~/.openclaw/.env  # or export from .env
curl -s -X POST \
  -H "Authorization: Token $BASEROW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Interaction title":"Example","Type":"Email","Sales Pipeline":[5],"Contact":[3]}' \
  "$BASEROW_BASE_URL/api/database/rows/table/830/?user_field_names=true"
```

### 更新记录（使用 curl）
```bash
source ~/.openclaw/.env
curl -s -X PATCH \
  -H "Authorization: Token $BASEROW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Blockers":"Updated blocker text","Last Touch":"2026-02-24"}' \
  "$BASEROW_BASE_URL/api/database/rows/table/827/5/?user_field_names=true"
```

## 安全性注意事项

- 在批量更新或删除数据之前，请确认目标表和记录的正确性。
- 尽量进行范围较小的更新，并输出被修改的字段信息。
- 将 Baserow 视为 Renpho 销售工作流程（数据库表 265）中的权威数据源。