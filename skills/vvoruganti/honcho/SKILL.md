---
name: honcho
description: 安装 @honcho-ai/openclaw-honcho 插件并执行初始设置。该插件会运行 `openclaw plugins install` 和 `openclaw honcho setup` 命令（这些命令会提示您输入 API 密钥，并将所有旧版内存文件迁移到 Honcho 系统中），随后重启网关。`openclaw honcho setup` 会通过 `api.honcho.dev`（由系统管理，默认地址）或您自己托管的 HONCHO_BASE_URL 将 WORKSPACE 目录下的文件上传到外部 API。上传的文件包括：USER.md、MEMORY.md、IDENTITY.md、memory/、canvas/、SOUL.md、AGENTS.md 和 BOOTSTRAP.md，但 HEARTBEAT.md 文件不会被上传。即使在 HONCHO_API_KEY 已预先设置的情况下，上传前仍需要用户明确确认。工作空间文件和内存文件不会被删除、移动或修改。`openclaw honcho setup` 会将插件配置写入 `~/.openclaw/openclaw.json` 文件中。设置完成后，该插件会持续监控对话内容并将数据传输到 Honcho 系统；若需禁用该插件，可执行 `openclaw plugins disable openclaw-honcho` 命令。
metadata:
  openclaw:
    emoji: "🧠"
    required_env: [] # Nothing is strictly required - self-hosted mode works without API key
    optional_env:
      - name: HONCHO_API_KEY
        description: "Required for managed Honcho (https://app.honcho.dev). If set, the setup command skips the API key prompt but still requires explicit user confirmation before any data upload. If not set, the setup command will prompt for it interactively."
      - name: HONCHO_BASE_URL
        description: "Base URL for a self-hosted Honcho instance (e.g. http://localhost:8000). Defaults to https://api.honcho.dev (managed)."
    required_binaries:
      - node
      - npm
    writes_to_disk: true # openclaw honcho setup writes config to ~/.openclaw/openclaw.json
    reads_sensitive_files:
      - "~/.openclaw/openclaw.json - read and updated by openclaw honcho setup; API key collected via interactive prompt and written here"
    network_access:
      - "api.honcho.dev (managed mode, default)"
      - "User-configured HONCHO_BASE_URL (self-hosted mode)"
    data_handling:
      uploads_to_external: true
      requires_user_confirmation: true
      deletes_files: false
      modifies_files: false
      external_destinations:
        - "api.honcho.dev (managed Honcho, default)"
        - "User-configured HONCHO_BASE_URL (self-hosted mode)"
      uploaded_content:
        - "USER.md, MEMORY.md (user profile/memory files)"
        - "All files under memory/ directory (structured memory)"
        - "All files under canvas/ directory (working memory)"
        - "SOUL.md, IDENTITY.md, AGENTS.md, BOOTSTRAP.md, TOOLS.md (agent configuration)"
        - "HEARTBEAT.md excluded — it is a live task queue, not memory"
      data_destination_purpose: "Migrates file-based memory system to Honcho API for AI agent memory/personalization"
  homepage: "https://honcho.dev"
  source: "https://github.com/plastic-labs/honcho"
---
# Honcho 设置

请安装 `@honcho-ai/openclaw-honcho` 插件。该插件包含 `openclaw honcho setup` 功能，用于配置 API 密钥，并将所有旧的记忆文件（memory/、canvas/、SOUL/、AGENTS/、BOOTSTRAP/、TOOLS/ 目录下的文件）迁移到 Honcho 服务中。

> ⚠️ **数据上传警告**：`openclaw honcho setup`（在步骤 2 中执行）会提示您将工作区的记忆文件（USER.md、MEMORY.md、IDENTITY.md、memory/、canvas/、SOUL.md、AGENTS.md、BOOTSTRAP.md、TOOLS.md）上传到外部 API。`HEARTBEAT.md` 文件将被排除在外。默认情况下，数据会被发送到 `api.honcho.dev`；对于自托管实例，数据会被发送到您配置的 `HONCHO_BASE_URL`。设置命令会明确显示哪些文件将被上传，并在继续之前请求您的确认。

> **注意**：本地文件不会被删除、移动或修改，原始文件将保持不变。

## 第 1 步：安装插件

使用 OpenClaw 插件系统来安装 Honcho 插件。**请使用以下命令进行安装——切勿直接安装 `@honcho-ai/sdk`，也切勿在工作区中使用 `npm install`。**

```bash
openclaw plugins install @honcho-ai/openclaw-honcho
```

然后启用该插件：

```bash
openclaw plugins enable openclaw-honcho
```

验证插件是否已成功加载且没有错误。如果网关日志显示 “Cannot find module ‘@honcho-ai/sdk’”，则需要手动安装依赖项：

