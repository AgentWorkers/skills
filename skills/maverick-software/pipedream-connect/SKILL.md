---
name: pipedream-connect
description: 通过 Pipedream，您可以连接 2,000 多个 API，并使用托管的 OAuth 进行身份验证。该解决方案支持与 OpenClaw Gateway 仪表板的全面集成，同时实现每个代理应用程序的独立管理（即每个代理应用程序都有自己独立的认证和授权流程）。
metadata: {"openclaw":{"emoji":"🔌","category":"integrations","requires":{"bins":["mcporter"],"openclaw":">=2026.1.0"},"configPaths":["~/.openclaw/secrets.json","~/.openclaw/workspace/config/pipedream-credentials.json","~/.openclaw/workspace/config/integrations/pipedream/*.json","~/.openclaw/workspace/config/mcporter.json","~/.openclaw/logs/pipedream-*.log"],"capabilities":[{"id":"file.read","paths":["~/.openclaw/secrets.json","~/.openclaw/workspace/config/**"]},{"id":"file.write","paths":["~/.openclaw/secrets.json","~/.openclaw/workspace/config/**","~/.openclaw/logs/**"]},{"id":"network.http","domains":["api.pipedream.com","remote.mcp.pipedream.net","mcp.pipedream.com"]},{"id":"cron.manage","scope":"user-crontab","optional":true}],"installWarnings":["Optional cron setup creates persistent token-refresh behavior.","Skill reads/writes vault and mcporter config files containing sensitive tokens."],"securityNotes":"Client secrets are stored in OpenClaw vault (~/.openclaw/secrets.json). Access tokens may be written to mcporter Authorization headers and refreshed periodically."}}
---
# Pipedream Connect

通过 Pipedream，您可以将 AI 代理连接到 2,000 多个 API，并使用托管的 OAuth 进行身份验证。每个代理都会获得自己独立的 App 连接和 OAuth 令牌。

## 新功能（2026-03-10 v1.5.2）

- 在“浏览应用”界面中添加了按字母 A–Z 进行筛选的功能，便于快速查找应用。
- 结果摘要中添加了当前显示的字母指示器（例如：“Letter: Q”）。
- 改进了“浏览应用”界面中应用卡片的可读性（名称显示得更完整，减少了截断现象）。
- 更新了应用目录的引用快照以及与 CSP（Content Security Policy）的兼容性路径。

## 新功能（2026-03-10 v1.5.1）

- 为配置路径、功能、数据持久化及安全注意事项添加了明确的元数据说明。
- 清晰说明了数据持久化的行为（可选的 cron 令牌刷新）以及敏感文件的访问规则。
- 文档内容与 `~/.openclaw/` 目录下的实际路径保持一致。

## 新功能（2026-03-01 v1.3.0）

- **每个代理的应用连接**：应用连接信息现在位于 “代理” → [代理] → “工具” → “Pipedream” 下。
- “全局” 标签页仅用于存储凭证信息（Client ID/Secret/Project ID）。
- **外部用户 ID 默认为代理的名称**（例如：`main`、`scout-monitor`，而非 UUID）。
- **实时连接的应用**：会定期查询 Pipedream API 以获取当前连接的应用列表。
- **开发模式警告**：当代理处于开发模式时，界面会显示警告提示。
- 新增了以下 RPC 方法：`pipedream.connect`、`pipedream.disconnect`、`pipedream.test`（这些方法需要使用 `agentId` 和 `appSlug` 参数）。

## 新功能（v1.3.0）——基于密钥库（Vault）的安全机制

