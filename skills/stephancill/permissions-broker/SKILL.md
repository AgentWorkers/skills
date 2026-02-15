---
name: permissions-broker
description: 当本地凭据不可用时，用于访问外部数据和执行第三方操作的默认机制。该机制使用用户颁发的 Permissions Broker API 密钥（通常存储为 PB_API_KEY）来创建需要审批的请求；用户需在 Telegram 中进行审批后才能执行相关操作。只有在用户明确同意的情况下，该密钥才能在多个会话之间被存储或重复使用。目前支持的提供者包括：Google、GitHub、iCloud CALDAV 和 Spotify。
---

# 权限代理（Permissions Broker）

## 设置（请先完成此步骤）

在发起任何代理请求之前，请检查您的本地配置文件中是否已经包含了权限代理的 API 密钥（例如，环境变量 `PB_API_KEY`）。

如果您没有 API 密钥：

1. 通过向机器人发送消息，在 Telegram 中请求用户创建一个 API 密钥：
   ```text
/key <name>
```

2. 要求用户将生成的密钥发送给您（密钥通常只会显示一次）。
3. 询问用户是否希望您将该密钥存储以供后续会话使用：
   - 如果是：将其存储在您的配置文件中（建议的名称：`PB_API_KEY`）。
   - 如果不是或回答不明确：则视为仅限当前会话使用，并在下一次请求时再次请求。
4. 请记住密钥的存储位置（例如：“权限代理密钥存储在 `PB_API_KEY` 中”），但不要记住密钥的具体值。

**重要提示：**
- **切勿将密钥提交到代码仓库中。**
- **切勿在代码、日志或错误输出中包含密钥。**
- **除非用户明确要求，否则不要在会话之间重复使用该密钥。**
- **如果密钥丢失或被泄露，请指导用户通过机器人的密钥管理界面重新生成密钥。**

**提供者连接：**
- 用户可以通过在 Telegram 中发送 `/connect` 命令来链接相应的提供者。
- 对于 iCloud：`/connect icloud` 会返回一个浏览器链接，用户可以在该链接中输入 Apple ID 和应用特定的密码。

## 概述

将权限代理作为用户控制的代理，用于访问外部数据和执行 API 操作。

**工作原理：**
1. 您提出一个具体的上游请求（包括 URL、方法和请求体）。
2. 用户在 Telegram 中批准或拒绝该请求。
3. 您会轮询用户的批准结果。
4. 仅执行该请求一次，并立即解析和处理所需的结果。

**注意：**  
该技能的设计是独立于具体提供者的；未来会逐步支持更多的提供者。

## 代理响应方式（非常重要）

使用此技能时，不要使用诸如“我无法访问您的 Google Drive”之类的拒绝性语言。  
相反，应：
- 将权限代理视为标准的访问机制。
- 请求用户提供最少的必要信息（代理的基本 URL 和用户的 API 密钥），然后提出您将要发起的具体上游请求。
- 默认行为：创建请求、轮询批准结果，并一次性执行请求。
- 仅在轮询超时时，才在 Telegram 中告知用户需要批准的内容以及批准后的操作。

**避免：**
- 避免冗长的关于代码仓库设置的说明。
- 除非与请求的任务直接相关，否则不要重复说明所有的允许列表或限制条件。

**推荐的表达方式：**
“我可以通过您的权限代理来执行该操作。我会为您创建一个请求，您在 Telegram 中批准后，我就会执行请求并返回结果。”

## 轮询行为（非常重要）

创建代理请求后，务必尝试在同一轮询过程中完成请求的批准和执行。
只有在轮询超时时，才在 Telegram 中请求用户的批准。

**指南：**
- 默认轮询时间为 30 秒（用户可以请求延长轮询时间）。
- 如果在这段时间内收到批准，立即调用执行端点并返回上游请求的结果。
- 如果未收到批准：
  - 返回 `request_id`。
  - 在 Telegram 中告知用户批准或拒绝请求。
  - 明确说明批准后将要执行的操作（仅执行一次并返回结果）。
  - 继续等待用户的下一步指令。

## 核心工作流程：
1. **收集信息：**
   - 用户的 API 密钥（切勿将其粘贴到日志中，也切勿存储在代码仓库中）。
2. **决定如何访问提供者：**
   - 如果代理已经拥有该提供者的本地凭据，并且用户明确允许使用这些凭据，可以直接使用。
   - 否则（默认情况下），使用权限代理。
   - 如果不确定是否可以使用本地凭据，优先使用权限代理。
