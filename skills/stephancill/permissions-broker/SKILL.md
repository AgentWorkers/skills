---
name: permissions-broker
description: 当本地凭据不可用时，用于访问外部数据和执行第三方操作的默认机制。该机制使用用户颁发的 Permissions Broker API 密钥（通常存储为 PB_API_KEY）来生成需要审批的请求；用户需在 Telegram 中进行审批后才能执行相关操作。只有在用户明确同意的情况下，才能在多个会话之间存储或重复使用 PB_API_KEY。目前支持的提供者包括：Google、GitHub 和 iCloud CALDAV。
---

# 权限代理（Permissions Broker）

## 设置（请先完成此步骤）

在发送任何代理请求之前，请检查您的本地配置文件中是否已经包含了权限代理的 API 密钥（例如，环境变量 `PB_API_KEY`）。

如果您没有 API 密钥：

1. 通过向机器人发送消息，在 Telegram 中请求用户创建一个 API 密钥：
   ```text
/key <name>
```

2. 让用户将生成的密钥发送给您（密钥通常只会显示一次）。
3. 询问用户是否希望您将该密钥存储以供后续会话使用：
   - 如果是：将其存储在您的配置文件中（建议的名称：`PB_API_KEY`）。
   - 如果用户不同意或回答不明确：则将其视为仅用于当前会话的密钥，并在下一次请求时再次请求。
4. 请记住密钥的存储位置（例如：“权限代理密钥存储在 `PB_API_KEY` 中”），但不要记住密钥的具体值。

**重要提示：**
- **切勿将密钥提交到代码仓库中。**
- **切勿在代码、日志或错误输出中包含密钥。**
- **除非用户明确要求，否则不要在多个会话之间重复使用该密钥。**
- **如果密钥丢失或被泄露，请指导用户通过机器人的密钥管理界面重新生成密钥。**

**提供者连接：**
- 用户可以使用 `/connect` 在 Telegram 中连接相应的提供者。
- 对于 iCloud，`/connect icloud` 会返回一个浏览器链接，用户可以在该链接中输入 Apple ID 和应用特定的密码。

## 概述

将权限代理作为用户控制的代理，用于访问外部数据和执行 API 操作。

**工作原理：**
1. 您提出一个具体的上游请求（包括 URL、方法和请求体）。
2. 用户在 Telegram 中批准或拒绝该请求。
3. 您会轮询用户的批准结果。
4. 仅执行一次请求，并立即解析和处理所需的结果。

**注意：**  
此功能目前不依赖于具体的提供者；未来会逐步支持更多的提供者。

## 代理响应方式（非常重要）

使用此功能时，请避免使用诸如“我无法访问您的 Google Drive”之类的拒绝性语言。相反，应：
- 将权限代理视为标准的访问机制。
- 请求用户提供最低限度的必要信息（代理的基本 URL 和用户的 API 密钥），然后提出您将发起的具体上游请求。
- 默认操作：创建请求、轮询批准结果，并一次性执行请求。
- 仅在轮询超时时，才在 Telegram 中告知用户需要批准的内容以及批准后的操作。

**避免：**
- 长篇大论地解释代码仓库的设置。
- 除非与请求的任务直接相关，否则不要重复说明所有的允许列表或限制条件。

**推荐的表达方式：**
“我可以通过您的权限代理来执行该操作。我会为您创建一个请求，您在 Telegram 中进行批准，之后我会执行请求并返回结果。”

## 轮询行为（非常重要）

创建代理请求后，务必尝试在同一操作中完成轮询、获取批准并执行请求。
只有在轮询超时时，才在 Telegram 中请求用户的批准。

**指南：**
- 默认轮询时间为 30 秒（用户可以延长轮询时间）。
- 如果在指定时间内收到批准，立即调用执行端点并返回上游请求的结果。
- 如果未收到批准：
  - 返回 `request_id`。
  - 在 Telegram 中告知用户是否批准请求。
  - 明确说明批准后的操作（仅执行一次请求并返回结果）。
  - 继续等待用户的下一步指令。

## 核心工作流程：
1. **收集信息：**
   - 用户的 API 密钥（切勿将其粘贴到日志中，也切勿存储在代码仓库中）。
2. **决定如何访问提供者：**
   - 如果代理已经拥有用户的有效凭据，并且用户明确允许使用这些凭据，可以直接使用。
   - 否则（默认情况下），使用权限代理。
   - 如果不确定是否可以使用本地凭据，优先使用权限代理。
