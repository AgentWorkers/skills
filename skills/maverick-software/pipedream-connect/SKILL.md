---
name: pipedream-connect
description: 通过 Pipedream，您可以利用托管的 OAuth 机制连接 2,000 多个 API。该解决方案还提供了与 OpenClaw Gateway 仪表板的完整 UI 集成，并支持每个代理应用程序的独立管理（即每个代理应用程序的设置和权限可以单独配置）。
metadata: {"openclaw":{"emoji":"🔌","requires":{"bins":["mcporter"],"openclaw":">=2026.1.0"},"category":"integrations"}}
---
# Pipedream Connect

通过 Pipedream，您可以将 AI 代理连接到 2,000 多个 API，并使用托管的 OAuth 进行身份验证。每个代理都会获得自己独立的应用连接和 OAuth 令牌。

## 新功能（2026-03-01 v1.3.0）

- **每个代理的应用连接** — 应用连接现在位于 “Agents” → [Agent] → “Tools” → “Pipedream” 下。
- **“Global” 标签页仅用于存储凭证** — “Pipedream” 标签页现在仅用于存储平台认证信息（客户端 ID/密钥/项目 ID）。
- **外部用户 ID 默认为代理的名称** — 例如 `main`、`scout-monitor`（而非 UUID）。
- **实时连接的应用** — 刷新操作会查询 Pipedream API 以获取当前连接的应用列表。
- **开发模式警告** — 当代理在开发模式下运行时，Pipedream 面板会显示警告。
- **新增 RPC 方法**：`pipedream.connect`、`pipedream.disconnect`、`pipedream.test`（这些方法针对每个代理，需要使用 `agentId` 和 `appSlug` 参数）。

## 新功能（v1.3.0）——基于密钥库（Vault）的凭证管理

- **`clientId` 和 `clientSecret` 现在存储在 `~/.openclaw/secrets.json` 文件中**（OpenClaw 密钥库），不再以明文形式保存在 `pipedream-credentials.json` 中。
- `PIPEDREAM_CLIENT_SECRET` 从 `mcporter.json` 环境变量中移除——客户端密钥永远不会被写入 `mcporter.json` 配置文件。
- **自动迁移**：升级后首次启动网关时，现有的 `pipedream-credentials.json` 中的凭证会自动迁移到密钥库，并从该文件中删除。
- **令牌刷新脚本** 现在会首先从密钥库中读取凭证（如果密钥库不存在，则会回退到 `credentials.json` 或 `mcporter.json）。
- `pipedream-credentials.json` 现在仅包含非敏感信息：`projectId`、`environment`、`externalUserId`。

## 架构

```
Global Pipedream Tab
  └── Platform credentials (Client ID, Secret, Project ID, Environment)
  └── Agent quick-links table (→ navigate to per-agent config)

Agents → [Agent] → Tools → Pipedream
  └── External User ID (defaults to agent slug)
  └── Connected Apps (live from Pipedream API)
  └── Available Apps grid + Browse All Apps modal
  └── Manual slug entry
```

## 先决条件

1. **拥有 Pipedream 账户** — [pipedream.com](https://pipedream.com)
2. 安装 `mcporter`：`npm install -g mcporter`
3. 使用 OpenClaw Gateway 的 v2026.1.0 或更高版本。

## 设置步骤

### 第 1 步：创建 OAuth 客户端和项目

1. 访问 [pipedream.com/settings/api](https://pipedream.com/settings/api) → 点击 “New OAuth Client”。
2. 复制 “客户端 ID” 和 “客户端密钥”。
3. 访问 [pipedream.com/projects](https://pipedream.com/projects) 并创建一个项目。
4. 复制 “项目 ID”（格式为 `proj_...`）。

### 第 2 步：配置平台凭证

1. 打开 OpenClaw 仪表板 → “Pipedream” 标签页 → 点击 “Configure”。
2. 输入客户端 ID、客户端密钥和项目 ID。
3. 将 “环境” 设置为 “production”（而非开发环境——开发环境的令牌有效期较短，且速率限制较低）。
4. 点击 “Save Credentials”（保存凭证）。

### 第 3 步：为每个代理配置应用连接

1. 转到 “Agents” → [Agent] → “Tools” → “Pipedream”。
2. 核对 “外部用户 ID”（默认为代理的名称，例如 `main`）。
3. 点击网格中的任意应用进行连接操作——系统会在弹出窗口中完成 OAuth 验证。
4. OAuth 验证完成后，点击 “↻ Refresh” 以查看应用是否已成功添加到 “Connected Apps” 列表中。

### 第 4 步：建议定期刷新令牌

```bash
# Cron job — runs every 45 minutes
(crontab -l 2>/dev/null; echo "*/45 * * * * /usr/bin/python3 $HOME/openclaw/skills/pipedream-connect/scripts/pipedream-token-refresh.py >> $HOME/openclaw/logs/pipedream-cron.log 2>&1") | crontab -
```

## 每个代理的独立性

每个代理使用独立的 `external_user_id`：

| 代理 | 外部用户 ID | Pipedream 身份信息 |
|-------|-----------------|-------------------|
| `main` | `main` | 独立的 OAuth 令牌 |
| `scout-monitor` | `scout-monitor` | 独立的 OAuth 令牌 |
| `scout-spark` | `scout-spark` | 独立的 OAuth 令牌 |

相关配置文件存储在：`~/.openclaw/workspace/config/integrations/pipedream/{agentId}.json`。

**外部用户 ID 默认为代理的名称。** 可在 “Agents” → “Tools” → “Pipedream” 中进行修改。

## RPC（远程过程调用）参考

### 全局（凭证相关）

| RPC | 参数 | 说明 |
|-----|--------|-------------|
| `pipedream.status` | — | 获取全局凭证状态及代理信息 |
| `pipedream.saveCredentials` | `clientId, clientSecret, projectId, environment` | 保存平台凭证 |
| `pipedream.getToken` | — | 获取/刷新平台 OAuth 访问令牌 |
| `pipedream.getConnectUrl` | `agentId, appSlug` | 获取用户和应用的 OAuth 连接 URL |
| `pipedream.connectApp` | `agentId, appSlug` | 完成应用连接并更新 `mcporter` 配置 |
| `pipedream.disconnectApp` | `agentId, appSlug` | 断开应用连接并从 `mcporter` 中删除该应用 |
| `pipedream.refreshToken` | `agentId?, appSlug?` | 刷新令牌（全部或特定代理/应用的令牌） |
| `pipedream.activate` | `agentId, appSlug` | 激活应用（如果应用尚未存在于 `mcporter` 中则进行添加） |

### 每个代理相关的 RPC

| RPC | 参数 | 说明 |
|-----|--------|-------------|
| `pipedream.agent.status` | `agentId` | 从 API 获取代理配置及实时连接的应用列表 |
| `pipedream.agent.save` | `agentId, externalUserId` | 保存代理的配置信息 |
| `pipedream.agent.delete` | `agentId` | 删除代理的配置信息 |
| `pipedream.connect` | `agentId, appSlug` | 获取代理的 OAuth 连接 URL |
| `pipedream.disconnect` | `agentId, appSlug` | 断开应用连接并从 `mcporter` 中删除该应用 |
| `pipedream.test` | `agentId, appSlug` | 测试应用的连接状态 |

## 使用已连接的应用

```bash
# Gmail (agent: main → externalUserId: main)
mcporter call pipedream-main-gmail.gmail-find-email \
  instruction="Find unread emails from today"

