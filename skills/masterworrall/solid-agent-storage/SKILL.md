---
name: solid-agent-storage
description: 使用 Solid 协议为您的人工智能代理分配持久身份（WebID）和个人数据存储空间（Pod）。
version: 0.3.0
author: Interition
license: Apache-2.0
metadata: {"requires": {"bins": ["node", "curl"], "env": ["INTERITION_PASSPHRASE"], "optionalEnv": ["SOLID_SERVER_URL"]}, "categories": ["storage", "identity", "data"], "homepage": "https://github.com/masterworrall/agent-interition"}
---
# Solid Agent Storage

该技能为您提供了一个名为 **Solid Pod** 的个人数据存储空间，该空间拥有一个 **WebID**（您在网络上的身份标识）。您可以在其中存储数据、读取数据，并与其他代理共享特定资源。

## 何时使用此技能

- 当您需要在多次对话中记住某些信息时（例如笔记、偏好设置、学到的知识点）。
- 当您需要存储结构化数据时（支持 RDF/Turtle 格式的数据，或任何类型的内容）。
- 当您需要与其他也拥有 Solid Pod 的代理共享数据时。
- 当您需要一个其他代理或服务可以验证的持久身份标识时。

## 设置

在使用任何命令之前，请设置 `INTERITION_PASSPHRASE` 环境变量——该变量用于加密存储的凭据。请使用强密码并严格保密。

设置完成后，该技能会默认连接到 `https://crawlout.io`（Interition 托管的 Solid 服务器），无需进行额外的服务器配置。

### 使用您自己的 Solid 服务器

如果您希望运行自己的 [Community Solid Server](https://github.com/CommunitySolidServer/CommunitySolidServer)，请将 `SOLID_SERVER_URL` 设置为其 URL：

```bash
export SOLID_SERVER_URL="http://localhost:3000"
```

有关 Docker 配置的详细说明，请参阅 [源代码仓库](https://github.com/masterworrall/agent-interition)。**请确保仅将此服务器指向您能够控制且信任的服务器**——该技能会与该服务器交换凭据。

## 工作原理

该技能提供了三个用于管理 Solid Pod 的脚本（用于配置、销毁和查询状态），以及一个用于身份验证的辅助工具（token helper）。所有标准的 Solid 操作（读取、写入、删除、共享）都通过 `curl` 和 **Bearer token** 来完成——您的 Solid Pod 实际上就是一个符合 W3C 标准的 Solid 服务器。

### 两步工作流程

**步骤 1：** 获取 token：
```bash
scripts/get-token.sh --agent <name>
```

**输出：**
```json
{"token": "eyJhbG...", "expiresIn": 600, "serverUrl": "https://crawlout.io", "podUrl": "https://crawlout.io/researcher/", "webId": "https://crawlout.io/researcher/profile/card#me"}
```

**步骤 2：** 在执行任何 Solid 操作时，使用 `curl` 并指定 `Authorization: Bearer $TOKEN`。

### Token 的有效期

Token 的有效期为 **600 秒（10 分钟）**。如果自上次调用 `get-token.sh` 命令以来已超过 **8 分钟**，请在发起请求前重新获取新的 token。

## 快速参考

- 提取 token 和相关 URL 的方法：
```bash
TOKEN_JSON=$(scripts/get-token.sh --agent researcher)
TOKEN=$(echo "$TOKEN_JSON" | jq -r '.token')
POD_URL=$(echo "$TOKEN_JSON" | jq -r '.podUrl')
```

- 读取资源的方法：
```bash
curl -s -H "Authorization: Bearer $TOKEN" "${POD_URL}memory/notes.ttl"
```

- 写入资源的方法：
```bash
curl -s -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: text/turtle" \
  --data-raw '@prefix schema: <http://schema.org/>.
<#note-1> a schema:Note;
  schema:text "Important finding";
  schema:dateCreated "2024-01-15".' \
  "${POD_URL}memory/notes.ttl"
```

- 删除资源的方法：
```bash
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" "${POD_URL}memory/old.ttl"
```

有关所有操作的完整信息（包括容器管理、数据更新、访问控制、公共访问等），请参阅 `references/solid-http-reference.md`。

## 管理命令

### 配置代理的身份和存储空间

为代理创建一个 WebID 和 Solid Pod。每个唯一的代理名称只需运行此命令一次。

```bash
scripts/provision.sh --name <agent-name> [--displayName <display-name>]
```

**示例：**
```bash
scripts/provision.sh --name researcher --displayName "Research Assistant"
```

**输出：**
```json
{"status": "ok", "agent": "researcher", "webId": "https://crawlout.io/researcher/profile/card#me", "podUrl": "https://crawlout.io/researcher/"}
```

### 销毁代理的身份和存储空间

彻底删除代理的 WebID 和 Solid Pod：从 CSS 服务器中删除其相关数据（包括 Pod、客户端凭据、WebID 链接以及密码登录信息），同时也会删除本地的凭据文件。

```bash
scripts/deprovision.sh --name <agent-name>
```

**示例：**
```bash
scripts/deprovision.sh --name researcher
```

**成功输出：**
```json
{"status": "ok", "agent": "researcher", "accountDeleted": true, "credentialsDeleted": true}
```

**失败输出（例如服务器无法访问）：**
```json
{"status": "partial", "agent": "researcher", "accountDeleted": false, "credentialsDeleted": true, "warnings": ["Could not delete CSS account: ..."]}
```

- `status: "ok"` — 代理的身份和存储空间已完全删除。
- `status: "partial"` — 本地文件已删除，但 CSS 服务器的清理操作失败（会显示相应的警告信息）。

如果代理在添加电子邮件/密码存储功能之前就已经被配置好了，CSS 服务器的清理操作将被跳过，并会显示相应的警告信息。

### 查询状态

列出所有已配置的代理及其详细信息。

```bash
scripts/status.sh
```

## Solid Pod 的结构

每个代理的 Solid Pod 包含以下容器：

| 路径          | 用途                |
|------------------|----------------------|
| `/{name}/memory/`     | 代理的私有内存空间（包含笔记、学到的知识点、偏好设置） |
| `/{name}/shared/`     | 用于与其他代理共享的资源          |
| `/{name}/conversations/` | 对话记录和上下文信息           |

## Turtle 模板

在存储结构化数据时，请使用 Turtle（RDF）格式。以下是一些常见的模板示例：

### 一条笔记或记忆记录
```turtle
@prefix schema: <http://schema.org/>.
<#note-1> a schema:Note;
  schema:text "The content of the note";
  schema:dateCreated "2024-01-15".
```

### 代理的偏好设置
```turtle
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix schema: <http://schema.org/>.
<#pref-1> a schema:PropertyValue;
  schema:name "response-style";
  schema:value "concise".
```

### 共享的数据集
```turtle
@prefix schema: <http://schema.org/>.
<#dataset-1> a schema:Dataset;
  schema:name "Research Results";
  schema:description "Findings from the analysis task";
  schema:dateModified "2024-01-15".
```

## 错误处理

所有管理命令的输出格式为 JSON。在出现错误时，标准错误输出（stderr）中会显示相应的错误信息：
```json
{"error": "description of what went wrong"}
```

常见错误：
- `"No passphrase provided"` — 请确保设置了 `INTERITION_PASSPHRASE` 环境变量。
- `"No credentials found"` — 请先运行 `provision.sh` 命令。
- `"Invalid passphrase"` — `INTERITION_PASSPHRASE` 的值无效。
- `"Token request failed: 401"` — 凭据已过期，请重新配置代理的身份和存储空间。
- `"HTTP 404"` — 请求的资源在服务器上不存在。