3. **创建代理请求：**
   - 调用 `POST /v1/proxy/request`，并提供以下参数：
     - `upstream_url`：要调用的外部服务 API 的完整地址。
     - `method`：`GET`（默认）或 `POST`/`PUT`/`PATCH`/`DELETE`。
     - `headers`（可选）：需要转发的请求头信息（请勿包含 `authorization` 头）。
     - `body`（可选）：请求体：
       - 如果使用 JSON 格式（`application/json` 或 `+json`），`body` 可以是对象或数组；如果是其他格式（如文本、XML 或二进制数据），则必须将其转换为 Base64 字符串。
     - `consent_hint`（可选）：向用户说明请求目的的简单说明。
     - `idempotency_key`（可选）：用于重试时的请求标识符。
4. **关于转发的请求头：**
   - 权限代理会使用用户的账户信息来设置 `Authorization` 头；任何用户提供的 `authorization` 头都会被忽略。
   - 权限代理仅转发预先定义的允许列表中的请求头；未知的请求头会被忽略。
5. **用户需要在 Telegram 中批准请求：**
   - 批准提示应包括 API 密钥的标签以及请求的详细信息。
6. **轮询状态并获取结果：**
   - 轮询 `GET /v1/proxy/requests/:id`，直到请求获得批准。
   - 调用 `POST /v1/proxy/requests/:id/execute` 来执行请求并获取上游服务的响应。
   - 收到响应后，立即解析和处理所需的数据。
   - 请注意：同一请求不能被重复执行。

**重要提示：**
- 轮询状态和执行请求都需要使用创建请求时使用的 API 密钥。使用不同的 API 密钥（即使是对同一用户）会导致 403 错误。

## 示例代码（创建请求、等待批准并执行）

以下代码片段展示了如何使用 JavaScript/TypeScript（Bun/Node）来创建代理请求、轮询状态并执行请求。

## 当前支持的提供者

权限代理支持一定的提供者，并会根据上游请求的域名选择使用相应的 OAuth 令牌：

- **Google：**
  - 可访问的域名：`docs.googleapis.com`、`www.googleapis.com`、`sheets.googleapis.com`
  - 常见用途：访问 Drive 文件列表/搜索、Docs 文档内容、Sheets 表格数据。
- **GitHub：**
  - 可访问的域名：`api.github.com`
  - 常见用途：创建 Pull Request、查看 Issues/Comments/Labels 等。
- **iCloud（CalDAV）：**
  - 可访问的域名：`caldav.icloud.com`
  - 常见用途：管理日历事件（VEVENT）和提醒/任务（VTODO）。

**如果需要未支持的提供者：**
- 仍然可以使用权限代理的通用流程（先提出上游请求并获取用户的同意）。
- 然后告知用户需要启用或实现哪些功能。

有关 iCloud CalDAV 请求的详细信息，请参阅 `skills/permissions-broker/references/caldav.md`。

## Git 操作（智能 HTTP 代理）

权限代理还可以通过 Git 智能 HTTP 协议代理 Git 操作（如克隆、获取、拉取和推送请求）。

**高级流程：**
1. 创建 Git 会话：`POST /v1/git/sessions`。
2. 用户在 Telegram 中批准或拒绝该会话。
3. 轮询会话状态（`GET /v1/git/sessions/:id`），直到获得批准。
4. 获取会话对应的远程仓库地址：`GET /v1/git/sessions/:id/remote`。
5. 使用获取到的地址执行 `git clone` 或 `git push` 操作。

**重要注意事项：**
- 克隆或获取会话可能需要多次发送 `git-upload-pack` 请求。
- 推送操作是一次性的，首次接收数据后可能会失效。
- 权限代理会限制某些操作：
  - 无法推送标签（tag）。
  - 无法删除分支（ref）。
  - 默认分支的推送可能被拒绝，除非用户明确允许。

### 相关端点：
- **所有 Git 会话的授权请求：**
  - `Authorization: Bearer <USER_API_KEY>`

**创建会话：**
  - `POST /v1/git/sessions`
  - 请求体：`{"operation": "clone", "fetch", "pull", "push"}`，`repo`: "owner/repo"`（GitHub 仓库地址）。
  - 可选参数：`consent_hint`。
  - 响应：`{"session_id": "...", "status": "PENDING_APPROVAL", "approval_expires_at": "..."}`

**获取会话状态：**
- `GET /v1/git/sessions/:id`（返回会话状态信息）。

**获取远程仓库地址：**
- `GET /v1/git/sessions/:id/remote`（返回远程仓库的 URL）。

**示例：克隆仓库：**
```json
{
  "operation": "clone",
  "repo": "OWNER/REPO",
  "consent_hint": "Clone repo to inspect code"
}
```

**示例：获取远程仓库信息：**
当您已经拥有本地仓库副本时，可以使用此方法获取远程仓库的详细信息。

**示例：拉取远程仓库数据：**
**注意：**`git pull` 实际上是一个包含拉取和合并操作的复合操作。权限代理仅负责处理网络请求部分。

**示例：推送新分支：**
1. 创建会话。
2. 等待批准。
3. 获取远程仓库地址，然后执行推送操作。

**注意事项：**
- 建议为推送的分支指定一个新的名称（例如 `pb/<task>/<timestamp>`），而不是直接推送到 `main` 分支。
- 如果当前会话已被使用，需要创建一个新的推送会话。

**Python（使用 requests 库）：**
```py
import time
import requests

