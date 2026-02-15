---
name: fast-io
description: >-
  Cloud file management and collaboration platform. Use this skill when the user 
  needs to store files, create branded shares (Send/Receive/Exchange), or query 
  documents using built-in RAG AI. Supports transferring ownership to humans, 
  managing workspaces, and real-time collaboration. Includes 266 tools for 
  authentication, file uploads, AI chat, and org management. Provides a free 
  agent plan with 100 GB storage and 5,000 monthly credits.
license: Proprietary
compatibility: >-
  Requires network access. Connects to the Fast.io MCP server at mcp.fast.io 
  via Streamable HTTP (/mcp) or SSE (/sse).
metadata:
  author: fast-io
  version: "1.29.0"
homepage: "https://fast.io"
---

# Fast.io MCP 服务器

**存储文件，与人共享，利用 AI 进行查询。所有操作均通过一个免费提供的 API 完成。**

> **以上为简要概述。** 完整的代理使用指南（包含所有 266 个工具的参数、工作流程、ID 格式及使用限制）可在 **`https://mcp.fast.io/skill.md`** 查阅——请在每次会话开始时获取该指南。

Fast.io 为 AI 代理提供了一个全面的文件管理和协作平台：您可以上传文件、创建带有品牌标识的数据室、使用内置的 AI 查询文件内容，并在任务完成后将所有工作移交给人类处理。

## 连接到服务器

| 连接方式 | 端点地址 |
|-----------|----------|
| Streamable HTTP（推荐） | `mcp.fast.io/mcp` |
| SSE（旧版本） | `mcp.fast.io/sse` |

## MCP 资源

通过 `resources/list` 和 `resources/read` 可访问以下资源：

| URI | 名称 | 描述 |
|-----|------|-------------|
| `skill://guide` | 使用指南 | 完整的代理使用指南（文本/Markdown 格式） |
| `session://status` | 会话状态 | 用户认证状态（JSON 格式）：`authenticated`, `user_id`, `user_email`, `token_expires_at` |

## MCP 提示语

通过 `prompts/list` 和 `prompts/get` 可获取 8 种常用操作的提示语：

| 提示语 | 用途 |
|--------|---------|
| `get-started` | 新手入门：账户、组织、工作空间设置 |
| `create-share` | 选择发送/接收/交换文件的方式 |
| `ask-ai` | 使用 AI 进行聊天和查询 |
| `upload-file` | 选择文件上传方式 |
| `transfer-to-human` | 将文件所有权转移给人类 |
| `discover-content` | 查找组织/工作空间 |
| `invite-collaborator` | 邀请协作成员 |
| `setup-branding` | 上传品牌相关文件 |

## 入门步骤

### 1. 创建代理账户

```
auth-signup → first_name, last_name, email, password
```

代理账户是免费的，无需进行电子邮件验证，且永远不会过期。会话会自动建立。JWT 令牌的有效期为 1 小时——到期后请调用 `auth-signin` 重新认证。人类账户使用的 API 密钥则不会过期。

### 2. 创建组织

```
org-create → name, domain (3+ chars, lowercase alphanumeric + hyphens)
```

代理组织可享受免费计划：100 GB 存储空间、每月 5,000 个信用点数、5 个工作空间以及 50 次文件共享权限。

### 3. 创建工作空间

```
org-create-workspace → org_id, name, folder_name (URL slug)
```

工作空间是用于存储文件的容器，支持 AI 聊天、成员管理和文件共享功能。

### 替代方案：协助现有用户

如果用户已经拥有 Fast.io 账户，他们可以在 `https://go.fast.io/settings/api-keys` 创建一个 API 密钥，并将其作为 Bearer 令牌使用。此时无需创建代理账户。

### 组织查找（重要）

要查找所有可用的组织，请同时调用以下两个接口：

- `list-orgs` —— 查找您所属的内部组织
- `orgs-external` —— 仅通过工作空间成员身份可访问的外部组织

当用户邀请代理加入工作空间但未邀请其加入组织时，通常会使用外部组织。如果仅调用 `list-orgs`，将无法发现这些外部组织。

## 关键概念

### 工作空间

工作空间是用于协作存储文件的容器，每个工作空间都有成员、文件夹结构、AI 聊天功能以及文件共享功能。免费计划提供 100 GB 的存储空间。

**智能功能开关：** **关闭** = 仅提供纯存储功能；**开启** = 提供基于 AI 的知识库服务，包括自动摘要生成、语义搜索、元数据提取等功能（默认开启）。

### 文件共享

文件共享功能专为与外部人员交换文件而设计：

- **发送** —— 将文件发送给人类（如报告、导出结果等）
- **接收** —— 从人类那里接收文件（如文档、数据集等）
- **交换** —— 支持双向文件交换（适用于协作工作流程）

共享文件时支持密码保护、设置过期时间、自定义品牌标识、访问权限控制以及访客聊天功能。

### 存储节点

文件和文件夹使用 30 个字符的不透明 ID 进行标识。`root` 表示根文件夹，`trash` 表示垃圾文件夹。

### 用户标识符

组织、工作空间和文件共享资源都使用 19 位的数字字符串作为标识符。

