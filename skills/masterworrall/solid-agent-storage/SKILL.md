---
name: solid-agent-storage
description: 使用 Solid 协议为你的 AI 代理分配一个持久性的身份标识（WebID）以及个人数据存储空间（Pod）。
version: 0.1.0
author: Interition
license: Apache-2.0
metadata: {"requires": {"bins": ["node", "docker"], "env": ["SOLID_SERVER_URL", "INTERITION_PASSPHRASE"]}, "categories": ["storage", "identity", "data"], "homepage": "https://github.com/masterworrall/agent-interition"}
---
# Solid Agent Storage

本技能为您提供了一个名为 **Solid Pod** 的个人数据存储服务，该存储服务具有一个 **WebID**（您在网络上的身份标识）。您可以使用它来存储数据、读取数据，并与其他代理共享特定资源。

## 何时使用本技能

- 当您需要在对话中记住某些信息（如笔记、偏好设置或学到的知识点）时。
- 当您需要存储结构化数据（支持 RDF/Turtle 格式的数据，或任何类型的内容）时。
- 当您需要与其他也拥有 Solid Pod 的代理共享数据时。
- 当您需要一个其他代理或服务可以验证的持久性身份标识时。

## 设置

在使用任何命令之前，请确保：
1. Solid 服务器正在运行（在 `agent-interaction` 目录中执行 `docker-compose up` 命令）。
2. `SOLID_SERVER_URL` 已经设置（默认值：`http://localhost:3000`）。
3. `INTERITION_PASSPHRASE` 已经设置（用于加密存储的凭据）。

## 命令

### 为新代理配置 Solid Pod

为代理创建一个 WebID 和 Solid Pod。每个代理只需执行此命令一次。

```bash
scripts/provision.sh --name <agent-name> [--displayName <display-name>]
```

**示例：**
```bash
scripts/provision.sh --name researcher --displayName "Research Assistant"
```

**输出：**
```json
{"status": "ok", "agent": "researcher", "webId": "http://localhost:3000/agents/researcher/profile/card#me", "podUrl": "http://localhost:3000/agents/researcher/"}
```

### 将数据写入 Solid Pod

将数据存储到代理的 Solid Pod 中的指定 URL 处。

```bash
scripts/write.sh --agent <name> --url <resource-url> --content <data> [--content-type <mime-type>]
```

**示例 — 存储一条笔记：**
```bash
scripts/write.sh --agent researcher \
  --url "http://localhost:3000/agents/researcher/memory/notes.ttl" \
  --content '@prefix schema: <http://schema.org/>.
<#meeting-2024-01> a schema:Note;
  schema:text "User prefers bullet-point summaries";
  schema:dateCreated "2024-01-15".' \
  --content-type "text/turtle"
```

**示例 — 存储纯文本：**
```bash
scripts/write.sh --agent researcher \
  --url "http://localhost:3000/agents/researcher/memory/summary.txt" \
  --content "Key finding: the API rate limit is 100 req/min" \
  --content-type "text/plain"
```

### 从 Solid Pod 中读取数据

从指定的 URL 中检索数据。

```bash
scripts/read.sh --agent <name> --url <resource-url>
```

**示例：**
```bash
scripts/read.sh --agent researcher --url "http://localhost:3000/agents/researcher/memory/notes.ttl"
```

**输出：**
```json
{"status": "ok", "url": "...", "contentType": "text/turtle", "body": "..."}
```

### 授予其他代理访问权限

允许其他代理读取或写入特定的资源。

```bash
scripts/grant-access.sh --agent <owner-name> --resource <url> --grantee <webId> --modes <Read,Write,...>
```

**有效权限模式：** `Read`、`Write`、`Append`、`Control`

**示例 — 允许其他代理读取您的笔记：**
```bash
scripts/grant-access.sh --agent researcher \
  --resource "http://localhost:3000/agents/researcher/shared/report.ttl" \
  --grantee "http://localhost:3000/agents/writer/profile/card#me" \
  --modes "Read"
```

### 撤销访问权限

移除之前授予的访问权限。

```bash
scripts/revoke-access.sh --agent <owner-name> --resource <url> --grantee <webId>
```

### 检查代理状态

列出所有已配置的代理及其详细信息。

```bash
scripts/status.sh
```

## Solid Pod 的结构

每个代理的 Solid Pod 包含以下容器：

| 路径          | 用途                         |
|-----------------|-----------------------------|
| `/agents/{name}/memory/`   | 代理的私有内存（笔记、学到的知识点、偏好设置） |
| `/agents/{name}/shared/`   | 用于与其他代理共享的资源         |
| `/agents/{name}/conversations/` | 对话记录和上下文信息         |

## Turtle 模板

在存储结构化数据时，请使用 Turtle（RDF）格式。以下是一些常见数据的模板：

### 一条笔记或记忆内容
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

所有命令的输出均为 JSON 格式。在发生错误时，标准错误输出（stderr）中会显示相应的错误信息：
```json
{"error": "description of what went wrong"}
```

常见错误：
- “未提供密码短语” — 请设置 `INTERITION_PASSPHRASE` 环境变量。
- “未找到凭据” — 请先运行 `provision.sh` 命令。
- “密码短语无效” — `INTERITION_PASSPHRASE` 的值不正确。
- “HTTP 401” — 凭据已过期；请重新配置代理。
- “HTTP 404” — 请求的资源在该 URL 处不存在。