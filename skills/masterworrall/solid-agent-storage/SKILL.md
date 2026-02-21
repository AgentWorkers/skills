---
name: solid-agent-storage
description: 使用 Solid 协议为你的 AI 代理分配一个持久性的身份标识（WebID）以及个人数据存储空间（Pod）。
version: 0.2.0
author: Interition
license: Apache-2.0
metadata: {"requires": {"bins": ["node", "docker", "curl"], "env": ["SOLID_SERVER_URL", "INTERITION_PASSPHRASE"]}, "categories": ["storage", "identity", "data"], "homepage": "https://github.com/masterworrall/agent-interition"}
---
# Solid Agent Storage

此技能为您提供了一个名为 **Solid Pod** 的个人数据存储空间，该存储空间拥有一个 **WebID**（即您在网络上的身份标识）。您可以在其中存储数据、读取数据，并与其他代理共享特定资源。

## 何时使用此技能

- 当您需要在对话中记住某些信息时（例如笔记、偏好设置、学到的知识点）  
- 当您需要存储结构化数据时（支持 RDF/Turtle 格式的数据，或任何类型的内容）  
- 当您需要与其他也拥有 Solid Pod 的代理共享数据时  
- 当您需要一个其他代理或服务可以验证的持久身份标识时  

## 设置要求

使用此技能需要一个正在运行的 [Community Solid Server](https://github.com/CommunitySolidServer/CommunitySolidServer)（简称 CSS）。该服务器不包含在此软件包中，请参阅 [源代码仓库](https://github.com/masterworrall/agent-interition) 以获取 Docker 设置说明。

在使用任何命令之前，请确保：  
1. Community Solid Server 正在运行且可访问（默认地址：`http://localhost:3000`）  
2. `SOLID_SERVER_URL` 已设置为服务器的 URL（默认值：`http://localhost:3000`）。**请确保指向您能够控制且信任的服务器**——此技能会与该服务器交换认证信息。  
3. `INTERITION_PASSPHRASE` 已设置（用于加密存储的认证信息）。请使用强密码并妥善保管。  

## 工作原理

此技能提供了三个用于 CSS 特定操作的管理脚本（配置代理、解除代理配置、查询状态），以及一个用于身份验证的辅助工具（token helper）。所有标准的 Solid 操作（读取、写入、删除、共享）均通过 `curl` 和 **Bearer token** 来完成——您的 Solid Pod 实际上就是一个符合 W3C Solid 标准的服务器。  

### 两步工作流程  

**步骤 1：** 获取 token：  
```bash
scripts/get-token.sh --agent <name>
```  
输出：  
```json
{"token": "eyJhbG...", "expiresIn": 600, "serverUrl": "http://localhost:3000", "podUrl": "http://localhost:3000/agents/researcher/", "webId": "http://localhost:3000/agents/researcher/profile/card#me"}
```  

**步骤 2：** 在执行任何 Solid 操作时，使用 `curl` 并设置 `Authorization: Bearer $TOKEN`。  

### Token 的有效期  

Token 的有效期为 **600 秒（10 分钟）**。如果自上次调用 `get-token.sh` 命令以来已超过 **8 分钟**，请在发起请求前重新获取新的 token。  

## 快速参考  

- 提取 token 和相关 URL：  
```bash
TOKEN_JSON=$(scripts/get-token.sh --agent researcher)
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
  -d '@prefix schema: <http://schema.org/>.
<#note-1> a schema:Note;
  schema:text "Important finding";
  schema:dateCreated "2024-01-15".' \
  "${POD_URL}memory/notes.ttl"
```  
- 删除资源：  
```bash
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" "${POD_URL}memory/old.ttl"
```  

有关所有操作的详细信息（包括容器管理、数据更新、访问控制、公共访问等），请参阅 `references/solid-http-reference.md`。  

## 管理命令  

### 配置新代理  

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

### 解除代理配置  

彻底删除代理的相关信息：从 CSS 服务器中删除该代理的 Pod、客户端凭证、WebID 链接及密码登录信息，并清除本地凭证文件。  
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
- `status: "ok"`：代理配置已完全删除，本地文件也被清除  
- `status: "partial"`：本地文件被删除，但 CSS 服务器的清理操作失败（请查看警告信息）  

**注意：** 如果代理是在添加电子邮件/密码存储功能之前被配置的，CSS 服务器将跳过清理操作，并会显示相应的警告信息。  

### 查询代理状态  

列出所有已配置的代理及其详细信息。  
```bash
scripts/status.sh
```  

## Pod 结构  

每个代理的 Solid Pod 包含以下容器：  
| 路径          | 用途                          |  
|----------------|-----------------------------|  
| `/agents/{name}/memory/`   | 代理的私有内存空间（包含笔记、学到的知识点、偏好设置）|  
| `/agents/{name}/shared/`   | 用于与其他代理共享的资源             |  
| `/agents/{name}/conversations/` | 对话记录和上下文信息                |  

## Turtle 模板  

在存储结构化数据时，请使用 Turtle（RDF）格式。以下是一些常见数据的模板示例：  
- **笔记或记忆记录**：  
```turtle
@prefix schema: <http://schema.org/>.
<#note-1> a schema:Note;
  schema:text "The content of the note";
  schema:dateCreated "2024-01-15".
```  
- **代理偏好设置**：  
```turtle
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix schema: <http://schema.org/>.
<#pref-1> a schema:PropertyValue;
  schema:name "response-style";
  schema:value "concise".
```  
- **共享数据集**：  
```turtle
@prefix schema: <http://schema.org/>.
<#dataset-1> a schema:Dataset;
  schema:name "Research Results";
  schema:description "Findings from the analysis task";
  schema:dateModified "2024-01-15".
```  

## 错误处理  

所有管理命令的输出结果均为 JSON 格式。发生错误时，标准错误输出（stderr）会显示相应的错误信息：  
```json
{"error": "description of what went wrong"}
```  

**常见错误：**  
- “未提供密码”：请设置 `INTERITION_PASSPHRASE` 环境变量  
- “未找到凭证”：请先运行 `provision.sh` 命令  
- “密码无效”：`INTERITION_PASSPHRASE` 的值不正确  
- “Token 请求失败（401 错误）”：凭证已过期，请重新配置代理  
- “HTTP 404 错误”：请求的资源在指定 URL 不存在