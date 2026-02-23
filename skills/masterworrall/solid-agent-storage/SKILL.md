---
name: solid-agent-storage
description: 使用 Solid 协议为您的人工智能代理分配持久性身份（WebID）和个人数据存储空间（Pod）。
version: 0.3.6
author: Interition
license: Apache-2.0
metadata:
  openclaw:
    requires:
      env:
        - INTERITION_PASSPHRASE
        - SOLID_SERVER_URL
      bins:
        - node
        - curl
        - jq
      config:
        - ~/.interition/agents/
    primaryEnv: INTERITION_PASSPHRASE
    install:
      - kind: brew
        formula: jq
        bins: [jq]
    categories:
      - storage
      - identity
      - data
    homepage: https://github.com/masterworrall/agent-interition
---
# Solid Agent Storage

本技能为您提供了一个名为 **Solid Pod** 的个人数据存储空间，该存储空间拥有一个 **WebID**（您在网络上的身份标识）。您可以在其中存储数据、读取数据，并与其他代理共享特定资源。

## 何时使用本技能

- 当您需要在对话中记住某些信息（如笔记、偏好设置或学到的知识点）时
- 当您需要存储结构化数据（支持 RDF/Turtle 格式的数据，或任何类型的内容）时
- 当您需要与同样拥有 Solid Pod 的其他代理共享数据时
- 当您需要一个可被其他代理或服务验证的持久身份标识时

## 设置

在使用任何命令之前，请设置 `INTERITION_PASSPHRASE` 环境变量。此密码用于加密存储在您设备上的 Solid 服务器凭据（位于 `~/.interition/agents/` 目录下），从而保护这些凭据的安全性。请使用强密码并严格保密。

### 运行自己的 Solid 服务器（推荐）