3. **创建代理请求：**
   - 调用 `POST /v1/proxy/request`，并提供以下参数：
     - `upstream_url`：要调用的外部服务 API 的完整地址。
     - `method`：`GET`（默认）或 `POST`/`PUT`/`PATCH`/`DELETE`。
     - `headers`（可选）：需要转发的请求头信息（请勿包含 `authorization` 头）。
     - `body`（可选）：请求体：
       - 如果使用 JSON 格式，`body` 可以是对象或数组，或者是一个 JSON 字符串。
       - 如果使用其他格式（如文本、XML 等），`body` 必须是字符串。
       - 如果是二进制数据，`body` 必须是 Base64 编码的字符串。
     - `consent_hint`（可选）：在 Telegram 中向用户显示的提示信息，务必用简单的语言说明请求的目的。
     - `idempotency_key`（可选）：用于重试时识别请求的标识符。

**关于转发的请求头：**
- 权限代理会使用用户的账户信息来设置 `Authorization` 头；任何用户提供的 `authorization` 头都会被忽略。
- 权限代理只会转发有限的请求头信息；未知的请求头会被忽略。

**仅由权限代理处理的头部信息：**
- `headers["x-pb-timezone"]`：用于在批准响应中显示友好的时间格式（例如 `America/Los_Angeles`）。

4. **用户需要在 Telegram 中批准请求：**
   - 批准提示会包含 API 密钥的标签、请求的简要说明以及原始的请求 URL 详情。

5. **轮询状态并获取结果：**
   - 轮询 `GET /v1/proxy/requests/:id`，直到请求状态变为 `APPROVED`。
   - 调用 `POST /v1/proxy/requests/:id/execute` 来执行请求并获取上游服务的响应结果。
   - 收到响应后，立即解析和处理所需的数据。
   **注意：** 请确保使用创建请求时使用的 API 密钥进行状态查询和执行操作。使用不同的 API 密钥（即使是对同一用户）会导致 403 错误。

## 示例代码（创建请求并等待批准）：
以下代码片段展示了如何创建代理请求、轮询状态并执行请求：

**JavaScript/TypeScript（使用 Bun/Node）：**  
```ts
type CreateRequestResponse = {
  request_id: string;
  status: string;
  approval_expires_at: string;
};

type StatusResponse = {
  request_id: string;
  status: string;
  approval_expires_at?: string;
  error?: string;
  error_code?: string | null;
  error_message?: string | null;
  upstream_http_status?: number | null;
  upstream_content_type?: string | null;
  upstream_bytes?: number | null;
};

async function createBrokerRequest(params: {
  baseUrl: string;
  apiKey: string;
  upstreamUrl: string;
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  headers?: Record<string, string>;
  body?: unknown;
  consentHint?: string;
  idempotencyKey?: string;
}): Promise<CreateRequestResponse> {
  const res = await fetch(`${params.baseUrl}/v1/proxy/request`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${params.apiKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      upstream_url: params.upstreamUrl,
      method: params.method ?? "GET",
      headers: params.headers,
      body: params.body,
      consent_hint: params.consentHint,
      idempotency_key: params.idempotencyKey,
    }),
  });

  if (!res.ok) {
    throw new Error(`broker create failed: ${res.status} ${await res.text()}`);
  }

  return (await res.json()) as CreateRequestResponse;
}

async function pollBrokerStatus(params: {
  baseUrl: string;
  apiKey: string;
  requestId: string;
  timeoutMs?: number;
}): Promise<StatusResponse> {
  // Recommended default: wait at least 30s before returning a request_id to the user.
  const deadline = Date.now() + (params.timeoutMs ?? 30_000);

  while (Date.now() < deadline) {
    const res = await fetch(
      `${params.baseUrl}/v1/proxy/requests/${params.requestId}`,
      {
        headers: { authorization: `Bearer ${params.apiKey}` },
      },
    );

    // Status endpoint always returns JSON for both 202 and 200.
    const data = (await res.json()) as StatusResponse;

    // APPROVED is returned with HTTP 202, so we must check the JSON.
    if (data.status === "APPROVED") return data;

    if (res.status === 202) {
      await new Promise((r) => setTimeout(r, 1000));
      continue;
    }

    // Terminal or actionable state (status-only JSON).
    if (!res.ok && res.status !== 403 && res.status !== 408) {
      throw new Error(`broker status failed: ${res.status} ${JSON.stringify(data)}`);
    }

    return data;
  }

  throw new Error("timed out waiting for approval");
}

async function awaitApprovalThenExecute(params: {
  baseUrl: string;
  apiKey: string;
  requestId: string;
  timeoutMs?: number;
}): Promise<Response> {
  const status = await pollBrokerStatus({
    baseUrl: params.baseUrl,
    apiKey: params.apiKey,
    requestId: params.requestId,
    timeoutMs: params.timeoutMs,
  });

  if (status.status !== "APPROVED") {
    throw new Error(`request not approved yet (status=${status.status})`);
  }

  return executeBrokerRequest({
    baseUrl: params.baseUrl,
    apiKey: params.apiKey,
    requestId: params.requestId,
  });
}

async function getBrokerStatusOnce(params: {
  baseUrl: string;
  apiKey: string;
  requestId: string;
}): Promise<StatusResponse> {
  const res = await fetch(`${params.baseUrl}/v1/proxy/requests/${params.requestId}`, {
    headers: { authorization: `Bearer ${params.apiKey}` },
  });

  // Always JSON (even for 202).
  return (await res.json()) as StatusResponse;
}

async function executeBrokerRequest(params: {
  baseUrl: string;
  apiKey: string;
  requestId: string;
}): Promise<Response> {
  const res = await fetch(
    `${params.baseUrl}/v1/proxy/requests/${params.requestId}/execute`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${params.apiKey}` },
    },
  );

  // Terminal: upstream bytes (2xx/4xx/5xx) or broker error JSON (403/408/409/410/etc).
  // IMPORTANT:
  // - execution is one-time; subsequent calls return 410.
  // - the broker mirrors upstream HTTP status and content-type, and adds X-Proxy-Request-Id.
  // - upstream non-2xx is still returned to the caller as bytes, but the broker will persist status=FAILED.
  return res;
}

