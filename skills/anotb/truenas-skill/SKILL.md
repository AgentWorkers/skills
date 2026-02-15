---
name: truenas-skill
description: >
  Manage TrueNAS SCALE via API. Check pool health, manage datasets and snapshots,
  monitor alerts, control services, manage apps, orchestrate Dockge container stacks,
  and manage bookmarks. Use when the user asks about their NAS, storage, backups,
  containers, bookmarks, or homelab services.
license: MIT
homepage: https://github.com/anotb/truenas-skill
compatibility: Requires curl, jq, and Node.js 18+. Network access to TrueNAS instance.
metadata: {"author": "anotb", "version": "1.2.0", "openclaw": {"requires": {"env": ["TRUENAS_URL", "TRUENAS_API_KEY"], "bins": ["curl", "jq", "node"]}, "primaryEnv": "TRUENAS_API_KEY"}}
---

# TrueNAS SCALE 技能

通过 TrueNAS API 和 Dockge Socket.IO 来管理 TrueNAS SCALE 服务器及其应用程序。

## 设置

### 必需的环境变量

```
TRUENAS_URL       — TrueNAS base URL (e.g., https://10.0.0.5:444)
TRUENAS_API_KEY   — API key from TrueNAS UI → API Keys
```

### 可选：TLS 配置

```
TRUENAS_VERIFY_TLS  — Set to "1" to enforce TLS certificate validation (default: skip for self-signed certs)
```

### 可选：Dockge（Docker Compose UI）

```
DOCKGE_URL        — Dockge URL (e.g., http://10.0.0.5:5001)
DOCKGE_USER       — Dockge login username
DOCKGE_PASS       — Dockge login password
```

### 可选：Homelab 服务 API 密钥

有关每个服务的环境变量，请参阅 `references/` 目录。常见的环境变量包括：

```
SONARR_URL, SONARR_API_KEY           — TV show management
RADARR_URL, RADARR_API_KEY           — Movie management
PROWLARR_URL, PROWLARR_API_KEY       — Indexer management
OVERSEERR_URL, OVERSEERR_API_KEY     — Media request UI
PLEX_URL                             — Media server (no auth on LAN)
TAUTULLI_URL, TAUTULLI_API_KEY       — Plex analytics
QBITTORRENT_URL                      — Torrent client (no auth)
SABNZBD_URL, SABNZBD_API_KEY         — Usenet client
AUDIOBOOKSHELF_URL, AUDIOBOOKSHELF_API_KEY
NTFY_URL                             — Push notifications
SYNCTHING_URL, SYNCTHING_API_KEY     — File sync
N8N_URL, N8N_API_KEY                 — Workflow automation
NOCODB_URL, NOCODB_API_KEY           — Database
CHANGEDETECTION_URL, CHANGEDETECTION_API_KEY
CRAFTY_URL, CRAFTY_API_KEY           — Game servers
LAZYLIBRARIAN_URL, LAZYLIBRARIAN_API_KEY
METUBE_URL                           — YouTube downloader
KARAKEEP_URL, KARAKEEP_API_KEY       — Bookmarks with AI tagging
```

## API 注意事项

**必须使用 HTTPS：** TrueNAS 会自动吊销通过 HTTP 使用的 API 密钥。

> **REST API 已弃用通知：** REST API（`/api/v2.0/`）在 TrueNAS 25.04 中已被弃用，并在 26.04 中完全移除。请使用 WebSocket API（通过 `scripts/truenas-ws.mjs`）作为向后兼容的方法。下面的 REST 示例在 24.10 和 25.x 版本中仍然有效。

### REST API（旧版本）

```bash
curl -sk "$TRUENAS_URL/api/v2.0/[endpoint]" \
  -H "Authorization: Bearer $TRUENAS_API_KEY"
```

对于自签名证书，需要使用 `-k` 标志（这在家庭服务器中很常见）。

### WebSocket API（推荐使用）

WebSocket API 使用类似 DDP 的协议（Meteor 风格）。REST 路径会转换为点表示法：
`/api/v2.0/app` → `app.query`，`/api/v2.0/system/info` → `system.info`。