为了获得完全的控制权，您可以运行自己的 [Community Solid Server](https://github.com/CommunitySolidServer/CommunitySolidServer)（CSS）。CSS 是由 [Open Data Institute](https://www.theodi.org/) 维护的开源软件。

将 `SOLID_SERVER_URL` 设置为您服务器的 URL：

```bash
export SOLID_SERVER_URL="http://localhost:3000"
```

有关可用的 Docker 配置示例，请参阅 [源代码仓库](https://github.com/masterworrall/agent-interition)。

### 使用共享的 Solid 服务器（用于多代理协作）

如果您的代理需要使用 Solid 协议与其他代理进行协作，它们需要共享同一个 Solid 服务器。目前有两个公开的 Solid 服务器实例：

- **https://solidcommunity.net** — 由 [Open Data Institute](https://www.theodi.org/) 运营
- **https://crawlout.io** — 由 [Interition](https://interition.net) 运营（本技能的提供者）

要使用共享服务器，请设置 `SOLID_SERVER_URL`：

```bash
export SOLID_SERVER_URL="https://crawlout.io"
```

如果未设置 `SOLID_SERVER_URL`，本技能将默认使用 `https://crawlout.io`。

## 凭据的工作原理

Solid 服务器会生成凭据，以防止未经授权的第三方访问其服务和数据。这与任何需要用户身份验证的远程服务的工作原理相同。当您为代理配置资源时：

1. CSS 会为您的代理创建一个账户、WebID 和 Pod。
2. CSS 会生成客户端凭据（ID 和密钥），代理使用这些凭据进行身份验证。
3. 代理使用这些凭据获取用于读取和写入数据的 **限时令牌**。
4. CSS 会对每个请求实施访问控制（WAC），只有经过授权的代理才能访问受保护的资源。

`INTERITION_PASSPHRASE` 并非服务器凭据本身。它用于初始化存储在您设备上的服务器生成的凭据的加密过程（使用 AES-256-GCM 算法），并设置权限为 `0600`，从而提高安全性。服务器本身永远不会看到您的密码。

## 工作原理

本技能提供了三个用于管理 CSS 相关操作的脚本（配置、解除配置和状态检查），以及一个用于身份验证的辅助工具。所有标准的 Solid 操作（读取、写入、删除和共享）都通过 `curl` 和令牌来完成。您的 Solid Pod 符合 W3C 的 Solid 协议标准。

有关使用 Solid 服务器及整个 Solid 生态系统的更多信息，请访问 [solidproject.org](https://solidproject.org)。完整的协议规范可在 [Solid Protocol (W3C)](https://solidproject.org/TR/protocol) 中找到。

### 两步工作流程

**步骤 1：** 获取令牌：
```bash
scripts/get-token.sh --agent <name>
```

**步骤 2：** 使用 `curl` 并设置 `Authorization: Bearer $TOKEN` 来执行任何 Solid 操作。

### 令牌有效期

令牌的有效期为 **600 秒（10 分钟）**。如果距离您上次调用 `get-token.sh` 命令已超过 **8 分钟**，请在发起请求前重新获取令牌。

## 快速参考

- 提取令牌和服务器地址：
```bash
TOKEN_JSON=$(scripts/get-token.sh --agent example-agent)
TOKEN=$(echo "$TOKEN_JSON" | jq -r '.token')
POD_URL=$(echo "$TOKEN_JSON" | jq -r '.podUrl')
```

- 读取资源：
```bash
curl -s -H "Authorization: Bearer $TOKEN" "${POD_URL}memory/notes.ttl"
```

- 写入资源：
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

- 删除资源：
```bash
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" "${POD_URL}memory/old.ttl"
```

有关所有操作的详细信息（包括容器、PATCH 请求、访问控制及公共访问权限），请参阅 `references/solid-http-reference.md`。

## 管理命令

### 配置代理的身份和存储空间

为代理创建一个 WebID 和 Pod。每个唯一的代理名称只需运行此命令一次。

```bash
scripts/provision.sh --name <agent-name> [--displayName <display-name>]
```

**示例：**
```bash
scripts/provision.sh --name example-agent --displayName "Example Agent"
```

**输出：**
```json
{"status": "ok", "agent": "example-agent", "webId": "https://crawlout.io/example-agent/profile/card#me", "podUrl": "https://crawlout.io/example-agent/"}
```

### 解除代理的身份和存储空间配置

彻底删除代理的 WebID 和 Pod：从 CSS 服务器中删除其相关数据、客户端凭据、WebID 链接以及密码登录信息，并清除本地的凭据文件。

```bash
scripts/deprovision.sh --name <agent-name>
```

**示例：**
```bash
scripts/deprovision.sh --name example-agent
```

**成功输出：**
```json
{"status": "ok", "agent": "example-agent", "accountDeleted": true, "credentialsDeleted": true}
```

**部分失败输出（例如：服务器无法访问）：**
```json
{"status": "partial", "agent": "example-agent", "accountDeleted": false, "credentialsDeleted": true, "warnings": ["Could not delete CSS account: ..."]}
```

- `status: "ok"` — 代理的所有配置已完全清除，本地文件也已删除
- `status: "partial"` — 本地文件已删除，但 CSS 清理失败（会显示相应的警告）

如果代理是在添加电子邮件/密码存储功能之前被配置的，CSS 将跳过清理操作，并会显示相应的警告。

### 检查状态

列出所有已配置的代理及其详细信息。

```bash
scripts/status.sh
```

## Pod 的结构

每个代理的 Pod 包含以下容器：

| 路径            | 用途                                      |
|------------------|-----------------------------------------|
| `/{name}/memory/`      | 代理的私有内存空间（包含笔记、学到的知识点和偏好设置）         |
| `/{name}/shared/`      | 用于与其他代理共享的资源                         |
| `/{name}/conversations/`   | 对话记录和上下文信息                         |

## Turtle 模板

在存储结构化数据时，请使用 Turtle（RDF）格式。以下是一些常见数据的模板示例：

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

所有管理命令的输出均为 JSON 格式。出现错误时，标准错误输出（stderr）会显示相应的错误信息：
```json
{"error": "description of what went wrong"}
```

常见错误包括：
- “未提供密码” — 请设置 `INTERITION_PASSPHRASE` 环境变量
- “未找到凭据” — 请先运行 `provision.sh` 命令
- “密码无效” — `INTERITION_PASSPHRASE` 的值不正确
- “令牌请求失败：401” — 凭据已过期，请重新配置代理的身份和存储空间
- “HTTP 404” — 请求的资源不存在