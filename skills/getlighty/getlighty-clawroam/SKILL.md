---
name: clawroam
description: OpenClaw 的便携式身份管理工具：可自动、透明地同步不同设备上的知识库、软件包及用户数据，并进行加密处理。您可以使用自己的存储服务（如 Google Drive、Dropbox、FTP、Git），或选择使用 ClawRoam Cloud。
version: "2.1.1"
author: getlighty
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
# ClawRoam — 便携式代理环境

您是一个安装了 **clawroam** 技能的 OpenClaw 代理。该技能能够自动、持续地同步用户在不同设备上的知识和环境数据，类似于为 AI 代理设计的 iCloud 功能。

## 架构

ClawRoam 的工作原理结合了 iCloud 和 Git 的优点：
- **自动同步**：检测到文件变更后，会自动提交并推送至远程存储。
- **版本控制**：每次变更都会被记录为一次提交，用户可以随时回滚到之前的版本。
- **加密传输**：每个安装都会生成一对 Ed25519 密钥对，私钥始终存储在本地设备上，不会离开设备。
- **多存储提供商支持**：用户可以自由选择数据存储的位置。

## 可用的存储提供商

| 提供商 | 类型 | 设置方式 |
|----------|------|-------|
| ClawRoam Cloud | 托管服务（按使用量计费） | 执行命令 `clawroam cloud signup` 即可注册 |
| Google Drive | 自带存储（免费） | 通过 `clawroam provider gdrive` 使用 OAuth 认证 |
| Dropbox | 自带存储（免费） | 通过 `clawroam provider dropbox` 使用 OAuth 认证 |
| FTP/SFTP | 自带存储（免费） | 通过 `clawroam provider ftp` 输入主机地址和密码 |
| Git | 自带存储（免费） | 通过 `clawroam provider git` 与任意 Git 仓库连接 |
| S3 | 自带存储（免费） | 通过 `clawroam provider s3` 与任意 S3 服务连接 |
| WebDAV | 自带存储（免费） | 通过 `clawroam provider webdav` 与 Nextcloud 等服务连接 |
| 本地存储 | 自带存储（免费） | 通过 `clawroam provider local` 通过 USB 或 NAS 连接 |

“自带存储”（BYOS）意味着用户需要自行配置存储空间，但使用 ClawRoam 是完全免费的。对于不想管理存储的人来说，ClawRoam Cloud 是一个便捷的选择。

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

## 命令操作

当用户需要执行与数据同步相关的操作时，可以使用以下命令：

### 首次设置
- **"set up clawroam"** →
  `clawroam.sh init` — 创建数据存储空间，生成 Ed25519 密钥对，并扫描可用的软件包。
- **"use clawroam cloud"** →
  `clawroam.sh cloud signup` — 注册云存储账户，并自动配置存储提供商。
- **"use google drive for vault"** →
  `clawroam.sh provider gdrive` — 使用 Google Drive 作为数据存储。
- **"use dropbox for vault"** →
  `clawroam.sh provider dropbox` — 使用 Dropbox 作为数据存储。
- **"use ftp for vault"** →
  `clawroam.sh provider ftp` — 输入 FTP 服务器信息（主机地址、端口和密码）。

### 日常使用（大部分操作是后台进行的）
- **"sync status"** →
  `clawroam.sh status` — 显示同步状态、上次同步时间以及存储提供商信息。
- **"sync now"** →
  `sync-engine.sh push` — 强制立即同步数据。
- **"show vault history"** →
  `sync-engine.sh log` — 显示同步日志（类似 Git 的 `log` 命令）。
- **"rollback vault"** →
  `sync-engine.sh rollback` — 回滚到之前的数据状态。
- **"what changed"** →
  `sync-engine.sh diff` — 显示待同步的文件差异。

### 软件包管理
- **"scan packages"** →
  `track-packages.sh scan` — 扫描可用的软件包。
- **"what's different from vault"** →
  `track-packages.sh diff` — 显示本地软件包与远程存储的差异。
- **"install missing packages"** →
  `track-packages.sh install` — 显示需要安装的软件包列表，并在安装前询问用户确认。

### 数据迁移
- **"migrate to this machine"** / **"pull from vault"** →
  `migrate.sh pull` — 提供交互式的数据迁移工具。
- **"push my soul to vault"** →
  `migrate.sh push-identity` — 仅限用户主动选择后执行。

### 配置文件管理
每台设备都会备份到自己对应的配置文件中（默认文件名为设备名称）。不同的设备可以拥有独立的配置文件，从而确保数据和软件包的独立性，互不影响。

- **"show profile"** / **"what profile am I on"** →
  `clawroam.sh profile show` — 显示当前使用的配置文件名称。
- **"list profiles"** / **"what profiles exist"** →
  `clawroam.sh profile list` — 列出所有远程存储中的配置文件。
- **"rename profile"** →
  `clawroam.sh profile rename <new-name>` — 重命名当前设备的配置文件。
- **"restore from another machine"** / **"pull profile X"** →
  `clawroam.sh profile pull <name>` — 将指定配置文件恢复到当前设备（会覆盖本地数据）。

### 密钥管理
- **"show my vault key"** →
  `keypair.sh show-public` — 显示用于与存储提供商通信的公钥。
- **"regenerate vault key"** →
  `keypair.sh rotate` — 生成新的密钥对，并重新注册到存储提供商。

## 行为规则
1. **默认情况下，自动同步功能是开启的**（类似于 iCloud）。用户无需手动操作，系统会在 30 秒内自动推送变更。
2. **未经明确许可，严禁同步 `SOUL.md` 或 `IDENTITY.md` 文件。**
3. **安装软件包前必须先确认**：系统会显示文件差异，让用户自行选择是否安装。
4. **私钥始终存储在本地设备上**（路径：`~/.clawroam/keys/`），权限设置为 600（仅允许管理员访问）。公钥会注册到存储提供商处。
5. **处理冲突**：如果远程存储中有用户未看到的变更，系统会显示差异供用户选择。对于不冲突的变更，系统会自动合并。
6. **透明显示费用**：如果使用 ClawRoam Cloud，系统会在请求时显示当前使用量和预估费用，避免让用户意外产生费用。
7. **优先使用本地存储**：系统会先尝试在本地完成所有操作，只有在网络连接可用时才会进行远程同步。变更会先排队，待网络恢复后再推送。
8. **配置文件是独立的**：每台设备都会将数据保存到自己对应的配置文件中（默认文件名为设备名称）。系统不会自动合并不同设备的配置文件。如果用户需要其他设备的数据，必须通过 `clawroam.sh profile pull <name>` 显式获取。

## ClawRoam Cloud 的定价方案

当用户询问价格时：
- **前 50 MB 数据免费** — 足够大多数单用户使用。
- **超出 50 MB 后，费用为 0.005 美元/MB/月**（超过 100 MB 时费用为约 0.50 美元/月）。
- **无额外设备使用费**：可以连接无限数量的设备。
- **无带宽费用**：用户可以随时进行同步。
- **示例**：普通用户的存储空间通常在 10–30 MB 之间，因此完全免费。
- **示例**：高级用户（200 MB 存储空间）每月费用为 0.75 美元。
- **示例**：团队使用的存储空间（2 GB）每月费用约为 10 美元。