```javascript
// Connect: wss://<host>/websocket (rejectUnauthorized: false for self-signed)

// 1. Handshake
send: {"msg": "connect", "version": "1", "support": ["1"]}
recv: {"msg": "connected", "session": "..."}

// 2. Authenticate
send: {"id": "1", "msg": "method", "method": "auth.login_with_api_key", "params": ["API_KEY"]}
recv: {"id": "1", "msg": "result", "result": true}

// 3. Call methods
send: {"id": "2", "msg": "method", "method": "system.info", "params": []}
send: {"id": "3", "msg": "method", "method": "app.query", "params": []}
```

使用辅助脚本进行 WebSocket 调用：`node scripts/truenas-ws.mjs <方法> [params_json]`

## 安全注意事项

- **自签名证书：** 由于家庭服务器通常使用自签名证书，因此默认会跳过 TLS 验证（`curl -k`，`rejectUnauthorized: false`）。设置 `TRUENAS_VERIFY_TLS=1` 以强制进行严格的 TLS 验证。
- **API 密钥权限：** 尽可能使用只读或最低权限的 API 密钥。TrueNAS 允许您将密钥限制在特定的端点上。
- **凭据保持本地：** 所有环境变量都在运行时读取，并且仅发送到配置的服务端点。没有任何数据会被发送到外部。

## 核心操作

### 系统信息

```bash
curl -sk "$TRUENAS_URL/api/v2.0/system/info" -H "Authorization: Bearer $TRUENAS_API_KEY"
```

### 存储池状态

```bash
# All pools with health status
curl -sk "$TRUENAS_URL/api/v2.0/pool" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {name, healthy}'

# Or via WebSocket
node scripts/truenas-ws.mjs pool.query '[]'
```

API 会为每个存储池返回一个 `.healthy` 布尔值。如需更详细的状态信息，请查看完整的存储池对象。

### 活动警报

```bash
curl -sk "$TRUENAS_URL/api/v2.0/alert/list" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {level, formatted}'
```

### 运行中的服务

```bash
curl -sk "$TRUENAS_URL/api/v2.0/service" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | select(.state == "RUNNING") | .service'
```

## 数据集管理

### 列出数据集

```bash
curl -sk "$TRUENAS_URL/api/v2.0/pool/dataset" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {name, type, used: .used.parsed, available: .available.parsed}'
```

### 创建数据集

```bash
curl -sk -X POST "$TRUENAS_URL/api/v2.0/pool/dataset" \
  -H "Authorization: Bearer $TRUENAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "pool/path/new-dataset"}'
```

### 删除数据集

```bash
# Destructive — confirm with user first
curl -sk -X DELETE "$TRUENAS_URL/api/v2.0/pool/dataset/id/DATASET_ID" \
  -H "Authorization: Bearer $TRUENAS_API_KEY"
```

## 快照与复制

### 列出快照

```bash
# WebSocket (required on 25.10+, /api/v2.0/zfs/snapshot returns 404)
node scripts/truenas-ws.mjs zfs.snapshot.query '[]'
```

### 创建快照

```bash
node scripts/truenas-ws.mjs zfs.snapshot.create '[{"dataset": "pool/dataset", "name": "manual-YYYY-MM-DD"}]'
```

### 快照任务状态

```bash
curl -sk "$TRUENAS_URL/api/v2.0/pool/snapshottask" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {dataset, schedule, enabled}'
```

### 复制状态

```bash
curl -sk "$TRUENAS_URL/api/v2.0/replication" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {name, state: .state.state}'
```

## 应用程序管理

TrueNAS 应用程序是用于安装容器化服务的官方市场。

### 列出已安装的应用程序

```bash
curl -sk "$TRUENAS_URL/api/v2.0/app" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {name, state, version}'
```

### 检查更新

```bash
curl -sk "$TRUENAS_URL/api/v2.0/app" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | select(.upgrade_available) | .name'
```

### 安装/更新应用程序

请参阅 `references/app-installation.md` 以获取完整的安装指南，内容包括：
- 检查应用程序模板和存储要求
- 创建具有正确 ACL 的数据集
- 使用正确的存储映射进行安装
- 处理具有多个存储挂载的应用程序

### 应用程序状态