# Google Calendar (agent: scout-monitor)
mcporter call pipedream-scout-monitor-google-calendar.google-calendar-find-event \
  instruction="Find events for tomorrow"
```

服务器名称遵循以下格式：`pipedream-{externalUserId}-{appSlug}`

## 环境设置：开发环境 vs 生产环境

⚠️ **请使用生产环境** 进行实际工作：
- 开发环境的令牌有效期较短，且速率限制较低。
- 设置方法：在 “Pipedream” 标签页 → “Edit Credentials” → “Environment” → 选择 “production”。
- 当代理在开发模式下运行时，Pipedream 面板会显示警告。

## 安全性

| 行为 | 详细说明 |
|----------|--------|
| **clientId** | 存储在 `~/.openclaw/secrets.json` 文件中（使用密钥库进行加密，加密强度为 0600） |
| **clientSecret** | 同样存储在 `~/.openclaw/secrets.json` 文件中（使用密钥库进行加密）——绝不会以明文形式保存在配置文件中 |
| 非敏感配置信息 | 存储在 `~/.openclaw/workspace/config/pipedream-credentials.json` 中（仅包含 `projectId`、`environment`、`externalUserId`） |
| 代理配置信息 | 存储在 `~/.openclaw/workspace/config/integrations/pipedream/{agentId}.json` 中 |
| 访问令牌（JWT） | 以短期令牌的形式存储在 `mcporter.json` 的 `Authorization` 头部——每 45 分钟更新一次 |
- **注意**：`PIPEDREAM_CLIENT_SECRET` 绝不会被写入 `mcporter.json` 文件中 |
- 外部 API 调用地址：`api.pipedream.com`、`remote.mcp.pipedream.net` |
- **自动迁移**：升级后首次启动网关时，现有的明文凭证会自动迁移到密钥库中。

## 故障排除

- **OAuth 验证后应用未显示在列表中**：点击 “↻ Refresh” 以重新查询连接状态。
- 出现 “unknown method: pipedream.connect” 错误：重新构建并重启网关：`pnpm build && openclaw gateway restart`。
- **未配置 Pipedream 凭证**：请先在全局 “Pipedream” 标签页中设置凭证。
- 开发环境警告：在 “Pipedream” 标签页中修改凭证设置，并将环境设置为 “production” 后保存。
- 令牌过期：设置定时任务（例如每 45 分钟刷新一次令牌），或再次点击 “Connect” 以重新授权。

## 支持资源

- **ClawHub**：[clawhub.ai/skills/pipedream-connect](https://clawhub.ai/skills/pipedream-connect)
- **Pipedream 文档**：[pipedream.com/docs](https://pipedream.com/docs)
- **MCP 应用**：[mcp.pipedream.com](https://mcp.pipedream.com)
- **OpenClaw Discord 频道**：[discord.com/invite/clawd](https://discord.com/invite/clawd)

## 参考文件

| 文件 | 用途 |
|------|---------|
| `reference/pipedream-backend.ts` | 网关的 RPC 处理逻辑（所有与 Pipedream 相关的方法） |
| `reference/pipedream-views.ts` | 全局 “Pipedream” 标签页的用户界面代码 |
| `reference/pipedream-controller.ts` | 全局标签页的状态管理逻辑 |
| `reference/agent-pipedream-views.ts` | 代理级别的 Pipedream 面板用户界面代码 |
| `reference/agent-pipedream-controller.ts` | 代理级别的状态管理逻辑 |
| `reference/README.md` | 参考文件说明 |
| `scripts/` | 用于刷新令牌和执行其他辅助操作的脚本 |