---
name: honcho-setup
description: >
  Install the @honcho-ai/openclaw-honcho plugin and migrate legacy file-based
  memory to Honcho. **UPLOADS WORKSPACE CONTENT TO EXTERNAL API**: Sends
  USER.md, MEMORY.md, IDENTITY.md, memory/, canvas/, SOUL.md, AGENTS.md,
  BOOTSTRAP.md, TOOLS.md, and HEARTBEAT.md contents to api.honcho.dev
  (managed, default) or your self-hosted HONCHO_BASE_URL. Requires user
  confirmation before uploading. Archives originals locally with user
  confirmation. Updates workspace docs to reference Honcho tools. Works with
  managed Honcho (requires API key) or self-hosted local instances (no key
  needed).
metadata:
  openclaw:
    emoji: "🧠"
    required_env: []  # Nothing is strictly required - self-hosted mode works without API key
    optional_env:
      - name: HONCHO_API_KEY
        description: "REQUIRED for managed Honcho (https://app.honcho.dev). NOT required for self-hosted instances. This skill reads this value from environment variables or ~/.openclaw/.env file."
      - name: HONCHO_BASE_URL
        description: "Base URL for a self-hosted Honcho instance (e.g. http://localhost:8000). Defaults to https://api.honcho.dev (managed)."
      - name: HONCHO_WORKSPACE_ID
        description: "Honcho workspace ID. Defaults to 'openclaw'."
      - name: WORKSPACE_ROOT
        description: "Path to the OpenClaw workspace root. Auto-detected from ~/.openclaw/openclaw.json if not set."
    required_binaries:
      - node
      - npm
    optional_binaries:
      - git
      - docker
      - docker-compose
    writes_to_disk: true
    archive_directory: "{workspace_root}/archive/"
    reads_sensitive_files:
      - "~/.openclaw/.env - reads ONLY the HONCHO_API_KEY value, no other environment variables are accessed"
      - "~/.openclaw/openclaw.json - reads workspace path configuration only"
    network_access:
      - "api.honcho.dev (managed mode, default)"
      - "User-configured HONCHO_BASE_URL (self-hosted mode)"
    data_handling:
      uploads_to_external: true
      requires_user_confirmation: true
      external_destinations:
        - "api.honcho.dev (managed Honcho, default)"
        - "User-configured HONCHO_BASE_URL (self-hosted mode)"
      uploaded_content:
        - "USER.md, MEMORY.md, IDENTITY.md (user profile/memory files)"
        - "All files under memory/ directory (structured memory)"
        - "All files under canvas/ directory (working memory)"
        - "SOUL.md, AGENTS.md, BOOTSTRAP.md, TOOLS.md, HEARTBEAT.md (agent configuration)"
      data_destination_purpose: "Migrates file-based memory system to Honcho API for AI agent memory/personalization"
  homepage: "https://honcho.dev"
  source: "https://github.com/plastic-labs/honcho"
---

# Honcho 设置

请安装 Honcho 插件，并将旧的工作区内存文件迁移到 Honcho。

> ⚠️ **数据上传警告**：此操作会将您的工作区内存文件（USER.md、MEMORY.md、IDENTITY.md、memory/、canvas/、SOUL.md、AGENTS.md、BOOTSTRAP.md、TOOLS.md、HEARTBEAT.md）的内容上传到外部 API。默认情况下，数据会被发送到 `api.honcho.dev`（托管的 Honcho 云服务）。对于自托管实例，数据会被发送到您配置的 `HONCHO_BASE_URL`。在上传之前，系统会请求您的明确确认，并显示将要上传的文件及其目标位置。

> **此操作会修改工作区文件**。在归档或删除任何文件之前，系统会请求您的确认。如果 Honcho 上传失败或被跳过，文件将不会被移动或删除。所有文件在删除前都会备份到 `{workspace_root}/archive/` 目录中。

> **敏感文件访问**：此操作仅会读取 `~/.openclaw/.env` 文件以获取 `HONCHO_API_KEY`（托管 Honcho 所需）。不会读取该文件中的其他环境变量。同时，还会读取 `~/.openclaw/openclaw.json` 文件以确定工作区的位置。
## 第一步：安装并启用插件

使用 OpenClaw 插件系统安装 Honcho 插件。**请使用以下命令进行安装——切勿直接安装 `@honcho-ai/sdk`，也勿在工作区内使用 `npm install`。**

```bash
openclaw plugins install @honcho-ai/openclaw-honcho
```

然后启用插件：

```bash
openclaw plugins enable openclaw-honcho
```

启用后，验证插件是否成功加载。如果网关日志显示 “Cannot find module ‘@honcho-ai/sdk’”，则需要手动安装插件的依赖项：

