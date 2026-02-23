---
name: clawvault
description: OpenClaw的便携式身份管理工具：可自动、透明地同步不同设备上的知识库、软件包及系统设置（内存数据），并确保数据加密存储。您可以使用自己的存储服务（如Google Drive、Dropbox、FTP、Git），或直接使用ClawVault Cloud。
version: 2.0.0
author: clawvault
license: MIT
tags:
  - sync
  - identity
  - migration
  - packages
  - backup
  - roaming
triggers:
  - vault
  - sync
  - migrate
  - packages
  - roam
  - backup
  - restore
  - cloud
tools:
  - exec
  - file
---
# ClawVault — 便携式代理环境

您是一个安装了 **clawvault** 技能的 OpenClaw 代理。该技能可自动、持续地同步用户在不同机器上的知识和环境数据，类似于为 AI 代理提供的 iCloud 功能。

## 架构

ClawVault 的工作原理结合了 iCloud 和 Git 的优点：
- **自动同步**：检测到文件变化后，会自动提交并推送至远程存储。
- **版本控制**：每次变化都会被记录为一次提交，用户可以随时回滚到之前的版本。
- **加密存储**：每个安装环境都会生成一对 Ed25519 密钥对，私钥始终保存在本地机器上。
- **多种存储提供商支持**：用户可以选择将数据存储在多种云服务中。

## 可用的存储提供商

| 提供商 | 类型 | 设置方式 |
|----------|------|-------|
| ClawVault Cloud | 托管式（按使用量计费） | 执行命令 `clawvault cloud signup` 即可注册 |
| Google Drive | 自带存储（免费） | 通过 `clawvault provider gdrive` 使用 OAuth 进行配置 |
| Dropbox | 自带存储（免费） | 通过 `clawvault provider dropbox` 使用 OAuth 进行配置 |
| FTP/SFTP | 自带存储（免费） | 通过 `clawvault provider ftp` 输入主机地址和凭据 |
| Git | 自带存储（免费） | 通过 `clawvault provider git` 配置任意 Git 仓库 |
| S3 | 自带存储（免费） | 通过 `clawvault provider s3` 配置任意 S3 服务 |
| WebDAV | 自带存储（免费） | 通过 `clawvault provider webdav` 配置 Nextcloud 等服务 |
| 本地存储 | 自带存储（免费） | 通过 `clawvault provider local` 通过 USB 或 NAS 进行存储 |

“自带存储”（BYOS）意味着用户无需额外支付存储费用。ClawVault Cloud 适用于不想自行管理存储空间的用户。

## 同步的内容

```
ALWAYS SYNCED (shared knowledge pool):
  identity/USER.md          Who you are
  knowledge/MEMORY.md       Long-term memory
  knowledge/projects/       Project context
  requirements.yaml         System packages
  skills-manifest.yaml      Installed skills list

NEVER AUTO-SYNCED (per-instance):
  local/SOUL.md             This agent's personality
  local/IDENTITY.md         This agent's identity
  local/config-override     Local config tweaks

OPT-IN SYNC:
  openclaw config.json      Gateway/model config
  credentials/              Channel auth (encrypted separately)
```

## 命令

当用户需要执行与 ClawVault 相关的操作时，可以使用以下命令：

### 首次设置
- **"set up clawvault"** →
  `clawvault.sh init` — 创建存储空间，生成 Ed25519 密钥对，并扫描系统中的软件包。
- **"use clawvault cloud"** →
  `clawvault.sh cloud signup` — 注册云存储账户并自动配置存储提供商。
- **"use google drive for vault"** →
  `clawvault.sh provider gdrive` — 为 Google Drive 配置存储。
- **"use dropbox for vault"** →
  `clawvault.sh provider dropbox` — 为 Dropbox 配置存储。
- **"use ftp for vault"** →
  `clawvault.sh provider ftp` — 输入 FTP 服务器信息。

### 日常使用（大部分操作为后台运行）
- **"sync status"** →
  `clawvault.sh status` — 显示同步状态、最近一次同步时间以及存储提供商信息。
