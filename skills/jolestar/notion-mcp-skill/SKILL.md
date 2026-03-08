---
name: notion-mcp-skill
description: 通过 UXC CLI 使用 Notion MCP 操作 Notion 工作区的内容，包括搜索、数据获取、用户/团队信息查询、页面/数据库的创建与更新以及评论功能的操作。当任务需要通过 MCP 使用 OAuth（authorization_code + PKCE）来调用 Notion 工具时，尤其是当需要安全写入控制机制或处理 JSON-envelope 格式的数据时，应使用此方法。
---
# Notion MCP 技能

使用此技能通过 `uxc` 以及 OAuth 认证和受保护的写入机制来执行 Notion MCP 操作。

可以重用 `uxc` 技能的相关指导，包括工具发现、模式检查、OAuth 生命周期管理以及错误处理等内容。请注意：并非所有操作都会自动触发其他技能；此技能应始终能够独立执行。

## 先决条件

- `uxc` 已安装，并且已添加到 `PATH` 环境变量中。
- 具备访问 `https://mcp.notion.com/mcp` 的网络权限。
- OAuth 回调监听器可正常访问（示例中使用的地址为 `http://127.0.0.1:8788/callback`）。
- `uxc` 技能支持通用性的发现、描述和执行操作。

## 核心工作流程（Notion 特定）

**此技能的端点参数格式：**
- 建议使用简写形式 `mcp.notion.com/mcp`（省略协议部分）。
- 完整的 URL `https://mcp.notion.com/mcp` 也是有效的。

1. 确保端点映射已配置：
   - `uxc auth binding match mcp.notion.com/mcp`

2. 如果端点映射或认证尚未完成，请启动 OAuth 登录：
   - `uxc auth oauth start notion-mcp --endpoint mcp.notion.com/mcp --redirect-uri http://127.0.0.1:8788/callback --scope read --scope write`
   - 提示用户打开生成的授权 URL。
   - 用户同意后，要求其复制完整的回调 URL。
   - 使用 `uxc auth oauth complete notion-mcp --session-id <session_id> --authorization-response '<callback-url>'` 完成登录。

3. 将端点与凭证绑定：
   - `uxc auth binding add --id notion-mcp --host mcp.notion.com --path-prefix /mcp --scheme https --credential notion-mcp --priority 100`

4. 默认使用固定的命令链接：
   - `command -v notion-mcp-cli`
   - 如果该命令不存在，可以使用 `uxc link notion-mcp-cli mcp.notion.com/mcp` 来创建它。
   - 执行 `notion-mcp-cli -h` 以查看命令帮助信息。
   - 如果发现命令冲突或无法安全重用，请联系技能维护者选择其他命令名称。

5. 在执行操作前，先发现相关工具并检查数据模式：
   - `notion-mcp-cli -h`
   - `notion-mcp-cli notion-fetch -h`
   - `notion-fetch` 需要一个标识符（URL 或 UUID）：
     - 示例：`notion-mcp-cli notion-fetch id="https://notion.so/your-page-url"`
     - `notion-mcp-cli notion-fetch id="12345678-90ab-cdef-1234-567890abcdef"`
   - 常用操作包括 `notion-search`、`notion-fetch` 和 `notion-update-page`。

6. 建议先执行读取操作：
   - 在进行任何写入操作之前，先搜索或获取当前页面内容。

7. 只有在用户明确确认后才能执行写入操作：
   - 对于可能删除内容的 `notion-update-page` 操作，必须先获得用户的确认。

## OAuth 交互流程

请按照以下步骤进行操作：
1. 启动登录命令并等待授权 URL 的生成。
2. 告诉用户：
   - 在浏览器中打开该授权 URL 并批准访问权限。
   - 复制浏览器地址栏中的完整回调 URL。
   - 将回调 URL 粘贴回聊天窗口。
3. 使用 `uxc auth oauth complete notion-mcp --session-id <session_id> --authorization-response '<callback-url>'` 完成登录。

4. （可选）使用 `uxc auth oauth info <credential_id>` 来确认登录是否成功。

**注意：** 不要要求用户手动提取或复制 bearer tokens；`uxc` 会自动处理 token 交换。只有在单进程交互场景下，才使用 `uxc auth oauth login ... --flow authorization_code`。

## 安全限制

- 确保所有输出数据都包含在 JSON 格式中；禁止使用 `--text` 参数。
- 首先解析以下稳定字段：`ok`、`kind`、`protocol`、`data`、`error`。
- 在此技能中，所有针对 Notion MCP 的调用都默认使用 `notion-mcp-cli` 作为命令路径。
- `notion-mcp-cli <operation> ...` 等价于 `uxc mcp.notion.com/mcp <operation> ...`。
- 仅在链接设置不可用时，才使用 `uxc mcp.notion.com/mcp ...` 作为临时替代方案。
- 在执行 `notion-create-pages` 或 `notion-update-page` 等操作之前，先使用 `notion-fetch` 获取数据库中的具体模式和属性名称。
- 默认情况下，所有操作都被视为高影响操作，因此需要用户的明确确认。
- 如果 OAuth 认证失败，请首先使用 `uxc` 的 OAuth 错误处理机制，然后再根据此技能中的说明进行相应的处理。

## 参考资料

- 与 Notion 相关的认证说明（基于 `uxc` 技能的定制版本）：
  - `references/oauth-and-binding.md`
- 按任务分类的调用模式：
  - `references/usage-patterns.md`
- 与 Notion 相关的错误处理说明（基于 `uxc` 技能的定制版本）：
  - `references/error-handling.md`