```bash
cd ~/.openclaw/extensions/openclaw-honcho && npm install
```

之后重启网关。这是 OpenClaw 插件安装程序在处理插件包依赖项时可能出现的问题。

如果插件已经安装并启用，可以直接跳到第二步。

## 第二步：验证 Honcho 连接

Honcho 可以作为 **托管的云服务** 或 **自托管的本地实例** 运行。请确定用户使用的是哪种模式。

### 选项 A：托管的 Honcho（默认）

确认 `HONCHO_API_KEY` 是否已设置。首先检查环境变量。如果没有找到 `HONCHO_API_KEY`，则仅从 `~/.openclaw/.env` 文件中读取该值（如果该文件存在）。**请勿读取或访问 `.env` 文件中的其他环境变量**——只需提取用于迁移的 `HONCHO_API_KEY` 值。

如果两个位置都没有设置 `HONCHO_API_KEY`，请停止操作并告知用户：

> `HONCHO_API_KEY` 未设置。请将其添加到您的环境变量或 `~/.openclaw/.env` 文件中，然后重新运行此操作。您可以在 https://app.honcho.dev 获取 API 密钥。

### 选项 B：自托管的 Honcho

Honcho 是开源的，可以本地运行。如果用户正在运行自己的实例，他们需要将 `HONCHO_BASE_URL` 设置为相应的地址（例如 `http://localhost:8000`）。SDK 的 `environment` 配置应设置为 `"local"`。

可以通过 Honcho 仓库使用 docker-compose 启动本地实例（需要 `git`、`docker` 和 `docker-compose`）：

```bash
git clone https://github.com/plastic-labs/honcho
cd honcho
cp .env.template .env
cp docker-compose.yml.example docker-compose.yml
docker compose up
```

对于本地实例，根据用户的配置，可能不需要 `HONCHO_API_KEY`。在继续之前，请先验证连接是否正常。

请参阅 https://github.com/plastic-labs/honcho?tab=readme-ov-file#local-development 以获取完整的自托管说明。

**在验证连接之前，请勿继续迁移操作。**在没有正常连接的情况下，系统不会读取、上传、归档或删除任何文件。**

## 第三步：检测旧内存文件

扫描工作区根目录以查找旧的内存文件。工作区根目录的确定顺序如下：
1. `WORKSPACE_ROOT` 环境变量
2. `~/.openclaw/openclaw.json` 文件中的 `agent_workspace` 或 `agents.defaults_workspace` 字段
3. `~/.openclaw/workspace`

### 需要检测的文件

**用户/所有者文件**（包含用户信息）：
- `USER.md`
- `IDENTITY.md`
- `MEMORY.md`

**代理/自我文件**（包含代理信息）：
- `SOUL.md`
- `AGENTS.md`
- `TOOLS.md`
- `BOOTSTRAP.md`
- `HEARTBEAT.md`

**目录**：
- `memory/` — 递归读取所有文件
- `canvas/` — 递归读取所有文件

`memory/` 和 `canvas/` 目录中的文件被视为用户/所有者的文件。

在继续之前，请向用户报告检测到的文件情况。**重要提示：在继续之前，必须获得用户的明确确认。**

在请求确认时，请向用户提供以下信息：
> **检测到的旧内存文件如下（附带文件大小）：**
>
> **如果用户确认继续，将会发生以下操作：**
> 1. **上传**：所有文件内容将被上传到 [api.honcho.dev 或您配置的 URL]
> 2. **归档**：文件将被复制到 {workspace_root}/archive/ 目录以进行备份
> 3. **删除**：仅删除旧文件（USER.md、MEMORY.md、IDENTITY.md、HEARTBEAT.md、memory/、canvas/）
> 4. **更新**：工作区文档（SOUL.md、AGENTS.md、BOOTSTRAP.md）将更新为使用 Honcho 工具的格式
>
> **数据传输目标**：文件内容将根据 `HONCHO_BASE_URL` 的配置发送到相应的地址
>
> **您是否同意继续此迁移操作？**

在没有用户明确确认之前，请勿进入第四步。

## 第四步：上传到 Honcho

使用 **messages upload** 端点（如果可用，则使用 `honcho_analyze`）将检测到的文件上传到 Honcho：

- **用户/所有者文件** → 作为消息通过会话上传，使用 `owner` 对等方（`peer_id` = 所有者对等方 ID）。
- **代理/自我文件** → 作为消息通过会话上传，使用 `openclaw` 对等方（`peer_id` = openclaw 对等方 ID）。

在上传之前，请确保工作区和两个对等方都存在（例如通过 SDK 或 API）。获取或创建一个上传会话，并报告每个类别（用户文件和代理文件）的上传数量。

