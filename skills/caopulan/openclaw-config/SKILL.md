---
name: openclaw-config
description: 编辑并验证 OpenClaw Gateway 的配置文件（openclaw.json，格式为 JSON5）。此操作适用于以下场景：添加或修改配置键（如 gateway*、agents*、models*、channels*、tools*、skills*、plugins*、$include）；或诊断 OpenClaw Doctor 在配置验证过程中出现的错误。通过执行此操作，可以避免因配置不匹配导致 Gateway 无法启动，或使安全策略失效的问题。
---

# OpenClaw 配置

## 概述

请使用基于模式（schema-based）的工作流程来安全地编辑 `~/.openclaw/openclaw.json` 文件（或由 `OPENCLAW_CONFIG_PATH` 指定的路径）。在修改前后进行验证，以避免无效的键或类型导致系统启动失败或安全行为发生变化。

## 工作流程（安全编辑）

1. **确定当前的配置文件路径**

- 优先级顺序：`OPENCLAW_CONFIG_PATH` > `OPENCLAW_STATE_DIR/openclaw.json` > `~/.openclaw/openclaw.json`
- 配置文件格式为 **JSON5**（允许包含注释和尾随逗号）。

2. **获取权威的配置模式（切勿猜测键名）**

- 如果 Gateway 正在运行：使用 `openclaw gateway call config.schema --params '{}'` 来获取与当前运行版本匹配的 JSON 模式。
- 否则：主要参考 `openclaw/openclaw` 项目的源代码：
  - `src/config/zod-schema.ts`（包含 `gateway`、`skills`、`plugins` 等核心配置键）
  - `src/config/zod-schema.*.ts`（包含子模块的配置文件，如 channels、providers、models、agents、tools）
  - `docs/gateway/configuration.md`（包含配置文档和示例）

3. **以最小的影响范围进行修改**

- 建议进行小范围的编辑：使用 `openclaw config get|set|unset`（支持点路径或括号表示法）。
- 如果 Gateway 处于在线状态，并且希望一步完成“写入、验证、重启”操作：可以使用 RPC `config.patch`（合并配置更改）或 `config.apply`（替换整个配置文件；请谨慎使用）。
- 对于复杂的配置结构，可以使用 `$include` 来分割配置文件（详见下文）。

4. **严格进行验证**

- 运行 `openclaw doctor` 命令，根据报告的问题进行修复。
- 未经用户明确同意，切勿运行 `openclaw doctor --fix/--yes`（该命令会直接修改配置文件和状态文件）。

## 避免配置模式错误

- **大多数配置对象都遵循严格规则**（使用 `.strict()` 标识）：未知的键会导致验证失败，Gateway 会因此拒绝启动。
- `channels` 配置项使用 `.passthrough()` 规则：扩展通道（如 matrix、zalo、nostr 等）可以添加自定义键，但大多数提供者的配置仍然需要遵循严格规则。
- `env` 配置项使用 `.catchall(z.string())` 规则：可以直接在 `env` 下添加字符串类型的环境变量，也可以使用 `env_vars`。
- **敏感信息**：建议使用环境变量或密钥文件来存储敏感信息。避免将长期有效的令牌或 API 密钥保存在 `openclaw.json` 中。

## `$include`（模块化配置）

`$include` 会在配置模式验证之前被解析，允许你将配置内容分散到多个 JSON5 文件中：

- 支持语法：`"$include": "./base.json5"` 或 `"$include": ["./a.json5", "./b.json5"]`
- 相对路径是相对于当前配置文件的目录来解析的。
- 合并规则：
  - 对象：递归合并
  - 数组：直接连接（不会被替换）
  - 原始类型：后出现的值会覆盖之前的值
- 如果 `$include` 和其他配置项同时存在，`$include` 中的定义会覆盖其他配置项的内容。
- 注意：最大嵌套深度为 10 层；循环引用会被检测并拒绝。

## 常见配置操作示例

1. 设置默认工作区
```bash
openclaw config set agents.defaults.workspace '"~/.openclaw/workspace"' --json
openclaw doctor
```

2. 更改 Gateway 的端口
```bash
openclaw config set gateway.port 18789 --json
openclaw doctor
```

3. 分割配置文件
```json5
// ~/.openclaw/openclaw.json
{
  "$include": ["./gateway.json5", "./channels/telegram.json5"],
}
```

4. 允许 Telegram 的私信功能（需要明确允许发送者）
> 配置约束：当 `dmPolicy="open"` 时，`allowFrom` 必须包含 `"*"`。
```bash
openclaw config set channels.telegram.dmPolicy '"open"' --json
openclaw config set channels.telegram.allowFrom '["*"]' --json
openclaw doctor
```

5. 设置 Discord 令牌（优先从配置文件或环境变量中获取）
```bash
# Option A: write to config
openclaw config set channels.discord.token '"YOUR_DISCORD_BOT_TOKEN"' --json

# Option B: env var fallback (still recommend a channels.discord section exists)
# export DISCORD_BOT_TOKEN="..."

openclaw doctor
```

6. 启用 Web 搜索功能（适用于 Brave 或 Perplexity）
```bash
openclaw config set tools.web.search.enabled true --json
openclaw config set tools.web.search.provider '"brave"' --json

# Recommended: provide the key via env var (or write tools.web.search.apiKey)
# export BRAVE_API_KEY="..."

openclaw doctor
```

## 参考资源

当你需要查找配置字段的索引或源代码位置时，请参考以下资源：

- `references/openclaw-config-fields.md`（包含根配置键的索引及对应的源代码文件列表）
- `references/schema-sources.md`（说明如何在 openclaw 项目中查找配置模式及其约束条件）
- `scripts/openclaw-config-check.sh`（用于打印配置文件路径并运行 `openclaw doctor` 命令）