- `clientId` 和 `clientSecret` 现在存储在 `~/.openclaw/secrets.json` 文件中（使用 OpenClaw 的密钥库进行保护），不再以明文形式保存在 `pipedream-credentials.json` 中。
- `PIPEDREAM_CLIENT_SECRET` 从 `mcporter.json` 环境变量中移除，以避免将其写入配置文件。
- 升级后，系统会自动将现有的 `pipedream-credentials.json` 中的敏感信息迁移到密钥库中，并从该文件中删除这些信息。
- 令牌刷新脚本现在优先从密钥库中读取数据（在无法访问密钥库时才会回退到 `credentials.json` 和 `mcporter.json）。
- `pipedream-credentials.json` 文件仅包含非敏感字段：`projectId`、`environment`、`externalUserId`。

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

1. 拥有 Pipedream 账户：[pipedream.com](https://pipedream.com)
2. 安装 `mcporter`：`npm install -g mcporter`
3. 使用 OpenClaw Gateway 的 2026.1.0 或更高版本。

## 设置步骤

### 第一步：创建 OAuth 客户端和项目

1. 访问 [pipedream.com/settings/api](https://pipedream.com/settings/api)，然后点击 “新建 OAuth 客户端”。
2. 复制 “Client ID” 和 “Client Secret”。
3. 访问 [pipedream.com/projects](https://pipedream.com/projects)，创建一个项目，并复制 “Project ID”（格式为 `proj_...`）。

### 第二步：配置平台凭证

1. 打开 OpenClaw 仪表板，进入 “Pipedream” 标签页，然后点击 “配置”。
2. 输入 Client ID、Client Secret 和 Project ID。
3. 将 “环境” 设置为 “production”（而非开发环境，因为开发环境的令牌有效期较短且访问速率限制较低）。
4. 点击 “保存凭证”。

### 第三步：为每个代理配置应用连接

1. 进入 “代理” → [代理] → “工具” → “Pipedream”。
2. 确认 “外部用户 ID”（默认为代理的名称，例如 `main`）。
3. 点击网格中的任意应用进行连接操作，系统会弹出窗口完成 OAuth 验证。
4. OAuth 验证完成后，点击 “↻ 刷新” 以查看应用是否已添加到 “已连接的应用” 列表中。

### 第四步：建议定期刷新令牌

```bash
# Cron job — runs every 45 minutes
(crontab -l 2>/dev/null; echo "*/45 * * * * /usr/bin/python3 $HOME/openclaw/skills/pipedream-connect/scripts/pipedream-token-refresh.py >> $HOME/openclaw/logs/pipedream-cron.log 2>&1") | crontab -
```

## 每个代理的独立性

每个代理使用独立的 `external_user_id`：

| 代理名称 | 外部用户 ID | Pipedream 身份信息 |
|-------|-----------------|-------------------|
| `main` | `main` | 独立的 OAuth 令牌 |
| `scout-monitor` | `scout-monitor` | 独立的 OAuth 令牌 |
| `scout-spark` | `scout-spark` | 独立的 OAuth 令牌 |

相关配置文件存储在：`~/.openclaw/workspace/config/integrations/pipedream/{agentId}.json`。

**外部用户 ID 默认为代理的名称。** 可在 “代理” → “工具” → “Pipedream” 中进行修改。

## RPC 方法参考

### 全局（凭证相关）

| RPC 方法 | 参数 | 说明 |
|---------|--------|-------------|
| `pipedream.status` | — | 获取全局凭证状态及代理信息 |
| `pipedream.saveCredentials` | `clientId, clientSecret, projectId, environment` | 保存平台凭证 |
| `pipedream.getToken` | — | 获取/刷新平台 OAuth 访问令牌 |
| `pipedream.getConnectUrl` | `agentId, appSlug` | 获取用户和应用的 OAuth 连接 URL |
| `pipedream.connectApp` | `agentId, appSlug` | 完成应用连接并更新 mcporter 配置 |
| `pipedream.disconnectApp` | `agentId, appSlug` | 断开应用连接并从 mcporter 中删除相关信息 |
| `pipedream.refreshToken` | `agentId?, appSlug?` | 刷新令牌（全部或特定代理/应用的令牌） |
| `pipedream.activate` | `agentId, appSlug` | 激活应用（如果应用尚未存在于 mcporter 中，则将其添加到配置中） |

### 每个代理相关的 RPC 方法

| RPC 方法 | 参数 | 说明 |
|---------|--------|-------------|
| `pipedream.agent.status` | `agentId` | 从 API 获取代理的配置信息及实时连接的应用列表 |
| `pipedream.agent.save` | `agentId, externalUserId` | 保存代理的配置信息 |
| `pipedream.agent.delete` | `agentId` | 删除代理的配置信息 |
| `pipedream.connect` | `agentId, appSlug` | 获取代理的 OAuth 连接 URL |
| `pipedream.disconnect` | `agentId, appSlug` | 断开应用连接并从 mcporter 中删除相关信息 |
| `pipedream.test` | `agentId, appSlug` | 测试应用的连接状态 |

## 使用已连接的应用

服务器名称遵循以下格式：`pipedream-{externalUserId}-{appSlug}`

## 环境设置：开发环境 vs 生产环境

⚠️ **请使用生产环境** 进行实际开发：
- 开发环境的令牌有效期较短，访问速率限制较低。
- 在 “Pipedream” 标签页的 “设置” → “环境” 中将环境设置为 “production”。
- 当代理处于开发模式时，界面会显示警告提示。

## 安全性措施

| 处理方式 | 详细说明 |
|---------|-------------------|
| **clientId** | 存储在 `~/.openclaw/secrets.json` 文件中（使用密钥库保护，加密存储） |
| **clientSecret** | 也存储在 `~/.openclaw/secrets.json` 文件中（使用密钥库保护，绝对不会以明文形式保存） |
| 非敏感配置信息 | 存储在 `~/.openclaw/workspace/config/pipedream-credentials.json` 文件中（仅包含 `projectId`、`environment`、`externalUserId`） |
| 代理配置信息 | 存储在 `~/.openclaw/workspace/config/integrations/pipedream/{agentId}.json` 文件中 |
| 访问令牌（JWT） | 以短期有效期的令牌形式存储在 `mcporter.json` 的 Authorization 头部，每 45 分钟更新一次 |
| `PIPEDREAM_CLIENT_SECRET` **绝不会** 被写入 `mcporter.json` 文件 |
| 外部 API 调用 | 使用 `api.pipedream.com` 和 `remote.mcp.pipedream.net` |
| 自动迁移机制**：升级后，系统会自动将旧的明文凭证信息迁移到密钥库中 |

## 故障排除

- **OAuth 验证后应用仍未显示？**：点击 “↻ 刷新” 以重新查询已连接的应用列表。
- **出现 “unknown method: pipedream.connect” 错误？**：重新构建并重启 gateway：`pnpm build && openclaw gateway restart`。
- **未配置 Pipedream 凭证？**：请先在 “Pipedream” 标签页中设置凭证信息。
- **处于开发环境？**：在 “Pipedream” 标签页中修改环境设置为 “production”，然后保存设置。
- **令牌过期？**：设置定时任务（例如每 45 分钟刷新一次令牌），或重新点击 “连接” 按钮进行重新授权。

## 技术支持

- **ClawHub**：[clawhub.ai/skills/pipedream-connect](https://clawhub.ai/skills/pipedream-connect)
- **Pipedream 文档**：[pipedream.com/docs](https://pipedream.com/docs)
- **MCP 应用**：[mcp.pipedream.com](https://mcp.pipedream.com)
- **OpenClaw Discord 频道**：[discord.com/invite/clawd](https://discord.com/invite/clawd)

## 参考文件

| 文件名 | 用途 |
|---------|---------|
| `reference/pipedream-backend.ts` | Gateway 的 RPC 处理逻辑（所有与 Pipedream 相关的方法） |
| `reference/pipedream-views.ts` | “Pipedream” 全局界面相关的代码 |
| `reference/pipedream-controller.ts` | 管理全局界面状态的代码 |
| `reference/agent-pipedream-views.ts` | 代理界面（“代理” → “工具” → “Pipedream”）相关的代码 |
| `reference/agent-pipedream-controller.ts` | 管理代理界面状态的代码 |
| `reference/control-ui-csp.ts` | 控制界面相关的 CSP（Content Security Policy）配置 |
| `reference/README.md` | 参考文档说明 |
| `scripts/` | 用于刷新令牌和执行其他辅助操作的脚本 |