如果任何上传失败，请停止操作并警告用户。切勿继续归档操作。

### SDK 设置示例（使用 messages 上传）

使用 Honcho SDK 通过会话上传 API 为每个文件创建消息（与 REST `.../messages/upload` 端点的操作相同，需要提供 `file` 和 `peer_id`）。设置客户端和对等方，获取或创建会话，然后将每个检测到的文件使用相应的对等方上传。

> **注意：** 下面的 `workspaceId` 和会话名称是默认值。如果您管理多个迁移操作，可以通过 `HONCHO_WORKSPACE_ID` 环境变量进行自定义。

```javascript
import fs from "fs";
import path from "path";
import { Honcho } from "@honcho-ai/sdk";

const apiKey = process.env.HONCHO_API_KEY;
const workspaceRoot = process.env.WORKSPACE_ROOT || "~/.openclaw/workspace";

const honcho = new Honcho({
  apiKey,
  baseURL: process.env.HONCHO_BASE_URL || "https://api.honcho.dev",
  // Customize via HONCHO_WORKSPACE_ID or leave as default
  workspaceId: process.env.HONCHO_WORKSPACE_ID || "openclaw",
});

await honcho.setMetadata({});
const openclawPeer = await honcho.peer("openclaw", { metadata: {} });
const ownerPeer = await honcho.peer("owner", { metadata: {} });

// Session name can be customized for multiple migration runs
const session = await honcho.session("migration-upload", { metadata: {} });
await session.addPeers([ownerPeer, openclawPeer]);

// For each detected file: read file and call session.uploadFile(file, peer)
// User/owner files → ownerPeer; agent/self files → openclawPeer
const filesToUpload = [
  { path: path.join(workspaceRoot, "USER.md"), peer: ownerPeer },
  { path: path.join(workspaceRoot, "SOUL.md"), peer: openclawPeer },
  // ... add every detected file and files under memory/ and canvas/
];

for (const { path: filePath, peer } of filesToUpload) {
  const stat = await fs.promises.stat(filePath).catch(() => null);
  if (!stat?.isFile()) continue;
  const filename = path.basename(filePath);
  const content = await fs.promises.readFile(filePath);
  const content_type = "text/markdown"; // or "text/plain", "application/pdf", "application/json"
  const messages = await session.uploadFile(
    { filename, content, content_type },
    peer,
    {}
  );
  console.log(`Uploaded ${filePath}: ${messages.length} messages`);
}
```

