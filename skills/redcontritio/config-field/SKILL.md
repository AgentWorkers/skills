---
name: config-field
description: 验证 OpenClaw 的配置字段是否符合官方的 Zod 架构。在读取或写入 `openclaw.json` 文件时，使用该功能来检查配置字段是否存在以及是否有效。该功能涵盖了代理（agents）、通道（channels）、工具（tools）、日志记录（logging）以及会话配置（session configuration）等部分，包含 136 个以上的字段定义。
---
# 配置字段验证器

该工具用于根据官方的 Zod 架构验证 OpenClaw 的配置字段。

## 适用场景

- **在编辑配置之前**：确保所需字段确实存在。
- **调试配置错误**：检查无效字段是否导致了问题。
- **迁移配置**：在版本升级后验证配置字段是否正确。
- **审查配置**：确保所有字段都符合架构规范。

## 工作原理

该工具自动管理架构同步过程：
1. **检测版本**：识别当前使用的 OpenClaw 版本。
2. **同步架构**：如有需要，从 GitHub 下载相应的 Zod 架构文件。
3. **提取字段信息**：解析 Zod 架构以获取字段定义。
4. **进行验证**：使用生成的架构来验证配置内容。

## 快速入门

```bash
# Validate a single field (auto-syncs schema if needed)
python3 scripts/validate_field.py agents.defaults.model.primary

# Validate entire config file
python3 scripts/validate_config.py /path/to/openclaw.json

# Force schema re-sync
python3 scripts/sync_schema.py --force

# Check current schema status
python3 scripts/sync_schema.py --status
```

## 字段路径格式

字段路径使用点表示法（例如：`agentsdefaults.model.id`）。

## 工作流程

### 对于用户

只需使用相应的验证命令即可，架构同步会自动完成。

```bash
# This will auto-sync schema if version mismatch detected
python3 scripts/validate_field.py agents.defaults.timeoutSeconds
```

### 对于架构管理

```bash
# Check schema status
python3 scripts/sync_schema.py --status
# Output: Schema version: 2.1.0 (matches OpenClaw)

# Force re-sync (if needed)
python3 scripts/sync_schema.py --force

# Generate fresh field reference
python3 scripts/generate_fields.py
```

## 架构存储

架构信息会缓存到本地。

```
~/.config/openclaw/skills/config-field/
├── schema/              # Downloaded TypeScript schema files
├── cache/               # Parsed schema cache
└── schema-fields.md     # Generated field reference
```

## 参考资料

- **完整的字段参考**：[references/schema-fields.md](references/schema-fields.md) – 该文档是根据官方 Zod 架构自动生成的。

## 脚本示例

| 脚本          | 功能                |
|------------------|----------------------|
| `validate_field.py <path>` | 验证单个字段            |
| `validate_config.py <file>` | 验证整个配置文件         |
| `field_info.py <path>` | 获取字段详细信息          |
| `sync_schema.py`     | 管理架构同步             |
| `generate_fields.py`    | 重新生成字段文档           |

## 常见配置字段

### 代理配置
- `agentsdefaults.model.primary`：默认模型 ID
- `agentsdefaults.workspace`：工作区路径
- `agentsdefaults.timeoutSeconds`：请求超时时间
- `agentsdefaults.sandbox.mode`：沙箱模式

### 频道配置
- `channelsTelegram_botToken`：Telegram 机器人令牌
- `channels/discord.token`：Discord 机器人令牌
- `channels.slack_botToken`：Slack 机器人令牌

### 工具配置
- `tools.web.search.enabled`：启用网络搜索功能
- `tools.web.search.provider`：搜索服务提供者
- `tools.exec.security`：执行安全模式设置

## 故障排除

### 架构版本过旧

如果出现关于“未知字段”的警告，请检查是否使用了过时的架构文件。

```bash
# Force schema refresh
python3 scripts/sync_schema.py --force
```

### 验证错误

```bash
# Check field info for correct usage
python3 scripts/field_info.py agents.defaults.model

# Verify config syntax
python3 scripts/validate_config.py ~/.config/openclaw/openclaw.json
```