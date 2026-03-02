---
name: crea-ddf-mcp
description: 通过加固后的MCP服务器和CLI查询CREA/REALTOR.ca的DDF（数据定义文件），以获取机构级房源信息、元数据并进行媒体内容访问。适用于需要在Claude MCP、OpenClaw或脚本化研究工作流程中使用DDF工具的场景。
---
# 创建 DDF MCP

使用此技能将 DDF 作为受管控的 MCP/CLI 集成工具，用于下游分析和自动化操作。

## 工作流程

### 1. 配置 DDF 凭据

设置环境变量：

- `DDF_BASE_URL`
- `DDF_AUTH_URL`
- `DDF_TOKEN_GRANT`（`client_credentials` 或 `password`）
- `DDF_CLIENT_ID` + `DDF_CLIENT_SECRET`（用于客户端凭证）
- `DDF_USERNAME` + `DDF_PASSWORD`（用于密码授权）

可选的操作控制参数：

- `DDF_HTTP_TIMEOUT_MS`, `DDF_HTTP_RETRIES`, `DDF_HTTP_RPS`, `DDF_HTTP_BURST`
- `DDF_MEDIA_entity`, `DDF_MEDIA_RECORD_KEY_FIELD`, `DDF_MEDIA_ORDER_FIELD`

### 2. 构建并运行 MCP

```bash
npm --workspace @fub/crea-ddf-mcp run build
node packages/crea-ddf-mcp/dist/mcp-server.js
```

### 3. 通过 CLI 进行验证

```bash
npm --workspace @fub/crea-ddf-mcp run dev:cli -- search-properties --filters-json '{"city":"Toronto"}' --top 5
npm --workspace @fub/crea-ddf-mcp run dev:cli -- get-property --id "<ListingKey>"
npm --workspace @fub/crea-ddf-mcp run dev:cli -- get-metadata
```

### 4. 与 Claude MCP/OpenClaw 集成

请参考 `references/claude-mcp-config.md` 以配置 Claude，以及 `references/openclaw-wiring.md` 以完成 OpenClaw 的运行时集成。

## 安全规则

- 尽量使用类型化的工具（如 `ddf.search_properties`、`ddf.get_property`）而非原始的调用方式。
- 除非管理策略有更新，否则请将字段选择限制在已批准的安全范围内。
- 将数据许可和显示要求视为上游政策的规定。
- 绝不要将凭证以明文形式存储在提交到 Git 的文件中。