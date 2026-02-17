---
name: holded-skill
description: 通过 `holdedcli` 来安全地操作 Holded ERP 系统，以读取和更新数据。当用户需要读取、搜索、创建、更新或删除 Holded 实体（联系人、发票、产品、CRM 数据、项目、团队、会计信息）时，或者需要从终端调用 Holded API 端点时，请使用该工具。
metadata: {"openclaw":{"homepage":"https://github.com/jaumecornado/holded-skill","requires":{"bins":["holded"]},"primaryEnv":"HOLDED_API_KEY","install":[{"id":"brew","kind":"brew","formula":"jaumecornado/tap/holded","bins":["holded"],"label":"Install holdedcli (brew)"}]}}
---
# holded-skill

使用 `holdedcli` 以安全、可重复的工作流程来读取和修改 Holded 数据。

## 操作流程

1. 确认技术前提条件。
2. 使用 `holded actions list` 查找可用的操作。
3. 使用 `holded actions describe <action> --json` 查看所选操作的详细信息。
4. 将操作分类为读取（read）或写入（write）。
5. 如果是写入操作，在执行前请获取用户的明确确认。
6. 使用 `--json` 选项运行命令，并汇总操作 ID、HTTP 状态码以及应用的更改内容。

## 前提条件

- 确保二进制文件存在：`holded help`
- 验证凭据：`holded auth status` 或 `HOLDED_API_KEY`
- 尽可能使用结构化输出：`--json`

## 安全规则

- 将任何 `POST`、`PUT`、`PATCH` 或 `DELETE` 操作视为写入（write）操作。
- 将任何 `GET` 操作（或存在的 `HEAD` 操作）视为读取（read）操作。
- 在执行任何操作之前，务必先使用 `holded actions describe <action> --json`（在 `holded actions list` 之后）来验证参数是否正确。
- 对于购买收据，必须设置 `docType=purchase` 并在 JSON 正文中包含 `"isReceipt": true`。由于 `holdedcli` 会根据 Holded 的数据模型进行验证（该模型不包含 `isReceipt` 字段），因此必须使用 `--skip-validation` 标志。
- 在执行任何写入操作之前，务必获取用户的明确确认。
- 如果收到含糊的回复（如 “ok”、“go ahead” 或 “continue”），请不要执行写入操作，直到获得进一步指示。
- 在确认之前，请重复执行命令，以避免意外更改。
- 如果用户未确认，请停止操作并提供调整建议。

## 强制确认协议

在执行任何写入操作之前，必须显示以下信息：

1. 操作的 ID（`action_id` 或 `operation_id`）。
2. 使用的方法和端点。
3. `--path`、`--query` 和 `--body` 参数。
4. 要执行的命令内容。

请按照以下格式显示这些信息：

```text
This operation will modify data in Holded.
Action: <action_id> (<METHOD> <endpoint>)
Changes: <short summary>
Command: holded actions run ... --json
Do you confirm that I should run exactly this command? (reply with "yes" or "confirm")
```

只有在用户明确同意后，才能执行命令。

## 执行模式

### 读取操作

1. 使用 `holded actions list --json`（可配合 `--filter`）找到相应的操作。
2. 使用 `holded actions describe <action> --json` 验证路径、查询参数和正文参数是否正确。
3. 使用 `holded actions run <action> ... --json` 执行操作。
4. 返回清晰的总结信息以及后续操作所需的 ID。

### 写入操作

1. 查找并验证要执行的操作。
2. 使用 `holded actions describe <action> --json` 验证所需的参数。
3. 准备最终的请求数据（payload）。
4. 如果是创建购买收据或票据，请确保 `docType=purchase` 且 `"isReceipt": true`，并使用 `--skip-validation` 标志。
5. 请求用户的确认。
6. 在获得确认后执行命令。
7. 报告操作结果（`status_code`、受影响的 ID 以及 API 响应内容）。

## 基本命令

```bash
holded auth set --api-key "$HOLDED_API_KEY"
holded auth status
holded ping --json
holded actions list --json
holded actions list --filter contacts --json
holded actions describe invoice.get-contact --json
holded actions run invoice.get-contact --path contactId=<id> --json
```

对于较大的请求数据，建议使用 `--body-file` 选项：

```bash
holded actions run invoice.update-contact \
  --path contactId=<id> \
  --body-file payload.json \
  --json
```

**购买收据规则（购买票据时必须使用）：**

```bash
holded actions describe invoice.create-document --json
holded actions run invoice.create-document \
  --path docType=purchase \
  --body '{"isReceipt": true, "date": 1770764400, "contactId": "<contactId>", "items": [{"name": "Description", "units": 1, "subtotal": 29.4, "tax": 0}]}' \
  --skip-validation \
  --json
```

**重要说明：**
- 由于 `holdedcli` 会根据 Holded 的数据模型进行验证（该模型不包含 `isReceipt` 字段），因此必须使用 `--skip-validation` 标志。
- 在物品信息中应使用 `subtotal` 字段（而非 `price` 字段），因为这是 Holded API 需要的字段名称。
- 时间戳必须以秒为单位（Unix 时间戳），并且时间区域应为 **Europe/Madrid**。
**时间戳计算（Python）：**
```python
from datetime import datetime, timezone, timedelta
# For 11/02/2026 00:00 in Madrid:
dt = datetime(2026, 2, 11, 0, 0, 0, tzinfo=timezone(timedelta(hours=1)))
print(int(dt.timestamp()))  # 1770764400
```

## 错误处理

- 如果出现 `MISSING_API_KEY`，请通过 `--api-key`、`HOLDED_API_KEY` 或 `holded auth set` 参数配置 API 密钥。
- 如果出现 `ACTION_NOT_FOUND`，请使用 `--filter` 参数列出可用的操作并重新搜索。
- 如果出现 `INVALID_BODY`，请在执行前验证 JSON 数据的有效性。
- 如果出现 `API_ERROR`，请报告 `status_code` 以及相关的 API 错误信息。

## 参考资料

- 请阅读 `{baseDir}/references/holdedcli-reference.md` 以获取快速参考命令和规范。
- 可以通过以下命令动态发现操作和检查参数：
  - `holded actions list --json`
  - `holded actions describe <action> --json`