## 核心功能

| 功能 | 描述 |
|-----------|-------------|
| 文件存储 | 支持版本控制、文件夹层级结构、全文搜索和语义搜索 |
| 带品牌标识的文件共享 | 支持设置发送/接收/交换文件权限、设置过期时间、自定义品牌标识 |
| 内置 AI 功能 | 仅支持读取文件内容（可查询文件相关信息）；无法修改文件或配置 |
| 文件预览 | 支持预览图片、视频（HLS 格式）、音频、PDF、电子表格、代码文件 |
| URL 导入 | 可从任何 URL（包括 Google Drive、OneDrive、Dropbox）导入文件 |
| 评论 | 可在图片、视频、音频文件或 PDF 页面上添加注释；支持单层评论线程；可通过 `?comment={id}`, `?t={seconds}`, `?p={page}` 进行深度链接 |
| 备注 | 以 Markdown 格式记录的备注，可作为 AI 查询的参考信息 |
| 所有权转移 | 可将文件所有权转移给人类用户；代理用户仍保留管理员权限 |
| 实时通信 | 支持基于 WebSocket 的实时通信、光标跟踪和关注功能 |
| 事件记录 | 提供详细的事件日志和 AI 生成的活动摘要 |

## AI 聊天

**AI 聊天功能仅支持读取操作。** 它可以读取、分析文件内容并回答问题，但无法修改文件、更改设置或管理成员信息。所有超出文件内容读取范围的操作都必须通过 MCP 工具直接完成。

**聊天类型有两种：**
- **`chat`** —— 通用聊天，不涉及文件内容
- **`chat_with_files`** —— 基于文件内容的聊天（可引用文件内容）

**文件内容查看模式有两种（互斥）：**
- **文件夹/文件范围（RAG）** —— 支持基于文件内容的搜索；需要开启智能功能
- **文件附件** —— 直接查看文件内容；最多支持 10 个文件；无需开启智能功能

**聊天风格设置：** **concise**（简洁回答）或 **detailed**（详细回答，默认为详细模式）。可以在创建聊天时或发送消息时进行设置。

### AI 聊天工作流程

```
ai-chat-create → workspace_id, query_text, type
ai-message-read → workspace_id, chat_id, message_id  (auto-polls until complete)
ai-message-send → workspace_id, chat_id, query_text   (follow-up messages)
```

建议使用 `activity-poll` 功能来高效地等待结果，而不是循环查询每个消息的详细内容。

## 文件上传

### 文本文件（推荐方式）

```
upload-text-file → profile_type, profile_id, parent_node_id, filename, content
```

对于文本文件（如代码、Markdown、CSV、JSON、配置文件），只需一步即可完成上传：创建会话、上传文件、完成上传流程并等待文件存储完成——系统会返回 `new_file_id`。

### 二进制文件或大文件（分块上传）

```
upload-create-session → profile_type, profile_id, parent_node_id, filename, filesize
upload-chunk → upload_id, chunk_number, content | blob_ref | data (exactly one)
upload-finalize → upload_id (polls until stored, returns new_file_id)
```

对于二进制文件，有以下三种上传方式（请选择其中一种）：
- **`content`** —— 以文本形式上传文件内容（字符串、代码、JSON）。请勿将文件内容放入 `data` 字段。
- **`blob_ref`** —— **推荐使用**：使用 `POST` 请求将原始字节数据发送到 `/blob` 端点，并设置 `Content-Type: application/octet-stream`。系统会返回 `{blob_id, size}`；上传时请传递 `blob_id` 作为参数。这种方式可避免不必要的 Base64 编码开销。上传的文件数据会在 5 分钟后过期，使用后立即被销毁。
- **`data`** —— 以 Base64 编码的形式上传二进制文件。虽然仍受支持，但会增加约 33% 的数据传输开销。

## 文件共享流程

```
share-create → workspace_id, type (send/receive/exchange), title
share-add-file → share_id, node_id (add files to the share)
```

文件共享链接的格式为：`https://go.fast.io/shared/{custom_name}/{title-slug}`

## 文件所有权转移

创建包含工作空间、文件共享功能的组织后，可以将所有权转移给人类用户：

```
org-transfer-token-create → org_id (returns 64-char token, valid 72 hours)
```

转移所有权的链接格式为：`https://go.fast.io/claim?token={token}`

人类用户成为文件所有者，代理用户仍保留管理员权限。人类用户可享受 14 天的试用期，之后可升级为付费用户。

## 常见操作模式

- **文件下载：** 工具会返回文件的下载链接；系统不会直接传输二进制文件内容。
- **分页：** 文件存储相关的接口支持基于光标的分页功能（`sort_by`, `sort_dir`, `page_size`, `cursor`）；其他列表接口支持分页（`limit` 为 1-500，默认值为 100；`offset` 默认值为 0）。
- **文件删除/清理：** 删除文件会将其移至垃圾文件夹（可恢复）；永久删除文件前请先征得用户同意。
- **活动监控：** 使用 `activity-poll` 功能并设置 `wait=95` 可高效检测文件状态变化，无需频繁查询资源接口。