- **所需参数：** `session.uploadFile(file, peer, options?)` — 第二个参数是对等方（对象或 ID）。对于用户/所有者文件（USER.md、IDENTITY.md、MEMORY.md 以及 `memory/` 和 `canvas/` 目录下的所有文件），使用 `owner` 对等方；对于代理/自我文件（SOUL.md、AGENTS.md、TOOLS.md、BOOTSTRAP.md、HEARTBEAT.md），使用 `openclaw` 对等方。
- **会话：** 在上传之前，使用 `session.addPeers([ownerPeer, openclawPeer])` 将两个对等方添加到会话中。
- **文件（Node）：** 传递 `{filename, content: Buffer | Uint8Array, content_type }`。有关支持的文件类型（PDF、text、JSON），请参阅 [Honcho 文件上传文档](https://docs.honcho.dev/v3/guides/file-uploads#file-uploads)。示例测试脚本位于 `scripts/test-upload-file.mjs`（需要 `HONCHO_API_KEY`）。

## 第五步：归档旧文件

**重要提示：在归档之前，请务必获得用户的明确确认。** 默认的归档目录是 `{workspace_root}/archive/`。用户可以选择其他目录。

**安全保障：** 在归档之前，必须先在归档目录中创建备份副本。

对于每个检测到的文件：
1. 如果归档目录不存在，则创建该目录。
2. 将文件复制到归档目录中。**在继续之前，请确认复制是否成功。**
3. 如果归档目录中已存在同名文件，请添加时间戳（例如 `USER.md-2026-02-10T22-55-12`）。
4. 仅在复制成功后，执行删除操作。

然后执行以下删除规则：
- **删除旧文件**（仅删除迁移到 Honcho 之后不再需要的文件）：
  - `USER.md`
  - `MEMORY.md`
  - `IDENTITY.md`
  - `HEARTBEAT.md`

- **保留原始文件**（这些文件是仍在使用中的工作区文档）：
  - `AGENTS.md`
  - `TOOLS.md`
  - `SOUL.md`
  - `BOOTSTRAP.md`

- **将目录移动到归档目录**（已上传到 Honcho 的文件）：
  - `memory/`
  - `canvas/`

在删除任何文件之前，必须先在归档目录中创建备份副本。每次删除操作之前都会进行确认。

如果第四步中的上传失败或被跳过，请**不要归档或删除任何文件**。请警告用户，以防止数据丢失。

## 第六步：更新工作区文档

插件提供了位于 `node_modules/@honcho-ai/openclaw-honcho/workspace_md/` 的模板文件。请使用这些模板作为基于 Honcho 的工作区文档的来源。

对于 `AGENTS.md`、`SOUL.md` 和 `BOOTSTRAP.md` 文件：
- 如果文件存在于工作区中：更新文件，将旧的内存系统引用（`USER.md`、`MEMORY.md`、`memory/` 目录以及手动读取/写入的操作）替换为 Honcho 工具的引用。
- 如果文件不存在：将模板文件复制到工作区中。
- 保留用户添加的任何自定义内容。仅更新与内存相关的部分。

Honcho 工具包括：`honcho_profile`、`honcho_context`、`honcho_search`、`honcho_recall`、`honcho_analyze`。

## 第七步：确认操作结果

总结以下操作内容：
- 找到了哪些旧文件
- 上传了多少文件（用户文件和代理文件的数量）
- 哪些文件被归档以及归档的位置
- 哪些工作区文档被创建或更新
- 现在 Honcho 已成为新的内存系统——无需再进行手动文件管理

提供 Honcho 文档的链接供参考：https://docs.honcho.dev

---

## 安全性与隐私声明

本操作的设计重点在于透明性和安全性。以下是关于本操作的完整说明：

### 数据上传
- **上传内容**：USER.md、MEMORY.md、IDENTITY.md、memory/ 目录下的所有文件、canvas/ 目录下的所有文件、SOUL.md、AGENTS.md、BOOTSTRAP.md、TOOLS.md、HEARTBEAT.md 的内容
- **上传目标**：默认情况下，数据会被发送到 `api.honcho.dev`（托管的 Honcho 云服务）。对于自托管实例，数据会被发送到您配置的 `HONCHO_BASE_URL`
- **用户控制**：在上传之前需要用户明确确认。系统会显示文件列表和目标地址
- **目的**：将基于文件的记忆系统迁移到 Honcho API，以便进行 AI 代理的个性化设置和内存管理

### 敏感文件访问
- **`~/.openclaw/.env`：此操作仅从该文件中读取 `HONCHO_API_KEY` 值（如果存在）。不会读取或访问其他环境变量
- **`~/.openclaw/openclaw.json`：此操作仅读取工作区路径配置（`agent_workspace` 或 `agents.defaults_workspace` 字段）
- **工作区文件**：上述所有旧内存文件都将被读取以进行上传

### 文件修改
- **归档**：在删除文件之前，会先创建 `{workspace_root}/archive/` 目录并将所有文件复制到其中
- **删除**：只有在成功复制并验证后，才会删除 `USER.md`、MEMORY.md、IDENTITY.md、HEARTBEAT.md、memory/、canvas/ 文件
- **更新**：SOUL.md、AGENTS.md、BOOTSTRAP.md 将更新为使用 Honcho 工具的格式（先在归档目录中保存备份）
- **安全措施**：在没有备份副本的情况下，不会删除任何文件

### 凭据
- **HONCHO_API_KEY**：仅对于托管的 Honcho（api.honcho.dev）是必需的。对于自托管实例则不需要
- **其他凭证**：此操作不会访问、读取或传输任何其他凭证或秘密信息

### 网络访问
- **托管模式**：连接到 `api.honcho.dev`（Honcho 云服务）
- **自托管模式**：连接到您配置的 `HONCHO_BASE_URL`（例如 `http://localhost:8000`）
- **协议**：所有上传操作都通过 Honcho SDK（`@honcho-ai/sdk`）和 `messages upload` 端点进行

### 用户控制
- **第三步**：在上传任何文件之前需要用户明确确认（显示文件列表和目标地址）
- **第五步**：在归档或删除任何文件之前需要用户明确确认
- **第六步**：工作区文档更新会保留自定义内容
- **错误处理**：如果上传失败，不会归档或删除任何文件

### 数据保留
- **本地备份**：所有原始文件都将无限期保存在 `{workspace_root}/archive/` 目录中
- **远程存储**：上传的数据将按照 Honcho 的数据保留政策进行存储（详见 https://honcho.dev/privacy）
- **自托管控制**：如果使用自托管的 Honcho，您可以控制所有数据的保留策略

### 开源信息
- **Honcho SDK**：开源代码位于 https://github.com/plastic-labs/honcho
- **插件代码**：安装后可在 `~/.openclaw/extensions/openclaw-honcho` 中找到
- **本操作**：您正在查看完整的操作说明——没有任何隐藏的行为或设置