```bash
curl -sk "$TRUENAS_URL/api/v2.0/app?name=APP_NAME" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[0] | {name, state, portals}'
```

## Dockge（Docker Compose 堆栈）

Dockge 是一个用于管理不在 TrueNAS 应用程序目录中的 Docker Compose 堆栈的配套 UI。它使用 Socket.IO，而不是 REST。请使用提供的脚本。

### 先决条件

```bash
npm install   # in this skill's root directory
```

### 列出堆栈

```bash
node scripts/dockge-list.mjs
```

### 更新堆栈

```bash
# Update all running stacks
node scripts/dockge-update.mjs

# Update specific stacks
node scripts/dockge-update.mjs mystack1 mystack2
```

### Socket.IO 协议详情

Dockge 使用基于 WebSocket 的 Socket.IO 协议。

**状态代码：**
- 1 = 不活动/已退出
- 3 = 运行中
- 4 = 更新中

**关键事件：**
- `login` — 使用用户名/密码进行身份验证
- `stackList` — 获取所有堆栈（通过 `agent` 事件接收）
- `agent`, "", "updateStack", stackName — 触发拉取和重启

**注意：** 以 `ix-` 开头的堆栈是由 TrueNAS 管理的应用程序，更新时请跳过这些堆栈。

## 监控检查清单

运行以下命令以快速了解系统状态：

```bash
# Pool health
curl -sk "$TRUENAS_URL/api/v2.0/pool" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {name, healthy}'

# Active alerts
curl -sk "$TRUENAS_URL/api/v2.0/alert/list" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {level, formatted}'

# Running services
curl -sk "$TRUENAS_URL/api/v2.0/service" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | select(.state == "RUNNING") | .service'

# App updates available
curl -sk "$TRUENAS_URL/api/v2.0/app" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | select(.upgrade_available) | .name'

# Replication status
curl -sk "$TRUENAS_URL/api/v2.0/replication" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | {name, state: .state.state}'
```

## 家庭实验室服务

此技能包含常见家庭实验室服务类别的参考文件。每个文件涵盖了这些服务的 API 模式、环境变量以及通常与 TrueNAS 一起运行的服务的常见代理任务：

| 参考文件 | 服务 | 文件名 |
|-----------|----------|------|
| 媒体管理 | Overseerr, Sonarr, Radarr, Prowlarr, Plex, Tautulli | `references/media-management.md` |
| 应用程序安装 | TrueNAS 原生应用程序安装指南 | `references/app-installation.md` |
| 下载客户端 | qBittorrent, SABnzbd, FlareSolverr | `references/downloads.md` |
| 家庭实验室服务 | ntfy, Syncthing, n8n, NocoDB, ChangeDetection, Crafty | `references/homelab-services.md` |
| 书籍与媒体 | Audiobookshelf, LazyLibrarian, Calibre-Web, MeTube | `references/books-and-media.md` |
| 书签 | Karakeep（基于 AI 的书签管理器） | `references/bookmarks.md` |

当用户询问特定服务类别时，请加载相应的参考文件。

## 常见任务

### “检查 NAS 状态”

运行上述监控检查清单，总结存储池的状态、警报以及任何待处理的更新。

### “当前正在运行什么？”

```bash
# TrueNAS apps
curl -sk "$TRUENAS_URL/api/v2.0/app" -H "Authorization: Bearer $TRUENAS_API_KEY" \
  | jq '.[] | select(.state == "RUNNING") | .name'

# Dockge stacks (if configured)
node scripts/dockge-list.mjs
```

### “安装一个应用程序”

按照 `references/app-installation.md` 中的指南操作：
1. 检查应用程序模板的存储要求
2. 在应用程序存储池下创建数据集
3. 设置应用程序预设的 ACL
4. 使用正确的存储映射安装应用程序

### “创建快照”

```bash
node scripts/truenas-ws.mjs zfs.snapshot.create '[{"dataset": "pool/dataset", "name": "manual-snapshot-name"}]'
```

### “正在下载什么？”

请参阅 `references/downloads.md` 以获取 qBittorrent 和 SABnzbd 的 API 命令。

### “添加电影/节目”

请参阅 `references/media-management.md` 以了解 Overseerr 的请求工作流程。