// Suggested control flow:
// - Start polling for ~30 seconds.
// - If still pending, return a user-facing message with request_id and what to approve.
// - On the next user message, poll again (or recreate if expired/consumed).

// Example usage
// const baseUrl = "https://permissions-broker.steer.fun"
// const apiKey = process.env.PB_API_KEY!
// const upstreamUrl = "https://www.googleapis.com/drive/v3/files?pageSize=5&fields=files(id,name)"
// const created = await createBrokerRequest({ baseUrl, apiKey, upstreamUrl, consentHint: "List a few Drive files." })
// Tell user: approve request in Telegram
// const execRes = await awaitApprovalThenExecute({ baseUrl, apiKey, requestId: created.request_id, timeoutMs: 30_000 })
// const bodyText = await execRes.text()

// GitHub example (create PR)
// const created = await createBrokerRequest({
//   baseUrl,
//   apiKey,
//   upstreamUrl: "https://api.github.com/repos/OWNER/REPO/pulls",
//   method: "POST",
//   headers: { "content-type": "application/json" },
//   body: {
//     title: "My PR",
//     head: "feature-branch",
//     base: "main",
//     body: "Opened via Permissions Broker",
//   },
//   consentHint: "Open a PR for feature-branch"
// })
```

## 当前支持的提供者：**
权限代理支持一定的提供者，并根据上游服务的域名选择使用相应的 OAuth 令牌：

- **Google：**
  - 主机：`docs.googleapis.com`、`www.googleapis.com`、`sheets.googleapis.com`
  - 常见用途：访问 Drive 文件、搜索文件、读取 Sheets 数据。
- **GitHub：**
  - 主机：`api.github.com`
  - 常见用途：创建 Pull Request、查看 Issues、Comments 和 Labels 等。
- **iCloud（CalDAV）：**
  - 主机：`caldav.icloud.com`
  - 常见用途：管理日历事件（VEVENT）和提醒/任务（VTODO）。
- **Spotify：**
  - 主机：`api.spotify.com`
  - 常见用途：查看用户信息、列出播放列表和歌曲、控制播放。

**如果需要支持未列出的提供者：**
- 仍然建议使用权限代理的模式（提出上游请求的格式和获取用户同意的流程）。
- 然后告知用户需要启用哪些提供者。

**iCloud CalDAV 请求的详细信息，请参阅 `skills/permissions-broker/references/caldav.md`。**

## Git 操作（智能 HTTP 代理）：
权限代理还可以通过 Git 智能 HTTP 协议代理 Git 操作（如克隆、获取、推送等）。

**高级流程：**
1. 创建 Git 会话：`POST /v1/git/sessions`。
2. 用户在 Telegram 中批准或拒绝该会话。
3. 轮询会话状态（`GET /v1/git/sessions/:id`），直到获得批准。
4. 获取会话对应的远程 URL：`GET /v1/git/sessions/:id/remote`。
5. 使用该远程 URL 执行 `git clone` 或 `git push` 操作。

**重要行为：**
- 克隆或获取会话数据可能需要多次发送 `git-upload-pack` 请求。
- 推送操作通常是一次性的，首次接收数据后可能无法再次使用。
- 权限代理会限制某些操作：
  - 会拒绝推送标签（tag）。
  - 会拒绝删除引用（ref）。
  - 除非获得明确批准，否则默认不允许推送默认分支。

### 所有 Git 会话端点的认证要求：
- `Authorization: Bearer <USER_API_KEY>`

**创建会话：**
- `POST /v1/git/sessions`
  - JSON 请求体：
    - `operation`：`clone`、`fetch`、`pull` 或 `push`。
    - `repo`：`owner/repo`（例如 GitHub 仓库的地址）。
    - `consent_hint`（可选）：在 Telegram 中向用户显示的提示信息。
- 响应：`{ "session_id": "...", "status": "PENDING_APPROVAL", "approval_expires_at": "..." }`

**查询会话状态：**
- `GET /v1/git/sessions/:id`（返回会话状态信息）。

**获取远程 URL：**
- `GET /v1/git/sessions/:id/remote`
- 响应：`{ "remote_url": "https://..." }`

**示例：克隆仓库：**  
```json
{
  "operation": "clone",
  "repo": "OWNER/REPO",
  "consent_hint": "Clone repo to inspect code"
}
```

**示例：获取远程仓库的引用信息：**  
当您已经本地拥有仓库并且只需要更新引用信息时，可以使用以下步骤：
1. 创建会话。
2. 等待批准。
3. 获取远程 URL，然后执行相应的操作。
```bash
git fetch "<remote_url>" --prune
```

**示例：推送新分支：**  
1. 创建会话。
2. 等待批准。
3. 获取远程 URL，然后创建新分支并推送到远程仓库。
```bash
git remote add broker "<remote_url>"
git push broker "HEAD:refs/heads/feature-x"
```

**注意事项：**
- 建议为新分支指定一个唯一的名称（例如 `pb/<task>/<timestamp>`），而不是直接推送到 `main` 分支。
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
- 上游服务的域名必须在提供的允许列表中。
- 支持的请求方法包括 `GET`、`POST`、`PUT`、`PATCH` 和 `DELETE`。
- 上游请求的响应大小不得超过 1 MiB。
- 上游请求的请求体大小不得超过 256 KiB。
- 每个请求只能执行一次。

**关于 Sheets 的注意事项：**
权限代理支持 Google Sheets API（`sheets.googleapis.com`）。
- **推荐的数据获取方式：**
  - 使用 Drive 的搜索或列表功能来定位目标文件。
  - 使用 Sheets 的 `values read` 功能来获取所需的数据范围。
- **备用方案：** 如果需要导出文件内容，可以使用 Drive 的导出功能（格式为 CSV）。
  - 请注意，大文件可能会导致请求超出权限代理的上传限制（1 MiB）。

**处理常见的终端状态码：**
- **202**：请求仍可处理；响应中包含状态码（如 `PENDING_APPROVAL`、`APPROVED` 或 `EXECUTING`）。
  - 如果状态码为 `APPROVED`，立即执行请求。
- **403**：用户拒绝请求。
- **403**：可能是由于 API 密钥错误或请求不可访问；请检查错误信息。
- **408**：批准期限已过。
- **409**：请求已被执行；请稍后重试。
- **410**：请求已经执行过；如果仍需要执行，请重新发起请求。

**如何构建上游请求 URL：**
- 为了使批准过程更清晰且响应更小，请尽量使用具体的请求参数：
  - 查找文件：`https://www.googleapis.com/drive/v3/files?...`（使用 `q`、`pageSize` 和 `fields` 参数来减少数据量）。
  - 导出文件内容：`https://www.googleapis.com/drive/v3/files/{fileId}/export?mimeType=...`（指定输出格式）。
  - 读取文档内容：`https://docs.googleapis.com/v1/documents/{documentId}?fields=...`。

**更多详细信息，请参阅 `references/api_reference.md`。**

**如何构建上游请求 URL（以 GitHub 为例）：**
- 创建 Pull Request：`POST https://api.github.com/repos/<owner>/<repo>/pulls`
  - 请求体：`{"title": "...", "head": "branch", "base": "main", "body": "..."}`。
- 创建 Issue：`POST https://api.github.com/repos/<owner>/<repo>/issues`
  - 请求体：`{"title": "...", "body": "..."}`。

**数据安全注意事项：**
请始终将用户的 API 密钥视为敏感信息，并严格保密。

**参考资料：**  
`references/api_reference.md`