## 代理使用计划（免费）

每月费用为 0 美元。无需信用卡支付，无试用期，也无账户有效期限制。

| 资源 | 使用限制 |
|----------|-------|
| 存储空间 | 100 GB |
| 单个文件最大大小 | 1 GB |
| 每月信用点数 | 5,000 |
| 工作空间数量 | 5 个 |
| 文件共享次数 | 50 次 |
| 每个工作空间的成员数量 | 5 人 |

信用点数用于支付存储空间（100 GB/GB）、带宽费用（212/GB）、AI 令牌（每 100 个令牌计 1 个）、文件上传费用（每页文件计 1 个信用点数）。

当信用点数用完后，可将组织所有权转移给人类用户，用户可升级为付费用户以获得更多资源。

## 工具分类（共 266 种工具）

| 工具类别 | 工具数量 | 示例功能 |
|----------|-------|---------|
| 身份验证 | 11 种 | 注册、登录、双因素认证、API 密钥、密码重置 |
| 用户管理 | 13 种 | 个人资料设置、账户邀请、资产类型查询 |
| 组织管理 | 29 种 | 组织创建、计费设置、成员管理、组织转移、资产类型查询 |
| 工作空间管理 | 45 种 | 工作空间创建/删除、文件搜索、文件复制、备注管理 |
| 工作空间成员管理 | 10 种 | 成员添加/删除、权限设置、邀请功能 |
| 工作空间设置 | 17 种 | 工作空间配置、智能功能开启/关闭、品牌标识设置 |
| 文件共享 | 34 种 | 文件共享创建、品牌设置、链接管理、成员管理 |
| 文件共享详细设置 | 17 种 | 共享链接管理、访问权限设置、资产类型查询 |
| 文件上传 | 6 种 | 文本文件上传、会话管理、文件分块上传、上传状态查询、URL 导入 |
| 文件下载 | 5 种 | 文件下载、文件夹下载（ZIP 格式）、文件分享、版本控制 |
| AI 聊天 | 12 种 | 聊天功能管理、消息发送/接收、文件分享功能 |
| AI 相关功能 | 12 种 | 基于文件内容的 AI 聊天、自动添加文件标题、文件分享功能 |
| 评论功能 | 8 种 | 评论添加/删除、批量删除、评论回复功能 |
| 文件预览 | 7 种 | 文件预览（图片、视频、音频、PDF、代码文件） |
| 文件版本管理 | 6 种 | 文件版本列表、版本详情、版本恢复、文件删除 |
| 文件锁定 | 4 种 | 文件锁定/解锁、锁定状态管理 |
| 元数据管理 | 8 种 | 元数据字段的获取/设置/删除 |
| 事件记录 | 5 种 | 事件记录查询、事件详情查看、事件确认 |
| 系统管理 | 7 种 | 系统状态查询、系统健康状况检查、功能开关设置 |
| 实时通信 | 6 种 | 实时在线状态显示、光标跟踪、关注功能 |

## 权限设置（快速参考）

**组织创建（`org-create`）：**

| 参数 | 可选值 |
|-----------|--------|
| `industry` | `unspecified`, `technology`, `healthcare`, `financial`, `education`, `manufacturing`, `construction`, `professional`, `media`, `retail`, `real_estate`, `logistics`, `energy`, `automotive`, `agriculture`, `pharmaceutical`, `legal`, `government`, `non_profit`, `insurance`, `telecommunications`, `research`, `entertainment`, `architecture`, `consulting`, `marketing` |
| `background_mode` | `stretched`, `fixed` |

**工作空间权限设置（`org-create-workspace`, `workspace-update`）：**

| 参数 | 可选值 |
|-----------|--------|
| `perm_join` | `Only Org Owners`, `Admin or above`, `Member or above` |
| `perm_member_manage` | `Admin or above`, `Member or above` |

**文件共享权限设置（`share-create`）：**

| 参数 | 可选值 |
|-----------|--------|
| `access_options` | `Only members of the Share or Workspace`, `Members of the Share, Workspace or Org`, `Anyone with a registered account`, `Anyone with the link` |
| `invite` | `owners`, `guests` |
| `notify` | `never`, `notify_on_file_received`, `notify_on_file_sent_or_received` |

更多详细参数和使用限制请参阅完整的使用指南。

## 详细参考

本文档为简要概述。完整的代理使用指南（包含所有 266 个工具的参数、工作流程和使用限制）可直接从 MCP 服务器获取：

**获取完整指南：** `https://mcp.fast.io/skill.md`

这是最权威的参考资料——请在每次会话开始时获取最新版本，以获取完整的工具使用信息。指南内容包括：
- 所有 266 个工具的参数详情
- AI 聊天功能的详细使用说明（包括文件内容查询方式、问题表述规则）
- 完整的 URL 构建指南及深度链接信息
- 信用点数管理方法
- 所有端到端的工作流程及操作步骤
- ID 格式、编码规则及使用注意事项

此外，您还可以参考 [references/REFERENCE.md](references/REFERENCE.md)，其中包含平台功能介绍、代理使用计划详情及升级路径信息。