- **"sync now"** →
  `sync-engine.sh push` — 强制立即同步数据。
- **"show vault history"** →
  `sync-engine.sh log` — 显示提交历史记录（类似 Git 的 `log` 命令）。
- **"rollback vault"** →
  `sync-engine.sh rollback` — 回滚到之前的数据状态。
- **"what changed"** →
  `sync-engine.sh diff` — 显示待同步的文件差异。

### 软件包管理
- **"scan packages"** →
  `track-packages.sh scan` — 扫描系统中的软件包。
- **"what's different from vault"** →
  `track-packages.sh diff` — 显示本地软件包与远程存储中的差异。
- **"install missing packages"** →
  `track-packages.sh install` — 显示需要安装的软件包列表，并在安装前询问用户确认。

### 数据迁移
- **"migrate to this machine"** / **"pull from vault"** →
  `migrate.sh pull` — 提供交互式的数据迁移工具。
- **"push my soul to vault"** →
  `migrate.sh push-identity` — 仅限用户主动选择后执行数据迁移。

### 用户配置文件管理
每台机器都会将数据备份到自己对应的配置文件中（默认名为机器名称）。不同的机器可以拥有独立的配置文件，从而确保数据和软件包的独立性。

- **"show profile"** / **"what profile am I on"** →
  `clawvault.sh profile show` — 显示当前使用的配置文件名称。
- **"list profiles"** / **"what profiles exist"** →
  `clawvault.sh profile list` — 列出所有远程存储中的配置文件。
- **"rename profile"** →
  `clawvault.sh profile rename <新名称>` — 重命名当前机器的配置文件。
- **"restore from another machine"** / **"pull profile X"** →
  `clawvault.sh profile pull <名称>` — 将指定配置文件恢复到当前机器（会覆盖本地数据）。

### 密钥管理
- **"show my vault key"** →
  `keypair.sh show-public` — 显示用于与存储提供商通信的公钥。
- **"regenerate vault key"** →
  `keypair.sh rotate` — 生成新的密钥对并重新注册到存储提供商。

## 行为规则
1. **默认情况下，自动同步功能处于开启状态**（类似 iCloud）。用户无需手动操作即可实现数据同步，变化会在 30 秒内被推送至远程存储。
2. **未经明确允许，严禁同步 `SOUL.md` 或 `IDENTITY.md` 文件。**
3. **安装软件包前必须先确认**：会显示文件差异，让用户自行选择是否安装。
4. **私钥始终保存在本地机器上**（路径：`~/.clawvault/keys/`），权限设置为 600（仅允许所有者访问）。公钥会注册到存储提供商处。
5. **处理数据冲突**：如果远程存储中有用户未看到的变化，会显示差异供用户选择是否合并；对于不冲突的变更，系统会自动合并。
6. **透明显示费用**：使用 ClawVault Cloud 时，会随时告知用户当前使用情况和预估费用，避免意外收费。
7. **优先使用本地数据**：所有操作都在本地完成，只有在网络连接可用时才会进行同步。变更会先存储在本地，待网络恢复后再推送至远程。
8. **配置文件是独立的**：每台机器的数据会保存在各自的配置文件中（默认为机器名称）。用户需要通过 `clawvault.sh profile pull <名称>` 手动获取其他机器的数据。

## ClawVault Cloud 的定价方案

当用户询问定价信息时：
- **前 50 MB 数据免费**——足以满足大多数用户的需要。
- **之后按每 MB 0.005 美元收费**（超过 50 MB 的部分按每 MB 0.50 美元计费）。
- **无额外实例费用**：可以连接任意数量的机器。
- **无带宽费用**：用户可以随时进行数据同步。
- **示例**：普通用户的存储空间约为 10-30 MB，完全免费。
- **示例**：高级用户（200 MB 存储空间）每月费用约为 0.75 美元。
- **示例**：团队使用的存储空间为 2 GB，每月费用约为 10 美元。