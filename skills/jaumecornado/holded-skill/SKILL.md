---
name: holded-skill
description: 通过 `holdedcli` 来安全地操作 `Holded ERP`，以读取和更新数据。当用户需要读取、搜索、创建、更新或删除 `Holded` 实体（联系人、发票、产品、客户关系管理（CRM）数据、项目、团队信息或会计记录），或者从终端调用 `Holded` API 端点时，请使用该工具。
metadata: {"openclaw":{"homepage":"https://github.com/jaumecornado/holded-skill","requires":{"bins":["holded"]},"primaryEnv":"HOLDED_API_KEY","install":[{"id":"brew","kind":"brew","formula":"jaumecornado/tap/holded","bins":["holded"],"label":"Install holdedcli (brew)"}]}}
---

# holded-skill

使用 `holdedcli` 以安全、可重复的工作流程来读取和修改 Holded 数据。

## 操作流程

1. 确认技术先决条件。
2. 使用 `holded actions list` 查找可用的操作。
3. 使用 `holded actions describe <action-id|operation-id>` 检查选定的操作。
4. 将操作分类为读取或写入。
5. 如果是写入操作，在执行前请获取明确的确认。
6. 使用 `--json` 参数运行命令，并汇总操作 ID、HTTP 状态码以及应用的更改。

## 先决条件

- 确认二进制文件存在：`holded help`
- 验证凭据：`holded auth status` 或 `HOLDED_API_KEY`
- 尽可能使用结构化输出：`--json`

## 安全规则

- 将任何 `POST`、`PUT`、`PATCH` 或 `DELETE` 操作视为 **写入** 操作。
- 将任何 `GET` 操作（或存在的 `HEAD` 操作）视为 **读取** 操作。
- 在执行前始终运行 `holded actions list` 和 `holded actions describe` 以验证操作的可用性和接受的参数。
- 在任何写入操作之前，务必获取用户的明确确认。
- 如果收到模棱两可的回复（如 `ok`、`go ahead`、`continue`），请不要执行写入操作，直到获得进一步说明。
- 在确认之前重复执行命令，以避免意外更改。
- 如果用户未确认，请停止操作并提供调整建议。

## 强制确认协议

在任何写入操作之前，显示以下信息：

1. 要执行的操作（`action_id` 或 `operation_id`）。
2. 方法和端点。
3. `--path`、`--query` 和请求体参数（`--body` 或 `--body-file`）。
4. 要执行的命令。

仅在执行用户明确同意后才能继续操作。

## 执行模式

### 读取操作

1. 使用 `holded actions list --json`（可选使用 `--filter`）找到相应的操作。
2. 使用 `holded actions describe <action-id|operation-id> --json` 验证路径/查询/请求体参数是否正确。
3. 运行 `holded actions run <action> ... --json`。
4. 返回清晰的摘要和相关操作 ID，以便后续操作。

### 写入操作

1. 找到并验证要执行的操作。
2. 使用 `holded actions describe <action-id|operation-id> --json` 验证所需的/可选参数。
3. 准备最终的请求数据（payload）。
4. 请求用户的确认。
5. 在获得确认后执行命令。
6. 报告操作结果（`status_code`、受影响的 ID、API 响应）。

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

对于较长的请求数据，建议使用 `--body-file` 参数：

```bash
holded actions run invoice.update-contact \
  --path contactId=<id> \
  --body-file payload.json \
  --json
```

## 错误处理

- 如果出现 `MISSING_API_KEY`，请通过 `--api-key`、`HOLDED_API_KEY` 或 `holded auth set` 配置 API 密钥。
- 如果出现 `ACTION_NOT_FOUND`，请列出操作目录并使用 `--filter` 进行搜索。
- 如果出现 `INVALID_BODY`，请在执行前验证 JSON 数据的有效性。
- 如果出现 `API_ERROR`，请报告 `status_code` 和 API 错误信息。

## 参考资料

- 阅读 `{baseDir}/references/holdedcli-reference.md` 以获取快速参考命令和标准。
- 使用以下命令动态发现操作和检查参数：
  - `holded actions list --json`
  - `holded actions describe <action-id|operation-id> --json`