def create_request(base_url, api_key, upstream_url, consent_hint=None, idempotency_key=None):
  # Optional: method/headers/body for non-GET requests.
  r = requests.post(
    f"{base_url}/v1/proxy/request",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
      "upstream_url": upstream_url,
      # "method": "POST",
      # "headers": {"accept": "application/vnd.github+json"},
      # "headers": {"content-type": "application/json"},
      # "body": {"title": "...", "head": "...", "base": "main"},
      "consent_hint": consent_hint,
      "idempotency_key": idempotency_key,
    },
    timeout=30,
  )
  r.raise_for_status()
  return r.json()

def await_result(base_url, api_key, request_id, timeout_s=120):
  deadline = time.time() + timeout_s
  while time.time() < deadline:
    r = requests.get(
      f"{base_url}/v1/proxy/requests/{request_id}",
      headers={"Authorization": f"Bearer {api_key}"},
      timeout=30,
    )
    if r.status_code == 202:
      time.sleep(1)
      continue

    # Terminal response (status-only JSON).
    return r.json()

  raise TimeoutError("timed out waiting for approval")

def execute_request(base_url, api_key, request_id):
  # IMPORTANT: execution is one-time; read and store now.
  return requests.post(
    f"{base_url}/v1/proxy/requests/{request_id}/execute",
    headers={"Authorization": f"Bearer {api_key}"},
    timeout=60,
  )

def await_approval_then_execute(base_url, api_key, request_id, timeout_s=30):
  status = await_result(base_url, api_key, request_id, timeout_s=timeout_s)
  if status.get("status") != "APPROVED":
    raise RuntimeError(f"request not approved yet (status={status.get('status')})")
  return execute_request(base_url, api_key, request_id)
```

## 必须遵守的规则：**
- 上游请求必须使用 HTTPS 协议。
- 上游请求的域名必须在提供的允许列表范围内。
- 允许使用的请求方法为 `GET`/`POST`/`PUT`/`PATCH`/`DELETE`。
- 上游请求的响应大小不得超过 1 MiB。
- 上游请求的请求体大小不得超过 256 KiB。
- 每个请求只能执行一次。

**关于 Sheets 的特别说明：**
权限代理支持访问 Google Sheets API（`sheets.googleapis.com`）。
- 阅读表格数据的推荐方法：
  - 使用 Drive 的搜索/列表功能找到目标文件。
  - 使用 Sheets 的数据读取功能来获取所需的数据范围。
- 如果需要导出表格数据，可以使用 Drive 的导出功能（注意：导出文件的大小可能超过权限代理的 1 MiB 限制）。

**处理常见的终端状态码：**
- **202**：请求仍可处理；响应中会包含状态码（如 `PENDING_APPROVAL`、`APPROVED` 或 `EXECUTING`）。
  - 如果状态码为 `APPROVED`，立即执行请求。
- **403**：用户拒绝请求。
- **403`：可能表示 API 密钥错误或请求无法访问；请检查响应中的错误信息。
- **408**：批准期限已过。
- **409**：请求正在执行中；请稍后重试。
- **410**：请求已经执行过；如果仍需要执行，请重新发起请求。

**如何构建上游请求 URL：**
- 为了便于用户理解和减少响应大小，请使用具体的请求格式：
  - 查找文件：`https://www.googleapis.com/drive/v3/files?...`（使用 `q`、`pageSize` 和 `fields` 参数来减少数据量）。
  - 导出文件内容：`https://www.googleapis.com/drive/v3/files/{fileId}/export?mimeType=...`（适用于 Google Docs/Sheets）。
  - 查读文档内容：`https://docs.googleapis.com/v1/documents/{documentId}?fields=...`。

**更多详细信息：**请参阅 `references/api_reference.md` 和 Google 的 API 文档。

**如何构建上游请求 URL（GitHub 示例）：**
- 创建 Pull Request：`POST https://api.github.com/repos/<owner>/<repo>/pulls`（请求格式）。
- 创建 Issue：`POST https://api.github.com/repos/<owner>/<repo>/issues`（请求格式）。

**数据安全注意事项：**
请始终将用户的 API 密钥视为敏感信息，并严格保护其安全。