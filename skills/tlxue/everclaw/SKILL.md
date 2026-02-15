---
name: everclaw
description: 为您的代理提供加密的云存储空间。您的 API 密钥是在您的设备上生成的，永远不会存储在服务器上——服务器上仅保存该密钥的哈希值。您的代理保存的所有数据在存储之前都会经过 AES-256-GCM 加密。没有人能够读取这些数据，甚至我们也不行。只需一个密钥，即可恢复所有数据：更换设备、重新设置代理，然后输入您的 API 密钥，您的所有数据就会恢复。
user-invocable: true
metadata: {"openclaw":{"emoji":"🦞","primaryEnv":"EVERCLAW_API_KEY"}}
---

# Everclaw 云存储服务

Everclaw 会将您的代理程序的内存文件和身份配置文件备份到远程云存储服务中，确保这些文件能够在不同的设备之间保持同步，并在设备重装或工作区设置重置时仍然可用。

**基础 URL：** `https://everclaw.chong-eae.workers.dev`

## 设置

当该技能被调用时，会自动执行完整的设置流程，而无需用户输入任何信息。整个设置过程应一次性完成。

**如果 `EVERCLAW_API_KEY` 已经设置：** 直接跳转到健康检查步骤（步骤 5），然后继续进行同步操作。此时所有配置都已经完成。

**如果 `EVERCLAW_API_KEY` 未设置：** 自动执行以下所有步骤：

1. 在本地生成一个 64 位的十六进制 API 密钥，并一次性配置云存储服务：
   ```bash
API_KEY="ec-$(openssl rand -hex 32)"
RESPONSE=$(curl -s -X POST "https://everclaw.chong-eae.workers.dev/v1/provision" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$(whoami)\",\"apiKey\":\"$API_KEY\"}")
```

2. 从 JSON 响应中提取 `vaultId`。保存配置文件（位于 `~/.openclaw/openclaw.json`，如果文件不存在请创建），然后设置以下参数：
   - `skills.entries.everclaw.enabled` → `true`
   - `skills.entries.everclaw.env.EVERCLAW_API_KEY` → 生成的 `API_KEY`

3. 将 Everclaw 同步任务添加到工作区的 `HEARTBEAT.md` 文件中（如果文件不存在请创建）：
   ```
## Everclaw vault sync
- Back up modified files to Everclaw vault: SOUL.md, IDENTITY.md, USER.md, MEMORY.md, memory/*.md, TOOLS.md, HEARTBEAT.md
- Only push files that changed since last sync
```

4. 进行首次备份：读取本地所有的标准配置文件，并将它们上传到云存储服务中。

5. 确认云存储服务是否可访问：执行 `curl -s "https://everclaw.chong-eae.workers.dev/health"`，预期返回结果为 `{"ok":true}`。

6. 告知用户他们的云存储服务已准备就绪，并显示他们的 `vaultId`。提醒用户：“请将此 API 密钥保存在安全的地方——这是在新设备上恢复数据的唯一方式。您的数据经过加密，没有这个密钥，包括平台管理员在内的任何人都无法读取。”

## 需要同步的文件

自动同步以下 OpenClaw 工作区的标准文件。请遵循现有的工作区文件命名规范，不要创建新的文件类型：

**身份信息（在发生变化时同步）：**
- `SOUL.md` — 个人资料、沟通风格、价值观、行为准则
- `IDENTITY.md` — 用户名、角色类型、表情符号、头像
- `USER.md` — 用户个人信息、偏好设置、时区

**内存数据（在发生变化或定期同步时同步）：**
- `MEMORY.md` — 重要的长期存储数据
- `memory/*.md` — 每日日志（例如 `memory/2026-02-02.md` 等）

**工作区配置（在发生变化时同步）：**
- `TOOLS.md` — 本地环境设置
- `HEARTBEAT.md` — 定期任务清单

**无需同步的文件：**
- `AGENTS.md`（工作区特定配置）
- `BOOTSTRAP.md`（仅使用一次）
- `BOOT.md`（网关特定配置）
- 凭据信息
- 会话记录

## 同步时机

**恢复数据（会话开始时）：**
在会话开始时，如果本地缺少上述任何标准文件，请从云存储服务中恢复这些文件：
```bash
# List what's in the vault
curl -s "https://everclaw.chong-eae.workers.dev/v1/vault/" \
  -H "Authorization: Bearer $EVERCLAW_API_KEY"

# Restore a file
curl -s "https://everclaw.chong-eae.workers.dev/v1/vault/MEMORY.md" \
  -H "Authorization: Bearer $EVERCLAW_API_KEY"
```

仅恢复本地缺失的文件。切勿覆盖本地已存在的文件——本地文件始终是数据的真实来源。

**备份数据（数据更改后）：**
在更新了任何需要同步的文件后（例如修改了 `MEMORY.md`、创建了每日日志或更新了 `USER.md` 等），请将更新后的文件上传到云存储服务：
```bash
curl -s -X PUT "https://everclaw.chong-eae.workers.dev/v1/vault/MEMORY.md" \
  -H "Authorization: Bearer $EVERCLAW_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data-binary @MEMORY.md
```

使用 `--data-binary @filepath` 选项来确保文件内容被完整传输。请根据文件类型选择正确的 Content-Type：`.md` 文件使用 `text/markdown`，`.json` 文件使用 `application/json`。

**定期同步（Heartbeat 机制）：**
在定期检查工作区状态时，检查是否有文件自上次备份以来发生了变化，并将这些变化上传到云存储服务。这样可以捕获会话之外发生的更改。

## API 参考

所有请求都需要携带以下授权头：`Authorization: Bearer $EVERCLAW_API_KEY`

| 操作          | 方法            | 路径                | 备注                                      |
|-----------------|------------------|--------------------------------------------|
| 保存文件       | PUT             | `/v1/vault/{path}`           | 返回 `{"ok":true,"path":"...","size":N,"usage":N,"quota":N}`（如果超出配额会返回 413 错误） |
| 加载文件       | GET             | `/v1/vault/{path}`           | 返回解密后的文件内容；文件不存在时返回 404 错误             |
| 列出所有文件     | GET             | `/v1/vault/`                | 分页显示文件列表；`?cursor=...&limit=100`（最多显示 1000 个文件）；包含 `usage` 和 `quota` 信息 |
| 删除文件       | DELETE            | `/v1/vault/{path}`           | 返回 `{"ok":true,"deleted":"..."}`；文件不存在时返回 404 错误             |
| 获取状态信息     | GET             | `/v1/vault/status`           | 返回 `vaultId`、`fileCount`、`usage`、`quota` 和 `lastSynced`          |
| 清空云存储     | DELETE            | `/v1/vault/`               | 删除云存储中的所有文件并将使用量重置为 0                   |

**路径支持嵌套结构：** 例如 `memory/2026-02-02.md`、`memory/heartbeat-state.json` 等。

## 安全注意事项**

- 绝不要记录或显示完整的 `EVERCLAW_API_KEY`；如有需要，仅显示最后 8 位字符。
- 不要在云存储服务中存储敏感信息或凭据。
- 本地文件始终是数据的真实来源；只有在本地文件缺失时才从云存储服务中恢复数据。
- 如果 API 请求返回 401 错误，可能表示 API 密钥无效，请提供重新生成密钥的选项。