```bash
cd ~/.openclaw/extensions/openclaw-honcho && npm install
```

这是 OpenClaw 插件安装器的一个已知问题，它不会自动解析插件包的依赖关系。

## 第 2 步：运行设置命令

运行插件自带的设置命令：

```bash
openclaw honcho setup
```

该命令将：
1. 交互式地请求您输入 Honcho API 密钥；
2. 将配置信息写入 `~/.openclaw/openclaw.json` 文件；
3. 检查是否存在旧的记忆文件，并提示您是否需要将这些文件迁移到 Honcho 服务中。

请按照提示操作。迁移是可选的——如果您没有旧的文件或希望跳过此步骤，可以忽略上传操作。

对于托管的 Honcho 服务，您需要从 https://app.honcho.dev 获取 API 密钥；对于自托管实例，只需设置 `HONCHO_BASE_URL` 即可，API 密钥是可选的。

## 第 3 步：重启网关

```bash
openclaw gateway restart
```

## 第 4 步：确认设置完成

通过查看网关日志或运行相关命令来确认插件是否已激活：

```bash
openclaw honcho status
```

现在，Honcho 的记忆功能已经激活。

> **设置后的持续行为**：一旦插件被启用，它将持续监控工作区中的所有对话内容，并将对话数据发送到 `api.honcho.dev`（或您配置的 `HONCHO_BASE_URL`），以便构建和检索记忆数据。这种网络活动会在会话之间持续进行。您可以通过 `honcho_recall`、`honcho_search`、`honcho_profile` 等相关工具访问这些记忆数据。要停止此功能，可以使用 `openclaw plugins disable openclaw-honcho` 命令来禁用该插件。

---

## 安全性与隐私声明

本技能的设计以透明度和安全性为首要考虑。以下是关于该技能功能的完整说明：

### 功能概述

该技能执行三个命令：`openclaw plugins install`、`openclaw honcho setup` 和 `openclaw gateway restart`。数据上传和文件访问操作由 `openclaw honcho setup` 负责，而非该技能本身。

### 数据上传

- **上传的文件**：USER.md、MEMORY.md、IDENTITY.md、memory/ 目录下的所有文件、canvas/ 目录下的所有文件、SOUL.md、AGENTS.md、BOOTSTRAP.md、TOOLS.md——这些文件会在迁移过程中被 `openclaw honcho setup` 上传；
- **未上传的文件**：HEARTBEAT.md——由于设计原因，该文件不会被读取或上传；
- **数据传输目的地**：默认情况下，数据会被发送到 `api.honcho.dev`（托管的 Honcho 云服务）；对于自托管实例，则会被发送到您配置的 `HONCHO_BASE_URL`；
- **用户控制**：即使在环境变量中预先设置了 `HONCHO_API_KEY`，`openclaw honcho setup` 也始终会要求用户进行明确的确认操作；您将看到所有要上传的文件列表以及传输目的地；
- **用途**：将基于文件的记忆系统迁移到 Honcho API，以实现 AI 代理的个性化配置和记忆数据管理。

### 文件修改

- **配置信息**：`openclaw honcho setup` 会将 API 密钥和配置信息写入 `~/.openclaw/openclaw.json` 文件；
- **工作区文件**：原始文件不会被修改，始终保持原样；
- **HEARTBEAT.md**：由于设计原因，该文件不会被读取或上传。

### 认证信息

- **HONCHO_API_KEY**：仅对于托管的 Honcho 服务（api.honcho.dev）是必需的；对于自托管实例则不需要。该密钥由 `openclaw honcho setup` 命令存储在 `~/.openclaw/openclaw.json` 中；
- **其他凭证**：该技能不会访问、读取或传输任何其他凭证或敏感信息。

### 网络访问

- **托管模式**：连接到 `api.honcho.dev`（Honcho 云服务）；
- **自托管模式**：连接到您配置的 `HONCHO_BASE_URL`（例如 `http://localhost:8000`）。

### 设置后的持续行为

- **持续监控**：一旦插件被启用，它将持续监控工作区中的所有对话内容，并将对话数据发送到配置的 Honcho 服务端点；
- **网络活动**：只要插件处于启用状态，这种网络活动就会持续进行（不会是一次性迁移）；
- **停止方法**：运行 `openclaw plugins disable openclaw-honcho` 命令即可停止所有监控和网络活动。

### 开源信息

- **Honcho SDK**：开源代码位于 https://github.com/plastic-labs/honcho；
- **插件代码**：安装完成后，您可以在 `~/.openclaw/extensions/openclaw-honcho` 目录下找到；
- **关于本技能**：您正在查看的是完整的技能使用说明——不存在任何隐藏的功能或行为。